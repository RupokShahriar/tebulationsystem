from django.contrib import admin
from .models import (Discipline, Student, TermData, Course, OfferedCourses, Teacher, CourseRegistration, TheoryMarks,
                     LabMarks, AttendanceMarks, Prerequisite, ThesisConfiguration, QuestionPreparationScriptExamination,
                     ClassTest, SessionalAssessmentViva, ModerationCommitee, AnswerScriptScrutiny, TabulationStudentWise,
                     TabulationCourseWise, QuestionDrawing )

admin.site.register(Course)
admin.site.register(CourseRegistration)
admin.site.register(Discipline)
admin.site.register(OfferedCourses)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(TermData)
admin.site.register(TheoryMarks)
admin.site.register(LabMarks)
admin.site.register(AttendanceMarks)
admin.site.register(Prerequisite)
admin.site.register(ThesisConfiguration)
admin.site.register(QuestionPreparationScriptExamination)
admin.site.register(ClassTest)
admin.site.register(SessionalAssessmentViva)
admin.site.register(ModerationCommitee)
admin.site.register(AnswerScriptScrutiny)
admin.site.register(TabulationStudentWise)
admin.site.register(TabulationCourseWise)
admin.site.register(QuestionDrawing)


