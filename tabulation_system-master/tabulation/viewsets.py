from pprint import pprint

from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet

from .models import (CourseRegistration, Course, Discipline, OfferedCourses, Student,
                     Teacher, TermData, TheoryMarks, LabMarks, AttendanceMarks, Prerequisite,
                     QuestionPreparationScriptExamination, ClassTest, SessionalAssessmentViva, ModerationCommitee,
                     AnswerScriptScrutiny, TabulationStudentWise, TabulationCourseWise, QuestionDrawing)

from .serializers import (CourseRegistrationSerializer, CourseSerializer,
                          DisciplineSerializer, OfferedCoursesSerializer, StudentSerializer, TeacherSerializer,
                          TermDataSerializer, TheoryMarksSerializer, LabMarksSerializer, AttendanceMarksSerializer,
                          PrerequisiteSerializer, QuestionPreparationScriptExaminationSerializer, ClassTestSerializer,
                          SessionalAssessmentVivaSerializer, ModerationCommiteeSerializer,
                          AnswerScriptScrutinySerializer, TabulationStudentWiseSerializer,
                          TabulationCourseWiseSerializer, QuestionDrawingSerializer)


class TheoryMarksViewSet(ModelViewSet):
    queryset = TheoryMarks.objects.all()
    serializer_class = TheoryMarksSerializer


class CourseRegistrationViewSet(ModelViewSet):
    queryset = CourseRegistration.objects.all()
    serializer_class = CourseRegistrationSerializer

    def create(self, request, *args, **kwargs):
        session = request.data.get("session")
        year = request.data.get("year")
        term = request.data.get("term")
        batch = request.data.get("batch")
        user = request.data.get("user")
        course_list = request.data.get("course_list")

        term_object = TermData.objects.get(session=session, year=year, term=term)

        student_id = user['data'].get("student_id")
        student_object = Student.objects.get(student_id=student_id)

        pprint(request.data)
        for i in course_list:
            course_object = Course.objects.get(course_title=i["course_data"]["course_title"])
            course_registration_object = CourseRegistration.objects.filter(term=term_object, student=student_object,
                                                                           course=course_object, with_batch=batch,
                                                                           is_deleted=False, status=1).first()

            if not course_registration_object:
                course_registration_object = CourseRegistration(term=term_object, student=student_object,
                                                                course=course_object, with_batch=batch)
                print(course_registration_object)
                course_registration_object.save()

        return Response({"status": True})


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class DisciplineViewSet(ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer


class OfferedCoursesViewSet(ModelViewSet):
    queryset = OfferedCourses.objects.all()
    serializer_class = OfferedCoursesSerializer

    def list(self, request, *args, **kwargs):
        session = request.query_params.get("session")
        year = request.query_params.get("year")
        term = request.query_params.get("term")
        discipline_id = request.query_params.get("discipline_id")
        student_id = request.query_params.get("student_id")

        term_object = TermData.objects.filter(session=session, year=year, term=term).first()
        discipline_object = Discipline.objects.filter(code_number=discipline_id).first()

        if term_object:
            offered_courses = OfferedCourses.objects.filter(term=term_object, discipline=discipline_object)

            already_registered_courses = CourseRegistration.objects.filter(term=term_object,
                                                                           student__student_id=student_id,
                                                                           status=2)
            pending_courses = CourseRegistration.objects.filter(term=term_object, student__student_id=student_id,
                                                                status=1)

            offered_course_numbers = [i.course.course_number for i in offered_courses]
            already_registered_course_numbers = [i.course.course_number for i in already_registered_courses]
            pending_course_numbers = [i.course.course_number for i in pending_courses]

            filtered_offered_courses = []
            for i in offered_courses:
                if i.course.course_number not in already_registered_course_numbers and \
                        i.course.course_number not in pending_course_numbers:
                    filtered_offered_courses.append(i)

            pending_courses_details = OfferedCourses.objects.filter(course__course_number__in=pending_course_numbers)

            offered_courses_serializer = OfferedCoursesSerializer(filtered_offered_courses, many=True)
            pending_courses_serializer = OfferedCoursesSerializer(pending_courses_details, many=True)
            already_registered_course_serializer = CourseRegistrationSerializer(already_registered_courses,
                                                                                many=True)
            pprint(already_registered_course_serializer.data)
            return Response({"status": True, "data": offered_courses_serializer.data,
                             "registered": already_registered_course_serializer.data,
                             "pending": pending_courses_serializer.data})

        return Response({"status": False, "errors": "invalid data"})


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TermDataViewSet(ModelViewSet):
    queryset = TermData.objects.all()
    serializer_class = TermDataSerializer


class LabMarksViewSet(ModelViewSet):
    queryset = LabMarks.objects.all()
    serializer_class = LabMarksSerializer


class AttendanceMarksViewSet(ModelViewSet):
    queryset = AttendanceMarks.objects.all()
    serializer_class = AttendanceMarksSerializer


class PrerequisiteViewSet(ModelViewSet):
    queryset = Prerequisite.objects.all()
    serializer_class = PrerequisiteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        code_number = self.request.query_params.get("discipline_code")

        if code_number:
            discipline_object = Discipline.objects.filter(code_number=code_number).first()
            queryset = queryset.filter(discipline=discipline_object)

            return queryset
        return queryset



#today

class QuestionPreparationScriptExaminationViewSet(ModelViewSet):
    queryset = QuestionPreparationScriptExamination.objects.all()
    serializer_class = QuestionPreparationScriptExaminationSerializer


class ClassTestViewSet(ModelViewSet):
    queryset = ClassTest.objects.all()
    serializer_class = ClassTestSerializer


class SessionalAssessmentVivaViewSet(ModelViewSet):
    queryset = SessionalAssessmentViva.objects.all()
    serializer_class = SessionalAssessmentVivaSerializer


class ModerationCommiteeViewSet(ModelViewSet):
    queryset = ModerationCommitee.objects.all()
    serializer_class = ModerationCommiteeSerializer


class AnswerScriptScrutinyViewSet(ModelViewSet):
    queryset = AnswerScriptScrutiny.objects.all()
    serializer_class = AnswerScriptScrutinySerializer


class TabulationStudentWiseViewSet(ModelViewSet):
    queryset = TabulationStudentWise.objects.all()
    serializer_class = TabulationStudentWiseSerializer



class TabulationCourseWiseViewSet(ModelViewSet):
    queryset = TabulationCourseWise.objects.all()
    serializer_class = TabulationCourseWiseSerializer


class QuestionDrawingViewSet(ModelViewSet):
    queryset = QuestionDrawing.objects.all()
    serializer_class = QuestionDrawingSerializer


