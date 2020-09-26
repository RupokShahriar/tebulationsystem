import React, {Component} from "react";


import ApiCalls from "../services/APICalls";
import TopBar from "./TopBar";
import UserService from "../services/User";
//import SpreadSheet from "./SpreadSheet";
//import YearTermSessionBatchComponent from "../components/YearTermSessionBatchComponent";

export default class ShowStudentWiseResults extends Component {

    constructor(props) {
        super(props);
        this.state = {
            student_id: '',
            results: [],
        };
        this.apiCalls = new ApiCalls();
        this.userService = new UserService();
        this.user = this.userService.getUser().data;


        this.get_result = this.get_result.bind(this);
        this.showResults = this.showResults.bind(this);
        this.get_option = this.get_option.bind(this);

    }

    componentWillMount() {
        document.title = "Result";

        if (this.user.student_id) {
            this.get_result();
        }
    }

    async get_result() {

        if (this.user.student_id) {
            const response = await this.apiCalls.get_student_wise_result(this.user.student_id);
            if (response.data.status) {
                const results = response.data.results;
                console.log(results);
                this.setState({results});
                console.log(this.state.results);
            }
        } else {
            const response = await this.apiCalls.get_student_wise_result(this.state.student_id);

            if (response.data.status) {
                const results = response.data.results;
                console.log(results);
                this.setState({results});
                console.log(this.state.results);
            }
        }
    }


    showResults() {
        if (this.state.results.length > 0) {
            return <div>
                {this.state.results.map((result, index) => {
                    return (
                        <div className="card" key={index}>
                            <div className="card-header">
                                Session : {result[0][0]} Year: {result[0][1]} Term:{result[0][2]} (CGPA:{result[2]})
                            </div>
                            <div className="card-body">
                                <table className="table table-striped">
                                    <thead>
                                    <tr>
                                        <th>Course Number</th>
                                        <th>Course Title</th>
                                        <th>Registered Credit Hour</th>
                                        <th>Letter Grade</th>
                                        <th>Grade point (GP)</th>
                                        <th>Earned Credit Hours (CH)</th>
                                        <th>Earned Credit Points (GP*CH)</th>
                                        <th>Remarks</th>

                                    </tr>
                                    </thead>
                                    <tbody>
                                    {
                                        result[1].length > 0 ?
                                            result[1].map((single_result, index) => {
                                                return (
                                                    <tr key={index}>
                                                        <td>{single_result[0]}</td>
                                                        <td>{single_result[1]}</td>
                                                        <td>{single_result[5]}</td>
                                                        <td>{single_result[2][0]}</td>
                                                        <td>{single_result[2][1]}</td>
                                                        <th>{single_result[3]}</th>
                                                        <th>{single_result[3] * single_result[2][1]}</th>
                                                        <th>{single_result[4] === true ? "Retake" : ""}</th>

                                                    </tr>
                                                )

                                            }) : <tr>
                                                <td>No result available for this term.</td>
                                            </tr>
                                    }
                                    {result[1].length > 0 ?

                                        <tr key={index}>
                                            <td></td>
                                           <td>Total</td>
                                            <td>{result[3]}</td>
                                            <td></td>
                                            <td></td>
                                            <td>{result[4]}</td>
                                            <td>{result[5]}</td>
                                            <td></td>


                                        </tr> : <tr></tr>
                                    }


                                    </tbody>
                                </table>



                            </div>
                        </div>)
                })
                }
            </div>

        }

    }

    get_option() {
        if (!this.user.student_id) {
            return (
                <div className="row">
                    <div className="col-md-2">
                        Student ID :
                    </div>
                    <div className="col-md-4">
                        <input className="form-control" value={this.state.student_id} placeholder="Enter Student ID"
                               onChange={(e) => {
                                   this.setState({student_id: e.target.value})
                               }}/>
                    </div>
                    <div className="col-md-2">
                        <button className="btn btn-primary" onClick={this.get_result}>Get Result</button>
                    </div>

                </div>
            )
        }

    }


    render() {
        return (
            <div>
                <TopBar/>
                <br/>
                {/*<YearTermSessionBatchComponent load={this.load}/>*/}
                <div className="container">
                    {!this.user.student_id ? this.get_option() :
                        ""}
                    <br/>
                    {this.showResults()}
                    <br/>
                </div>
                <br/>

            </div>
        )
    }
}