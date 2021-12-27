from flask import Flask, request, abort, redirect, Response, url_for
from flask import render_template
from flask_login import LoginManager, login_required, UserMixin
from flask_login import login_user
from team_project_db import DBManager
import os

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.root_path, 'woodle.sqlite')

app.config.update(DEBUG=True, SECRET_KEY='secret_xxx')

# log in managers
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

db = DBManager(app)  # create object to interact w/ data base


class User(UserMixin):
    """
    A user entity (either student or faculty). Used by login_manager to
    handle tokens for login sessions.
    """

    def __init__(self, username, password, id, active=True):
        self.username = username
        self.password = password
        self.id = id
        self.active = active

    # def get_auth_token(self):
    #     return make_secure_token(self.username, key='secret_key')


class UserRepository:
    """
    Stores users for the session. Long term storage is in the sqlite db
    """

    def __init__(self):
        self.users = dict()
        self.identifier = 0
        self.users_id_dict = dict()

    def save_user(self, user):
        self.users_id_dict.setdefault(user.id, user)
        self.users.setdefault(user.username, user)

    # def get_user(self, username):
    #     return self.users(username)

    def get_user_by_id(self, userid):
        return self.users.get(userid)

    def next_index(self):
        self.identifier += 1
        return self.identifier


local_user_repository = UserRepository()


@app.cli.command('initdb')  # '@app' decorated functions should be in this file
def init_db():
    """
    When 'flask initdb' is entered on the command line while the program is
    running, this function is called. The database is initialized
    by the data base handler's init_db() class method.
    """
    initialization_sql_file = 'init_db.sql'  # name of sql file that inits db
    db.init_db(initialization_sql_file)
    print('The website\'s database has been initialized.')


@app.cli.command('populatedb')
def populate_db():
    """
    When 'flask populatedb' is entered on the command line while the program is
    running, this function is called. The database is populated.

    Assumes that the database has already been initialized.
    """
    populate_db_sql_file = 'populate_db.sql'  # sql file that populates db

    db.populate_db(populate_db_sql_file)
    print('The website\'s database has been populated.')

@login_required
@app.route('/')
@app.route('/hello')
def index():
    """
    Determines the response to a /hello request
    :return:
    """
    return render_template('home.html')


@login_required
@app.route('/home')
def home():
    """
    Determines response to a /home request
    """
    return "<h1>Welcome home!</h1>"


@login_required
@app.route('/faculty/<username>')
def faculty(username):
    """
    Determines response to a /faculty request

    :return: a rendered template webpage specific to the faculty memeber
    """
    faculty_query = db.get_faculty(username)
    return render_template('faculty.html',
                           grade=faculty_query,
                           full_name=db.get_name_of_user(username, 'faculty')
                           )


@login_required
@app.route('/student/<username>')
def student(username):
    """
    Determines response to a /student request

    :return: a rendered template webpage specific to the student
    """
    student_query = db.get_class_grade(username)
    return render_template('student.html',
                           grade=student_query,
                           full_name=db.get_name_of_user(username, 'student')
                           )


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This function handles the login process for the website. A successful login
    means that the student or faculty memeber gets to his or her unique page
    that is generated from one of two templates. An unsuccessful login
    routes to the register funciton.

    :return: a url redirect
    """
    # if post request - triggered if login form in else statement is submitted
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # None if username and password are a valid pair
        query_result = db.query_login_info(username, password)

        # if a user w/ that username and password exists
        if query_result is not None:
            # if user logging in is a student
            if 'student_id' in query_result[0]:
                new_session_student_user = User(username,
                                                password,
                                                query_result[0]['student_id'])
                local_user_repository.save_user(new_session_student_user)
                login_user(new_session_student_user)
                return redirect(url_for('student', username=username))

            # else user is one of the faculty
            else:
                new_session_faculty_user = User(username,
                                                password,
                                                query_result[0]['faculty_id'])
                local_user_repository.save_user(new_session_faculty_user)
                login_user(new_session_faculty_user)
                return redirect(url_for('faculty', username=username))

        # else, username and password are not a pair, no such user exists,
        # so go ahead and direct the user to make one such user
        else:
            return redirect(url_for('register'))

    # else, get request
    else:
        # the login request form
        return Response('''
            <form action="" method="post">
            <fieldset>
            <legend>Login</legend>
                <p><input type=text name=username placeholder="Username">
                <p><input type=password name=password placeholder="Password">
                <p><input type=submit value=Login>
            <fieldset
            </form>
        ''')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register a new user such that the user is inserted into the data base.
    Provides an HTML form to create a new profile. Successful registration
    will route back to the login page.

    :return: some sort of webpage or webform
    """
    if request.method == 'POST':

        # check that all of the forms were filled out
        all_data_keys = ['username', 'password', 'is_student',
                         'name', 'title', 'class_id']
        for key in all_data_keys:
            if key not in request.form:
                return redirect(url_for('register'))

        username = request.form['username']
        password = request.form['password']
        is_student = 'Y' is request.form['is_student']\
                        or 'y' is request.form['is_student']
        name = request.form['name']
        title = request.form['title']
        class_id = request.form['class_id']

        # if registering user is a student and provided all info
        if is_student:
            # if failed to insert
            if db.insert_user(username, password, name, class_id) is None:
                return abort(401)

            # else, success; go login
            return redirect(url_for('login'))

        # else, must be faculty
        else:
            # if failed to insert
            db.insert_user(username, password, name, class_id, title=title)

            return redirect(url_for('login'))

    else:
        # Provide a form to create a new user profile
        return Response('''
            <form action="" method="post">
            <fieldset>
            <legend>Create a New Profile</legend>
            <p><input type=text name=username placeholder="Enter username">
            <p><input type=password name=password placeholder="Enter password">
            <p><input type=text name=name placeholder="Enter full name">
            <p><input type=text name=title placeholder="Position">
            <p><input type=text name=class_id placeholder="Class ID">
            <p><input type=text name=is_student placeholder="Student? (Y/N)">
            <p><input type=submit value=Login>
            </fieldset>
            </form>
        ''')


# handle login failed
@app.errorhandler(401)
def page_not_found():
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return local_user_repository.get_user_by_id(userid)


if __name__ == "__main__":
    app.run(app.run(host='127.0.0.1', port=12345))
