import React, {Component} from "react";


import APICalls from "../services/APICalls";
import marks_validation from "../services/Validation";

export default class EditSpreadSheet extends Component {

    constructor(props) {
        super(props);

        this.apiCalls = new APICalls();
        this.get_spreadsheet = this.get_spreadsheet.bind(this);
        this.submit_marks = this.submit_marks.bind(this);
    }

    submit_marks() {
        let marks = [];
        let validation_marks_list = [];

        // eslint-disable-next-line
        this.props.students.map((course) => {
            const mark = document.getElementsByName(course.course_registration.student.student_id)[0].value;
            marks.push([course.course_registration.student.student_id, mark]);
            validation_marks_list.push(mark ? mark : 0);
        });

         if (marks_validation(0, this.props.highest ? this.props.highest : 30, validation_marks_list)) {
             this.props.input_marks(marks);
         }
    }

    get_spreadsheet() {
        let spreadsheet_array = [];

        spreadsheet_array.push(<div className="row" key="student_id">
            <div className='col-md-4'></div>
            <div className='col-md-2'>
                <label>Student ID</label>
            </div>
            <div className="col-md-2">
                <label>Obtained Marks</label>
            </div>
            <div className="col-md-4"></div>
        </div>);

// eslint-disable-next-line
        this.props.students.map((course, index) => {


            spreadsheet_array.push(<div className="row" key={index}>
                <div className='col-md-4'></div>
                <div className='col-md-2'>
                    <label>{course.course_registration.student.student_id}</label>
                </div>
                <div className="col-md-2">
                    <input type="number" defaultValue={course.obtained_marks} className="form-control"
                           name={course.course_registration.student.student_id}/>
                </div>
                <div className="col-md-4"></div>
            </div>);
        });
        return spreadsheet_array;
    }

    render() {
        return (
            <div className="container">
                {this.get_spreadsheet()}
                <br/>
                <button className="btn btn-primary" onClick={this.submit_marks}>Update Marks</button>
            </div>
        )
    }
}