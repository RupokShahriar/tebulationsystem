import React, {Component} from "react";
import TopBar from "./TopBar";
import UserService from "../services/User";


export default class MyInfo extends Component {
    constructor(props) {
        super(props);
        this.userService = new UserService();

        this.user = this.userService.getUser().data;
        this.get_teacher_info = this.get_teacher_info.bind(this);
        this.get_student_info = this.get_student_info.bind(this);
    }

    componentWillMount() {
    document.title="My Info"
    }
    get_teacher_info()
    {
        return (
            <div>
                <div className="row">
                        <div className="col-md-4">
                            <h2>Email : </h2>
                        </div>
                        <div className="col-md-8">
                            <h2>{this.user.email}</h2>
                        </div>
                    </div>

                     <div className="row">
                        <div className="col-md-4">
                            <h2>Designation : </h2>
                        </div>
                        <div className="col-md-8">
                            <h2>{this.user.designation}</h2>
                        </div>
                    </div>

                <div className="row">
                        <div className="col-md-4">
                            <h2>Contact Number : </h2>
                        </div>
                        <div className="col-md-8">
                            <h2>{this.user.contact_number}</h2>
                        </div>
                    </div>

                    <div className="row">
                        <div className="col-md-4">
                            <h2>Discipline : </h2>
                        </div>
                        <div className="col-md-8">
                            <h2>{this.user.discipline.name}</h2>
                        </div>
                    </div>

                    <div className="row">
                        <div className="col-md-4">
                            <h2>Discipline Code : </h2>
                        </div>
                        <div className="col-md-8">
                            <h2>{this.user.discipline.code_number}</h2>
                        </div>
                    </div>

                    <div className="row">
                        <div className="col-md-4">
                            <h2>School : </h2>
                        </div>
                        <div className="col-md-8">
                            <h2>{this.user.discipline.school}</h2>
                        </div>
                    </div>
            </div>
        )
    }
    get_student_info()
    {
        return (
            <div>
                <div className="row">
                        <div className="col-md-4">
                            <h2>Student ID : </h2>
                        </div>
                        <div className="col-md-8">
                            <h2>{this.user.student_id}</h2>
                        </div>
                    </div>

                <div className="row">
                        <div className="col-md-4">
                            <h2>Contact Number : </h2>
                        </div>
                        <div className="col-md-8">
                            <h2>{this.user.contact_number}</h2>
                        </div>
                    </div>

                    <div className="row">
                        <div className="col-md-4">
                            <h2>Discipline : </h2>
                        </div>
                        <div className="col-md-8">
                            <h2>{this.user.discipline.name}</h2>
                        </div>
                    </div>

                    <div className="row">
                        <div className="col-md-4">
                            <h2>Discipline Code : </h2>
                        </div>
                        <div className="col-md-8">
                            <h2>{this.user.discipline.code_number}</h2>
                        </div>
                    </div>

                    <div className="row">
                        <div className="col-md-4">
                            <h2>School : </h2>
                        </div>
                        <div className="col-md-8">
                            <h2>{this.user.discipline.school}</h2>
                        </div>
                    </div>
            </div>
        )
    }

    render() {
        return (
            <div>
                <TopBar/>
                <br/>
                <div className="container">
                    <div className="row">
                        <div className="col-md-4">
                            <h2>Name : </h2>
                        </div>
                        <div className="col-md-8">
                            <h2>{this.user.name}</h2>
                        </div>
                    </div>

                    {
                     this.user.student_id?this.get_student_info(): this.get_teacher_info()
                    }


                    
                </div>
            </div>
        )
    }
}