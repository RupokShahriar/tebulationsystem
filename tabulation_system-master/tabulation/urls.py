from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *
from .viewsets import *

router = DefaultRouter()
router.register("offered_course", OfferedCoursesViewSet,)
router.register("course-registration", CourseRegistrationViewSet,)
router.register("prerequisites", PrerequisiteViewSet)
router.register("QuestionPreparationScriptExamination", QuestionPreparationScriptExaminationViewSet)
router.register("ClassTest", ClassTestViewSet)
router.register("SessionalAssessmentViva", SessionalAssessmentVivaViewSet)
router.register("ModerationCommitee", ModerationCommiteeViewSet)
router.register("AnswerScriptScrutiny", AnswerScriptScrutinyViewSet)
router.register("TabulationStudentWise", TabulationStudentWiseViewSet)
router.register("TabulationCourseWise", TabulationCourseWiseViewSet)
router.register("QuestionDrawing", QuestionDrawingViewSet)


urlpatterns = [
    path("allow/", allow, name="allow"),
    path("login/", login, name="login"),
    path("get_pending_registration/", get_pending_registration, name="get_pending_registration"),
    path("get_registered_students/", get_registered_students, name="get_registered_steudents"),
    path("get_registration_details/", get_registration_details, name="get_registration_details"),
    path("input_attendance_marks/", input_attendance_marks, name="input_attendance_marks"),
    path("input_theory_marks/", input_theory_marks, name="input_theory_marks"),
    path("input_sessional_marks/", input_sessional_marks, name="input_sessional_marks"),
    path("reject/", reject, name="reject"),
    path("get-class-test-marks/", get_class_test_marks, name="get_class_test_marks"),
    path("get-sessions-years-terms-batches/", get_sessions_years_terms_batches,
         name="get_sessions_years_terms_batches"),
    path("get-term-wise-result/", get_term_wise_result, name="get_term_wise_result"),
    path("get-student-wise-result/", get_student_wise_result, name="get_student_wise_result"),
    path("get-all-attendance-marks/", get_all_attendance_marks, name="get_all_attendance_marks"),
    path("get-theory-marks-for-edit/", get_theory_marks_for_edit, name="get_theory_marks_for_edit"),
    path("update-theory-marks/", update_theory_marks, name="update_theory_marks"),
    path("get-sessional-marks-for-edit/", get_sessional_marks_for_edit, name="get_sessional_marks_for_edit"),
    path("update-sessional-marks/", update_sessional_marks, name="update_sessional_marks"),
    path("get-attendance-marks-for-edit/", get_attendance_marks_for_edit, name="get_attendance_marks_for_edit"),
    path("update-attendance-marks/", update_attendance_marks, name="update_attendance_marks"),
    path("get-remuneration-info/", get_info_for_remuneration, name="get_info_for_remuneration"),

]

urlpatterns += router.urls
