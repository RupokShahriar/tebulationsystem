from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinLengthValidator


class Discipline(models.Model):
    code_number = models.CharField(max_length=20, null=False, unique=True)
    name = models.CharField(max_length=100, unique=True)
    school = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, help_text="Discipline : ")
    student_id = models.CharField(max_length=25, unique=True)
    batch = models.CharField("batch", max_length=4, validators=[MinLengthValidator(4)])
    name = models.CharField(help_text="Name : ", max_length=100)
    contact_number = models.CharField(help_text="Contact Number :", max_length=25)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class TermData(models.Model):
    session = models.CharField(max_length=20)
    year = models.CharField(max_length=20)
    term = models.CharField(max_length=20)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("session", "year", "term")

    def __str__(self):
        return "session: " + self.session + " year : " + self.year + " - term : " + self.term


class Course(models.Model):
    COURSE_TYPE = (
        (1, "Theory"),
        (2, "Lab"),
        (3, "Thesis")
    )
    course_number = models.CharField(help_text="Course number : ", max_length=25, unique=True)
    course_title = models.CharField(help_text="Course title : ", max_length=250)
    credit_hour = models.FloatField(help_text="Credit hours : ")
    course_type = models.IntegerField(choices=COURSE_TYPE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course_number + " : " + self.course_title


class OfferedCourses(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    term = models.ForeignKey(TermData, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("course", "discipline", "term")

    def __str__(self):
            return self.course.course_title


class Teacher(models.Model):
    discipline = models.ForeignKey(Discipline, help_text="Select Discipline : ", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="User object for teacher")
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=25)
    email = models.EmailField(max_length=200)
    designation = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name + " (" + self.discipline.name + ")"


class Conversation(models.Model):
    teacher = models.ForeignKey(Teacher, help_text="Teacher : ", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, help_text="Student: ", on_delete=models.CASCADE)
    term = models.ForeignKey(TermData, help_text="Term : ", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)


class CourseRegistration(models.Model):
    STATUS_CHOICES = ((1, "Pending"),
                      (2, "Approved"),
                      (3, "Rejected"))

    term = models.ForeignKey(TermData, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    times = models.IntegerField(default=1)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    with_batch = models.CharField(max_length=4)
    comment = models.CharField(max_length=25, default="N/A")
    cause_of_rejection = models.CharField(max_length=500, null=True, blank=True)
    is_retake = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_withdrawn = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course.course_number


class Prerequisite(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    main_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='main_course')
    prerequisite_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="prerequisite_course")
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class AttendanceMarks(models.Model):
    SECTION_CHOICES = (
        (1, "A"),
        (2, "B"),
        (3, "Both")
    )
    course_registration = models.ForeignKey(CourseRegistration, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    obtained_marks = models.CharField(max_length=100,default="0")
    section = models.IntegerField(choices=SECTION_CHOICES)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class TheoryMarks(models.Model):
    TYPE_CHOICES = ((1, "Class Test"),
                    (2, "Semester Final"))

    course_registration = models.ForeignKey(CourseRegistration, on_delete=models.CASCADE)
    type = models.IntegerField(choices=TYPE_CHOICES)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    section = models.CharField(max_length=5)
    class_test_no = models.IntegerField(null=True, blank=True)
    obtained_marks = models.CharField(max_length=100,default="0")
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class LabMarks(models.Model):
    TYPE_CHOICES = ((1, "Sessional Assessment"),
                    (2, "Viva"))

    course_registration = models.ForeignKey(CourseRegistration, on_delete=models.CASCADE)
    type = models.IntegerField(choices=TYPE_CHOICES)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    obtained_marks = models.CharField(max_length=100, default="0")
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class ThesisConfiguration(models.Model):
    THESIS_CHOICES = (
        (1, "Duration 1 term, evaluation 1 term"),
        (2, "Duration 2 terms, evaluation 1 term"),
        (3, "duration 2 terms, evaluation 2 terms"),
    )
    discipline = models.ForeignKey(Discipline, verbose_name="Discipline", on_delete=models.CASCADE)
    thesis_type = models.IntegerField("Thesis type", choices=THESIS_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class QuestionPreparationScriptExamination(models.Model):
    TERM_CHOICES = (
        (1, "1st term"),
        (2, "2nd term"),
        (3, "Special term"),
    )
    YEAR_CHOICES = (
        (1, "1st year"),
        (2, "2nd year"),
        (3, "3rd year"),
        (4, "4th year"),
    )
    discipline = models.ForeignKey(Discipline, verbose_name="Discipline", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE)
    term = models.IntegerField(choices=TERM_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    session = models.CharField(max_length=50, default="")
    teacher1 = models.ForeignKey(Teacher, related_name="teacher1", on_delete=models.CASCADE)
    teacher2 = models.ForeignKey(Teacher, related_name="teacher2", on_delete=models.CASCADE)
    no_question_t1 = models.IntegerField(default=0)
    no_question_t2 = models.IntegerField(default=0)
    no_script_t1 = models.IntegerField(default=0)
    no_script_t2 = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class ClassTest(models.Model):
    TERM_CHOICES = (
        (1, "1st term"),
        (2, "2nd term"),
        (3, "Special term"),

    )
    YEAR_CHOICES = (
        (1, "1st year"),
        (2, "2nd year"),
        (3, "3rd year"),
        (4, "4th year"),
    )
    discipline = models.ForeignKey(Discipline, verbose_name="Discipline", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE)
    term = models.IntegerField(choices=TERM_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    session = models.CharField(max_length=50, default="")
    teacher = models.ForeignKey(Teacher, verbose_name="Teacher", on_delete=models.CASCADE)
    no_question = models.IntegerField(default=0)
    no_script = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class SessionalAssessmentViva(models.Model):
    TERM_CHOICES = (
        (1, "1st term"),
        (2, "2nd term"),
        (3, "Special term"),
    )
    YEAR_CHOICES = (
        (1, "1st year"),
        (2, "2nd year"),
        (3, "3rd year"),
        (4, "4th year"),
    )
    discipline = models.ForeignKey(Discipline, verbose_name="Discipline", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE)
    term = models.IntegerField(choices=TERM_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    session = models.CharField(max_length=50, default="")
    teacher1 = models.ForeignKey(Teacher, related_name="Teacher1", on_delete=models.CASCADE)
    teacher2 = models.ForeignKey(Teacher, related_name="Teacher2", on_delete=models.CASCADE)
    no_student = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class ModerationCommitee(models.Model):
    TERM_CHOICES = (
        (1, "1st term"),
        (2, "2nd term"),
        (3, "Special term"),
    )
    YEAR_CHOICES = (
        (1, "1st year"),
        (2, "2nd year"),
        (3, "3rd year"),
        (4, "4th year"),
    )
    discipline = models.ForeignKey(Discipline, verbose_name="Discipline", on_delete=models.CASCADE)
    term = models.IntegerField(choices=TERM_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    session = models.CharField(max_length=50, default="")
    teacher = models.ForeignKey(Teacher, verbose_name="Teacher", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class AnswerScriptScrutiny(models.Model):
    TERM_CHOICES = (
        (1, "1st term"),
        (2, "2nd term"),
        (3, "Special term"),
    )
    YEAR_CHOICES = (
        (1, "1st year"),
        (2, "2nd year"),
        (3, "3rd year"),
        (4, "4th year"),
    )
    discipline = models.ForeignKey(Discipline, verbose_name="Discipline", on_delete=models.CASCADE)
    term = models.IntegerField(choices=TERM_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    session = models.CharField(max_length=50, default="")
    teacher = models.ForeignKey(Teacher, verbose_name="Teacher", on_delete=models.CASCADE)
    no_script = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class TabulationStudentWise(models.Model):
    TERM_CHOICES = (
        (1, "1st term"),
        (2, "2nd term"),
        (3, "Special term"),
    )
    YEAR_CHOICES = (
        (1, "1st year"),
        (2, "2nd year"),
        (3, "3rd year"),
        (4, "4th year"),
    )
    discipline = models.ForeignKey(Discipline, verbose_name="Discipline", on_delete=models.CASCADE)
    term = models.IntegerField(choices=TERM_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    session = models.CharField(max_length=50, default="")
    teacher = models.ForeignKey(Teacher, verbose_name="Teacher", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, verbose_name="Student", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class TabulationCourseWise(models.Model):
    TERM_CHOICES = (
        (1, "1st term"),
        (2, "2nd term"),
        (3, "Special term"),
    )
    YEAR_CHOICES = (
        (1, "1st year"),
        (2, "2nd year"),
        (3, "3rd year"),
        (4, "4th year"),
    )
    discipline = models.ForeignKey(Discipline, verbose_name="Discipline", on_delete=models.CASCADE)
    term = models.IntegerField(choices=TERM_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    session = models.CharField(max_length=50, default="")
    teacher = models.ForeignKey(Teacher, verbose_name="Teacher", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class QuestionDrawing(models.Model):
    TERM_CHOICES = (
        (1, "1st term"),
        (2, "2nd term"),
        (3, "Special term"),
    )
    YEAR_CHOICES = (
        (1, "1st year"),
        (2, "2nd year"),
        (3, "3rd year"),
        (4, "4th year"),
    )
    discipline = models.ForeignKey(Discipline, verbose_name="Discipline", on_delete=models.CASCADE)
    term = models.IntegerField(choices=TERM_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    session = models.CharField(max_length=50, default="")
    teacher = models.ForeignKey(Teacher, verbose_name="Teacher", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)