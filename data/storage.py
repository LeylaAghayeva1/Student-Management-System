import sqlite3
import json
from models.student import Student
from models.teacher import Teacher
from models.course import Course
from models.grade import Grade
class Storage:
    """
    Handles data persistence for the Student Management System.
    Provides SQLite database storage and JSON import/export functionality.
    Responsible for saving and loading students, teachers, courses,
    and grades.
    """

    def __init__(self, db_path: str):
        """
        Initializes Storage object.
        Args:
            db_path (str): Path to SQLite database file.
        """
        self._db_path = db_path
        self._connection = None

    def connect(self) -> None:
        """
        Opens a connection to the SQLite database.
        Creates or connects to the file at db_path.
        """
        self._connection = sqlite3.connect(self._db_path)

    def disconnect(self) -> None:
        """
        Closes the current SQLite database connection.
        Safe to call even if already disconnected.
        """
        if self._connection:
            self._connection.close()
            self._connection = None

    def create_tables(self) -> None:
        """
        Creates all required database tables if they do not exist.
        Tables created:
            - students: stores student records
            - teachers: stores teacher records
            - courses: stores course records with prerequisites as text
            - enrollments: stores student-course enrollment pairs
            - grades: stores grade records including max_score
        """
        cursor = self._connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY,
            name TEXT,
            surname TEXT,
            email TEXT,
            year_of_study INTEGER
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers(
            id INTEGER PRIMARY KEY,
            name TEXT,
            surname TEXT,
            email TEXT,
            department TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses(
            crn INTEGER PRIMARY KEY,
            name TEXT,
            teacher_id INTEGER,
            prerequisites TEXT,
            max_capacity INTEGER,
            credits INTEGER
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS enrollments(
            course_crn INTEGER,
            student_id INTEGER,
            PRIMARY KEY(course_crn, student_id)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades(
            student_id INTEGER,
            course_crn TEXT,
            score REAL,
            letter_grade TEXT,
            semester TEXT,
            max_score REAL,
            PRIMARY KEY(student_id, course_crn, semester)
        )
        """)
        self._connection.commit()

    def save_student(self, student: Student) -> None:
        """
        Inserts or updates a student record in the database.
        Uses INSERT OR REPLACE so existing records are updated.
        Args:
            student (Student): Student object to save.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO students
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                student.get_id(),
                student.get_name(),
                student.get_surname(),
                student.get_email(),
                student.get_year_of_study()
            )
        )
        self._connection.commit()

    def load_all_students(self) -> list:
        """
        Loads all student records from the database.
        Reconstructs Student objects from raw row data.
        Returns:
            list: List of Student objects.
        """
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM students")
        students = []
        for row in cursor.fetchall():
            students.append(
                Student(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4]
                )
            )
        return students

    def save_teacher(self, teacher: Teacher) -> None:
        """
        Inserts or updates a teacher record in the database.
        Uses INSERT OR REPLACE so existing records are updated.
        Args:
            teacher (Teacher): Teacher object to save.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO teachers
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                teacher.get_id(),
                teacher.get_name(),
                teacher.get_surname(),
                teacher.get_email(),
                teacher.get_department()
            )
        )
        self._connection.commit()

    def load_all_teachers(self) -> list:
        """
        Loads all teacher records from the database.
        Reconstructs Teacher objects from raw row data.
        Returns:
            list: List of Teacher objects.
        """
        cursor = self._connection.cursor()

        cursor.execute("SELECT * FROM teachers")

        teachers = []

        for row in cursor.fetchall():
            teachers.append(
                Teacher(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4]
                )
            )

        return teachers

    def save_course(self, course: Course) -> None:
        """
        Saves course information and enrollment data to the database.
        Converts prerequisites set into comma-separated string
        because SQLite cannot store Python sets directly.
        Also saves each enrolled student into the enrollments table.
        Args:
            course (Course): Course object to save.
        """
        cursor = self._connection.cursor()

        prereq = ",".join(
            str(x) for x in course.get_prerequisites()
        )

        cursor.execute(
            """
            INSERT OR REPLACE INTO courses
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                course.get_crn(),
                course.get_name(),
                course.get_teacher_id(),
                prereq,
                course.get_max_capacity(),
                course.get_credits()
            )
        )

        for student_id in course.get_student_ids():
            cursor.execute(
                """
                INSERT OR REPLACE INTO enrollments
                VALUES (?, ?)
                """,
                (
                    course.get_crn(),
                    student_id
                )
            )
        self._connection.commit()

    def load_all_courses(self) -> list:
        """
        Loads all course records from the database.
        Converts prerequisite string back to a set of integers.
        Uses a second cursor to load enrollment data per course
        without overwriting the outer query cursor.
        Returns:
            list: List of Course objects with enrolled students restored.
        """
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM courses")
        courses = []
        for row in cursor.fetchall():
            prerequisites = (
                set(int(x) for x in row[3].split(","))
                if row[3]
                else set()
            )
            course = Course(
                row[0],
                row[1],
                row[2],
                prerequisites,
                row[4],
                row[5]
            )
            cursor2 = self._connection.cursor()
            cursor2.execute(
                """
                SELECT student_id
                FROM enrollments
                WHERE course_crn = ?
                """,
                (row[0],)
            )
            for student in cursor2.fetchall():
                course.add_student(student[0])
            courses.append(course)
        return courses

    def save_grade(self, grade: Grade) -> None:
        """
        Inserts or updates a grade record in the database.
        Saves all grade fields including max_score for reconstruction.
        Args:
            grade (Grade): Grade object to save.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO grades
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                grade.get_student_id(),
                grade.get_course_crn(),
                grade.get_score(),
                grade.get_letter_grade(),
                grade.get_semester(),
                grade.get_max_score()
            )
        )
        self._connection.commit()

    def load_all_grades(self) -> list:
        """
        Loads all grade records from the database.
        Reconstructs Grade objects using student_id, course_crn,
        score, semester, and max_score.
        Returns:
            list: List of Grade objects.
        """
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM grades")
        grades = []
        for row in cursor.fetchall():
            grades.append(
                Grade(
                    row[0],  # student_id
                    row[1],  # course_crn
                    row[2],  # score
                    row[4],  # semester
                    row[5]   # max_score
                )
            )
        return grades

    def export_to_json(self, data: list, filepath: str) -> None:
        """
        Exports a list of model objects to a JSON file.
        Calls to_dict() on each object before serializing.
        Args:
            data (list): List of objects with to_dict() method.
            filepath (str): Destination file path for the JSON file.
        """
        with open(filepath, "w") as file:
            json.dump(
                [obj.to_dict() for obj in data],
                file,
                indent=4
            )

    def import_from_json(self, filepath: str) -> list:
        """
        Imports raw dictionary data from a JSON file.
        Caller is responsible for converting dicts to model objects
        using the appropriate from_dict() method.
        Args:
            filepath (str): Path to the JSON file to import.
        Returns:
            list: List of raw dictionaries loaded from JSON.
        """
        with open(filepath, "r") as file:
            return json.load(file)

    def save_all(self, system) -> None:
        """
        Saves all system data to the database in one call.
        Iterates over all students, teachers, courses, and grades
        and saves each one individually.
        Args:
            system (StudentManagementSystem): The system to save from.
        """
        for student in system.get_all_students():
            self.save_student(student)
        for teacher in system.get_all_teachers():
            self.save_teacher(teacher)
        for course in system.get_all_courses():
            self.save_course(course)
        for grade in system.get_all_grades():
            self.save_grade(grade)

    def load_all(self, system) -> None:
        """
        Loads all stored data from the database into the system.
        Populates the system with students, teachers, courses,
        and grades by calling the appropriate system add methods.
        Args:
            system (StudentManagementSystem): The system to load into.
        """
        for student in self.load_all_students():
            system.add_student(student)
        for teacher in self.load_all_teachers():
            system.add_teacher(teacher)
        for course in self.load_all_courses():
            system.add_course(course)
        for grade in self.load_all_grades():
            system.add_grade(grade)