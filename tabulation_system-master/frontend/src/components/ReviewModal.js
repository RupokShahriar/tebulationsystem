import React, {Component} from "react";

import APICalls from "../services/APICalls";

export default class ReviewModal extends Component {
    constructor(props) {
        super(props);
        this.state = {
            courses: [],
            rejection_cause: "",
            reject: false,
        };

        this.apiCalls = new APICalls();

        this.confirmReview = this.confirmReview.bind(this);
        this.reject = this.reject.bind(this);
        this.rejection_field = this.rejection_field.bind(this);
        this.check_all_function = this.check_all_function.bind(this);

    }

    rejection_field() {
        // if (1) {
        //     return (
        //         <textarea className="form-control" rows="3"
        //                   placeholder={"Write cause of rejection (in case of rejection)"}
        //                   onChange={(e) => this.setState({rejection_cause: e.target.value})}/>
        //     )
        //
        // }
    }

    async confirmReview() {
        //const response = await this.apiCalls.allow(this.props.session, this.props.year, this.props.term, this.props.batch, this.props.student_id)
        //console.log(response);

        let all_checkboxes = document.getElementsByClassName("checkbox");
        let allowed_courses=[],rejected_courses=[];

        for (let i=0;i<all_checkboxes.length;i++)
        {
            let checkbox = all_checkboxes[i];
            let td1 = checkbox.parentNode.parentNode.childNodes[0];

            if (td1.childNodes[0].checked)
            {
                allowed_courses.push(checkbox.parentNode.parentNode.childNodes[1].innerText);
            }
            else
            {
                rejected_courses.push(checkbox.parentNode.parentNode.childNodes[1].innerText);
            }
        }
        const response = await this.apiCalls.allow(this.props.session, this.props.year, this.props.term,this.props.batch,this.props.student_id,

            allowed_courses,rejected_courses);
        console.log(response);

    }

    async reject() {
        let cause = this.state.rejection_cause;
        cause = cause.split(" ").join("");
        if (cause.length === 0) {
            alert("Cause of rejection cannot be blank");
            return;
        }
        console.log(this.props);
        const response = await this.apiCalls.reject(
            this.props.session, this.props.year, this.props.term, this.props.batch, this.props.student_id, this.state.rejection_cause);

        console.log(response);
    }

    check_all_function(e)
    {
        let value = e.target.checked;
        console.log(value);
        let all_checkboxes = document.getElementsByClassName("checkbox");
        console.log(all_checkboxes,typeof all_checkboxes);
        for(let i=0;i<all_checkboxes.length;i++)
        {
            all_checkboxes[i].checked = true?value:false;
        }

    }

    render() {

        return (
            <div className="modal fade" id="reviewRegistrationModal" tabIndex="-1" role="dialog"
                 aria-labelledby="reviewRegistrationModalLabel" aria-hidden="true">
                <div className="modal-dialog modal-lg" role="document">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h5 className="modal-title" id="reviewRegistrationModalLabel">Requested Coursed</h5>
                            <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div className="modal-body">
                            <div className="card">
                                <div className="card-body">
                                    <table className="table table-striped table-bordered">
                                        <tbody>
                                        <tr>
                                            <td><input type="checkbox"  value="" onChange={this.check_all_function}/></td>
                                            <th>Course No.</th>
                                            <th>Course Title</th>
                                            <th>Credit Hours</th>
                                            <th>Comment</th>
                                        </tr>
                                        {this.props.courses.map((course) => {
                                            return <tr key={course[0]}>
                                                <td><input type="checkbox" className="checkbox" value=""/></td>
                                                <td>{course[0]}</td>
                                                <td>{course[1]}</td>
                                                <td>{course[2]}</td>
                                                <td>{course[3]}</td>
                                            </tr>
                                        })}
                                        </tbody>

                                    </table>
                                </div>
                            </div>
                            {this.rejection_field()}
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-secondary" data-dismiss="modal">Close</button>
                            {/*<button type="button" className="btn btn-danger" data-dismiss="modal"*/}
                                    {/*onClick={() => this.reject()}>Reject*/}
                            {/*</button>*/}
                            <button type="button" className="btn btn-primary" data-dismiss="modal" onClick={this.confirmReview}>Confirm</button>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}