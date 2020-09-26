from .models import (Discipline, Student, TermData, Course, OfferedCourses, Teacher, CourseRegistration)

discipline_tuples = (("01", "Architecture", "SET"), ("02", "CSE", "SET"))

course_tuples = (("CSE 1103", "Structured Programming", 3.00, 1), ("CSE 1101", "Computer fundamental", 2.00, 1),
                 ("CSE 1104", "Structured Programming Laboratory", 1.50, 2),
                 ("ME 1151", "Mechanics and Heat Engineering", 3.00, 1), ("MATH 1153", "Calculus", 3.00, 1),
                 ("PHY 1153", "Physics I", 3.00, 1), ("PHY 1154", "Physics Laboratory I", 0.75, 2),
                 ("CHEM 1151", "Chemistry", 3.00, 1), ("CHEM 1152", "Chemistry Laboratory", 0.75, 2),
                 ("ENG 1151", "English", 2.00, 1), ("CSE 1201", "Object Oriented Programming", 3.00, 1),
                 ("CSE 1202", "Object Oriented Programming Laboratory", 1.50, 2),
                 ("CSE 1203", "Discrete Mathematics", 3.00, 1), ("ECE 1251", "Electrical Circuits", 3.00, 1),
                 ("ECE 1252", "Electrical Circuits Laboratory", 0.75, 2),
                 ("ME 1252", "Engineering Drawing and CAD Project", 0.75, 2),
                 ("MATH 1253", "Geometry and Differential Equations", 3.00, 1), ("PHY 1253", "Physics II", 3.00, 1),
                 ("PHY 1254", "Physics Laboratory II", 0.75, 2), ("HSS 1253", "Government and Sociology", 2.00, 1),
                 ("CSE 2101", "Data Structure", 3.00, 1), ("CSE 2102", "Data Structure Laboratory", 1.50, 2),
                 ("CSE 2111", "Digital Logic Design", 3.00, 1),
                 ("CSE 2112", "Digital Logic Design Laboratory", 1.50, 2),
                 ("CSE 2114", "Advanced Programming Laboratory", 1.50, 2),
                 ("ECE 2151", "Electronic Devices and Circuits", 3.00, 1),
                 ("ECE 2152", "Electronic Devices and Circuits Laboratory", 1.50, 2),
                 ("MATH 2153", "Vector Analysis and Matrix", 3.00, 1), ("ECON 2151", "Economics", 2.00, 1),
                 ("CSE 2200", "Software Development Project", 3.00, 2), ("CSE 2201", "Algorithms", 3.00, 1),
                 ("CSE 2202", "Algorithms Laboratory", 1.50, 2), ("CSE 2203", "Computer Architecture", 3.00, 1),
                 ("CSE 2208", "Assembly Language Laboratory", 1.50, 2),
                 ("ECE 2251", "Electrical Drives and Instrumentation", 3.00, 1),
                 ("ECE 2252", "Electrical Drives and Instrumentation Laboratory", 0.75, 2),
                 ("MATH 2253", "Statistics and Complex Variable", 3.00, 1), ("HSS 2251", "Psychology", 2.00, 1),
                 ("CSE 3100", "Technical Writing and Presentation", 0.75, 2), ("CSE 3101", "Database Systems", 3.00, 1),
                 ("CSE 3102", "Database Systems Project/Fieldwork", 1.5, 2), ("CSE 3105", "Numerical Methods", 3.00, 1),
                 ("CSE 3106", "Numerical Methods Laboratory", 0.75, 2),
                 ("CSE 3111", "Microprocessors and Microcontrollers", 0.75, 2),
                 ("CSE 3112", "Microprocessors and Microcontrollers Laboratory/Project", 3.00, 1),
                 ("ECE 3151", "Digital Electronics", 0.75, 2), ("MATH 3153", "Mathematical Methods", 2.00, 1),
                 ("BA 3151", "Accounting", 3.00, 1), ("CSE 3200", "Web Programming Project/Fieldwork", 1.50, 2),
                 ("CSE 3201", "Operating System and Systems Programming", 3.00, 1),
                 ("CSE 3202", "Operating System and Systems Programming Laboratory/Project", 1.50, 2),
                 ("CSE 3203", "Software Engineering and Information System", 4.00, 1),
                 ("CSE 3204", "Software Engineering and Information System Project", 1.50, 2),
                 ("ECE 3251", "Data Communication", 3.00, 1), ("BA 3251", "Industrial Management and Law", 3.00, 1),
                 ("CSE 3225", "Digital Image Processing", 3.00, 1),
                 ("CSE 3226", "Digital Image Processing Laboratory/Project", 1.50, 2),
                 ("CSE 4100", "Project and Thesis I", 3.00, 3), ("CSE 4103", "Computer Graphics ", 3.00, 1),
                 ("CSE 4104", "Computer Graphics Laboratory/Project", 0.75, 2),
                 ("CSE 4105", "Compiler Design", 3.00, 1), ("CSE 4106", "Compiler Design Laboratory/Project", 0.75, 2),
                 ("CSE 4111", "Computer Networks", 3.00, 1),
                 ("CSE 4112", "Computer Networks Laboratory/Fieldwork", 1.50, 2),
                 ("CSE 4121", "Applied Probability and Queuing Theory", 2.00, 1),
                 ("CSE 4125", "Computational Geometry", 2.00, 1), ("CSE 4160", "Industrial Training", 0.00, 2),
                 ("CSE 4200", "Project and Thesis II ", 3.00, 3), ("CSE 4205", "Artificial Intelligence", 3.00, 1),
                 ("CSE 4206", "Artificial Intelligence Laboratory/Project", 1.50, 2),
                 ("CSE 4221", "Pattern Recognition", 3.00, 1),
                 ("CSE 4222", "Pattern Recognition Laboratory/Project", 0.75, 2),
                 ("CSE 4223", "Data Warehousing and Mining", 3.00, 1),
                 ("CSE 4224", "Data Warehousing and Mining Laboratory/Fieldwork", 0.75, 2))


def input_discipline_tuples():
    for i in discipline_tuples:
        discipline_object = Discipline(code_number=i[0], name=i[1], school=i[1])
        discipline_object.save()


def input_course_tuples():
    for i in course_tuples:
        course_object = Course(course_number=i[0], course_title=i[1], credit_hour=i[2], course_type=i[3])
        course_object.save()



