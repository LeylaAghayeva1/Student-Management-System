class Grade:
    """
    Represents a student's grade for a course.
    """
    _student_id: int
    _course_crn: str
    _score: float
    _letter_grade: str
    _semester: str
    def __init__(
        self,
        student_id: int,
        course_crn: str,
        score: float,
        semester: str
    ):
        """
        Initializes grade information.
        """
        self._student_id = student_id
        self._course_crn = course_crn
        self._score = score
        self._semester = semester
        self._letter_grade = ""
        self.calculate_letter()


    def get_student_id(self) -> int:
        """Returns student ID."""
        return self._student_id
    def get_course_crn(self) -> str:
        """Returns course CRN."""
        return self._course_crn
    def get_score(self) -> float:
        """Returns score."""
        return self._score
    def get_letter_grade(self) -> str:
        """Returns letter grade."""
        return self._letter_grade
    def get_semester(self) -> str:
        """Returns semester."""
        return self._semester
    def set_score(self, score: float) -> None:
        """
        Updates score and recalculates letter grade.
        """
        self._score = score
        self.calculate_letter()
        
    def calculate_letter(self) -> None:
        """
        Converts numeric score into letter grade.
        """
        if self._score < 0 :
            raise ValueError("Score cannot be negative.")
        if self._score >= 93.5:
            self._letter_grade = "A"
        elif self._score >= 89.5:
            self._letter_grade = "A-"
        elif self._score >= 86.5:
            self._letter_grade = "B+"
        elif self._score >= 82.5:
            self._letter_grade = "B"
        elif self._score >= 79.5:
            self._letter_grade = "B-"
        elif self._score >= 76.5:
            self._letter_grade = "C+"
        elif self._score >= 72.5:
            self._letter_grade = "C"
        elif self._score >= 66.5:
            self._letter_grade = "D+"
        elif self._score >= 59.5:
            self._letter_grade = "D"
        else:
            self._letter_grade = "F"
        
    def calculate_grade_points(self) -> float:
        """
        Converts letter grade into grade points for GPA calculation.
        """
        if self._letter_grade == "A":
            return 4.0
        elif self._letter_grade == "A-":
            return 3.67
        elif self._letter_grade == "B+":
            return 3.33
        elif self._letter_grade == "B":
            return 3.0
        elif self._letter_grade == "B-":
            return 2.67
        elif self._letter_grade == "C+":
            return 2.33
        elif self._letter_grade == "C":
            return 2.0
        elif self._letter_grade == "D+":
            return 1.33
        elif self._letter_grade == "D":
            return 1.0
        else:
            return 0.0

    def __str__(self) -> str:
        """
        Returns grade information as a string.
        """
        return (
            "Student ID: " + str(self._student_id)
            + " - Course CRN: " + self._course_crn
            + " - Score: " + str(self._score)
            + " - Letter Grade: " + self._letter_grade
            + " - Semester: " + self._semester
        )