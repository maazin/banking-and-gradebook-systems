"""Demo script for the gradebook assignment."""

from gradebook.assignment import Assignment
from gradebook.enums import Category
from gradebook.gradebook import GradeBook


def add_sample_assignments(gradebook: GradeBook) -> None:
	gradebook.add_assignment("S1", "COP101", Assignment("HW1", 80, 100, Category.HOMEWORK))
	gradebook.add_assignment("S1", "COP101", Assignment("HW2", 90, 100, Category.HOMEWORK))
	gradebook.add_assignment("S1", "COP101", Assignment("Quiz1", 85, 100, Category.QUIZZES))
	gradebook.add_assignment("S1", "CDA101", Assignment("HW1", 100, 100, Category.HOMEWORK))
	gradebook.add_assignment("S1", "CDA101", Assignment("Midterm", 88, 100, Category.MIDTERM))

	gradebook.add_assignment("S2", "COP101", Assignment("HW1", 100, 100, Category.HOMEWORK))
	gradebook.add_assignment("S2", "COP101", Assignment("Quiz1", 95, 100, Category.QUIZZES))
	gradebook.add_assignment("S2", "MTH100", Assignment("HW1", 70, 100, Category.HOMEWORK))
	gradebook.add_assignment("S2", "MTH100", Assignment("Final", 92, 100, Category.FINAL_EXAM))

	gradebook.add_assignment("S3", "CDA101", Assignment("HW1", 60, 100, Category.HOMEWORK))
	gradebook.add_assignment("S3", "CDA101", Assignment("Quiz1", 0, 100, Category.QUIZZES))
	gradebook.add_assignment("S3", "PHY200", Assignment("HW1", 75, 100, Category.HOMEWORK))
	gradebook.add_assignment("S3", "PHY200", Assignment("Midterm", 80, 100, Category.MIDTERM))


def main() -> None:
	gradebook = GradeBook()

	gradebook.add_student("S1", "Sam")
	gradebook.add_student("S2", "Jordan")
	gradebook.add_student("S3", "Taylor")

	gradebook.enroll_in_course("S1", "COP101", 3)
	gradebook.enroll_in_course("S1", "CDA101", 4)

	gradebook.enroll_in_course("S2", "COP101", 3)
	gradebook.enroll_in_course("S2", "MTH100", 4)

	gradebook.enroll_in_course("S3", "CDA101", 4)
	gradebook.enroll_in_course("S3", "PHY200", 2)

	add_sample_assignments(gradebook)

	print("Course Grades")
	print("=============")
	for student_id, course_name in [
		("S1", "COP101"),
		("S1", "CDA101"),
		("S2", "COP101"),
		("S2", "MTH100"),
		("S3", "CDA101"),
		("S3", "PHY200"),
	]:
		print(f"{student_id} {course_name}: {gradebook.get_course_grade(student_id, course_name)}")

	print()
	print("GPAs")
	print("====")
	for student_id in ["S1", "S2", "S3"]:
		print(f"{student_id}: {gradebook.calculate_gpa(student_id):.2f}")

	print()
	print("Transcripts")
	print("===========")
	for student_id in ["S1", "S2", "S3"]:
		print()
		print(gradebook.generate_transcript(student_id))


if __name__ == "__main__":
	main()
