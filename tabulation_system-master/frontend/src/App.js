import React, {Component} from 'react';
import './App.css';
import {BrowserRouter, Route, Switch} from "react-router-dom";
import CourseRegistration from "./components/CourseRegistration"
import Home from "./components/Home";
import Login from "./components/Login";
import MarksEntry from "./components/MarksEntry";
import MyInfo from "./components/MyInfo";
import ReviewCourseRegistration from "./components/ReviewCourseRegistration";
import SessionalMarksEntry from "./components/SessionalMarksEntry";
import AttendanceMarksEntry from "./components/AttendanceMarksEntry";
import ShowClassTestMarks from "./components/ShowClassTestMarks";
import TheoryMarksEdit from "./components/TheoryMarksEdit";
import ShowTermWiseResultsTeacher from "./components/ShowTermWiseResultsTeacher";
import ShowStudentWiseResults from "./components/ShowStudentWiseResults";
import ShowAttendanceMarks from "./components/ShowAttendanceMarks";
import SessionalMarksEdit from "./components/SessionalMarksEdit";
import AttendanceMarksEdit from "./components/AttendanceMarksEdit";


class App extends Component {
    render() {
        return (
            <BrowserRouter>
                <Switch>
                    <Route exact path="/" component={Home}/>
                    <Route exact path="/course-registration" component={CourseRegistration}/>
                    <Route exact path="/login" component={Login}/>
                    <Route exact path="/theory-marks-entry" component={MarksEntry}/>
                    <Route exact path="/sessional-marks-entry" component={SessionalMarksEntry}/>
                    <Route exact path="/attendance-marks-entry" component={AttendanceMarksEntry}/>
                    <Route exact path="/my-info" component={MyInfo}/>
                    <Route exact path="/review-course-registration" component={ReviewCourseRegistration}/>
                    <Route exact path="/show-class-test-marks" component={ShowClassTestMarks}/>
                    <Route exact path="/term-wise-result" component={ShowTermWiseResultsTeacher}/>
                    <Route exact path="/student-wise-result" component={ShowStudentWiseResults}/>
                    <Route exact path="/show-attendance-marks" component={ShowAttendanceMarks}/>
                    <Route exact path="/theory-marks-edit" component={TheoryMarksEdit}/>
                    <Route exact path="/sessional-marks-edit" component={SessionalMarksEdit}/>
                    <Route exact path="/attendance-marks-edit" component={AttendanceMarksEdit}/>
                </Switch>

            </BrowserRouter>

        );
    }
}

export default App;
