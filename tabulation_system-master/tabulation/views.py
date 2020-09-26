import traceback
from pprint import pprint


from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q

from .models import (Course, CourseRegistration, OfferedCourses, Student, Teacher, TermData, TheoryMarks, LabMarks,
                     AttendanceMarks, QuestionPreparationScriptExamination, ClassTest, SessionalAssessmentViva, ModerationCommitee,
                     AnswerScriptScrutiny, TabulationCourseWise, TabulationStudentWise, QuestionDrawing)

from .serializers import (ConversationSerializer, CourseSerializer, CourseRegistrationSerializer, StudentSerializer,
                          TeacherSerializer, TheoryMarksSerializer, LabMarksSerializer, AttendanceMarksSerializer,
                          QuestionPreparationScriptExaminationSerializer, ClassTestSerializer, SessionalAssessmentVivaSerializer,
                          ModerationCommiteeSerializer, AnswerScriptScrutinySerializer, TabulationStudentWiseSerializer,
                          TabulationCourseWiseSerializer, QuestionDrawingSerializer)
from .utils import *


@api_view(["POST"])
def allow(request):
    session, year, term = request.data.get("session"), request.data.get("year"), request.data.get("term")
    batch, student_id, teacher = request.data.get("batch"), request.data.get("student_id"), request.data.get("teacher")
    teacher_id = teacher['data']['id']
    allowed_courses = request.data.get("allowed_courses")
    rejected_courses = request.data.get("rejected_courses")

    teacher_object = Teacher.objects.filter(id=teacher_id).first()
    student_object = Student.objects.filter(student_id=student_id).first()
    term_object = TermData.objects.filter(session=session, year=year, term=term).first()
    times = get_course_registration_times(session, year, term, student_object)

    pprint(request.data)
    print(student_id, term_object, allowed_courses)

    for i in allowed_courses:
        course_objects = CourseRegistration.objects.filter(student__student_id=student_id, term=term_object,
                                                           is_deleted=False, course__course_number=i).first()
        course_objects.status = 2
        course_objects.approved_by = teacher_object
        course_objects.save()

    for i in rejected_courses:
        course_objects = CourseRegistration.objects.filter(student__student_id=student_id, term=term_object,
                                                           is_deleted=False, course__course_number=i).first()
        course_objects.status = 3
        course_objects.approved_by = teacher_object
        course_objects.save()

    return Response({"status": True})


@api_view(["POST"])
def login(request):
    #from .populate_database import input_discipline_tuples, input_course_tuples
    #input_discipline_tuples()
    #input_course_tuples()
    print(request.data)
    mode = request.data.get("mode")
    student_id = request.data.get("student_id")
    email = request.data.get("email")
    student_password = request.data.get("student_password")
    teacher_password = request.data.get("teacher_password")

    if mode == "student":
        user = authenticate(username=student_id, password=student_password)
    else:
        user = authenticate(username=email, password=teacher_password)
    print(user)

    try:
        if not user:
            return Response({"status": False})
        else:
            if mode == "student":
                student_object = Student.objects.filter(user=user).first()
                student_serializer = StudentSerializer(student_object)
                pprint(student_serializer.data)
                return Response({"status": True, "data": student_serializer.data})

            elif mode == "teacher":
                teacher_object = Teacher.objects.filter(user=user).first()
                teacher_serializer = TeacherSerializer(teacher_object)
                return Response({"status": True, "data": teacher_serializer.data})

    except Exception as ex:
        traceback.print_exc()
        return Response({"status": False})


@api_view(["POST"])
def get_all_offered_courses(request):
    term_object = get_term_object(request)

    if not term_object:
        return Response({"status": False, "errors": "Invalid term data"})

    offered_courses_queryset = OfferedCourses.objects.filter(term=term_object)

    if offered_courses_queryset:

        serialized_courses = CourseSerializer(offered_courses_queryset, many=True)

        if serialized_courses.is_valid():
            return Response({"status": True, "data": serialized_courses.data})
        else:
            return Response({"status": False, "errors": serialized_courses.errors})
    else:
        return Response({"status": False, "errors": "No courses found"})


@api_view(["POST"])
def get_pending_registration(request):
    session = request.data.get("session")
    year = request.data.get("year")
    term = request.data.get("term")
    batch = request.data.get("batch")

    try:
        term_object = TermData.objects.get(session=session, year=year, term=term)
        course_registration_objects = CourseRegistration.objects.filter(term=term_object, status=1,
                                                                        with_batch=batch, is_deleted=False)

        students = []

        for i in course_registration_objects:
            if i.student not in students:
                students.append(i.student)

        return Response({"status": True, "data": StudentSerializer(students, many=True).data})
    except Exception as ex:
        print(ex)
        return Response({"status": False})


@api_view(["POST"])
def get_registered_students(request):
    pprint(request.data)
    session, year, term = request.data.get("session"), request.data.get("year"), request.data.get("term")
    batch, course_number = request.data.get("batch"), request.data.get("course_number")

    term_data = TermData.objects.filter(session=session, year=year, term=term).first()
    course_object = Course.objects.filter(course_number=course_number).first()

    course_registration_objects = CourseRegistration.objects.filter(term=term_data, course=course_object,
                                                                    status=2, is_deleted=False)
    students = [i.student.student_id for i in course_registration_objects]
    return Response({"status": True, "students": students})


@api_view(["POST"])
def get_registration_details(request):
    session = request.data.get('session')
    year = request.data.get("year")
    term = request.data.get("term")
    batch = request.data.get("batch")
    student_id = request.data.get("student_id")

    pprint(request.data)

    try:
        student_object = Student.objects.get(student_id=student_id)
        term_object = TermData.objects.get(session=session, year=year, term=term)
        course_registration_objects = CourseRegistration.objects.filter(term=term_object, student=student_object,
                                                                        status="1",
                                                                        with_batch=batch, is_deleted=False)
        return Response(
            {"status": True, "data": CourseRegistrationSerializer(course_registration_objects, many=True).data})
    except Exception as ex:
        print(ex)
        return Response({"status": False})


@api_view(["GET"])
def get_registered_student_list(request):
    term_object = get_term_object(request)

    if not term_object:
        return Response({"status": False, "errors": "Invalid term data"})


@api_view(["POST"])
def input_theory_marks(request):
    session, year, term = request.data.get("session"), request.data.get("year"), request.data.get("term")
    course_number, section, marks_type = request.data.get("course_number"), request.data.get(
        "section"), request.data.get(
        "type")
    class_test_no, marks = request.data.get("class_test_no"), request.data.get("marks")
    teacher = request.data.get("teacher")
    teacher_id = teacher['data']['id']

    teacher_object = Teacher.objects.filter(id=teacher_id).first()
    term_object = TermData.objects.filter(session=session, year=year, term=term).first()

    for i in marks:
        student_id = i[0]
        obtained_marks = i[1]
        course_registration_object = CourseRegistration.objects.filter(term=term_object,
                                                                       course__course_number=course_number,
                                                                       student__student_id=student_id).first()
        pprint(request.data)
        print(course_registration_object, term_object, student_id)

        theory_marks_object = TheoryMarks(course_registration=course_registration_object,
                                          type=1 if marks_type == "Class Test" else 2,
                                          teacher=teacher_object, section=section, obtained_marks=obtained_marks)
        if marks_type == "Class Test":
            theory_marks_object.class_test_no = class_test_no
        theory_marks_object.save()
    return Response({"status": True})


@api_view(["POST"])
def input_sessional_marks(request):
    session, year, term = request.data.get("session"), request.data.get("year"), request.data.get("term")
    course_number, marks_type = request.data.get("course_number"), request.data.get("type")
    marks = request.data.get("marks")
    teacher = request.data.get("teacher")
    teacher_id = teacher['data']['id']
    print(course_number)

    teacher_object = Teacher.objects.filter(id=teacher_id).first()
    term_object = TermData.objects.filter(session=session, year=year, term=term).first()

    for i in marks:
        student_id = i[0]
        obtained_marks = i[1]
        course_registration_object = CourseRegistration.objects.filter(term=term_object,
                                                                       course__course_number=course_number,
                                                                       student__student_id=student_id).first()
        pprint(request.data)

        lab_marks_object = LabMarks(course_registration=course_registration_object,
                                    type=1 if marks_type == "Sessional Assessment" else 2,
                                    teacher=teacher_object, obtained_marks=obtained_marks)

        lab_marks_object.save()
    return Response({"status": True})


@api_view(["POST"])
def input_attendance_marks(request):
    session, year, term = request.data.get("session"), request.data.get("year"), request.data.get("term")
    course_number, section = request.data.get("course_number"), request.data.get("section")
    marks = request.data.get("marks")
    teacher = request.data.get("teacher")
    teacher_id = teacher['data']['id']

    teacher_object = Teacher.objects.filter(id=teacher_id).first()
    term_object = TermData.objects.filter(session=session, year=year, term=term).first()

    for i in marks:
        student_id = i[0]
        obtained_marks = i[1]
        course_registration_object = CourseRegistration.objects.filter(term=term_object,
                                                                       course__course_number=course_number,
                                                                       student__student_id=student_id).first()

        attendance_marks_object = AttendanceMarks(course_registration=course_registration_object,
                                                  section=1 if section == "A" else 2 if section == "B" else 3,
                                                  teacher=teacher_object, obtained_marks=obtained_marks)

        attendance_marks_object.save()
    return Response({"status": True})


@api_view(["POST"])
def reject(request):
    session, year, term = request.data.get("session"), request.data.get("year"), request.data.get("term")
    batch, student_id, teacher = request.data.get('batch'), request.data.get("student_id"), request.data.get('teacher')
    cause = request.data.get("cause")
    teacher_id = teacher['data']['id']

    teacher_object = Teacher.objects.filter(id=teacher_id).first()
    student_object = Student.objects.get(student_id=student_id)
    term_object = TermData.objects.filter(session=session, year=year, term=term).first()
    times = get_course_registration_times(session, year, term, student_object)

    conversation_serializer = ConversationSerializer(
        data={"teacher": teacher_id, "student": student_object.id, "term": term_object.id, "text": cause})
    if conversation_serializer.is_valid():
        conversation_serializer.save()

    course_objects = CourseRegistration.objects.filter(student=student_object, term=term_object, times=times,
                                                       is_deleted=False)
    for i in course_objects:
        i.approved_by = teacher_object
        i.status = "rejected"
        i.save()
    return Response({"status": True})


@api_view(["POST"])
def get_class_test_marks(request):
    session, year, term = request.data.get("session"), request.data.get("year"), request.data.get("term")
    batch, student_id = request.data.get("batch"), request.data.get("student_id")

    term_object = TermData.objects.filter(session=session, year=year, term=term).first()
    class_test_marks = TheoryMarks.objects.filter(course_registration__term=term_object,
                                                  course_registration__student__student_id=student_id,
                                                  course_registration__with_batch=batch, is_deleted=False, type=1)
    pprint(request.data)
    class_test_marks_serializer = TheoryMarksSerializer(class_test_marks, many=True)

    return Response({"status": True, "data": class_test_marks_serializer.data})


@api_view(["POST"])
def get_term_wise_result(request):
    term_object = get_term_object(request)
    batch = request.data.get("batch")
    course_number = request.data.get("course_title")

    course_object = Course.objects.filter(course_number=course_number).first()
    result_list = list()
    if course_object.course_type == 1 or course_object.course_type == 2:
        class_test_marks = get_all_class_test_marks(request, batch, course_number)

        attendance_marks = get_utils_all_attendance_marks(request, batch, course_number)

        section_a_marks = get_all_theory_marks(request, course_number, batch, course_type=course_object.course_type,
                                               section="A", lab_marks_type=1)

        section_b_marks = get_all_theory_marks(request, course_number, batch, course_type=course_object.course_type,
                                               section="B", lab_marks_type=2)
        print(attendance_marks, section_a_marks, section_b_marks)
        for student_id in attendance_marks:
            if attendance_marks is not None and section_a_marks is not None and section_b_marks is not None:
                obtained_class_test_marks = class_test_marks.get(student_id)
                if not obtained_class_test_marks:
                    obtained_class_test_marks = 0
                total_marks = obtained_class_test_marks + attendance_marks[student_id] + \
                              section_a_marks[
                                  student_id] + \
                              section_b_marks[student_id]
                retake = is_retake(student_id, course_number)
                grade = get_grade(total_marks, retake)
                result_list.append((student_id, grade, attendance_marks.get(student_id),
                                    class_test_marks.get(student_id), section_a_marks.get(student_id),
                                    section_b_marks.get(student_id), retake))
                print(result_list)

    return Response({"status": True, "result": result_list})


@api_view(["GET"])
def get_sessions_years_terms_batches(request):
    terms = TermData.objects.all()
    sessions = list()
    for i in terms:
        if i.session not in sessions:
            sessions.append(i.session)

    terms = TermData.objects.all()
    years = list()
    for i in terms:
        if i.year not in years:
            years.append(i.year)

    term_objects = TermData.objects.all()
    all_terms = list()
    for i in term_objects:
        if i.term not in all_terms:
            all_terms.append(i.term)

    batch_queryset = Student.objects.values("batch").distinct()

    batches = [i.get("batch") for i in batch_queryset]

    return Response({"status": True, "sessions": sorted(sessions, reverse=True), "years": sorted(years),
                     "terms": sorted(all_terms), "batches": sorted(batches, reverse=True)})


@api_view(["POST"])
def get_student_wise_result(request):
    student_id = request.data.get("student_id")

    results = list()
    term_queryset = get_terms_of_student(student_id)
    global total_credit

    for term in term_queryset:
        term_result = list()
        total_cgpa = 0
        total_credit = 0
        total_earned_credit_hourse = 0
        total_credit_points = 0
        total_registered = 0

        course_registration_queryset = get_courses(student_id, term)

        for course in course_registration_queryset:
            attendance_marks = get_attendance_mark(student_id, course.course.course_number, term)
            if attendance_marks is None:
                continue

            if course.course.course_type == 1:
                class_test_marks = get_utils_class_test_marks(student_id, course.course.course_number, term)

                if class_test_marks is None:
                    continue

                semester_final_marks = get_semester_final_marks(student_id, course.course.course_number, term)

                if semester_final_marks is None:
                    continue

                total_marks = attendance_marks + class_test_marks + semester_final_marks

                retake = is_retake(student_id, course.course.course_number)
                grade = get_grade(total_marks, retake)
                term_result.append((course.course.course_number, course.course.course_title, grade,
                                    course.course.credit_hour if grade[0] != "F" else 0.00, retake,
                                    course.course.credit_hour))

                total_registered += course.course.credit_hour

                if grade[0] != "F":
                    total_cgpa += grade[1] * course.course.credit_hour
                    total_credit += course.course.credit_hour

                    total_earned_credit_hourse += course.course.credit_hour
                    total_credit_points += grade[1] * course.course.credit_hour

            elif course.course.course_type == 2:
                session_marks = get_sessional_marks(student_id, course.course.course_number, term)

                if session_marks is None:
                    continue

                viva_marks = get_viva_marks(student_id, course.course.course_number, term)

                if viva_marks == None:
                    continue

                print(attendance_marks, session_marks, viva_marks)

                total_marks = int(attendance_marks) + int(session_marks) + int(viva_marks)

                retake = is_retake(student_id, course.course.course_number)
                grade = get_grade(total_marks, retake)

                total_registered += course.course.credit_hour

                if grade[0] != "F":
                    total_cgpa += grade[1] * course.course.credit_hour
                    total_credit += course.course.credit_hour

                    total_earned_credit_hourse += course.course.credit_hour
                    total_credit_points += grade[1] * course.course.credit_hour

                term_result.append((course.course.course_number, course.course.course_title, grade,
                                    course.course.credit_hour if grade[0] != "F" else 0.00, retake,
                                    course.course.credit_hour))
                print(term_result)

        if total_credit > 0:
            cgpa = round(total_cgpa / total_credit, 2)
        else:
            cgpa = round(0, 2)

        results.append(
            ((term.session, term.year, term.term), term_result, cgpa, total_registered,total_earned_credit_hourse, total_credit_points))

    return Response({"status": True, "results": results})


@api_view(["POST"])
def get_theory_marks_for_edit(request):
    course_number, batch = request.data.get("course_number"), request.data.get("batch")
    marks_type = request.data.get("marks_type")
    section = request.data.get("section")
    class_test_no = request.data.get('class_test_no')
    term_object = get_term_object(request)

    theory_marks_queryset = TheoryMarks.objects.filter(course_registration__term=term_object, section=section,
                                                       course_registration__course__course_number=course_number,
                                                       course_registration__with_batch=batch, is_deleted=False)
    if marks_type == "Semester Final":
        theory_marks_queryset = theory_marks_queryset.filter(class_test_no=None)
        return Response({"status": True, "data": TheoryMarksSerializer(theory_marks_queryset, many=True).data})
    else:
        theory_marks_queryset = theory_marks_queryset.filter(class_test_no=class_test_no)
        return Response({"status": True, "data": TheoryMarksSerializer(theory_marks_queryset, many=True).data})


@api_view(["POST"])
def get_sessional_marks_for_edit(request):
    course_number, batch = request.data.get("course_number"), request.data.get("batch")
    marks_type = request.data.get("marks_type")
    term_object = get_term_object(request)

    theory_marks_queryset = LabMarks.objects.filter(course_registration__term=term_object,
                                                    course_registration__course__course_number=course_number,
                                                    course_registration__with_batch=batch, is_deleted=False)
    if marks_type == "Sessional Assessment":
        theory_marks_queryset = theory_marks_queryset.filter(type=1)
        return Response({"status": True, "data": LabMarksSerializer(theory_marks_queryset, many=True).data})
    else:
        theory_marks_queryset = theory_marks_queryset.filter(type=2)
        return Response({"status": True, "data": LabMarksSerializer(theory_marks_queryset, many=True).data})


@api_view(["POST"])
def get_all_attendance_marks(request):
    term_object = get_term_object(request)
    batch = request.data.get("batch")

    attendance_marks = AttendanceMarks.objects.filter(course_registration__term=term_object,
                                                      course_registration__with_batch=batch)

    marks_list = [
        (i.course_registration.course.course_number, i.course_registration.course.course_title, i.get_section_display(),
         i.obtained_marks) for i in
        attendance_marks]

    return Response({"status": True, "data": marks_list})


@api_view(["POST"])
def update_theory_marks(request):
    session, year, term = request.data.get("session"), request.data.get("year"), request.data.get("term")
    course_number, section, marks_type = request.data.get("course_number"), request.data.get(
        "section"), request.data.get(
        "type")
    class_test_no, marks = request.data.get("class_test_no"), request.data.get("marks")
    teacher = request.data.get("teacher")
    teacher_id = teacher['data']['id']

    if marks_type != "Class Test":
        class_test_no = None

    teacher_object = Teacher.objects.filter(id=teacher_id).first()
    term_object = TermData.objects.filter(session=session, year=year, term=term).first()

    for i in marks:
        student_id = i[0]
        obtained_marks = i[1]
        course_registration_object = CourseRegistration.objects.filter(term=term_object,
                                                                       course__course_number=course_number,
                                                                       student__student_id=student_id,
                                                                       is_deleted=False).first()
        pprint(request.data)
        print(course_registration_object, term_object, student_id)

        theory_marks_object = TheoryMarks.objects.filter(course_registration=course_registration_object,
                                                         type=1 if marks_type == "Class Test" else 2,
                                                         class_test_no=class_test_no,
                                                         teacher=teacher_object, section=section).first()
        theory_marks_object.obtained_marks = obtained_marks
        theory_marks_object.save()
    return Response({"status": True})


@api_view(["POST"])
def update_sessional_marks(request):
    session, year, term = request.data.get("session"), request.data.get("year"), request.data.get("term")
    course_number, marks_type = request.data.get("course_number"), request.data.get("type")
    marks = request.data.get("marks")
    teacher = request.data.get("teacher")
    teacher_id = teacher['data']['id']

    teacher_object = Teacher.objects.filter(id=teacher_id).first()
    term_object = TermData.objects.filter(session=session, year=year, term=term).first()

    for i in marks:
        student_id = i[0]
        obtained_marks = i[1]
        course_registration_object = CourseRegistration.objects.filter(term=term_object,
                                                                       course__course_number=course_number,
                                                                       student__student_id=student_id,
                                                                       is_deleted=False).first()
        pprint(request.data)
        print(course_registration_object, term_object, student_id)

        sessional_marks_object = LabMarks.objects.filter(course_registration=course_registration_object,
                                                         type=1 if marks_type == "Sessional Assessment" else 2,
                                                         teacher=teacher_object).first()
        sessional_marks_object.obtained_marks = obtained_marks
        sessional_marks_object.save()
    return Response({"status": True})


@api_view(["POST"])
def get_attendance_marks_for_edit(request):
    course_number, batch = request.data.get("course_number"), request.data.get("batch")
    section = request.data.get("section")
    term_object = get_term_object(request)

    attendance_marks_queryset = AttendanceMarks.objects.filter(course_registration__term=term_object,
                                                               section=1 if section == "A" else 2 if section == "B" else 3,
                                                               course_registration__course__course_number=course_number,
                                                               course_registration__with_batch=batch, is_deleted=False)

    return Response({"status": True, "data": AttendanceMarksSerializer(attendance_marks_queryset, many=True).data})


@api_view(["POST"])
def update_attendance_marks(request):
    session, year, term = request.data.get("session"), request.data.get("year"), request.data.get("term")
    course_number, section = request.data.get("course_number"), request.data.get("section")
    marks = request.data.get("marks")
    teacher = request.data.get("teacher")
    teacher_id = teacher['data']['id']

    teacher_object = Teacher.objects.filter(id=teacher_id).first()
    term_object = TermData.objects.filter(session=session, year=year, term=term).first()

    for i in marks:
        student_id = i[0]
        obtained_marks = i[1]
        course_registration_object = CourseRegistration.objects.filter(term=term_object,
                                                                       course__course_number=course_number,
                                                                       student__student_id=student_id,
                                                                       is_deleted=False).first()
        pprint(request.data)
        print(course_registration_object, term_object, student_id)

        attendance_marks_object = AttendanceMarks.objects.filter(course_registration=course_registration_object,
                                                                 section=1 if section == "A" else 2 if section == "B" else 3,
                                                                 teacher=teacher_object).first()
        attendance_marks_object.obtained_marks = obtained_marks
        attendance_marks_object.save()
    return Response({"status": True})


@api_view(["POST"])
def get_info_for_remuneration(request):
    session = request.data.get("session")
    year = request.data.get("year")
    term = request.data.get("term")
    teacher_id = request.data.get("teacher_id")
    discipline_id = request.data.get("discipline")

    question_preparation_ans_script_queryset = QuestionPreparationScriptExamination.objects.filter(Q(
                                               session=session, year=year, term=term, discipline=discipline_id,
                                               teacher1=teacher_id) | Q(session=session, year=year, term=term,
                                               discipline=discipline_id, teacher2=teacher_id))

    class_test_queryset = ClassTest.objects.filter(session=session, year=year, term=term, discipline=discipline_id,
                                                   teacher=teacher_id)

    sessional_viva_queryset = SessionalAssessmentViva.objects.filter(Q(
                                               session=session, year=year, term=term, discipline=discipline_id,
                                               teacher1=teacher_id) | Q(session=session, year=year, term=term,
                                               discipline=discipline_id, teacher2=teacher_id))

    moderation_committee_queryset = ModerationCommitee.objects.filter(session=session, year=year, term=term,
                                                                      discipline=discipline_id,teacher=teacher_id)

    answer_script_scrutiny_queryset = AnswerScriptScrutiny.objects.filter(session=session, year=year, term=term,
                                                                          discipline=discipline_id, teacher=teacher_id)

    tabulation_student_queryset = TabulationStudentWise.objects.filter(session=session, year=year, term=term,
                                                                       discipline=discipline_id, teacher=teacher_id)

    tabulation_course_queryset = TabulationCourseWise.objects.filter(session=session, year=year, term=term,
                                                                     discipline=discipline_id, teacher=teacher_id)

    question_drawing_queryset = QuestionDrawing.objects.filter(session=session, year=year, term=term,
                                                               discipline=discipline_id, teacher=teacher_id)

    return Response({"status": True,
                     "question_preparation_data": QuestionPreparationScriptExaminationSerializer(
                                                  question_preparation_ans_script_queryset, many=True).data,
                     "class_test_data": ClassTestSerializer(class_test_queryset, many=True).data,
                     "sessional_viva_data": SessionalAssessmentVivaSerializer(
                                            sessional_viva_queryset, many=True).data,
                     "moderation_committee_data": ModerationCommiteeSerializer(
                                                  moderation_committee_queryset, many=True).data,
                     "answer_script_scrutiny": AnswerScriptScrutinySerializer(
                                        answer_script_scrutiny_queryset, many=True).data,
                     "tabulation_student_data": TabulationStudentWiseSerializer(
                                                tabulation_student_queryset, many=True).data,
                     "tabulation_course_data": TabulationCourseWiseSerializer(
                                               tabulation_course_queryset, many=True).data,
                     "question_drawing_data": QuestionDrawingSerializer(question_drawing_queryset, many=True).data
                     })
