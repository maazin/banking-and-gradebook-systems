# Assignment 2 Gradebook

## Overview

This project implements a gradebook system with students, courses, assignments, course grades, GPA calculation, and transcript generation.

## Setup Instructions

Needs Python 3.9 or higher.

1. Open a terminal in the `assignment2_gradebook` folder.
2. Activate the virtual environment.
3. Run the test suite.
4. Run the demo script to see a sample end-to-end workflow.

### Example Commands

```bash
cd assignment2_gradebook
source ../venv/bin/activate
pip install -r requirements.txt
python demo.py
python -m pytest tests -v   #runs the tests
python demo.py              #runs the demo script
```
### Sample Input

The demo script in `demo.py` performs the following workflow:

```text
1. Create GradeBook
2. Add students
	- S1: Sam
	- S2: Jordan
	- S3: Taylor
3. Enroll courses
	- S1 -> COP101 (3), CDA101 (4)
	- S2 -> COP101 (3), MTH100 (4)
	- S3 -> CDA101 (4), PHY200 (2)
4. Add assignments
	- S1 COP101: HW1 80/100, HW2 90/100, Quiz1 85/100
	- S1 CDA101: HW1 100/100, Midterm 88/100
	- S2 COP101: HW1 100/100, Quiz1 95/100
	- S2 MTH100: HW1 70/100, Final 92/100
	- S3 CDA101: HW1 60/100, Quiz1 0/100
	- S3 PHY200: HW1 75/100, Midterm 80/100
5. Print course grades, GPAs, and transcripts
```

This sample input is intentionally small but covers the full pipeline: student creation, course enrollment, assignment submission, grade calculation, GPA weighting, and transcript rendering.

### Sample Output

```
Course Grades
=============
S1 COP101: (85.0, <LetterGrade.B: 'B'>)
S1 CDA101: (93.33333333333333, <LetterGrade.A: 'A'>)
S2 COP101: (97.5, <LetterGrade.A: 'A'>)
S2 MTH100: (83.99999999999999, <LetterGrade.B: 'B'>)
S3 CDA101: (30.0, <LetterGrade.F: 'F'>)
S3 PHY200: (77.77777777777777, <LetterGrade.C: 'C'>)

GPAs
====
S1: 3.57
S2: 3.43
S3: 0.67

Transcripts
===========

_____________________________________________________________
| Student Name   | Sam          | Student ID | S1           |
-------------------------------------------------------------
| Course Name    | Credit Hours | Percentage | Letter Grade |
-------------------------------------------------------------
| COP101         | 3.0          | 85.00%     | B            |
| CDA101         | 4.0          | 93.33%     | A            |
-------------------------------------------------------------
| Cumulative GPA | 3.57         |            |              |
_____________________________________________________________

_____________________________________________________________
| Student Name   | Jordan       | Student ID | S2           |
-------------------------------------------------------------
| Course Name    | Credit Hours | Percentage | Letter Grade |
-------------------------------------------------------------
| COP101         | 3.0          | 97.50%     | A            |
| MTH100         | 4.0          | 84.00%     | B            |
-------------------------------------------------------------
| Cumulative GPA | 3.43         |            |              |
_____________________________________________________________

_____________________________________________________________
| Student Name   | Taylor       | Student ID | S3           |
-------------------------------------------------------------
| Course Name    | Credit Hours | Percentage | Letter Grade |
-------------------------------------------------------------
| CDA101         | 4.0          | 30.00%     | F            |
| PHY200         | 2.0          | 77.78%     | C            |
-------------------------------------------------------------
| Cumulative GPA | 0.67         |            |              |
_____________________________________________________________
```

## Assumptions

- Category average is the mean of each assignment's individual percentage within the category and not the sum of all points earned divided by the sum of all points possible.
- GPA is weighted by credit hours.
- Categories with no assignments don't count against the grade. If a course has no midterms, the midterm category is ignored in the final grade calculation. 
- The weights are renormalized against each other. For example, if a course has only a final exam and no midterms, the final exam is worth 100% of the grade.
- getCategoryAverage() returns None if there are no assignments in the category and not 0.0. This is to avoid confusion with a 0% average.
- Category weights are fixed at 20/20/25/35 for homework/midterm/final project/final exam respectively.
- Letter grade thresholds follow the standard 90/80/70/60 scale.
- A missing assignment defaults to 0.
- Transcript output is an ASCII table.

## Project Structure
```text
assignment2_gradebook/
├── demo.py
├── README.md
├── DESIGNNOTES.md
├── requirements.txt
├── gradebook/
│   ├── __init__.py
│   ├── assignment.py
│   ├── course.py
│   ├── enums.py
│   ├── gradebook.py
│   └── student.py
└── tests/
	├── __init__.py
	└── test_gradebook.py
```

### Notes

- `gradebook/` contains the core data models and business logic.

- `tests/` contains the unit test suite for the assignment.

- `demo.py` runs a full sample workflow with students, courses, assignments, GPA, and transcripts.
