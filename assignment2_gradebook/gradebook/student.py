from typing import Dict
from .course import Course

class Student:
    def __init__(self, student_id: str, name: str):
        self.student_id = student_id
        self.name = name
        self.courses: Dict[str,Course] = {}

    def enroll(self, course:Course) -> None:
        if course.course_name in self.courses:
            raise ValueError(f'{self.name} is already enrolled in {course.course_name}')
        self.courses[course.course_name] = course
