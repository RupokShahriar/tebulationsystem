import React, {Component} from "react";


import ApiCalls from "../services/APICalls";
import TopBar from "./TopBar";
//import SpreadSheet from "./SpreadSheet";
import YearTermSessionBatchComponent from "../components/YearTermSessionBatchComponent";

export default class ShowAttendancetMarks extends Component {

    constructor(props) {
        super(props);
        this.state = {
            marks: [],
            searched: false,
        };

        this.apiCalls = new ApiCalls();

        this.session = "";
        this.year = "";
        this.term = "";
        this.batch = "";

        this.load = this.load.bind(this);
        this.getAttendanceMarks = this.getAttendanceMarks.bind(this);
    }
      componentWillMount() {
        document.title = "Show Attendance Marks";
    }

    async load(session, year, term, batch) {
        this.session = session;
        this.year = year;
        this.term = term;
        this.batch = batch;

        const response = await this.apiCalls.get_all_attendance_marks(session, year, term, batch);
        console.log(response);

        const data = response.data.data;
        this.setState({marks: []});
        // eslint-disable-next-line
        data.map((course) => {
            this.setState({marks: [...this.state.marks, course]});
        });
        this.setState({searched: true});
    }

    getAttendanceMarks() {
        if (this.state.marks.length > 0 && this.state.searched) {
            return <table className="table table-dark table-striped">
                <tbody>
                <tr>
                    <th>Course Number</th>
                    <th>Course Title</th>
                    <th>Section</th>
                    <th>Obtained Marks</th>
                </tr>
                {this.state.marks.map((mark,index) => {
                    return <tr key={index}>
                        <td>{mark[0]}</td>
                        <td>{mark[1]}</td>
                        <td>{mark[2]}</td>
                        <td>{mark[3]}</td>

                    </tr>
                })}
                </tbody>
            </table>
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
                    <br/>
                    {this.getAttendanceMarks()}
                </div>
            </div>
        )
    }
}