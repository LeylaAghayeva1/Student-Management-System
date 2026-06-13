class Grade:
    """
    Represents a student's grade record for a specific course.
    Stores student ID, course CRN, numeric score, calculated
    letter grade, semester information, and a unique record key.
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
        semester: str, 
        max_score=100
    ):
        """
        Initializes a Grade object.
        Creates a grade record and automatically calculates the
        corresponding letter grade from the numeric score.
        Args:
        student_id (int): ID of the student.
        course_crn (str): CRN of the course.
        score (float): Student's numeric score.
        semester (str): Semester in which the course was taken.
        max_score (int, optional): Maximum possible score.
        Defaults to 100.
        """
        self._max_score=max_score
        self._student_id = student_id
        self._course_crn = course_crn
        self._score = score
        self._semester = semester
        self._letter_grade = ""
        self._record_key=(student_id, course_crn, semester)
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
    def get_record_key(self) -> tuple:
        """
        Returns the id of the student, 
        the crn of the class that student took, 
        and the semester
        """
        return self._record_key
    def get_max_score(self):
        """
        Returns max score
        """
        return self._max_score
    def set_score(self, score: float) -> None:
        """
        Updates score and recalculates letter grade.
        """
        if score < 0 or score > self._max_score:
            raise ValueError(f"Score must be between 0 and {self._max_score}.")
        else:
            self._score = score
            self.calculate_letter()
        
    def calculate_letter(self) -> None:
        """
        Converts numeric score into letter grade.
        """
        if self._score < 0 or self._score>self._max_score:
            raise ValueError(f"Score must be between 0 and {self._max_score}.")
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
        
    def to_dict(self) -> dict:
        """
        Converts the Grade object into a dictionary.
        The dictionary contains all grade-related information including
        student ID, course CRN, score, letter grade, semester, and record key.
        Returns:
            dict: Dictionary representation of the grade.
        """
        return {
            "student_id": self._student_id,
            "course_crn": self._course_crn,
            "score": self._score,
            "letter_grade": self._letter_grade,
            "semester": self._semester,
            "max_score": self._max_score,
        }
        
    @staticmethod
    def from_dict(data: dict):
        """
        Creates a Grade object from dictionary data.
        Used when loading grade information from storage.
        Args:
            data (dict): Dictionary containing grade information.
        Returns:
            Grade: Reconstructed Grade object.
        """
        grade = Grade(
            data["student_id"],
            data["course_crn"],
            data["score"],
            data["semester"],
            data["max_score"]
        )
        return grade