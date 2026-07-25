from typing import Dict, List, Optional
from .enums import Category
from .assignment import Assignment

CATEGORY_WEIGHTS: Dict[Category, float] = {
    Category.HOMEWORK: 0.20,
    Category.QUIZZES: 0.20,
    Category.MIDTERM: 0.25,
    Category.FINAL_EXAM: 0.35,
}

""""Track assignments for one course and calculate weighted grades"""
class Course:
    def __init__(self, course_name: str, credit_hours: float):
        self.course_name = course_name
        self.credit_hours = credit_hours
        self.categories = dict(CATEGORY_WEIGHTS)
        self.assignments: List[Assignment] = []

    def add_assignment (self, assignment: Assignment) -> None:
        if not isinstance(assignment, Assignment):
            raise TypeError("assignment must be an Assignment instance")
        if assignment.category not in self.categories:
            raise ValueError("assignment category is not supported by this course")

        self.assignments.append(assignment)
    
    def get_category_average(self, category: Category) -> Optional[float]:
        if category not in self.categories:
            raise ValueError("category is not supported by this course")

        category_assignments = [
            assignment for assignment in self.assignments if assignment.category == category
        ]
        if not category_assignments:
            return None

        return sum(assignment.percentage for assignment in category_assignments) / len(category_assignments)
        
    def get_course_grade(self) -> Optional[float]:
        weighted_sum = 0.0
        weight_used = 0.0

        for category, weight in self.categories.items():
            category_average = self.get_category_average(category)
            if category_average is None:
                continue

            weighted_sum += category_average * weight
            weight_used += weight

        if weight_used == 0:
            return None

        return weighted_sum / weight_used
