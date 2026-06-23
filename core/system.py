from models.student import Student
from models.teacher import Teacher
from models.course import Course
from models.grade import Grade
from core.structures import Stack, Queue
class StudentManagementSystem:
    """
    Main controller class of the Student Management System.
    Manages:
    - students
    - teachers
    - courses
    - grades
    - enrollment
    - analysis
    """

    def __init__(self):
        """
        Initializes system storage dictionaries.
        """
        self._students = {}
        self._teachers = {}
        self._courses = {}
        self._grades_by_student = {}
        self._grades_by_course = {}
        self._grade_history = {}
        self._waitlists = {}

    # ================= STUDENTS =================

    def add_student(self, student: Student) -> bool:
        """Adds a student to the system."""
        student_id = student.get_id()
        if student_id in self._students:
            return False
        self._students[student_id] = student
        self._grades_by_student[student_id] = []
        self._grade_history[student_id] = Stack()
        return True

    def get_student(self, student_id: int):
        """Returns a student by ID."""
        return self._students.get(student_id)

    def get_all_students(self):
        """Returns all students."""
        return list(self._students.values())

    def update_student(self, student_id: int, name: str, email: str) -> bool:
        """Updates student information."""
        student = self.get_student(student_id)
        if student is None:
            return False
        student.set_name(name)
        student.set_email(email)
        return True

    def delete_student(self, student_id: int) -> bool:
        """Deletes a student."""
        if student_id not in self._students:
            return False
        del self._students[student_id]
        del self._grades_by_student[student_id]
        del self._grade_history[student_id]
        return True

    # ================= TEACHERS =================

    def add_teacher(self, teacher: Teacher) -> bool:
        """Adds a teacher."""
        teacher_id = teacher.get_id()
        if teacher_id in self._teachers:
            return False
        self._teachers[teacher_id] = teacher
        return True

    def get_teacher(self, teacher_id: int):
        """Returns a teacher by ID."""
        return self._teachers.get(teacher_id)

    def get_all_teachers(self):
        """Returns all teachers."""
        return list(self._teachers.values())

    def update_teacher(self, teacher_id: int, name: str, email: str) -> bool:
        """Updates teacher info."""
        teacher = self.get_teacher(teacher_id)
        if teacher is None:
            return False
        teacher.set_name(name)
        teacher.set_email(email)
        return True

    def delete_teacher(self, teacher_id: int) -> bool:
        """Deletes a teacher."""
        if teacher_id not in self._teachers:
            return False
        del self._teachers[teacher_id]
        return True

    # ================= COURSES =================

    def add_course(self, course: Course) -> bool:
        """Adds a course."""
        course_crn = course.get_crn()
        if course_crn in self._courses:
            return False
        self._courses[course_crn] = course
        return True

    def get_course(self, course_crn: int):
        """Returns course by CRN."""
        return self._courses.get(course_crn)

    def get_all_courses(self):
        """Returns all courses."""
        return list(self._courses.values())

    def update_course(self, course_crn: int, name: str, teacher_id: int,
                      prerequisites: set, max_capacity: int, credits: int) -> bool:
        """Updates course details."""
        course = self.get_course(course_crn)
        if course is None:
            return False
        course.set_name(name)
        course.set_teacher_id(teacher_id)
        course.set_prerequisites(prerequisites)
        course.set_max_capacity(max_capacity)
        course.set_credits(credits)
        return True

    def delete_course(self, course_crn: int) -> bool:
        """Deletes a course."""
        if course_crn not in self._courses:
            return False
        del self._courses[course_crn]
        return True

    # ================= GRADES =================

    def add_grade(self, grade: Grade) -> bool:
        """Adds a grade."""
        student_id = grade.get_student_id()
        course_crn = grade.get_course_crn()

        if student_id not in self._students:
            return False
        if course_crn not in self._courses:
            return False

        if student_id not in self._grades_by_student:
            self._grades_by_student[student_id] = []
        if course_crn not in self._grades_by_course:
            self._grades_by_course[course_crn] = []

        self._grades_by_student[student_id].append(grade)
        self._grades_by_course[course_crn].append(grade)

        if student_id not in self._grade_history:
            self._grade_history[student_id] = Stack()

        self._grade_history[student_id].push(grade)
        return True

    def update_grade(self, student_id: int, course_crn: str, new_score: float) -> bool:
        """Updates a grade."""
        grades = self._grades_by_student.get(student_id)
        if grades is None:
            return False

        for grade in grades:
            if grade.get_course_crn() == course_crn:
                self._grade_history[student_id].push(
                    Grade(
                        student_id,
                        course_crn,
                        grade.get_score(),
                        grade.get_semester()
                    )
                )
                grade.set_score(new_score)
                return True
        return False

    def undo_grade_change(self, student_id: int) -> bool:
        """Undo last grade change."""
        if student_id not in self._grade_history:
            return False

        history = self._grade_history[student_id]
        if history.is_empty():
            return False

        old_grade = history.pop()
        grades = self._grades_by_student[student_id]

        for index, grade in enumerate(grades):
            if grade.get_course_crn() == old_grade.get_course_crn():
                grades[index] = old_grade
                return True
        return False

    def get_student_grades(self, student_id: int):
        """Returns student grades."""
        return self._grades_by_student.get(student_id, [])

    def get_course_grades(self, course_crn: str):
        """Returns course grades."""
        return self._grades_by_course.get(course_crn, [])

    # ================= ENROLLMENT =================

    def enroll_student(self, student_id: int, crn: int) -> bool:
        """Enrolls a student in a course."""
        student = self._students.get(student_id)
        course = self._courses.get(crn)

        if student is None or course is None:
            return False

        if crn in student.get_enrolled_courses():
            return False

        completed_courses = [
            grade.get_course_crn()
            for grade in self._grades_by_student.get(student_id, [])
        ]

        if not course.get_prerequisites().issubset(completed_courses):
            return False

        if course.is_full():
            if crn not in self._waitlists:
                self._waitlists[crn] = Queue()
            self._waitlists[crn].enqueue(student_id)
            return False

        course.add_student(student_id)
        student.enroll_course(crn)
        return True

    def process_waitlist(self, crn: int) -> bool:
        """Processes waitlist."""
        course = self._courses.get(crn)
        if course is None:
            return False

        waitlist = self._waitlists.get(crn)
        if waitlist is None or waitlist.is_empty():
            return False

        if course.is_full():
            return False

        student_id = waitlist.dequeue()
        student = self._students.get(student_id)

        if student is None:
            return False

        course.add_student(student_id)
        student.enroll_course(crn)
        return True

    def drop_student(self, student_id: int, crn: int) -> bool:
        """Drops a student from a course."""
        student = self._students.get(student_id)
        course = self._courses.get(crn)

        if student is None or course is None:
            return False

        if crn not in student.get_enrolled_courses():
            return False

        course.remove_student(student_id)
        student.drop_course(crn)

        self.process_waitlist(crn)
        return True

    # ================= SEARCH AND SORT =================

    def search_student_by_name(self, name: str):
        """Searches students by name."""
        result = []
        for student in self._students.values():
            if name.lower() in student.get_name().lower():
                result.append(student)
        return result

    def sort_students_by_name(self, reverse: bool = False):
        """Sorts students by name."""
        students = list(self._students.values())
        n = len(students)

        for i in range(n):
            for j in range(0, n - i - 1):
                current = students[j].get_name().lower()
                nxt = students[j + 1].get_name().lower()

                if (not reverse and current > nxt) or \
                   (reverse and current < nxt):
                    students[j], students[j + 1] = students[j + 1], students[j]

        return students

    def sort_students_by_gpa(self, reverse: bool = False):
        """Sorts students by GPA."""
        students = list(self._students.values())
        return sorted(
            students,
            key=lambda student: self.calculate_gpa(student.get_id()),
            reverse=reverse
        )

    # ================= ANALYSIS =================

    def calculate_gpa(self, student_id: int) -> float:
        """Calculates GPA."""
        grades = self._grades_by_student.get(student_id)
        if not grades:
            return 0.0

        total_points = 0
        total_credits = 0

        for grade in grades:
            course = self._courses.get(grade.get_course_crn())
            if course is None:
                continue

            total_points += grade.calculate_grade_points() * course.get_credits()
            total_credits += course.get_credits()

        if total_credits == 0:
            return 0.0

        return total_points / total_credits

    def get_class_average(self, crn: int) -> float:
        """Returns class average."""
        grades = self._grades_by_course.get(crn)
        if not grades:
            return 0.0

        total = 0
        for grade in grades:
            total += grade.get_score()

        return total / len(grades)

    def get_top_students(self, n: int):
        """Returns top N students by GPA."""
        students = list(self._students.values())

        sorted_students = sorted(
            students,
            key=lambda student: self.calculate_gpa(student.get_id()),
            reverse=True
        )

        return sorted_students[:n]
    
    def get_available_roles(self) -> list:
        """Returns all available roles dynamically."""
        return list(set(
            user.get_role()
            for user in self.get_all_students() + self.get_all_teachers()
        ))
        
    def get_all_grades(self) -> list:
        """
        Returns all grades in the system.
        Complexity: O(n)
        """
        all_grades = []
        for grades in self._grades_by_student.values():
            all_grades.extend(grades)
        return all_grades