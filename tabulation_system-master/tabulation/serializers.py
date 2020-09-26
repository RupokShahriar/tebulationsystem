from rest_framework.serializers import ModelSerializer

from .models import (Conversation, Course, Student, Teacher, Discipline, OfferedCourses, TermData, CourseRegistration,
                     TheoryMarks, LabMarks, AttendanceMarks, Prerequisite, QuestionPreparationScriptExamination,
                     ClassTest, SessionalAssessmentViva, ModerationCommitee, AnswerScriptScrutiny, TabulationStudentWise,
                     TabulationCourseWise, QuestionDrawing)


class TermDataSerializer(ModelSerializer):
    class Meta:
        model = TermData
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class PrerequisiteSerializer(ModelSerializer):
    main_course = CourseSerializer(read_only=True)
    prerequisite_course = CourseSerializer(read_only=True)

    class Meta:
        model = Prerequisite
        fields = "__all__"


class DisciplineSerializer(ModelSerializer):
    class Meta:
        model = Discipline
        fields = "__all__"


class ConversationSerializer(ModelSerializer):
    class Meta:
        model = Conversation
        fields = "__all__"


class OfferedCoursesSerializer(ModelSerializer):
    course_data = CourseSerializer(source="course", read_only=True)
    discipline_data = DisciplineSerializer(source="discipline", read_only=True)
    term_data = TermDataSerializer(source="term", read_only=True)

    class Meta:
        model = OfferedCourses
        fields = "__all__"


class StudentSerializer(ModelSerializer):
    discipline = DisciplineSerializer(read_only=True)

    class Meta:
        model = Student
        fields = "__all__"


class CourseRegistrationSerializer(ModelSerializer):
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = CourseRegistration
        fields = "__all__"


class TheoryMarksSerializer(ModelSerializer):
    course_registration = CourseRegistrationSerializer()

    class Meta:
        model = TheoryMarks
        fields = "__all__"


class LabMarksSerializer(ModelSerializer):
    course_registration = CourseRegistrationSerializer()

    class Meta:
        model = LabMarks
        fields = "__all__"


class AttendanceMarksSerializer(ModelSerializer):
    course_registration = CourseRegistrationSerializer()

    class Meta:
        model = AttendanceMarks
        fields = "__all__"


class TeacherSerializer(ModelSerializer):
    discipline = DisciplineSerializer(read_only=True)

    class Meta:
        model = Teacher
        fields = "__all__"


class QuestionPreparationScriptExaminationSerializer(ModelSerializer):
    discipline = DisciplineSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    teacher1 = TeacherSerializer(read_only=True)
    teacher2 = TeacherSerializer(read_only=True)

    class Meta:
        model = QuestionPreparationScriptExamination
        fields = "__all__"


class ClassTestSerializer(ModelSerializer):
    discipline = DisciplineSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)

    class Meta:
        model = ClassTest
        fields = "__all__"


class SessionalAssessmentVivaSerializer(ModelSerializer):
    discipline = DisciplineSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    teacher1 = TeacherSerializer(read_only=True)
    teacher2 = TeacherSerializer(read_only=True)

    class Meta:
        model = SessionalAssessmentViva
        fields = "__all__"


class ModerationCommiteeSerializer(ModelSerializer):
    discipline = DisciplineSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)

    class Meta:
        model = ModerationCommitee
        fields = "__all__"


class AnswerScriptScrutinySerializer(ModelSerializer):
    discipline = DisciplineSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)

    class Meta:
        model = AnswerScriptScrutiny
        fields = "__all__"


class TabulationStudentWiseSerializer(ModelSerializer):
    discipline = DisciplineSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)

    class Meta:
        model = TabulationStudentWise
        fields = "__all__"


class TabulationCourseWiseSerializer(ModelSerializer):
    discipline = DisciplineSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)
    student = StudentSerializer(read_only=True)

    class Meta:
        model = TabulationCourseWise
        fields = "__all__"


class QuestionDrawingSerializer(ModelSerializer):
    discipline = DisciplineSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = QuestionDrawing
        fields = "__all__"


#class TermDataSerializer(ModelSerializer):
 #   class Meta:
  #      model = TermData
   #     fields = "__all__"
