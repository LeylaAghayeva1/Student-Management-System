# Student Management System

A desktop application for managing students, teachers, courses and grades.
Built with Python using OOP principles, SQLite storage, pandas analysis and a tkinter GUI.

---

## Features

- Add, edit, delete and search students and teachers
- Manage courses with prerequisites and enrollment capacity
- Assign grades with automatic GPA calculation
- Undo grade changes using a history stack
- Course waitlist using a queue when capacity is full
- Data analysis with pandas and 4 matplotlib chart types
- Role-based login — Teacher and Student views
- SQLite database with JSON export/import
- Unit tested with unittest

---

## Project 

Student-Management-System/

├── main.py

├── requirements.txt

├── models/          # Person, Student, Teacher, Course, Grade

├── core/            # StudentManagementSystem, Stack, Queue

├── data/            # Storage — SQLite and JSON

├── analysis/        # Analytics — pandas and matplotlib

├── gui/             # tkinter interface

│   └── screens/     # login, dashboard, students, courses, analytics

└── test/            # Unit tests

---

## Installation

**Requirements:** Python 3.10 or higher

1. Clone or download the project
2. Navigate to the project folder:
```bash
cd Student-Management-System
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
python3 main.py
```

The database is created automatically on first run.

---

## Login

Two demo accounts are created automatically on first run:

| Name | Role |
|------|------|
| Demo | Student |
| Demo | Teacher |

Type the name in the login field, select the role and click Login.

---

## Usage

**Teacher view:**
- **Dashboard** — see total students, courses, grades and average GPA
- **Students** — add, edit, delete and search students
- **Courses** — manage courses, view and add grades
- **Analytics** — view statistics and charts

**Student view:**
- **Dashboard** — see personal GPA and grade history
- **Courses** — view available courses

---

## Running Tests

```bash
python3 -m unittest test.test_models -v
```

23 unit tests covering Student, Teacher, Course and Grade models.

---

## Data Management

- Data is saved automatically to `students.db` on exit
- Export data to JSON via the export button
- Import data from JSON files

---

## Technologies

| Technology | Purpose |
|------------|---------|
| Python 3 | Core language |
| tkinter | GUI framework |
| SQLite | Database storage |
| pandas | Data analysis |
| matplotlib | Charts and visualization |
| unittest | Unit testing |