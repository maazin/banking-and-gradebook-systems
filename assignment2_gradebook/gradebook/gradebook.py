from typing import Dict, List, Tuple
from .student import Student
from .course import Course
from .assignment import Assignment
from .enums import Category, LetterGrade

LETTER_GRADE_THRESHOLDS: List[Tuple[float, LetterGrade, float]] = [
    (90, LetterGrade.A, 4.0),
    (80, LetterGrade.B, 3.0),
    (70, LetterGrade.C, 2.0),
    (60, LetterGrade.D, 1.0),
    (0, LetterGrade.F, 0.0),
]

class GradeBook:
    def __init__(self):
        self.students: Dict[str, Student] = {}

    def add_student(self, student_id: str, name: str) -> Student:
        if student_id in self.students:
            raise ValueError(f"Student {student_id} already exists")

        student = Student(student_id, name)
        self.students[student_id] = student
        return student
    
    def add_assignment(self, student_id: str, course_name: str, assignment: Assignment) -> None:
        student = self.students.get(student_id)
        if student is None:
            raise ValueError(f"Student {student_id} not found")

        course = student.courses.get(course_name)
        if course is None:
            raise ValueError(f"Course {course_name} not found for student {student_id}")

        course.add_assignment(assignment)

    def enroll_in_course(self, student_id: str, course_name: str, credit_hours: float) -> Course:
        student = self.students.get(student_id)
        if student is None:
            raise ValueError(f"Student {student_id} not found")

        course = Course(course_name, credit_hours)
        student.enroll(course)
        return course

    def get_category_average(self, student_id: str, course_name: str, catergory: Category):
        student = self.students.get(student_id)
        if student is None:
            raise ValueError(f"Student {student_id} not found")

        course = student.courses.get(course_name)
        if course is None:
            raise ValueError(f"Course {course_name} not found for student {student_id}")

        return course.get_category_average(category)


    def get_course_grade(self, student_id: str, course_name: str):
        student = self.students.get(student_id)
        if student is None:
            raise ValueError(f"Student {student_id} not found")

        course = student.courses.get(course_name)
        if course is None:
            raise ValueError(f"Course {course_name} not found for student {student_id}")

        percentage = course.get_course_grade()
        if percentage is None:
            return None

        for threshold, letter_grade, _gpa_points in LETTER_GRADE_THRESHOLDS:
            if percentage >= threshold:
                return percentage, letter_grade

        return percentage, LetterGrade.F

    def calculate_gpa(self, student_id: str) -> float:
        student = self.students.get(student_id)
        if student is None:
            raise ValueError(f"Student {student_id} not found")

        if not student.courses:
            return 0.0

        total_points = 0.0
        total_credit_hours = 0.0

        for course in student.courses.values():
            course_grade = course.get_course_grade()
            if course_grade is None:
                # Assumption: courses without graded assignments behave like pass/fail
                # and do not affect GPA until a percentage grade exists.
                continue

            gpa_points = 0.0
            for threshold, _letter_grade, points in LETTER_GRADE_THRESHOLDS:
                if course_grade >= threshold:
                    gpa_points = points
                    break

            total_points += gpa_points * course.credit_hours
            total_credit_hours += course.credit_hours

        if total_credit_hours == 0:
            return 0.0

        return total_points / total_credit_hours

    def generate_transcript(self, student_id: str) -> str:
        student = self.students.get(student_id)
        if student is None:
            raise ValueError(f"Student {student_id} not found")

        course_rows = []
        for course in student.courses.values():
            course_grade = self.get_course_grade(student_id, course.course_name)
            if course_grade is None:
                course_rows.append([
                    course.course_name,
                    f"{course.credit_hours:.1f}",
                    "No grades available",
                    "No grades available",
                ])
            else:
                percentage, letter_grade = course_grade
                course_rows.append([
                    course.course_name,
                    f"{course.credit_hours:.1f}",
                    f"{percentage:.2f}%",
                    letter_grade.value,
                ])

        gpa = self.calculate_gpa(student_id)

        headers = ["Course Name", "Credit Hours", "Percentage", "Letter Grade"]
        rows = [["Student Name", student.name, "Student ID", student.student_id]] + [headers] + course_rows + [["Cumulative GPA", f"{gpa:.2f}", "", ""]]

        widths = [0, 0, 0, 0]
        for row in rows:
            for index, cell in enumerate(row):
                widths[index] = max(widths[index], len(str(cell)))

        def format_row(row):
            cells = [str(cell).ljust(widths[index]) for index, cell in enumerate(row)]
            return f"| {' | '.join(cells)} |"

        table_width = sum(widths) + (3 * len(widths)) + 1
        top_border = "_" * table_width
        separator = "-" * table_width

        output_lines = [top_border, format_row(rows[0]), separator, format_row(rows[1]), separator]

        if course_rows:
            for row in course_rows:
                output_lines.append(format_row(row))
        else:
            output_lines.append(format_row(["No grades available", "", "", ""]))

        output_lines.append(separator)
        output_lines.append(format_row(rows[-1]))
        output_lines.append(top_border)
        return "\n".join(output_lines)
