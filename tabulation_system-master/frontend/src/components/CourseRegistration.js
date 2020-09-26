import React, {Component} from "react";
//import axios from "axios";

import YearTermSessionBatchComponent from "./YearTermSessionBatchComponent";
import TopBar from "./TopBar";
import APICalls from "../services/APICalls"


export default class CourseRegistration extends Component {

    constructor(props) {
        super(props);


        this.state = {
            total_credit: 0.0,
            courseList: [],
            offeredCourses: [],
            expectedCourses: [],
            pendingCourses: [],
            registeredCourses: [],
            prerequisites: [],
        };

        this.session = "";
        this.year = "";
        this.term = "";
        this.batch = "";
        this.apiCalls = new APICalls();

        this.addToExpectedCourses = this.addToExpectedCourses.bind(this);
        this.load = this.load.bind(this);
        this.removeFromExpectedCourses = this.removeFromExpectedCourses.bind(this);
        this.submit = this.submit.bind(this);
        this.getRegisteredCoures = this.getRegisteredCoures.bind(this);
        this.load_prerequisites = this.load_prerequisites.bind(this);
        this.update_credit_hours = this.update_credit_hours.bind(this);
    }

    componentWillMount() {
        document.title = "Course Registration";
        this.load_prerequisites();
    }

    async load_prerequisites() {
        const response = await this.apiCalls.get_prerequisites();
        const data = response.data;
        this.setState({prerequisites: data});
    }

    async load(session, year, term, batch) {
        this.session = session;
        this.year = year;
        this.term = term;
        this.batch = batch;

        const response = await this.apiCalls.get_course_response(session, year, term);
        this.setState({courseList: [], expectedCourses: [], registeredCourses: [], pendingCourses: []});
        if (response.data.status) {
            // eslint-disable-next-line
            response.data.data.map((course) => {
                this.setState({courseList: [...this.state.courseList, course]});
            });
            // eslint-disable-next-line
            response.data.registered.map((course) => {
                this.setState({registeredCourses: [...this.state.registeredCourses, course]});
            });
            // eslint-disable-next-line
            response.data.pending.map((course) => {
                this.setState({
                    pendingCourses: [...this.state.registeredCourses, course],
                    expectedCourses: [...this.state.expectedCourses, course]
                });
            });
        }
        this.update_credit_hours();
    }

    getRegisteredCoures() {
        if (this.state.registeredCourses.length > 0) {
            return <div className="card">
                <div className="card-header">
                    Already registered course for this term
                </div>
                <div className="card-body">
                    <table className="table table-striped table-bordered">
                        <tbody>
                        {this.state.registeredCourses.map((courseDetails, index) => {
                            const courseData = courseDetails.course;
                            return <tr key={courseData.course_number}>
                                <td>{courseData.course_number}</td>
                                <td>{courseData.course_title}</td>
                                <td>{courseData.credit_hour}</td>
                                {/*<td><a href="javascript:;" onClick={() => this.addToExpectedCourses(index)}><span*/}
                                {/*className="fa fa-plus-circle"></span></a></td>*/}
                            </tr>;
                        })}
                        </tbody>

                    </table>
                </div>
            </div>
        }
    }

    update_credit_hours() {
        let credit = 0;
        // eslint-disable-next-line
        this.state.expectedCourses.map((course) => {
            credit += course.course_data.credit_hour;
        });
        this.setState({total_credit: credit});
    }

    addToExpectedCourses(index) {

        let tempArray = this.state.courseList;
        const toRemoveItem = this.state.courseList[index];
        this.setState({total_credit: this.state.total_credit + toRemoveItem.course_data.credit_hour});
        this.setState({expectedCourses: [...this.state.expectedCourses, toRemoveItem]});

        tempArray.splice(index, 1);
        this.setState({courseList: tempArray});

    }

    removeFromExpectedCourses(index) {

        let tempArray = this.state.expectedCourses;
        const toRemoveItem = this.state.expectedCourses[index];
        this.setState({total_credit: this.state.total_credit - toRemoveItem.course_data.credit_hour});
        this.setState({courseList: [...this.state.courseList, toRemoveItem]});

        tempArray.splice(index, 1);
        this.setState({expectedCourses: tempArray});

    }

    async submit() {


        const response = await this.apiCalls.course_registration(this.session, this.year, this.term, this.batch, this.state.expectedCourses);
        if (response.data.status) {
            alert("Successfully submitted your request");
            this.props.history.push("/");
        } else {
            alert("Something went wrong, please try again");
        }
    }

    render() {
        return (
            <div>
                <TopBar/>
                <YearTermSessionBatchComponent load={this.load}/>

                <div className={"row"} style={{paddingLeft: "10px", paddingRight: "10px", paddingTop: "20px"}}>
                    <div className={"col-md-6"}>
                        <div className="card">
                            <div className="card-header">
                                Expected Courses (Total credit hours : {this.state.total_credit})
                            </div>
                            <div className="card-body">
                                <table className="table table-striped table-bordered">
                                    <tbody>
                                    {this.state.expectedCourses.map((course, index) => {
                                        const courseData = course.course_data;
                                        return <tr key={courseData.course_number}>
                                            <td>{courseData.course_number}</td>
                                            <td>{courseData.course_title}</td>
                                            <td>{courseData.credit_hour}</td>
                                            <td><a 
                                            // eslint-disable-next-line
                                            href="javascript:;"
                                                   onClick={() => this.removeFromExpectedCourses(index)}><span
                                                className="fa fa-minus-circle" style={{color: "red"}}></span></a></td>
                                        </tr>;
                                    })}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <br/>
                        <div style={{paddingTop: 20, paddingLeft: 20}}>
                            <button className="btn btn-primary" onClick={this.submit}>Submit</button>
                        </div>
                    </div>

                    <div className={"col-md-6"}>
                        <div className="card">
                            <div className="card-header">
                                Offered Courses
                            </div>
                            <div className="card-body">
                                <table className="table table-striped table-bordered">
                                    <tbody>
                                    {this.state.courseList.map((course, index) => {
                                        const courseData = course.course_data;
                                        return <tr key={courseData.course_number}>
                                            <td>{courseData.course_number}</td>
                                            <td>{courseData.course_title}</td>
                                            <td>{courseData.credit_hour}</td>
                                            <td><a 
                                            // eslint-disable-next-line
                                            href="javascript:;" onClick={() => this.addToExpectedCourses(index)}><span
                                                className="fa fa-plus-circle"></span></a></td>
                                        </tr>;
                                    })}
                                    </tbody>

                                </table>
                            </div>
                        </div>
                        <br/>
                        {this.getRegisteredCoures()}
                        <br/>
                        <div className="card">
                            <div className="card-header">
                                Prerequisite Courses
                            </div>
                            <div className="card-body">
                                <table className="table table-striped table-bordered">
                                    <thead>
                                    <tr>
                                        <th>Course</th>
                                        <th>Prerequiste course</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {this.state.prerequisites.map((course, index) => {
                                        return <tr key={index}>
                                            <td>{course.main_course.course_number} ({course.main_course.course_title})</td>
                                            <td>{course.prerequisite_course.course_number} ({course.prerequisite_course.course_title})</td>

                                        </tr>;
                                    })}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>


            </div>
        )
    }
}