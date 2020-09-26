const domain = "http://127.0.0.1:8000";

const APPCONFIG = {
    allowURL : domain+"/tabulation/allow/",
    courseRegistrationURL: domain+"/tabulation/course-registration/",
    getOfferedCoursesURL : "",
    inputTheoryMarksURL:domain+"/tabulation/input_theory_marks/",
    inputSessionalMarksURL:domain+"/tabulation/input_sessional_marks/",
    inputAttendanceMarksURL:domain+"/tabulation/input_attendance_marks/",
    getRegisteredStudentsURL:domain+"/tabulation/get_registered_students/",
    pendingRegistrationURL:domain+"/tabulation/get_pending_registration/",
    registrationDetailsURL:domain+"/tabulation/get_registration_details/",
    rejectURL:domain+"/tabulation/reject/",
    loginURL : domain+"/tabulation/login/",
    getClassTestMarksURL: domain+"/tabulation/get-class-test-marks/",
    sessionsYearsTermsBatchesURL: domain+"/tabulation/get-sessions-years-terms-batches/",
    getTermWiseResultURL: domain+"/tabulation/get-term-wise-result/",
    getStudentWiseResultURL: domain+"/tabulation/get-student-wise-result/",
    getAllAttendanceMarksURL:domain+"/tabulation/get-all-attendance-marks/",
    getTheoryMarksForEditURL: domain+"/tabulation/get-theory-marks-for-edit/",
    updateTheoryMarksURL : domain+"/tabulation/update-theory-marks/",
    getSessionalMarksForEditURL: domain+"/tabulation/get-sessional-marks-for-edit/",
    updateSessionalMarksURL : domain+"/tabulation/update-sessional-marks/",
    getAttendanceMarksForEditURL: domain+"/tabulation/get-attendance-marks-for-edit/",
    updateAttendanceMarksURL : domain+"/tabulation/update-attendance-marks/",
    prerequisitesURL: domain+"/tabulation/prerequisites/"

};

export default APPCONFIG;