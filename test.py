"""
This module contains tests for the Flask app in fun_app.py

Create and activate a new virtual environment, or activate an existing
virtual environment that you have used for this class.

If you need to create a new one:
  python3 -m venv pytest_environment
  source pytest_environment/bin/activate

If you need to install flask and/or pytest:
  python3 -m pip install flask
  python3 -m pip install pytest

Set up your environment as normal:
  export FLASK_APP=fun_app.py
  export FLASK_DEBUG=1

Now instead of running the app directly, you can run these tests with pytest:
  python3 -m pytest test_fun_app.py
"""
import pytest
import tempfile
import json
import os

# change this with the python file.
import team_project_api

@pytest.fixture
def test_client():
    # tempfile.mkstemp() creates a temporary file and returns a tuple containing
    # a file descriptor for the file and the name of the file. We store the
    # file descriptor as db_fd so we can close it later, and store the filename
    # in the app's config dictionary, setting the app's database to be this
    # temporary file.
    db_fd, team_project_api.app.config['DATABASE'] = tempfile.mkstemp()
    # This enables testing mode for the app
    team_project_api.app.testing = True
    # A test client provides methods for simulating requests to the app
    test_client = team_project_api.app.test_client()

    # In order to call the init_db() function from fun_app.py, we need to set
    # up an application context.
    with team_project_api.app.app_context():
        team_project_api.init_db()

    # Any function using this fixture will be passed test_client
    yield test_client

    # Close the temporary file
    os.close(db_fd)
    # Delete the temporary file
    os.unlink(team_project_api.app.config['DATABASE'])

# Tests GET requests
def test_no_students_id(test_client):
    """
    Tests GET requests for student id.
    """
    response = test_client.get('/api/students/1')

    # Make sure we got a status code of 200
    assert response.status_code == 200

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    response_json = json.loads(response.data)

    # Since no messages were posted, this should be an empty list
    assert response_json == []

def test_no_faculity(test_client):
    '''
    Test GET requests for faculity. It's return value should be empty.
    '''
    response = test_client.get('/api/faculty')

    # Make sure we got a status code of 200
    assert response.status_code == 200

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    response_json = json.loads(response.data)

    # Since no messages were posted, this should be an empty list
    assert response_json == []

def test_no_faculity_id(test_client):
    '''
    Test GET request for faculity id.
    It's return value should be empty.
    '''
    response = test_client.get('/api/faculty/1')

    # Make sure we got a status code of 200
    assert response.status_code == 200

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    response_json = json.loads(response.data)

    # Since no messages were posted, this should be an empty list
    assert response_json == []

def test_no_grades(test_client):
    '''
    Test GET request for grades.
    Return value should be empty.
    '''
    response = test_client.get('/api/grades')

    # Make sure we got a status code of 200
    assert response.status_code == 200

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    response_json = json.loads(response.data)

    # Since no messages were posted, this should be an empty list
    assert response_json == []

def test_no_faculity(test_client):
    '''
    Tests GET request for faculty.
    Return value should be empty.
    '''
    response = test_client.get('/api/faculty')

    # Make sure we got a status code of 200
    assert response.status_code == 200

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    response_json = json.loads(response.data)

    # Since no messages were posted, this should be an empty list
    assert response_json == []

# Tests POST requests
def test_post_faculty(test_client):
    '''
    Tests POST request for faculity.
    Return value should be the same as message.
    '''
    message = {
        'name': "Jane Kaine"
        'title': "professor"
    }

    response = test_client.post('/api/faculty', data=message)

    assert response.status_code == 200

    response_json = json.loads(response.data)

    # The response JSON should have these 3 keys
    expected_keys = ('faculty_id', 'name', 'title')
    for key in expected_keys:
        assert key in response_json

    # This should be the structure of the JSON, minus the timestamp. We won't
    # check the timestamp because we won't know what it is.
    expected_values = {
        'faculty_id': 1,
        'name': "Jane Kaine"
        'title': "professor"
    }

    for key, value in expected_values.items():
        assert response_json[key] == value


def test_post_grade(test_client):
    '''
    Test POST requests for grade
    Return value should be the same as
    message.

    '''

    message = {
        'grade': '100',
        'class_id': '1',
        'student_id': '1',
        'faculty_id': '1',
    }

    response = test_client.post('/api/grades', data=message)

    assert response.status_code == 200

    response_json = json.loads(response.data)

    # The response JSON should have these 4 keys
    expected_keys = ('grade', 'class_id', 'student_id', 'faculty_id')
    for key in expected_keys:
        assert key in response_json

    # This should be the structure of the JSON, minus the timestamp. We won't
    # check the timestamp because we won't know what it is.
    expected_values = {
        'grade': '100',
        'class_id': '1',
        'student_id': '1',
        'faculty_id': '1',
    }

    for key, value in expected_values.items():
        assert response_json[key] == value

def test_post_class(test_client):
    '''
    Test POST requests for classes.
    Return value should be the same as message.
    '''

    message = {
        'name':'Intermediate Subliminal Basket Weaving',
    }

    response = test_client.post('/api/classes/', data=message)

    assert response.status_code == 200

    response_json = json.loads(response.data)

    # The response JSON should have these 2 keys
    expected_keys = ('class_id', 'name')
    for key in expected_keys:
        assert key in response_json

    # This should be the structure of the JSON, minus the timestamp. We won't
    # check the timestamp because we won't know what it is.
    expected_values = {
        'class_id': 1,
        'name': 'Intermediate Subliminal Basket Weaving',
    }

    for key, value in expected_values.items():
        assert response_json[key] == value

def test_post_student(test_client):
    '''
    Test POST request for student.
    Return value should be the same as message.
    '''

    message = {
        'name':'Harrison Walls',
    }

    response = test_client.post('/api/students/', data=message)

    assert response.status_code == 200

    response_json = json.loads(response.data)

    # The response JSON should have these 2 keys
    expected_keys = ('student_id', 'name')
    for key in expected_keys:
        assert key in response_json

    # This should be the structure of the JSON, minus the timestamp. We won't
    # check the timestamp because we won't know what it is.
    expected_values = {
        'student_id': 1,
        'name': 'Harrison Walls',
    }

    for key, value in expected_values.items():
        assert response_json[key] == value

def test_post_faculty(test_client):
    '''
    Test POST request for faculty.
    Return value should be the same as message.
    '''

    message = {
        'name':'Harrison Walls',
        'title': 'professor',
    }

    response = test_client.post('/api/faculty/', data=message)

    assert response.status_code == 200

    response_json = json.loads(response.data)

    # The response JSON should have these 3 keys
    expected_keys = ('faculty_id', 'name', 'title')
    for key in expected_keys:
        assert key in response_json

    # This should be the structure of the JSON, minus the timestamp. We won't
    # check the timestamp because we won't know what it is.
    expected_values = {
        'faculty_id': 1,
        'name': 'Harrison Walls',
        'title': 'professor',
    }

    for key, value in expected_values.items():
        assert response_json[key] == value

# Tests DELETE requests
def test_delete_grades (test_client):
    '''
    Test Delete request for student.
    Return value should be empty.
    '''
    message = {
        'name':'Harrison Walls',
        'title': 'professor',
    }

    response = test_client.delete('/api/faculty/', data=message)

    assert response.status_code == 200

    response_json = json.loads(response.data)

    assert response_json == []

def test_put_student(test_client):
    '''
    Tests PUT requests for students.
    '''
    message = {
        'name':'Harrison Harrison  Walls',
    }

    response = test_client.put('/api/students/1', data=message)

    assert response.status_code == 200

    response_json = json.loads(response.data)

    expected_keys = ('student_id', 'name')
    for key in expected_keys:
        assert key in response_json

    expected_values = {
        'student_id': 1,
        'name': 'Harrison Harrison Walls',
    }

    for key, value in expected_values.items():
        assert response_json[key] == value

def test_put_faculty(test_client):
    '''
    Test PUT request for student.
    Return value should be the same as message.
    '''
    message = {
        'name':'Harrison Harrison Walls',
    }

    response = test_client.put('/api/faculty_id/1', data=message)

    assert response.status_code == 200

    response_json = json.loads(response.data)

    expected_keys = ('faculty_id', 'name')
    for key in expected_keys:
        assert key in response_json

    expected_values = {
        'faculty_id': 1,
        'name': 'Harrison Harrison Walls',
    }

    for key, value in expected_values.items():
        assert response_json[key] == value

def test_put_class(test_client):
    '''
    Test PUT request for class.
    Return value should be the same as message.
    '''
    message = {
        'name':'Fly Fishing',
    }

    response = test_client.put('/api/classes/1', data=message)

    assert response.status_code == 200

    response_json = json.loads(response.data)

    # The response JSON should have these 3 keys
    expected_keys = ('class_id', 'name')
    for key in expected_keys:
        assert key in response_json

    # This should be the structure of the JSON, minus the timestamp. We won't
    # check the timestamp because we won't know what it is.
    expected_values = {
        'student_id': 1,
        'name': 'Fly Fishing',
    }

    for key, value in expected_values.items():
        assert response_json[key] == value

# Testing the data Base
 def test_DBmanager_constructor(tmpdir):
     '''
     Checks the connection to the database.
     '''
     db_file_path = os.path.join(tmpdir, 'DBmanager.sqlite')
     db = DBmanager(db_file_path)
