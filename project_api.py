"""
### API Description
This is a RESTful API for interacting with the school focused data base
and website. API requests return JSON objects or an error code with a message.
The API provides support for GET and POST requests where
relevant and allowed.

### Supported Requests

                            ## Student Requests
# GET class requests

GET /api/students/
Description:
Get all student entities from the student table.
Parameters:
none
Example Response:
[
{
    s_name: "Johnny Johns",
    c_name: "CS-232",
    grade: "A"
},
{
    s_name: "Daniel Daniellovich",
    c_name: "CS-112",
    grade: "B+"
}
]

# POST student request

POST /api/students/
Description:
Post a new student entity to the student table. Returns the entity posted
or an error.
Parameters:
name - name of the student want to add (text, form data)
username - usernaem
password - password for new
class_id - id of class enrolled in
Example Response:
[
{
    class_id - 987,
    name - "Mark Kram",
    username - "mkUltra",
    password- "cia"
}
]

                            ## Faculty Requests
# POST faculty requests

POST /api/faculty/
Description:
Add a faculty entity to the faculty table. Returns entity added or an error.
Parameters:
name - name of the faculty member to insert (text, form data)
title - title of the person inserting (text, form data)
username - username of new faculty
paassword - paswrod of new faculty
Example Response:
[
{
    username: "jkaine",
    name: "Jane Kaine"
    title: "professor",
    password: "jkaine",
    class_id: 1
}
]


                            ## Grade Requests
# GET grade requests
GET /api/grades/
Description:
One of four actions:

Parameters:
    username - username of student for whom want grades (can be None for all)
Example Response:
[
{
    grade: A,
    s_name: 'Boberto',
    c_name: 'cs-232',
},
{
    grade: C+,
    s_name: 'Mo',
    c_name: 'cs-200',
}
]

"""
from flask import Flask, jsonify, request
from flask.views import MethodView
from team_project_db import DBManager
import os

app = Flask(__name__)  # flask app
database_path = 'woodle.sqlite'  # should be same as db in main_app.py
app.config['DATABASE'] = os.path.join(app.root_path,
                                      database_path)  # same as in main_app
db = DBManager(app)  # object fo database class
# to handle database interactions w/in API classes


class StudentsAPIView(MethodView):
    """
    This view handles all /api/students/ requests.
    """

    def get(self):
        """
        Handle GET requests for the student table.

        :return: a list of dictionaries where each dictionary
        represents a student entity
        """

        # some of the db function names make no sense
        students = db.get_id()

        if students is not None:
            response = students
        else:
            raise RequestError(404, 'student with that id not found')
        return jsonify(response)

    def post(self):
        """
        Handles a POST request to insert a student. Returns a list with 1 dict,
        representing the newly inserted student.

        The student's name must be provided in the request's form data.

        :return: a list with a dictionary of the student entity just inserted
        """
        no_username = 'username' not in request.form
        no_password = 'password' not in request.form
        no_name = 'name' not in request.form
        no_class_id = 'class_id' not in request.form

        # if form is incomplete (lacks name)
        if no_username or no_password or no_name or no_class_id:
            raise RequestError(422, 'username, password, name,'
                                    ' class_id required')

        # else form is complete, go ahead and insert
        else:
            username = request.form['username']
            password = request.form['password']
            name = request.form['name']
            class_id = request.form['class_id']

            inserted_student = db.insert_user(username,
                                              password,
                                              name,
                                              class_id)

            if not inserted_student:  # empty list, w/out any dicts
                raise RequestError(405, 'unable to insert that faculty')
            else:
                response = inserted_student
            return jsonify(response)


class FacultyAPIView(MethodView):
    """
    This view handles all /api/faculty/ requests.
    """

    def post(self):
        """
        Handles a POST request to insert faculty. Returns a list with 1 dict,
        representing the newly inserted faculty.

        The faculty name and title must be provided in the request form data.

        :return: a list with a dictionary of the class entity just inserted
        """
        no_username = 'username' not in request.form
        no_password = 'password' not in request.form
        no_name = 'name' not in request.form
        no_class_id = 'class_id' not in request.form
        no_title = 'title' not in request.form

        # if form is incomplete (lacks name)
        if no_username or no_password or no_name or no_class_id or no_title:
            raise RequestError(422, 'username, password, name,'
                                    ' class_id, title required')

        # else form is complete, go ahead and insert
        else:
            username = request.form['username']
            password = request.form['password']
            name = request.form['name']
            class_id = request.form['class_id']
            title = request.form['title']

            inserted_faculty = db.insert_user(username,
                                              password,
                                              name,
                                              class_id,
                                              title)

            if not inserted_faculty:
                raise RequestError(405, 'unable to insert that faculty')
            else:
                response = inserted_faculty

        return jsonify(response)


class GradesAPIView(MethodView):
    """
    This view handles all /api/grades/ requests.
    """

    def get(self, username=None):
        """
        Handle grade GET requests.

        :param username: student username for whom want grades
        :return: a JSONified list of dictionaries where each dictionary
        represents a grade entity
        """
        if username is None:
            grades = db.get_class_grade()

        # else looking for grades for a specific class AND a specific student
        else:
            grades = db.get_class_grade(username)

        if grades is None:
            raise RequestError(404, 'grades for that student and/or '
                                    'class were not found')
        else:
            response = grades
            return jsonify(response)


# Custom request error handling class and functions
class RequestError(Exception):
    """
    This custom exception class is for easily handling errors in requests,
    such as when the user provides an ID that does not exist or omits a
    required field.
    """

    def __init__(self, status_code, error_message):
        # Call the parent class's constructor.
        Exception.__init__(self)

        self.status_code = str(status_code)
        self.error_message = error_message

    def to_response(self):
        """
        Create a Response object containing the error message as JSON.

        :return: the error response, the JSONified list with 1 dict and
        the status code
        """
        response = jsonify([{'error': self.error_message}])
        response.status = self.status_code
        return response


# URL rules for the API
# Student rules
# Register StudentsAPIView as the view/handler for all api/students/ requests
students_api_view = StudentsAPIView.as_view('students_api_view')

# GET student
app.add_url_rule('/api/students/', defaults={'student_id': None},
                 view_func=students_api_view, methods=['GET'])
app.add_url_rule('/api/students/<int:student_id>', view_func=students_api_view,
                 methods=['GET'])
# POST student
app.add_url_rule('/api/students/', view_func=students_api_view,
                 methods=['POST'])

# Faculty rules
# Register FacultyAPIView as the view/handler for all api/faculty/ requests.
faculty_api_view = FacultyAPIView.as_view('faculty_api_view')

# POST faculty
app.add_url_rule('/api/faculty/', view_func=faculty_api_view, methods=['POST'])

# Grade rules
# Register UsersAPIView as the view/handler for all api/grades/ requests.
grades_api_view = GradesAPIView.as_view('grades_api_view')
# GET grades
app.add_url_rule('/api/grades/', view_func=grades_api_view, methods=['GET'])
