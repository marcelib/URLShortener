from flask import Flask, render_template, request, redirect, session
from uuid import uuid4

app_url = '/baczewm1/urlshortener'
app = Flask(__name__, static_url_path='/baczewm1/urlshortener/static', static_folder='static')
app.secret_key = '!@#dfr23[[]@#%$SDFSasdgg?:"{'
link_dictionary = {}
usernames_and_passwords = {'admin': 'admin123', 'abc': 'abc'}


@app.route(app_url + '/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        if 'username' in session:
            logged_in = "Log out from user " + session['username']
            return render_template('index_logged.html', logged_in=logged_in, )
        return render_template('index.html')
    if request.method == 'POST':
        url = request.form['url']
        uuid = uuid4().__str__()
        short_url = str(uuid)[:6]
        link_dictionary[short_url] = url
        return render_template('link_created.html', shortUrl=short_url)


@app.route(app_url + '/<url>')
def redirect_url(url):
    return redirect(link_dictionary[url], 301)


@app.route(app_url + '/link')
def link():
    if 'username' in session:
        return render_template('links.html', linkbase=link_dictionary)
    return redirect(app_url)


@app.route(app_url + '/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if 'username' in session:
            return render_template('index_logged.html', linkbase=link_dictionary)
    if request.method == 'POST':
        if not user_register_match(request.form.get('username')):
            user_register()
            invalid_message = "User registered successfully."
            return render_template('base_template.html', invalid_message=invalid_message)
        else:
            invalid_message = "User already registered."
            return render_template('base_template.html', invalid_message=invalid_message)


@app.route(app_url + '/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'username' in session:
            del session['username']
            return redirect(app_url)
        return render_template('index.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if user_match(username, password):
            session['username'] = username
            return redirect(app_url)
        invalid_message = "Incorrect login or password."
        return render_template('base_template.html', invalid_message=invalid_message)


def user_match(username, password):
    return username in usernames_and_passwords and usernames_and_passwords[username] == password


def user_register_match(username):
    return username in usernames_and_passwords


def user_register():
    usernames_and_passwords.update(
        {request.form.get('username'): request.form.get('password')})


if __name__ == '__main__':
    app.run()
