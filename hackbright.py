"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a GitHub account name, print info about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :github
        """

    db_cursor = db.session.execute(QUERY, {'github': github})

    row = db_cursor.fetchone()

    print("Student: {} {}\nGitHub account: {}".format(row[0], row[1], row[2]))


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """
    sql = """INSERT INTO students (first_name, last_name, github)
            VALUES (:first_name, :last_name, :github) """

    db.session.execute(sql, {'first_name': first_name,
                            'last_name': last_name,
                            'github': github})

    db.session.commit()

    print(f"Successfully added student {first_name} {last_name}")


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    QUERY = """
        SELECT title, description, max_grade
        FROM projects
        WHERE title = :title """ #SQL and SQLalchemy query, setting the params for what we want
    
    db_cursor = db.session.execute(QUERY, {'title': title}) #processes the query and points to the info  

    row = db_cursor.fetchone() #returns a tuple of what was requested in line 60 SELECT

    print(f'The {row[0]} project involves {row[1]} and has a max grade of {row[2]}') 
    #row[0] = title because it's the first thing requested in line 60 SELECT


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    QUERY = """ SELECT student_github, project_title, grade
        FROM grades
        WHERE project_title = :title AND student_github = :github """
        # :title(placeholder) we'll give you that value later in line 79 (db_cursor)

    db_cursor = db.session.execute(QUERY, {'title': title, 'github': github})
    #:title (placeholder) is referring to the 'title' key. 

    row = db_cursor.fetchone()

    print(f"{row[0]}'s grade for the {row[1]} project was {row[2]}")


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    sql = """INSERT INTO grades (student_github, project_title, grade)
            VALUES (:student_github, :project_title, :grade) """

    db.session.execute(sql, {'student_github': github, 
                            'project_title': title,
                            'grade': grade })

    db.session.commit()

    print(f"Successfully added grade for {github}")

def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received
    as a command.
    """

    command = None

    while command != "quit":
        input_string = input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

    #input_string = "student marissaskud"
    #tokens = ["student", 'marissaskud']
    #command = ["student"]
    #args = ["marissaskud"]

        elif command == "new_student":
            first_name, last_name, github = args  # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project_title":
            title = args[0]
            get_project_by_title(title)

        elif command == "grade_on_project":
            username, project = args
            get_grade_by_github_title(username, project)

        elif command == "give_grade":
            username, project_title, grade = args
            assign_grade(username, project_title, grade)

        else:
            if command != "quit":
                print("Invalid Entry. Try again.")


if __name__ == "__main__":
    connect_to_db(app)

    handle_input()

    # To be tidy, we close our database connection -- though,
    # since this is where our program ends, we'd quit anyway.

    db.session.close()
