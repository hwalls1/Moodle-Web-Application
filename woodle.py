#  python3 -m venv flask_env
#  source flask_env/bin/activate
#  python3 -m pip install flask
#  export FLASK_APP=flask-login.py
#  export FLASK_DEBUG=1
#  flask run

from flask import Flask, request, abort, redirect, Response, url_for
from flask import render_template
from flask.ext.login import LoginManager, login_required, UserMixin, login_user
from team_project_db import *


app = Flask(__name__)
app.config.update(DEBUG=True, SECRET_KEY='secret_xxx')

# log in managers
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

db = DBManager(app)  # create object to interact w/ data base


class User(UserMixin):
    def __init__(self, username, password, id, active=True):
        self.id = id
        self.username = username
        self.password = password
        self.active = active

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    def get_auth_token(self):
        return make_secure_token(self.username, key='secret_key')


class UsersRepository:

    def __init__(self):
        self.users = dict()
        self.users_id_dict = dict()
        self.identifier = 0

    def save_user(self, user):
        self.users_id_dict.setdefault(user.id, user)
        self.users.setdefault(user.username, user)

    def get_user(self, username):
        return self.users.get(username)

    def get_user_by_id(self, userid):
        return self.users.get(userid)

    def next_index(self):
        self.identifier += 1
        return self.identifier


users_repository = UsersRepository()


@app.route('/')
@app.route('/hello')
def index():
    return render_template('home.html')


@app.route('/home')
@login_required
def home():
    return "<h1>User Home</h1>"


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if post request
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        registered_user = users_repository.get_user(username)
        print('Users ' + str(users_repository.users))
        print('Register user %s , password %s' % (registered_user.username,
                                                  registered_user.password))
        if registered_user != None and registered_user.password == password:
            print('Logged in..')
            login_user(registered_user)
            return redirect(url_for('/home'))
        else:
            return abort(401)

    # else, get request
    else:
        return Response('''
            <form action="" method="post">
                <p><input type=text name=username>
                <p><input type=password name=password>
                <p><input type=submit value=Login>
            </form>
        ''')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #student_id = 1
        # I only wrote mine because no one else put there stuff in the db.md
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password, users_repository.next_index())
        users_repository.save_user(new_user)
        return render_template('Micheas.html', grade=get_class_grade())
    else:
        return Response('''
            <form action="" method="post">
            <p><input type=text name=username placeholder="Enter username">
            <p><input type=password name=password placeholder="Enter password">
            <p><input type=submit value=Login>
            </form>
        ''')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         #faculty_id = 1
#         username = request.form['username']
#         password = request.form['password']
#         new_user = User(username, password, users_repository.next_index())
#         users_repository.save_user(new_user)
#         return render_template('Sommer.html', faculty=db.get_faculty())
#     else:
#         return Response('''
#             <form action="" method="post">
#             <p><input type=text name=username placeholder="Enter username">
#             <p><input type=password name=password placeholder="Enter password">
#             <p><input type=submit value=Login>
#             </form>
#         ''')
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         #faculty_id= 2
#         username = request.form['username']
#         password = request.form['password']
#         new_user = User(username, password, users_repository.next_index())
#         users_repository.save_user(new_user)
#         return render_template('Hartman.html', faculty=db.get_faculty())
#     else:
#         return Response('''
#             <form action="" method="post">
#             <p><input type=text name=username placeholder="Enter username">
#             <p><input type=password name=password placeholder="Enter password">
#             <p><input type=submit value=Login>
#             </form>
#         ''')
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         #faculty_id = 3
#         username = request.form['username']
#         password = request.form['password']
#         new_user = User(username, password, users_repository.next_index())
#         users_repository.save_user(new_user)
#         return render_template('Pasteur.html', faculty=db.get_faculty())
#     else:
#         return Response('''
#             <form action="" method="post">
#             <p><input type=text name=username placeholder="Enter username">
#             <p><input type=password name=password placeholder="Enter password">
#             <p><input type=submit value=Login>
#             </form>
#         ''')

# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return users_repository.get_user_by_id(userid)


if __name__ == "__main__":
    app.run(app.run(host='127.0.0.1', port=12345))
