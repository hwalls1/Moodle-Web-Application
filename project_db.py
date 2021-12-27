import sqlite3
from flask import g


class DBManager:
    """
        This class handles all database interactions for a flask app.

        Functions return lists of dictionaries where relevant
        Lists of dictionaries can be accessed the same way an OrderedDict
        can be accessed. The only difference, really, is that the
        dictionaries are not in a particular order.
    """
    def __init__(self, flask_app):
        """
            Creates a DBHandler object.
        :param flask_app - Flask app object
        """
        self.app = flask_app

    def connect_db(self):
        """
            Returns a sqlite connection object associated with the
            application's database file.
            """

        conn = sqlite3.connect(self.app.config['DATABASE'], timeout=1)
        conn.row_factory = sqlite3.Row

        return conn

    def get_db(self):
        """
            Returns a database connection. If a connection has already been
            created, the existing connection is used, otherwise it creates
            a new connection.
             """

        if not hasattr(g, 'sqlite_db'):
            g.sqlite_db = self.connect_db()

        return g.sqlite_db

    def init_db(self, init_db_sql_file):
        """
        This function initializes an empty database for the app.
        Creates the 4 tables in their entirety
        It does not populate the database; that is done elsewhere.
        Warning: wipes the entire database and creates all empty tables.

        :param init_db_sql_file: the name of a file that creates all of the
        tables in the data base.

        :return: n/a; makes all empty table in database
        """

        conn = self.get_db()
        cur = conn.cursor()

        db_creation_script = self.read_sql_script(init_db_sql_file)

        cur.executescript(db_creation_script)
        conn.commit()  # database should have all empty tables

    def populate_db(self, populate_db_sql_file):
        """
        Populates the database for the app by executing some script
        in populate_db_sql_file.

        :param populate_db_sql_file: sql script that populates the data
        :return: n/a; database now populated
        """
        conn = self.get_db()
        cur = conn.cursor()

        populate_db_script = self.read_sql_script(populate_db_sql_file)

        cur.executescript(populate_db_script)
        conn.commit()  # database should no longer be empty

    def read_sql_script(self, filename):
        """
        This function will read in and then return an SQL script
        and then return it.

        Based on: https://stackoverflow.com/questions/19472922/
        reading-external-sql-script-in-python

        :return: the entire SQL script in filename
        """
        try:
            file = open(filename, 'r')

            sql_file = file.read()
            file.close()
            return sql_file

        except FileNotFoundError or FileExistsError:
            print('Could not find that .sql file')

    def get_id(self):
        """
            Returns a list of students in the same class sorted by name.
            """

        conn = self.get_db()
        cur = conn.cursor()

        query = '''
            SELECT student.name as s_name, class.name as c_name, grade
            FROM student, grade, class
            WHERE student.class_id = class.class_id;
            '''
        cur.execute(query)
        # fetchall() gets all the rows as a list
        all_rows_gotten = cur.fetchall()

        results = []
        for row in all_rows_gotten:
            results.append(dict(row))

        return results

    def get_class_grade(self, username=None):
        """
            Returns the classes and grades for students.
            """

        conn = self.get_db()
        cur = conn.cursor()

        # if want names, classes and grades for a specific user
        if username is not None:
            query = '''
                SELECT student.name as s_name, class.name as c_name, grade
                FROM student, grade, class
                WHERE student.class_id = class.class_id AND
                      student.username = ?;
                '''
            cur.execute(query, (username,))

        # else, get names, classes and grades for everybody
        else:
            query = '''
                SELECT student.name as s_name, class.name as c_name, grade
                FROM student, grade, class
                WHERE student.class_id = class.class_id;
                '''
            cur.execute(query)

        # fetchall() gets all the rows as a list
        all_rows_gotten = cur.fetchall()

        results = []
        for row in all_rows_gotten:
            results.append(dict(row))

        return results

    def get_name_of_user(self, username, table):
        """
        Returns the full, actual name of a user with user name username

        :return: 1 dict with 1 name,value pair
        """
        conn = self.get_db()
        cur = conn.cursor()

        # if want name of a faculty member given the username
        if table == 'faculty':
            query = '''
                    SELECT name FROM faculty WHERE username = ?;
                    '''

            cur.execute(query, (username,))

        # else want the name of a student given the username
        else:
            query = '''
                    SELECT name FROM student WHERE username = ?;
                    '''

            cur.execute(query, (username,))

        name_gotten = cur.fetchone()
        return dict(name_gotten)

    def get_faculty(self, username=None):
        """
            Returns a list of faculty, the class they teach, the students
            in that class, and what grade they have.
            """

        conn = self.get_db()
        cur = conn.cursor()

        if username is None:
            query = '''
                SELECT faculty.name as f_name, class.name as c_name,
                student.name as s_name, grade
                FROM student, grade, class, faculty
                WHERE grade.faculty_id = faculty.faculty_id
                AND grade.student_id = student.student_id
                AND grade.class_id = class.class_id;
                '''
            cur.execute(query)

        else:
            query = '''
                SELECT faculty.name as f_name, class.name as c_name,
                student.name as s_name, grade
                FROM student, grade, class, faculty
                WHERE grade.faculty_id = faculty.faculty_id
                AND grade.student_id = student.student_id
                AND grade.class_id = class.class_id
                AND faculty.username = ?;
                '''
            cur.execute(query, (username,))

        all_rows_gotten = cur.fetchall()

        results = []
        for row in all_rows_gotten:
            results.append(dict(row))

        # fetchall() gets all the rows as a list
        if results.__len__ == 0:
            return None
        return results

    def get_student_user(self):
        """
            Returns username and password of a student.
            """

        conn = self.get_db()
        cur = conn.cursor()

        query = '''
            SELECT username, password
            FROM student;
            '''

        cur.execute(query)
        # fetchall() gets all the rows as a list
        all_rows_gotten = cur.fetchall()

        results = []
        for row in all_rows_gotten:
            results.append(dict(row))

        return results

    def get_faculty_user(self):
        """
            Returns username and password of a teacher.
            """

        conn = self.get_db()
        cur = conn.cursor()

        query = '''
            SELECT username, password
            FROM faculty;
            '''

        cur.execute(query)
        # fetchall() gets all the rows as a list
        all_rows_gotten = cur.fetchall()

        results = []
        for row in all_rows_gotten:
            results.append(dict(row))

        return results

    def query_login_info(self, username, password):
        """
        Query the student table to see if the username and password pair
        exists for some student entity in the student table. If not, then
        check the same for a faculty entity

        :param username: candidate username
        :param password: candidate password
        :return: list of 1 dict with matching entity OR None
        """
        conn = self.get_db()
        cur = conn.cursor()

        # if the user is a student
        student_query = '''
                        SELECT username, password, student_id
                        FROM student
                        WHERE student.username = ? AND
                              student.password = ?;
                        '''

        cur.execute(student_query, (username, password))

        student_result = cur.fetchone()
        if student_result is not None:
            return [dict(student_result)]

        # else the user is faculty
        faculty_query = '''
                        SELECT username, password, faculty_id
                        FROM faculty
                        WHERE faculty.username = ? AND
                              faculty.password = ?;
                        '''
        cur.execute(faculty_query, (username, password))

        faculty_result = cur.fetchone()
        if faculty_result is not None:
            return [dict(faculty_result)]
        else:
            return None  # no faculty or student with that username passw pair

    def insert_user(self, username, password, name, class_id, title=None):
        """
        Inserts faculty or a student into the database. If title is None, then
        the entity is assumed to be a student. If the title is some string,
        then the entity must be some faculty member.

        :param username: username of the entity to register
        :param password: password for new entity
        :param name: full name of the actual person
        :param class_id: for faculty this is class taught; for students, it is
        the class enrolled in
        :param title: title of the faculty member
        :return: Nothing. User is entered into database.
        """

        conn = self.connect_db()
        cur = conn.cursor()

        if title is None:
            insertion = '''
                        INSERT INTO student(
                        username, password, name, class_id)
                        VALUES(?,?,?,?);
                        '''
            cur.execute(insertion, (username, password, name, class_id))
            conn.commit()
            # just_inserted_row = self.query_by_id(cur.lastrowid, 'student')
            # return just_inserted_row  # list with 1 dict
            return [{'username': username,
                    'password': password,
                    'name': name,
                    'class_id': class_id}]

        else:
            insertion = '''
                        INSERT INTO faculty(
                        username, password, name, class_id, title)
                        VALUES(?,?,?,?,?);
                        '''
            cur.execute(insertion, (username, password, name, class_id, title))
            conn.commit()
            return [{'username': username,
                     'password': password,
                     'name': name,
                     'class_id': class_id,
                     'title': title}]
