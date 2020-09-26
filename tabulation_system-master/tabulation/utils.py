from pprint import pprint

from django.db.models import Max, Sum, Q

from .models import TermData, CourseRegistration, AttendanceMarks, TheoryMarks, LabMarks
import math


def get_term_object(request):
    session = request.data.get("session")
    year = request.data.get("year")
    term = request.data.get("term")

    term_object = TermData.objects.filter(session=session, year=year, term=term).first()

    return term_object


def get_course_registration_times(session, year, term, student_object):
    term_object = TermData.objects.filter(session=session, year=year, term=term).first()

    course_registration_object = CourseRegistration.objects.filter(student=student_object, term=term_object)
    times = course_registration_object.aggregate(Max("times"))
    return times['times__max']


def is_retake(student_id, course_number):
    course_registration_queryset = CourseRegistration.objects.filter(student__student_id=student_id,
                                                                     course__course_number=course_number,
                                                                     is_deleted=False)
    return not len(course_registration_queryset) == 1


def get_grade(marks, retake=False):
    if retake:
        marks -= 5
        if marks < 40:
            marks = 40

        if marks >= 80:
            marks = 79

    if marks >= 80:  # 80 <= marks <= 100 is a better option?
        return "A+", 4.00
    elif 75 <= marks <= 79:
        return "A", 3.75
    elif 70 <= marks <= 74:
        return "A-", 3.50
    elif 65 <= marks <= 69:
        return "B+", 3.25
    elif 60 <= marks <= 64:
        return "B", 3.00
    elif 55 <= marks <= 59:
        return "B-", 2.75
    elif 50 <= marks <= 54:
        return "C+", 2.50
    elif 45 <= marks <= 49:
        return "C", 2.25
    elif 40 <= marks <= 44:
        return "D", 2.00
    else:
        return "F", 0.00


def get_all_class_test_marks(request, batch, course_number):
    term_object = get_term_object(request)

    class_test_marks_queryset = TheoryMarks.objects.filter(~Q(class_test_no=None),
                                                           course_registration__course__course_number=course_number,
                                                           course_registration__with_batch=batch,
                                                           course_registration__term=term_object,
                                                           is_deleted=False).order_by("-obtained_marks")

    marks_dict = dict()

    for i in class_test_marks_queryset:
        student_id = i.course_registration.student.student_id
        if student_id in marks_dict:
            marks_dict[student_id].append(int(i.obtained_marks) if i.obtained_marks.isdigit() else 0)
        else:
            marks_dict[student_id] = [int(i.obtained_marks) if i.obtained_marks.isdigit() else 0]

    for key in marks_dict.keys():
        marks_dict[key] = math.ceil(sum(sorted(marks_dict[key], reverse=True)[:2]) / 2)
    return marks_dict


def get_utils_all_attendance_marks(request, batch, course_number):
    term_object = get_term_object(request)

    attendance_queryset = AttendanceMarks.objects.filter(
        course_registration__course__course_number=course_number,
        course_registration__with_batch=batch, course_registration__term=term_object,
        is_deleted=False)

    if attendance_queryset.first() and attendance_queryset.first().section == 3:
        marks_list = [
            (i.course_registration.student.student_id, int(i.obtained_marks) if i.obtained_marks.isdigit() else 0) for i
            in attendance_queryset]
        return dict(marks_list)

    student_list = list()
    marks_list = list()

    for i in attendance_queryset:
        student_list.append(i.course_registration.student.student_id)

    for i in student_list:
        obtained_marks = attendance_queryset.filter(course_registration__student__student_id=i).aggregate(
            Sum("obtained_marks"))
        marks_list.append((i, obtained_marks.get("obtained_marks__sum")))
        return dict(marks_list)


def get_all_theory_marks(request, course_number, batch, course_type, section=None, lab_marks_type=1):
    term_object = get_term_object(request)

    if course_type == 1:
        obtained_marks_queryset = TheoryMarks.objects.filter(course_registration__term=term_object, section=section,
                                                             course_registration__course__course_number=course_number,
                                                             course_registration__course__course_type=course_type,
                                                             course_registration__with_batch=batch,
                                                             class_test_no=None,
                                                             is_deleted=False)
        marks_list = [
            (i.course_registration.student.student_id, int(i.obtained_marks) if i.obtained_marks.isdigit() else 0) for i
            in obtained_marks_queryset]
        return dict(marks_list)

    elif course_type == 2:
        obtained_marks_queryset = LabMarks.objects.filter(course_registration__term=term_object, type=lab_marks_type,
                                                          course_registration__course__course_number=course_number,
                                                          course_registration__course__course_type=course_type,
                                                          course_registration__with_batch=batch,
                                                          is_deleted=False)
        print(obtained_marks_queryset)
        marks_list = [
            (i.course_registration.student.student_id, int(i.obtained_marks) if i.obtained_marks.isdigit() else 0) for i
            in
            obtained_marks_queryset]
        return dict(marks_list)

    elif course_type == 3:
        obtained_marks_queryset = LabMarks.objects.filter(tcourse_registration__term=term_object, type=2,
                                                          course_registration__course__course_number=course_number,
                                                          course_registration__course__course_type=course_type,
                                                          course_registration__with_batch=batch,
                                                          is_deleted=False)
        marks_list = [
            (i.course_registration.student.student_id, int(i.obtained_marks) if i.obtained_marks.isdigit() else 0) for i
            in
            obtained_marks_queryset]
        return dict(marks_list)


def get_terms_of_student(student_id):
    term_list = list()
    course_registration_queryset = CourseRegistration.objects.filter(student__student_id=student_id, is_deleted=False)

    for i in course_registration_queryset:
        if i.term not in term_list:
            term_list.append(i.term)

    return term_list


def get_courses(student_id, term):
    course_registration_queryset = CourseRegistration.objects.filter(student__student_id=student_id, term=term,
                                                                     is_deleted=False)
    return course_registration_queryset


def get_attendance_mark(student_id, course_number, term):
    obtained_marks = AttendanceMarks.objects.filter(course_registration__course__course_number=course_number,
                                                    course_registration__student__student_id=student_id,
                                                    course_registration__term=term, is_deleted=False).aggregate(
        Sum("obtained_marks"))
    if obtained_marks:
        return obtained_marks.get("obtained_marks__sum")


def get_utils_class_test_marks(student_id, course_number, term):
    class_test_marks = TheoryMarks.objects.filter(~Q(class_test_no=None),
                                                  course_registration__student__student_id=student_id,
                                                  course_registration__course__course_number=course_number,
                                                  course_registration__term=term, is_deleted=False).order_by(
        "-obtained_marks")[
                       :2].aggregate(Sum("obtained_marks"))

    if class_test_marks:
        return math.ceil(class_test_marks.get("obtained_marks__sum") / 2)


def get_semester_final_marks(student_id, course_number, term):
    semester_final_marks = TheoryMarks.objects.filter(class_test_no=None,
                                                      course_registration__student__student_id=student_id,
                                                      course_registration__course__course_number=course_number,
                                                      course_registration__term=term, is_deleted=False).aggregate(
        Sum("obtained_marks"))

    return semester_final_marks.get("obtained_marks__sum")


def get_sessional_marks(student_id, course_number, term):
    sessional_marks = LabMarks.objects.filter(course_registration__course__course_number=course_number,
                                              course_registration__student__student_id=student_id,
                                              course_registration__term=term, type=1, is_deleted=False).first()

    print(sessional_marks)
    if sessional_marks:
        return sessional_marks.obtained_marks


def get_viva_marks(student_id, course_number, term):
    viva_marks = LabMarks.objects.filter(course_registration__course__course_number=course_number,
                                         course_registration__student__student_id=student_id,
                                         course_registration__term=term, type=2, is_deleted=False).first()
    if viva_marks:
        return viva_marks.obtained_marks
