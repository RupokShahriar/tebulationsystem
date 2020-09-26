//import React from "react";
import axios from "axios";

import UserService from "../services/User";

import AppConfig from "../config/AppConfig";
//import User from "./User";


export default class APICalls {

    async get_course_response(session, year, term) {
        const userService = new UserService().getUser().data;
        const student_id = userService.student_id;
        const discipline_id = userService.discipline.code_number;

        const url = "http://127.0.0.1:8000/tabulation/offered_course/?session=" + session + "&year=" +
            year + "&term=" + term + "&discipline_id=" + discipline_id + "&student_id=" + student_id;
        console.log(url);
        const response = await axios({
            method: "GET",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },

            url: url,
            timeout: 10 * 1000,
        });
        console.log(response.status);
        return response;
    }

    async course_registration(session, year, term, batch, courseList) {
        console.log(session);
        const userService = new UserService();
        const {courseRegistrationURL} = AppConfig;
        let course_numbers = [];

        for (let i = 0; i < courseList.length; i++) {
            course_numbers.push(courseList[i].course_data.course_number);
        }

        console.log(courseRegistrationURL);
        const response = await axios({
            method: "POST",
            url: courseRegistrationURL,
            data: {
                session: session,
                year: year,
                term: term,
                batch: batch,
                course_list: courseList,
                user: userService.getUser()
            }
        });
        return response;
    }

    async get_pending_registration(session, year, term, batch) {
        const userService = new UserService();
        const {pendingRegistrationURL} = AppConfig;

        const response = await axios({
            method: "POST",
            url: pendingRegistrationURL,
            data: {
                session: session,
                year: year,
                term: term,
                batch: batch,
                user: userService.getUser()
            }
        });
        return response;
    }

    async get_registration_details(session, year, term, batch, student_id) {
        const {registrationDetailsURL} = AppConfig;

        const response = await axios({
            method: "POST",
            url: registrationDetailsURL,
            data: {
                session: session,
                year: year,
                term: term,
                batch: batch,
                student_id: student_id
            }
        });
        return response;
    }

    async reject(session, year, term, batch, student_id, cause) {
        const {rejectURL} = AppConfig;
        const userService = new UserService();

        const response = await axios({
            method: "POST",
            url: rejectURL,
            data: {
                session: session,
                year: year,
                term: term,
                batch: batch,
                student_id: student_id,
                cause: cause,
                teacher: userService.getUser()
            }
        });
        return response;
    }

    async allow(session, year, term, batch, student_id, allowed_courses, rejected_courses) {
        const {allowURL} = AppConfig;
        const userService = new UserService();

        const response = await axios({
            method: "POST",
            url: allowURL,
            data: {
                session: session,
                year: year,
                term: term,
                batch: batch,
                allowed_courses,
                rejected_courses,
                student_id,
                teacher: userService.getUser()
            }

        });

        return response;
    }

    async get_registered_students(session, year, term, batch, course_number) {
        const {getRegisteredStudentsURL} = AppConfig;


        const response = await axios({
            method: "POST",
            url: getRegisteredStudentsURL,
            data: {
                session: session,
                year: year,
                term: term,
                batch: batch,
                course_number: course_number
            }
        });
        return response;
    }


    async input_sessional_marks(session, year, term, batch, course_number, type, marks) {
        const {inputSessionalMarksURL} = AppConfig;
        const userService = new UserService();

        const response = await axios({
            method: "POST",
            url: inputSessionalMarksURL,
            data: {
                session,
                year,
                term,
                batch,
                course_number,
                type,
                marks,
                teacher: userService.getUser()
            }
        });
        return response;
    }

    async input_attendance_marks(session, year, term, batch, course_number, section, marks) {
        const {inputAttendanceMarksURL} = AppConfig;
        const userService = new UserService();

        const response = await axios({
            method: "POST",
            url: inputAttendanceMarksURL,
            data: {
                session,
                year,
                term,
                batch,
                course_number,
                section,
                marks,
                teacher: userService.getUser()
            }
        });
        return response;
    }

    async get_class_test_marks(session, year, term, batch) {
        const userService = new UserService();
        const student_id = userService.getUser().data.student_id;
        const {getClassTestMarksURL} = AppConfig;

        const response = await axios({
            method: "POST",
            url: getClassTestMarksURL,
            data: {
                session, year, term, batch, student_id
            }
        });
        return response;
    }

    async get_sessions_years_terms_batches() {

        const {sessionsYearsTermsBatchesURL} = AppConfig;

        const response = await axios({
            method: "GET",
            url: sessionsYearsTermsBatchesURL
        });
        return response;
    }

    async get_term_wise_result(session, year, term, batch, course_title) {
        const {getTermWiseResultURL} = AppConfig;

        const response = await axios({
            method: "POST",
            url: getTermWiseResultURL,
            data: {
                session, year, term, batch, course_title

            }
        });
        return response;
    }

    async get_student_wise_result(student_id) {
        const {getStudentWiseResultURL} = AppConfig;

        const response = await axios({
            method: "POST",

            url: getStudentWiseResultURL,
            data: {
                student_id
            }
        });
        return response;
    }

    async get_all_attendance_marks(session, year, term, batch) {
        const {getAllAttendanceMarksURL} = AppConfig;

        const response = await axios({
            method: "POST",
            url: getAllAttendanceMarksURL,
            data: {
                session, year, term, batch
            }
        });
        return response;
    }

    async get_theory_marks_for_edit(session, year, term, batch, course_number, section, class_test_no, marks_type) {
        const {getTheoryMarksForEditURL} = AppConfig;

        const response = await axios({
            method: "POST",
            url: getTheoryMarksForEditURL,
            data: {
                session, year, term, batch, course_number, section, class_test_no, marks_type
            }
        });
        return response;

    }
        async input_theory_marks(session, year, term, batch, course_number, section, type, class_test_no, marks) {
        const {inputTheoryMarksURL} = AppConfig;
        const userService = new UserService();

        const response = await axios({
            method: "POST",
            url: inputTheoryMarksURL,
            data: {
                session,
                year,
                term,
                batch,
                course_number,
                section,
                type,
                class_test_no,
                marks,
                teacher: userService.getUser()
            }
        });
        return response;
    }

    async update_theory_marks(session, year, term, batch, course_number, section, type, class_test_no, marks) {
        const {updateTheoryMarksURL} = AppConfig;
        const userService = new UserService();

        const response = await axios({
            method: "POST",
            url: updateTheoryMarksURL,
            data: {
                session,
                year,
                term,
                batch,
                course_number,
                section,
                type,
                class_test_no,
                marks,
                teacher: userService.getUser()
            }
        });
        return response;
    }


    async get_sessional_marks_for_edit(session, year, term, batch, course_number, marks_type) {
        const {getSessionalMarksForEditURL} = AppConfig;

        const response = await axios({
            method: "POST",
            url: getSessionalMarksForEditURL,
            data: {
                session, year, term, batch, course_number, marks_type
            }
        });
        return response;

    }

    async update_sessional_marks(session, year, term, batch, course_number, type, marks) {
        const {updateSessionalMarksURL} = AppConfig;
        const userService = new UserService();

        const response = await axios({
            method: "POST",
            url: updateSessionalMarksURL,
            data: {
                session,
                year,
                term,
                batch,
                course_number,
                type,
                marks,
                teacher: userService.getUser()
            }
        });
        return response;
    }

    async get_attendance_marks_for_edit(session, year, term, batch, course_number, section) {
        const {getAttendanceMarksForEditURL} = AppConfig;

        const response = await axios({
            method: "POST",
            url: getAttendanceMarksForEditURL,
            data: {
                session, year, term, batch, course_number, section
            }
        });
        return response;

    }

    async update_attendance_marks(session, year, term, batch, course_number, section, marks) {
        const {updateAttendanceMarksURL} = AppConfig;
        const userService = new UserService();

        const response = await axios({
            method: "POST",
            url: updateAttendanceMarksURL,
            data: {
                session,
                year,
                term,
                batch,
                course_number,
                section,
                marks,
                teacher: userService.getUser()
            }
        });
        return response;
    }

    async get_prerequisites() {
        const userService = new UserService();
        let {prerequisitesURL} = AppConfig;

        prerequisitesURL = prerequisitesURL + "?discipline_code=" + userService.getUser().data.discipline.code_number;


        const response = await axios({
            method: "GET",
            url: prerequisitesURL,
        });
        return response;
    }


}
