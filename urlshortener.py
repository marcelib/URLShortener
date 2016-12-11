from flask import Flask, render_template, request, redirect, session
from uuid import uuid4
import os

app_url = '/baczewm1/urlshortener'
app = Flask(__name__, static_url_path='/baczewm1/short/static', static_folder='static')
app.secret_key = '!@#dfr23[[]@#%$SDFSasdgg?:"{'
linkbase = {}
usernames_and_passwords = []


@app.route(app_url + '/static/<resource>')
def static_resource(resource):
    path = app.root_path + '/static/' + resource
    if os.path.isfile(path):
        return open(path)
    return render_template('404.html'), 404


@app.route(app_url + '/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        logged_in = "Log in"
        if 'username' in session:
            logged_in = "Log out from user " + session['username']
            return render_template('index_logged.html', logged_in=logged_in,)
        return render_template('index.html', log_in=logged_in, register="Register")
    if request.method == 'POST':
        url = request.form['url']
        uuid = uuid4().__str__()
        short_url = str(uuid)[:6]
        linkbase[short_url] = url
        return render_template('link_created.html', shortUrl=short_url)


@app.route(app_url + '/<url>')
def redirect_url(url):
    return redirect(linkbase[url], 301)


@app.route(app_url + '/link')
def link():
    if 'username' in session:
        return render_template('links.html', linkbase=linkbase)
    return redirect(app_url)


@app.route(app_url + '/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if 'username' in session:
            return render_template('index_logged.html', linkbase=linkbase)
        else:
            return render_template('register_form.html')
    if request.method == 'POST':
        if not user_match(request.form.get('username'), request.form.get('password')):
            user_register()
        return redirect(app_url)


@app.route(app_url + '/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'username' in session:
            del session['username']
            return redirect(app_url)
        return render_template('login_form.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if user_match(username, password):
            session['username'] = username
            return redirect(app_url)
        return render_template('login_failure.html', username=username)


def user_match(username, password):
    return any(d["username"] == username and d["password"] == password for d in usernames_and_passwords)


def user_register():
    usernames_and_passwords.append(
        {'username': request.form.get('username'), 'password': request.form.get('password')})


if __name__ == '__main__':
    app.run()
