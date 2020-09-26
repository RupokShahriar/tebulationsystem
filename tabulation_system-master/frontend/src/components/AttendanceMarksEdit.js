import React, {Component} from "react";


import ApiCalls from "../services/APICalls";
import TopBar from "./TopBar";
import EditSpreadSheet from "./EditSpreadSheet";
import YearTermSessionBatchComponent from "../components/YearTermSessionBatchComponent";
//import SpreadSheet from "./SpreadSheet";

export default class AttendanceMarksEdit extends Component {

    constructor(props) {
        super(props);
        this.state = {
            section: "A",
            courseList: [],
            course_number: '',
            students: [],
        };
        this.apiCalls = new ApiCalls();


        this.load = this.load.bind(this);
        this.get_student_list = this.get_student_list.bind(this);
        this.input_marks = this.input_marks.bind(this);


        this.session = "";
        this.year = "";
        this.term = "";
        this.batch = "";
    }
    componentWillMount() {
        document.title = "Attendance Marks Edit";
    }

    async input_marks(marks) {

        const response = await this.apiCalls.update_attendance_marks(this.session, this.year, this.term,
            this.batch, this.state.course_number, this.state.section, marks);

        console.log(response);

        if (response.status) {
            alert("Successfully Marks edited");
            window.location.reload();
        }
    }

    async load(session, year, term, batch) {

        this.session = session;
        this.year = year;
        this.term = term;
        this.batch = batch;
        this.setState({courseList: []});

        const response = await this.apiCalls.get_course_response(session, year, term);

        if (response.data.status) {
            if (response.data.data.length > 0) {
                this.setState({course_number: response.data.data[0].course_data.course_number});
            }
            // eslint-disable-next-line
            response.data.data.map((course) => {
                this.setState({courseList: [...this.state.courseList, course]});
            });

        }
        console.log(this.state.courseList);
    }

    async get_student_list() {
        this.setState(({students: []}));
        const response = await this.apiCalls.get_attendance_marks_for_edit(this.session, this.year, this.term, this.batch,
            this.state.course_number, this.state.section);

        const students = response.data.data;
        console.log(students);
        this.setState({students: students});

    }

    render() {
        return (
            <div>
                <TopBar/>
                <YearTermSessionBatchComponent load={this.load}/>
                <div className="container">
                    <div className="row">
                        <div className="col-md-2">
                            Select Course :
                        </div>
                        <div className="col-md-4">
                            <select className="form-control" onChange={(e) => {
                                this.setState({course_number: e.target.value})
                            }}>
                                {this.state.courseList.map((course) => {
                                    return <option key={course.course_data.course_title}
                                                   value={course.course_data.course_number}>
                                        {course.course_data.course_number} : {course.course_data.course_title}</option>
                                })}
                            </select>
                        </div>
                        <div className="col-md-6">
                            <div className="row">
                                <div className="col-md-4">
                                    Select Section :
                                </div>
                                <div className="col-md-8">
                                    <select className="form-control" value={this.state.section}
                                            onChange={(e) => this.setState({section: e.target.value})}>
                                        <option value="A">A</option>
                                        <option value="B">B</option>
                                        <option value="Both">Both (Sum of A and B sections)</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                    <br/>

                    <div className="row">
                        <div className="col-md-6"><button className="btn btn-primary" onClick={this.get_student_list}>Get Registered
                                Students
                            </button>

                        </div>

                    </div>
                </div>
                <br/>
                <EditSpreadSheet type="theory" input_marks={this.input_marks} students={this.state.students}
                             courseLise={this.state.courseList} highest={10}/>

            </div>
        )
    }
}