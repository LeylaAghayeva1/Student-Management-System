import pandas as pd
import matplotlib.pyplot as plt
class Analytics:
    """
    Handles data analysis and visualization for the Student Management System.
    This class uses pandas DataFrames to process student and grade data.
    It provides statistical calculations and chart generation.
    """
    def __init__(self, system):
        """
        Initializes Analytics object.
        Args:
            system:
                Reference to StudentManagementSystem object.
        """
        self._system = system
        self._grades_df = None
        self._students_df = None

    def build_grades_dataframe(self) -> pd.DataFrame:
        """
        Creates a DataFrame containing all grade information.
        Columns:
        - Student ID
        - Student Name
        - Course CRN
        - Course Name
        - Score
        - Letter Grade
        - Semester
        Complexity:
        O(n), where n is number of grades.
        """
        data = []
        for grade in self._system.get_all_grades():
            student = self._system.get_student(
                grade.get_student_id()
            )
            course = self._system.get_course(
                grade.get_course_crn()
            )
            data.append(
                {
                    "student_id":
                        grade.get_student_id(),
                    "student_name":
                        student.get_name()
                        if student else "Unknown",
                    "course_crn":
                        grade.get_course_crn(),
                    "course_name":
                        course.get_name()
                        if course else "Unknown",
                    "score":
                        grade.get_score(),
                    "letter_grade":
                        grade.get_letter_grade(),
                    "semester":
                        grade.get_semester()
                }
            )
        self._grades_df = pd.DataFrame(data)
        return self._grades_df

    def build_students_dataframe(self) -> pd.DataFrame:
        """
        Creates DataFrame containing students and GPA values.
        Columns:
        - Student ID
        - Name
        - Surname
        - GPA
        Complexity:
        O(n), where n is number of students.
        """
        data = []
        for student in self._system.get_all_students():
            gpa = self._system.calculate_gpa(
                student.get_id()
            )
            data.append(
                {
                    "student_id":
                        student.get_id(),
                    "name":
                        student.get_name(),
                    "surname":
                        student.get_surname(),
                    "gpa":
                        gpa
                }
            )
        self._students_df = pd.DataFrame(data)
        return self._students_df


    def get_grade_statistics(self) -> dict:
        """
        Returns statistical information about grades.
        Returns:
            Dictionary containing:
            - mean score
            - maximum score
            - minimum score
            - standard deviation
        Complexity:
        O(n)
        """
        if self._grades_df is None:
            self.build_grades_dataframe()
        if self._grades_df.empty:
            return {}
        return {
            "mean":
                self._grades_df["score"].mean(),
            "max":
                self._grades_df["score"].max(),
            "min":
                self._grades_df["score"].min(),
            "std":
                self._grades_df["score"].std()
        }


    def get_top_students(self, n: int) -> list:
        """
        Returns top n students based on GPA.
        Complexity:
        O(n log n) because sorting is used.
        """
        students = []
        for student in self._system.get_all_students():
            students.append(
                {
                    "student_id":
                        student.get_id(),
                    "name":
                        student.get_name(),
                    "gpa":
                        self._system.calculate_gpa(
                            student.get_id()
                        )
                }
            )
        return sorted(
            students,
            key=lambda x: x["gpa"],
            reverse=True
        )[:n]


    def get_course_averages(self) -> dict:
        """
        Calculates average score for every course.
        Returns:
            Dictionary:
            {
                course_crn: average_score
            }
        Complexity:
        O(n)
        """
        if self._grades_df is None:
            self.build_grades_dataframe()
        if self._grades_df.empty:
            return {}
        result = {}
        grouped = (
            self._grades_df
            .groupby("course_crn")["score"]
            .mean()
        )
        for course, average in grouped.items():
            result[course] = average
        return result

    def plot_grade_distribution(self) -> None:
        """
        Creates pie chart showing distribution
        of letter grades.
        Complexity:
        O(n)
        """
        if self._grades_df is None:
            self.build_grades_dataframe()
        if self._grades_df.empty:
            return None
        counts = (
            self._grades_df["letter_grade"]
            .value_counts()
        )
        counts.plot(
            kind="pie",
            autopct="%1.1f%%"
        )
        plt.title(
            "Grade Distribution"
        )
        plt.ylabel("")
        plt.tight_layout()
        plt.show()


    def plot_course_averages(self) -> None:
        """
        Creates bar chart showing average score
        per course.
        Complexity:
        O(n)
        """
        averages = self.get_course_averages()
        if not averages:
            return None
        pd.Series(averages).plot(
            kind="bar"
        )
        plt.title(
            "Course Average Scores"
        )
        plt.xlabel(
            "Course CRN"
        )
        plt.ylabel(
            "Average Score"
        )
        plt.tight_layout()
        plt.show()


    def plot_gpa_distribution(self) -> None:
        """
        Creates histogram showing student GPA distribution.
        Complexity:
        O(n)
        """
        if self._students_df is None:
            self.build_students_dataframe()
        if self._students_df.empty:
            return None
        self._students_df["gpa"].plot(
            kind="hist",
            bins=10
        )
        plt.title(
            "GPA Distribution"
        )
        plt.xlabel(
            "GPA"
        )
        plt.tight_layout()
        plt.show()


    def plot_top_students(self, n:int) -> None:
        """
        Creates horizontal bar chart showing top students.
        Complexity:
        O(n log n)
        """
        top_students = self.get_top_students(n)
        if not top_students:
            return None
        df = pd.DataFrame(top_students)
        df.plot(
            kind="barh",
            x="name",
            y="gpa"
        )
        plt.title(
            f"Top {n} Students by GPA"
        )
        plt.xlabel(
            "GPA"
        )
        plt.ylabel(
            "Student"
        )
        plt.tight_layout()
        plt.show()