import React, {Component} from "react";


import ApiCalls from "../services/APICalls";
import TopBar from "./TopBar";
//import SpreadSheet from "./SpreadSheet";
import YearTermSessionBatchComponent from "../components/YearTermSessionBatchComponent";

export default class ShowTermWiseResultsTeacher extends Component {

    constructor(props) {
        super(props);
        this.state = {
            course_number: '',

            courseList: [],
            results: [],
        };
        this.apiCalls = new ApiCalls();


        this.load = this.load.bind(this);
        this.get_result = this.get_result.bind(this);


        this.course_type = 1;
        this.session = "";
        this.year = "";
        this.term = "";
        this.batch = "";
    }

    componentWillMount() {
        document.title = "Result";
    }

    async get_result() {
        this.setState({results: []});

        const response = await this.apiCalls.get_term_wise_result(this.session, this.year, this.term, this.batch, this.state.course_number);

        if (response.data.status) {
            const results = response.data.result;
            console.log(results);
            this.setState({results})
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

    }


    showResults() {
        if (this.state.results.length > 0) {
            if (this.state.results[0][3]) {
                return <table className="table table-striped">
                    <tbody>
                    <tr>
                        <th>Student ID</th>
                        <th>Attendance</th>
                        <th>Class Test</th>
                        <th>Section A</th>
                        <th>Section B</th>
                        <th>Letter Grade</th>
                        <th>Grade point</th>
                        <th>Comment</th>
                    </tr>
                    {this.state.results.map((result, index) => {
                        return <tr key={index}>
                            <td>{result[0]}</td>
                            <td>{result[2]}</td>
                            <td>{result[3]}</td>
                            <td>{result[4]}</td>
                            <td>{result[5]}</td>
                            <td>{result[1][0]}</td>
                            <td>{result[1][1]}</td>
                            <td>{result[6] === true ? "Retake" : ""}</td>

                        </tr>
                    })}
                    </tbody>
                </table>
            } else {
                return <table className="table table-striped">
                    <tbody>
                    <tr>
                        <th>Student ID</th>
                        <th>Attendance</th>
                        <th>Sessional Assessment</th>
                        <th>Viva</th>
                        <th>Letter Grade</th>
                        <th>Grade point</th>
                        <th>Comment</th>
                    </tr>
                    {this.state.results.map((result, index) => {
                        return <tr key={index}>
                            <td>{result[0]}</td>
                            <td>{result[2]}</td>
                            <td>{result[4]}</td>
                            <td>{result[5]}</td>
                            <td>{result[1][0]}</td>
                            <td>{result[1][1]}</td>
                            <td>{result[6] === true ? "Retake" : ""}</td>

                        </tr>
                    })}
                    </tbody>
                </table>
            }
        } else if (this.state.searched) {
            return (
                <div>
                    <br/>
                    <h2>No class test marks available for this term.</h2>
                </div>)
        }
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
                                this.setState({course_number: e.target.value, results: []});
                            }}>
                                {this.state.courseList.map((course) => {
                                    return <option key={course.course_data.course_title}
                                                   value={course.course_data.course_number}>
                                        {course.course_data.course_number} : {course.course_data.course_title}</option>
                                })}
                            </select>
                        </div>
                        <div className="col-md-2">
                            <button className="btn btn-primary" onClick={this.get_result}>Get Result</button>
                        </div>

                    </div>
                    <br/>
                    {this.showResults()}
                    <br/>
                </div>
                <br/>

            </div>
        )
    }
}