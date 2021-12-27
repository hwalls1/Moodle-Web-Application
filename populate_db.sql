
INSERT INTO class(name) VALUES('CS-232');

INSERT INTO student(name, class_id, username, password)
VALUES('Micheas', 1, 'micheas', 'micheas');

INSERT INTO faculty(name, title, username, password, class_id)
VALUES('Sommer','Prof','Sommer', 'Sommer', 1);

INSERT INTO grade(grade, class_id, student_id, faculty_id)
VALUES ('A',1,1,1);

INSERT INTO class(name)
VALUES('Math-339');

INSERT INTO student(name, class_id, username, password)
VALUES('Micheas', 2, 'micheas', 'micheas');

INSERT INTO faculty(name, title, username, password, class_id)
VALUES('Hartman','Prof','Hartman', 'Hartman', 2);

INSERT INTO grade(grade, class_id, student_id, faculty_id)
VALUES ('A',2,1,2);

INSERT INTO class(name)
VALUES('Math-229');

INSERT INTO student(name, class_id, username, password)
VALUES('Micheas', 3, 'micheas', 'micheas');

INSERT INTO faculty(name, title, username, password, class_id)
VALUES('Pasteur','Prof','Pasteur', 'Pasteur', 3);

INSERT INTO grade(grade, class_id, student_id, faculty_id)
VALUES ('B-',3,1,3);

/* More aribitray entries */
/* classes */
INSERT INTO class(name) VALUES('CS-200'); /* 4 */
INSERT INTO class(name) VALUES('CS-112');
INSERT INTO class(name) VALUES('Math-211');
INSERT INTO class(name) VALUES('Math-212'); /* 7 */
INSERT INTO class(name) VALUES('Math-112');
INSERT INTO class(name) VALUES('Math-111');
INSERT INTO class(name) VALUES('Math-229'); /* 10 */
INSERT INTO class(name) VALUES('Math-339');

/* students */
INSERT INTO student(name, class_id, username, password) /* 4 */
VALUES('A`dmin', 5, 'admin', 'password');
INSERT INTO student(name, class_id, username, password)
VALUES('John Johns', 3, 'username', 'password');
INSERT INTO student(name, class_id, username, password)
VALUES('Michael Michaels', 2, 'ubername', 'password');
INSERT INTO student(name, class_id, username, password) /* 7 */
VALUES('David Davidson', 8, 'user_name', 'password');
INSERT INTO student(name, class_id, username, password)
VALUES('Ron Ronaldo', 6, 'usernam', 'password');
INSERT INTO student(name, class_id, username, password)
VALUES('Gen`erc Ericson', 1, 'name', 'password');

/*  faculty */
INSERT INTO faculty(name, title, username, password, class_id) /* 4 */
VALUES('Bowen','Prof','Bowen', 'Bowen', 6);
INSERT INTO faculty(name, title, username, password, class_id)
VALUES('Byrnes','Prof','Byrnes', 'Byrnes', 4);
INSERT INTO faculty(name, title, username, password, class_id)
VALUES('Byrnes','Prof','Byrnes', 'Byrnes', 5);
INSERT INTO faculty(name, title, username, password, class_id) /* 7 */
VALUES('The Mysterious Stranger','Prof','username', 'password', 11);

/* grades */
INSERT INTO grade(grade, class_id, student_id, faculty_id)
VALUES ('C+', 5, 4, 6);
INSERT INTO grade(grade, class_id, student_id, faculty_id)
VALUES ('C+', 6, 8, 4);
