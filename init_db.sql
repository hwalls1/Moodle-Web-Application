DROP TABLE IF EXISTS class;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS faculty;
DROP TABLE IF EXISTS grade;

PRAGMA foreign_keys = ON;

CREATE TABLE class(name TEXT, class_id INTEGER PRIMARY KEY);

CREATE TABLE student(name TEXT, student_id INTEGER PRIMARY KEY,
                     username TEXT, password TEXT,
                     class_id INTEGER,
                     FOREIGN KEY (class_id) REFERENCES class(class_id));

CREATE TABLE faculty(name TEXT, title TEXT, faculty_id INTEGER PRIMARY KEY,
                     username TEXT, password TEXT,
                     class_id INTEGER,
                     FOREIGN KEY (class_id) REFERENCES class(class_id));

CREATE TABLE grade(grade TEXT, class_id INTEGER, student_id INTEGER,
                   faculty_id INTEGER,
                    FOREIGN KEY (class_id) REFERENCES class(class_id),
                    FOREIGN KEY (student_id) REFERENCES student(student_id),
                    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id));