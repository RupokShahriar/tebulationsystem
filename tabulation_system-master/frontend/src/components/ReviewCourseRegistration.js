import React, {Component} from 'react';
import TopBar from "./TopBar";
import YearTermSessionBatchComponent from "./YearTermSessionBatchComponent";
import APICalls from "../services/APICalls";
import ReviewModal from "./ReviewModal";


export default class ReviewCourseRegistration extends Component {

    constructor(props) {
        super(props);
        this.state = {
            pendingCourses: [],
            student_id: "",
            courses: [],
            prerequisites: [],

        };
        this.load = this.load.bind(this);
        this.getRegistrationDetails = this.getRegistrationDetails.bind(this);
        this.load_prerequisites = this.load_prerequisites.bind(this);
        this.session = "";
        this.year = "";
        this.term = "";
        this.batch = "";
        this.student_id = "";
        this.apiCalls = new APICalls();
    }

    componentWillMount() {
        document.title = "Review Course Registration";
        this.load_prerequisites();
    }

    async load_prerequisites() {
        const response = await this.apiCalls.get_prerequisites();
        const data = response.data;
        console.log(data);
        this.setState({prerequisites: data});
    }

    async load(session, year, term, batch) {
        this.session = session;
        this.year = year;
        this.term = term;
        this.batch = batch;
        const apiCalls = new APICalls();
        const response = await apiCalls.get_pending_registration(session, year, term, batch);
        const pendingCourses = response.data.data;

        console.log(pendingCourses);
        if (pendingCourses) {
            this.setState({pendingCourses: pendingCourses});
        }

    }

    async getRegistrationDetails() {
        const apiCalls = new APICalls();
        const response = await apiCalls.get_registration_details(this.session, this.year, this.term, this.batch, this.student_id);
        let data = response.data.data;


        if (data) {
            let courses = [];
// eslint-disable-next-line
            data.map((d) => {
                courses.push([d.course.course_number, d.course.course_title, d.course.credit_hour, d.comment]);
            });

            this.setState({courses: courses});
            console.log(data, this.state.courses);
        } else {
            this.setState({course: []});
        }
    }

    render() {
        return (
            <div>
                <TopBar/>
                <ReviewModal student_id={this.state.student_id} session={this.session} year={this.year} term={this.term}
                             batch={this.batch} courses={this.state.courses}/>
                <div className="container">
                    <YearTermSessionBatchComponent load={this.load}/>
                </div>
                <div className="container">
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
                    <br/>
                    <div className="card" style={{marginTop: 20}}>
                        <ul className="list-group list-group-flush">
                            {this.state.pendingCourses.map((course) => {
                                return <li className="list-group-item" key={course.id}>
                                    <div className="row">
                                        <div className="col-md-3">
                                            <h3>{course.student_id}</h3>
                                        </div>
                                        <div className="col-md-9">
                                            <button className="btn btn-primary" data-toggle="modal"
                                                    data-target="#reviewRegistrationModal"
                                                    onClick={() => {
                                                        this.setState({student_id: course.student_id});
                                                        this.student_id = course.student_id;
                                                        this.getRegistrationDetails();
                                                    }}>
                                                See Details
                                            </button>
                                        </div>
                                    </div>
                                </li>
                            })}
                        </ul>
                    </div>
                </div>
            </div>
        )
    }
}