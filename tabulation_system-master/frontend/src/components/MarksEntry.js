import React, {Component} from "react";


import ApiCalls from "../services/APICalls";
import TopBar from "./TopBar";
import SpreadSheet from "./SpreadSheet";
import YearTermSessionBatchComponent from "../components/YearTermSessionBatchComponent";

export default class MarksEntry extends Component {

    constructor(props) {
        super(props);
        this.state = {
            type: "Semester Final",
            section: "A",
            class_test_no: 1,
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
        document.title = "Marks Entry";
    }

    async input_marks(marks) {

        const response = await this.apiCalls.input_theory_marks(this.session, this.year, this.term,
            this.batch, this.state.course_number, this.state.section, this.state.type, this.state.class_test_no, marks);

        console.log(response);
        if (response.data.status) {
            alert("Marks Entry Operation Successful");
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
        const response = await this.apiCalls.get_registered_students(this.session, this.year, this.term, this.batch,
            this.state.course_number);

        const students = response.data.students;
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
                                {// eslint-disable-next-line
                                this.state.courseList.map((course) => {
                                    
                                        if (course.course_data.course_type === 1) {
                                            return <option key={course.course_data.course_title}
                                                           value={course.course_data.course_number}>
                                                {course.course_data.course_number} : {course.course_data.course_title}</option>
                                        }
                                    
                                })}
                            </select>
                        </div>
                        <div className="col-md-2">
                            <button className="btn btn-primary" onClick={this.get_student_list}>Get Registered
                                Students
                            </button>
                        </div>
                    </div>
                    <br/>


                    <div className="row">
                        <div className="col-md-4">
                            <div className="row">
                                <div className="col-md-6">
                                    Type
                                </div>
                                <div className="col-md-6">

                                    <select className="form-control" value={this.state.type}
                                            onChange={(e) => this.setState({type: e.target.value})}>
                                        <option value="Semester final">
                                            Semester Final
                                        </option>
                                        <option value="Class Test">
                                            Class Test
                                        </option>

                                    </select>
                                </div>
                            </div>
                        </div>

                        {/*{this.state.type == "Semester Final" ?*/}
                            {/*<div className="col-md-4">*/}
                                {/*<div className="row">*/}
                                    {/*<div className="col-md-6">*/}
                                        {/*Select Section :*/}
                                    {/*</div>*/}
                                    {/*<div className="col-md-6">*/}
                                        {/*<select className="form-control" value={this.state.section}*/}
                                                {/*onChange={(e) => this.setState({section: e.target.value})}>*/}
                                            {/*<option value="A">A</option>*/}
                                            {/*<option value="B">B</option>*/}
                                        {/*</select>*/}
                                    {/*</div>*/}
                                {/*</div>*/}
                            {/*</div>*/}
                            {/*: ""*/}
                        {/*}*/}

                        {
                            this.state.type === "Class Test" ?
                                <div className="col-md-4">
                                    <div className="row">
                                        <div className="col-md-6">
                                            Select Class Test No :
                                        </div>
                                        <div className="col-md-6">
                                            <select className="form-control" value={this.state.class_test_no}
                                                    onChange={(e) => this.setState(({class_test_no: e.target.value}))}>
                                                <option value="1">1</option>
                                                <option value="2">2</option>
                                                <option value="3">3</option>
                                                <option value="4">4</option>
                                                <option value="5">5</option>
                                            </select>
                                        </div>
                                    </div>
                                </div> : <div className="col-md-4">
                                    <div className="row">
                                        <div className="col-md-6">
                                            Select Section :
                                        </div>
                                        <div className="col-md-6">
                                            <select className="form-control" value={this.state.section}
                                                    onChange={(e) => this.setState({section: e.target.value})}>
                                                <option value="A">A</option>
                                                <option value="B">B</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                        }
                    </div>
                </div>
                <br/>
                <SpreadSheet type="theory" input_marks={this.input_marks} students={this.state.students}
                             courseLise={this.state.courseList} highest={30} />

            </div>
        )
    }
}