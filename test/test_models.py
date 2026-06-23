import unittest
from models.student import Student
from models.teacher import Teacher
from models.course import Course
from models.grade import Grade
# ============================
# Student Tests
# ============================
class TestStudent(unittest.TestCase):
    def setUp(self):
        self.student = Student(
            1,
            "Alice",
            "Smith",
            "alice@gmail.com",
            2
        )
        self.course = Course(
            101,
            "Programming",
            1,
            set(),
            30,
            3
        )
    def test_get_name(self):
        """
        Checks student name getter.
        """
        self.assertEqual(
            self.student.get_name(),
            "Alice"
        )
    def test_enroll_course(self):
        """
        Checks adding a course.
        """
        result = self.student.enroll_course(
            self.course.get_crn()
        )
        self.assertTrue(result)
        self.assertIn(
            self.course.get_crn(),
            self.student.get_enrolled_courses()
        )
    def test_enroll_duplicate(self):
        """
        Checks duplicate enrollment prevention.
        """
        self.student.enroll_course(
            self.course.get_crn()
        )
        result = self.student.enroll_course(
            self.course.get_crn()
        )
        self.assertFalse(result)
        # ensure course exists only once
        self.assertEqual(
            self.student.get_enrolled_courses().count(
                self.course.get_crn()
            ),
            1
        )
    def test_drop_course(self):
        """
        Checks course removal.
        drop_course() does not return bool,
        so we test the final state.
        """
        self.student.enroll_course(
            self.course.get_crn()
        )
        self.student.drop_course(
            self.course.get_crn()
        )
        self.assertNotIn(
            self.course.get_crn(),
            self.student.get_enrolled_courses()
        )
    def test_get_role(self):
        """
        Checks student role.
        """
        self.assertEqual(
            self.student.get_role(),
            "Student"
        )
    def test_to_dict(self):
        """
        Checks serialization keys.
        """
        data = self.student.to_dict()
        self.assertIn(
            "id",
            data
        )
        self.assertIn(
            "name",
            data
        )
        self.assertIn(
            "surname",
            data
        )
        self.assertIn(
            "email",
            data
        )
        self.assertIn(
            "year_of_study",
            data
        )
    def test_from_dict(self):
        """
        Checks object reconstruction.
        """
        data = self.student.to_dict()
        new_student = Student.from_dict(data)
        self.assertEqual(
            new_student.get_name(),
            self.student.get_name()
        )
        self.assertEqual(
            new_student.get_id(),
            self.student.get_id()
        )
# ============================
# Teacher Tests
# ============================
class TestTeacher(unittest.TestCase):
    def setUp(self):
        self.teacher = Teacher(
            1, "John", "Smith",
            "john@gmail.com",
            "Computer Science"
        )
        self.course = Course(
            101, "Python", 1, set(), 30, 3
        )
    def test_assign_course(self):
        result = self.teacher.assign_course(self.course.get_crn())
        self.assertTrue(result)
        self.assertIn(
            self.course.get_crn(),
            self.teacher.get_teaching_courses()
        )
    def test_assign_duplicate(self):
        self.teacher.assign_course(self.course.get_crn())
        result = self.teacher.assign_course(self.course.get_crn())
        self.assertFalse(result)
    def test_get_role(self):
        self.assertEqual(self.teacher.get_role(), "Teacher")
    def test_get_department(self):
        self.assertEqual(
            self.teacher.get_department(),
            "Computer Science"
        )
# ============================
# Course Tests
# ============================
class TestCourse(unittest.TestCase):
    def setUp(self):
        self.course = Course(
            101,
            "Data Structures",
            1,
            set(),
            1,
            3
        )
    def test_get_crn(self):
        self.assertEqual(
            self.course.get_crn(),
            101
        )
    def test_get_name(self):
        self.assertEqual(
            self.course.get_name(),
            "Data Structures"
        )
    def test_add_student(self):
        result = self.course.add_student(
            1
        )
        self.assertTrue(result)
        self.assertIn(
            1,
            self.course.get_student_ids()
        )
    def test_add_duplicate_student(self):
        self.course.add_student(
            1
        )
        result = self.course.add_student(
            1
        )
        self.assertFalse(result)
    def test_is_full(self):
        self.course.add_student(
            1
        )
        self.assertTrue(
            self.course.is_full()
        )
    def test_prerequisites(self):
        self.course.add_prerequisite(
            100
        )
        self.assertIn(
            100,
            self.course.get_prerequisites()
        )
# ============================
# Grade Tests
# ============================
class TestGrade(unittest.TestCase):
    def setUp(self):
        self.grade = Grade(
            1,
            101,
            95,
            "Spring"
        )
    def test_letter_grade_a(self):
        self.assertEqual(
            self.grade.get_letter_grade(),
            "A"
        )
    def test_letter_grade_f(self):
        grade = Grade(
            1,
            101,
            40,
            "Spring"
        )
        self.assertEqual(
            grade.get_letter_grade(),
            "F"
        )
    def test_grade_points_a(self):
        self.assertEqual(
            self.grade.calculate_grade_points(),
            4.0
        )
    def test_invalid_score(self):
        with self.assertRaises(ValueError):
            Grade(
                1,
                101,
                -10,
                "Spring"
            )
    def test_set_score(self):
        self.grade.set_score(
            80
        )
        self.assertEqual(
            self.grade.get_score(),
            80
        )
        self.assertEqual(
            self.grade.get_letter_grade(),
            "B-"
        )
    def test_record_key(self):
        key = self.grade.get_record_key()
        self.assertEqual(
            key,
            (
                1,
                101,
                "Spring"
            )
        )
# ============================
# Run tests
# ============================
if __name__ == "__main__":
    unittest.main()