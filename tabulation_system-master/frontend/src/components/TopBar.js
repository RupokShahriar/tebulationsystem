import React, {Component} from "react";
import UserService from "../services/User";

//import {NavLink} from "react-router-dom";

export default class TopBar extends Component {

    constructor(props) {
        super(props);
        this.userService = new UserService();
        this.user = this.userService.getUser().data;
    }

    render() {

        if (this.userService.getUser()) {
            return (
                <nav className="navbar navbar-expand-lg  navbar-dark bg-dark ">
                    <a className="navbar-brand" href="/">Khulna University Tabulation System</a>
                    <button className="navbar-toggler" type="button" data-toggle="collapse"
                            data-target="#navbarNavDropdown"
                            aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>

                    <div className="collapse navbar-collapse justify-content-end" id="navbarNavDropdown">
                        <ul className="navbar-nav">
                            {!this.user.student_id ?
                                <li className="nav-item dropdown">
                                    <a className="nav-link" href="review-course-registration">
                                        Review Course Registration
                                    </a>
                                </li> :
                                <li className="nav-item dropdown">
                                    <a className="nav-link" href="/course-registration">
                                        Course Registration
                                    </a>
                                </li>
                            }
                            {this.user.student_id ?
                                <li className="nav-item dropdown">
                                    <a className="nav-link dropdown-toggle" id="navbarDropdownMenuStudent"
                                       data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        Marks
                                    </a>
                                    <div className="dropdown-menu" aria-labelledby="navbarDropdownMenuStudent">
                                        <a className="dropdown-item" href="/show-class-test-marks">Show Class Test
                                            Marks</a>
                                        <a className="dropdown-item" href="/show-attendance-marks">Show Attendance
                                            Marks</a>
                                    </div>
                                </li> : ""
                            }
                            {this.user.student_id ?
                                <li className="nav-item dropdown">
                                    <a className="nav-link dropdown-toggle"  id="navbarDropdownMenuStudent"
                                       data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        Result
                                    </a>
                                    <div className="dropdown-menu" aria-labelledby="navbarDropdownMenuStudent">
                                        <a className="dropdown-item" href="/student-wise-result">Show result</a>

                                    </div>
                                </li> : ""
                            }
                            {this.user.student_id ?
                                <li className="nav-item dropdown">
                                    <a className="nav-link dropdown-toggle"  id="navbarDropdownMenuStudent"
                                       data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        Student
                                    </a>
                                    <div className="dropdown-menu" aria-labelledby="navbarDropdownMenuStudent">
                                        <a className="dropdown-item" href="/my-info">My Info</a>
                                        <a className="dropdown-item" href="/login"
                                           onClick={this.userService.clearData}>Logout</a>
                                        {/*<a className="dropdown-item" href="/result">Results</a>*/}

                                    </div>
                                </li> : ""
                            }

                            {!this.user.student_id ?
                                <li className="nav-item dropdown">
                                    <a className="nav-link dropdown-toggle"  id="navbarDropdownMenuResult"
                                       data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        Marks Entry
                                    </a>
                                    <div className="dropdown-menu" aria-labelledby="navbarDropdownMenuREsult">
                                        <a className="dropdown-item" href="/theory-marks-entry">Theory Marks Entry</a>
                                        <a className="dropdown-item" href="/sessional-marks-entry">Sessional Marks
                                            Entry</a>
                                        <a className="dropdown-item" href="/attendance-marks-entry">Attendance Marks
                                            Entry</a>
                                        {/*<a className="dropdown-item" href="/edit-marks">Edit Marks</a>*/}
                                    </div>
                                </li>
                                : ""}

                            {!this.user.student_id ?
                                <li className="nav-item dropdown">
                                    <a className="nav-link dropdown-toggle"  id="navbarDropdownMenuResult"
                                       data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        Edit Marks
                                    </a>
                                    <div className="dropdown-menu" aria-labelledby="navbarDropdownMenuREsult">
                                        <a className="dropdown-item" href="/theory-marks-edit">Edit Theory Marks</a>
                                         <a className="dropdown-item" href="/sessional-marks-edit">Edit Sessional Marks</a>
                                         <a className="dropdown-item" href="/attendance-marks-edit">Edit Attendance Marks</a>
                                    </div>
                                </li>
                                : ""}
                            {!this.user.student_id ?
                                <li className="nav-item dropdown">
                                    <a className="nav-link dropdown-toggle"  id="navbarDropdownMenuTeacher"
                                       data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        Result
                                    </a>
                                    <div className="dropdown-menu" aria-labelledby="navbarDropdownMenuTeacher">
                                        <a className="dropdown-item" href="/term-wise-result">Term Wise Result</a>
                                        <a className="dropdown-item" href="/student-wise-result">Student Wise Result</a>
                                    </div>
                                </li> : ""
                            }
                            {!this.user.student_id ?
                                <li className="nav-item dropdown">
                                    <a className="nav-link dropdown-toggle"  id="navbarDropdownMenuTeacher"
                                       data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        Teacher
                                    </a>
                                    <div className="dropdown-menu" aria-labelledby="navbarDropdownMenuTeacher">
                                        <a className="dropdown-item" href="/my-info">My Info</a>
                                        <a className="dropdown-item" href="/login"
                                           onClick={this.userService.clearData}>Logout</a>
                                    </div>
                                </li> : ""
                            }

                            {/*<li className="nav-item">*/}
                            {/*<NavLink to="/login" className="nav-link" onClick={() => {*/}
                            {/*this.userService.clearData();*/}
                            {/*}}>Logout</NavLink>*/}
                            {/*</li>*/}
                        </ul>
                    </div>
                </nav>
            )
        } else {
            return (
                <nav className="navbar navbar-expand-lg  navbar-dark bg-dark">
                    <a className="navbar-brand" href="/">Khulna University Tabulation System</a>
                    <button className="navbar-toggler" type="button" data-toggle="collapse"
                            data-target="#navbarNavDropdown"
                            aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                </nav>
            )
        }
    }
}