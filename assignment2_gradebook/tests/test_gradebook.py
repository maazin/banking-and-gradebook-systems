import unittest
from enum import Enum

from gradebook.assignment import Assignment
from gradebook.course import Course
from gradebook.enums import Category, LetterGrade
from gradebook.gradebook import GradeBook


class ExtraCategory(Enum):
	EXTRA = "EXTRA"


class GradeBookTests(unittest.TestCase):
	def setUp(self):
		self.gradebook = GradeBook()

	def make_assignment(self, name, earned, possible, category):
		return Assignment(name=name, points_earned=earned, points_possible=possible, category=category)

	def enroll_student_with_course(self, student_id="S1", name="Alice", course_name="Math", credit_hours=3.0):
		student = self.gradebook.add_student(student_id, name)
		course = self.gradebook.enroll_in_course(student_id, course_name, credit_hours)
		return student, course

	def test_percentage_points_possible_zero_raises(self):
		assignment = self.make_assignment("Quiz 1", 5, 0, Category.HOMEWORK)

		with self.assertRaises(ValueError):
			_ = assignment.percentage

	def test_percentage_points_earned_greater_than_possible_raises(self):
		assignment = self.make_assignment("Quiz 1", 11, 10, Category.HOMEWORK)

		with self.assertRaises(ValueError):
			_ = assignment.percentage

	def test_percentage_zero_earned_returns_zero(self):
		assignment = self.make_assignment("Quiz 1", 0, 10, Category.HOMEWORK)

		self.assertEqual(assignment.percentage, 0.0)

	def test_course_rejects_category_not_in_weights(self):
		course = Course("Math", 3.0)
		assignment = self.make_assignment("Extra Credit", 1, 1, ExtraCategory.EXTRA)

		with self.assertRaises(ValueError):
			course.add_assignment(assignment)

	def test_course_rejects_same_assignment_object_twice(self):
		course = Course("Math", 3.0)
		assignment = self.make_assignment("Quiz 1", 8, 10, Category.QUIZZES)

		course.add_assignment(assignment)

		with self.assertRaises(ValueError):
			course.add_assignment(assignment)

	def test_single_assignment_category_average_matches_assignment_percentage(self):
		course = Course("Math", 3.0)
		assignment = self.make_assignment("HW 1", 18, 20, Category.HOMEWORK)
		course.add_assignment(assignment)

		self.assertEqual(course.get_category_average(Category.HOMEWORK), assignment.percentage)

	def test_multiple_assignments_same_category_average_is_mean_of_percentages(self):
		course = Course("Math", 3.0)
		first = self.make_assignment("HW 1", 8, 10, Category.HOMEWORK)
		second = self.make_assignment("HW 2", 15, 20, Category.HOMEWORK)
		course.add_assignment(first)
		course.add_assignment(second)

		expected = (first.percentage + second.percentage) / 2
		self.assertAlmostEqual(course.get_category_average(Category.HOMEWORK), expected)

	def test_empty_category_returns_none(self):
		course = Course("Math", 3.0)

		self.assertIsNone(course.get_category_average(Category.QUIZZES))

	def test_category_with_all_zero_scores_returns_zero(self):
		course = Course("Math", 3.0)
		course.add_assignment(self.make_assignment("HW 1", 0, 10, Category.HOMEWORK))
		course.add_assignment(self.make_assignment("HW 2", 0, 20, Category.HOMEWORK))

		self.assertEqual(course.get_category_average(Category.HOMEWORK), 0.0)

	def test_all_four_categories_populated_weighted_sum_matches(self):
		course = Course("Math", 3.0)
		course.add_assignment(self.make_assignment("HW", 10, 10, Category.HOMEWORK))
		course.add_assignment(self.make_assignment("Quiz", 8, 10, Category.QUIZZES))
		course.add_assignment(self.make_assignment("Midterm", 9, 10, Category.MIDTERM))
		course.add_assignment(self.make_assignment("Final", 7, 10, Category.FINAL_EXAM))

		expected = (100.0 * 0.20) + (80.0 * 0.20) + (90.0 * 0.25) + (70.0 * 0.35)
		self.assertAlmostEqual(course.get_course_grade(), expected)

	def test_partial_categories_are_renormalized(self):
		course = Course("Math", 3.0)
		course.add_assignment(self.make_assignment("HW", 10, 10, Category.HOMEWORK))
		course.add_assignment(self.make_assignment("Midterm", 8, 10, Category.MIDTERM))

		expected = ((100.0 * 0.20) + (80.0 * 0.25)) / (0.20 + 0.25)
		self.assertAlmostEqual(course.get_course_grade(), expected)

	def test_single_category_grade_equals_that_category_average(self):
		course = Course("Math", 3.0)
		course.add_assignment(self.make_assignment("Quiz 1", 7, 10, Category.QUIZZES))

		self.assertEqual(course.get_course_grade(), course.get_category_average(Category.QUIZZES))

	def test_zero_assignments_anywhere_returns_none(self):
		course = Course("Math", 3.0)

		self.assertIsNone(course.get_course_grade())

	def test_letter_grade_boundary_one_hundred_is_a(self):
		student, course = self.enroll_student_with_course()
		self.gradebook.add_assignment(student.student_id, course.course_name, self.make_assignment("HW", 10, 10, Category.HOMEWORK))

		percentage, letter_grade = self.gradebook.get_course_grade(student.student_id, course.course_name)

		self.assertEqual(percentage, 100.0)
		self.assertEqual(letter_grade, LetterGrade.A)

	def test_letter_grade_boundary_ninety_is_a(self):
		student, course = self.enroll_student_with_course()
		self.gradebook.add_assignment(student.student_id, course.course_name, self.make_assignment("HW", 9, 10, Category.HOMEWORK))

		percentage, letter_grade = self.gradebook.get_course_grade(student.student_id, course.course_name)

		self.assertEqual(percentage, 90.0)
		self.assertEqual(letter_grade, LetterGrade.A)

	def test_course_grade_stays_between_zero_and_hundred(self):
		course = Course("Math", 3.0)
		course.add_assignment(self.make_assignment("HW", 0, 10, Category.HOMEWORK))
		course.add_assignment(self.make_assignment("Quiz", 10, 10, Category.QUIZZES))

		grade = course.get_course_grade()

		self.assertGreaterEqual(grade, 0.0)
		self.assertLessEqual(grade, 100.0)

	def test_duplicate_student_id_raises(self):
		self.gradebook.add_student("S1", "Alice")

		with self.assertRaises(ValueError):
			self.gradebook.add_student("S1", "Alicia")

	def test_enrolling_unknown_student_raises(self):
		with self.assertRaises(ValueError):
			self.gradebook.enroll_in_course("missing", "Math", 3.0)

	def test_enrolling_same_course_twice_for_one_student_raises(self):
		self.gradebook.add_student("S1", "Alice")
		self.gradebook.enroll_in_course("S1", "Math", 3.0)

		with self.assertRaises(ValueError):
			self.gradebook.enroll_in_course("S1", "Math", 3.0)

	def test_same_course_name_for_two_students_does_not_conflict(self):
		self.gradebook.add_student("S1", "Alice")
		self.gradebook.add_student("S2", "Bob")

		first = self.gradebook.enroll_in_course("S1", "Math", 3.0)
		second = self.gradebook.enroll_in_course("S2", "Math", 4.0)

		self.assertEqual(first.course_name, second.course_name)
		self.assertEqual(self.gradebook.students["S1"].courses["Math"].credit_hours, 3.0)
		self.assertEqual(self.gradebook.students["S2"].courses["Math"].credit_hours, 4.0)

	def test_add_assignment_unknown_student_raises(self):
		assignment = self.make_assignment("HW", 5, 10, Category.HOMEWORK)

		with self.assertRaises(ValueError):
			self.gradebook.add_assignment("missing", "Math", assignment)

	def test_add_assignment_unknown_course_raises(self):
		self.gradebook.add_student("S1", "Alice")
		assignment = self.make_assignment("HW", 5, 10, Category.HOMEWORK)

		with self.assertRaises(ValueError):
			self.gradebook.add_assignment("S1", "Math", assignment)

	def test_assignment_appears_in_get_category_average(self):
		student, course = self.enroll_student_with_course()
		assignment = self.make_assignment("HW 1", 8, 10, Category.HOMEWORK)
		self.gradebook.add_assignment(student.student_id, course.course_name, assignment)

		self.assertEqual(self.gradebook.get_category_average(student.student_id, course.course_name, Category.HOMEWORK), assignment.percentage)

	def test_credit_hours_weight_gpa_not_plain_average(self):
		self.gradebook.add_student("S1", "Alice")
		self.gradebook.enroll_in_course("S1", "Short", 1.0)
		self.gradebook.enroll_in_course("S1", "Long", 5.0)

		self.gradebook.add_assignment("S1", "Short", self.make_assignment("HW", 10, 10, Category.HOMEWORK))
		self.gradebook.add_assignment("S1", "Long", self.make_assignment("HW", 5, 10, Category.HOMEWORK))

		expected = ((4.0 * 1.0) + (0.0 * 5.0)) / 6.0
		self.assertAlmostEqual(self.gradebook.calculate_gpa("S1"), expected)

	def test_zero_assignment_courses_are_excluded_from_gpa(self):
		self.gradebook.add_student("S1", "Alice")
		self.gradebook.enroll_in_course("S1", "Graded", 3.0)
		self.gradebook.enroll_in_course("S1", "Empty", 12.0)
		self.gradebook.add_assignment("S1", "Graded", self.make_assignment("HW", 10, 10, Category.HOMEWORK))

		self.assertAlmostEqual(self.gradebook.calculate_gpa("S1"), 4.0)

	def test_student_with_zero_courses_has_zero_gpa(self):
		self.gradebook.add_student("S1", "Alice")

		self.assertEqual(self.gradebook.calculate_gpa("S1"), 0.0)

	def test_transcript_includes_student_name_and_id(self):
		self.gradebook.add_student("S1", "Alice")

		transcript = self.gradebook.generate_transcript("S1")

		self.assertIn("Student Name", transcript)
		self.assertIn("Alice", transcript)
		self.assertIn("Student ID", transcript)
		self.assertIn("S1", transcript)

	def test_transcript_includes_every_enrolled_course(self):
		self.gradebook.add_student("S1", "Alice")
		self.gradebook.enroll_in_course("S1", "Math", 3.0)
		self.gradebook.enroll_in_course("S1", "History", 4.0)

		transcript = self.gradebook.generate_transcript("S1")

		self.assertIn("Math", transcript)
		self.assertIn("History", transcript)

	def test_ungraded_course_displays_something_sensible(self):
		self.gradebook.add_student("S1", "Alice")
		self.gradebook.enroll_in_course("S1", "Math", 3.0)

		transcript = self.gradebook.generate_transcript("S1")

		self.assertIn("No grades available", transcript)

	def test_transcript_cumulative_gpa_matches_calculate_gpa(self):
		self.gradebook.add_student("S1", "Alice")
		self.gradebook.enroll_in_course("S1", "Math", 3.0)
		self.gradebook.enroll_in_course("S1", "Science", 2.0)
		self.gradebook.add_assignment("S1", "Math", self.make_assignment("HW", 10, 10, Category.HOMEWORK))
		self.gradebook.add_assignment("S1", "Science", self.make_assignment("HW", 5, 10, Category.HOMEWORK))

		gpa = self.gradebook.calculate_gpa("S1")
		transcript = self.gradebook.generate_transcript("S1")

		self.assertIn(f"{gpa:.2f}", transcript)

	def test_transcript_works_for_student_with_only_one_course(self):
		self.gradebook.add_student("S1", "Alice")
		self.gradebook.enroll_in_course("S1", "Math", 3.0)
		self.gradebook.add_assignment("S1", "Math", self.make_assignment("HW", 10, 10, Category.HOMEWORK))

		transcript = self.gradebook.generate_transcript("S1")

		self.assertIn("Math", transcript)
		self.assertIn("Cumulative GPA", transcript)

	def test_transcript_works_for_student_with_zero_courses(self):
		self.gradebook.add_student("S1", "Alice")

		transcript = self.gradebook.generate_transcript("S1")

		self.assertIn("No grades available", transcript)
		self.assertIn("Cumulative GPA", transcript)
		self.assertIn("0.00", transcript)

	def test_full_pipeline(self):
		self.gradebook.add_student("S1", "Alice")
		self.gradebook.enroll_in_course("S1", "Math", 3.0)
		self.gradebook.enroll_in_course("S1", "Science", 4.0)

		math_hw = self.make_assignment("Math HW", 9, 10, Category.HOMEWORK)
		math_quiz = self.make_assignment("Math Quiz", 8, 10, Category.QUIZZES)
		science_hw = self.make_assignment("Science HW", 10, 10, Category.HOMEWORK)
		science_midterm = self.make_assignment("Science Midterm", 7, 10, Category.MIDTERM)

		self.gradebook.add_assignment("S1", "Math", math_hw)
		self.gradebook.add_assignment("S1", "Math", math_quiz)
		self.gradebook.add_assignment("S1", "Science", science_hw)
		self.gradebook.add_assignment("S1", "Science", science_midterm)

		math_category_average = self.gradebook.get_category_average("S1", "Math", Category.HOMEWORK)
		math_grade = self.gradebook.get_course_grade("S1", "Math")
		science_grade = self.gradebook.get_course_grade("S1", "Science")
		gpa = self.gradebook.calculate_gpa("S1")
		transcript = self.gradebook.generate_transcript("S1")

		self.assertEqual(math_category_average, math_hw.percentage)
		self.assertEqual(math_grade[1], LetterGrade.B)
		self.assertIsNotNone(science_grade)
		self.assertIn("Alice", transcript)
		self.assertIn("Math", transcript)
		self.assertIn("Science", transcript)
		self.assertIn(f"{gpa:.2f}", transcript)


if __name__ == "__main__":
	unittest.main()
