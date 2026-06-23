import tkinter as tk
from tkinter import ttk
class AnalyticsFrame(tk.Frame):
    """
    Analytics screen.
    Provides:
    - Statistics panel
    - Grade distribution chart
    - Course averages chart
    - GPA distribution chart
    - Top students chart
    Uses Analytics class for all calculations.
    GUI does not contain analysis logic.
    """
    def __init__(self, parent, analytics):
        """
        Initializes analytics screen.
        Args:
            parent:
                Parent tkinter widget.
            analytics:
                Analytics object.
        Complexity:
            O(n) because DataFrames are prepared.
        """
        super().__init__(parent)
        self._analytics = analytics
        # Build data before displaying statistics
        self._analytics.build_grades_dataframe()
        self._analytics.build_students_dataframe()
        self.create_statistics()
        self.create_buttons()
        
    def create_statistics(self):
        """
        Displays:
        - Mean grade
        - Maximum grade
        - Minimum grade
        - Standard deviation
        Complexity:
            O(n)
        """
        stats = self._analytics.get_grade_statistics()
        text = (
            f"Mean: {round(stats.get('mean', 0), 2)}\n"
            f"Max: {round(stats.get('max', 0), 2)}\n"
            f"Min: {round(stats.get('min', 0), 2)}\n"
            f"Std: {round(stats.get('std', 0), 2)}"
        )
        frame = ttk.LabelFrame(
            self,
            text="Grade Statistics"
        )
        frame.pack(
            pady=15,
            padx=15,
            fill="x"
        )
        ttk.Label(
            frame,
            text=text,
            font=("Arial", 12)
        ).pack(
            pady=10
        )
        
    def create_buttons(self):
        """
        Creates chart buttons.
        Complexity:
            O(1)
        """
        ttk.Button(
            self,
            text="Grade Distribution",
            command=self._analytics.plot_grade_distribution
        ).pack(
            pady=5
        )
        ttk.Button(
            self,
            text="Course Averages",
            command=self._analytics.plot_course_averages
        ).pack(
            pady=5
        )
        ttk.Button(
            self,
            text="GPA Distribution",
            command=self._analytics.plot_gpa_distribution
        ).pack(
            pady=5
        )
        ttk.Button(
            self,
            text="Top Students",
            command=lambda:
                self._analytics.plot_top_students(5)
        ).pack(
            pady=5
        )