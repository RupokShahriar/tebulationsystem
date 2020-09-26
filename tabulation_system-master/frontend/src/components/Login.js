import React, {Component} from "react";
import axios from "axios";

import NavBarLogin from "./NavBarLogin";
import AppConfig from "../config/AppConfig";
import UserService from "../services/User";


export default class Login extends Component {

    constructor(props) {
        super(props);
        this.state = {
            mode: "student",
            student_id: "",
            student_password: "",
            teacher_password: "",
            email: "",
        };

        this.userService = new UserService();
        this.studentLogin = this.studentLogin.bind(this);
        this.teacherLogin = this.teacherLogin.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.loadUserDataOrRedirect = this.loadUserDataOrRedirect.bind(this);
    }

    componentWillMount() {
        document.title = "Login";
        this.loadUserDataOrRedirect();
    }

    async loadUserDataOrRedirect() {
        const user = await this.userService.getUser();
        if (user) {
            this.props.history.push("/");
        }
    }

    handleChange(e) {
        this.setState({[e.target.name]: e.target.value});
    }

    async handleSubmit(e) {
        e.preventDefault();

        console.log(this.state);

        const {loginURL} = AppConfig;
        console.log(loginURL);
        const response = await axios({
            method: "POST",
            url: loginURL,
            data: {
                mode: this.state.mode,
                student_id: this.state.student_id,
                email: this.state.email,
                student_password: this.state.student_password,
                teacher_password: this.state.teacher_password
            }
        });
        console.log(response.data);
        if (response.data.status) {

            this.userService.storeUser(response.data);
            console.log(response);
            this.props.history.push("/");
        } else {
            alert("Something went wrong. Please try again later");
        }

    }

    studentLogin() {
        return (
            <div className="form-group" style={{paddingTop: 20, paddingLeft: 30, paddingRight: 30}}>

                <div>
                    <label htmlFor="student_id">Student ID</label>
                    <input type="student_id" className="form-control" id="student_id" name="student_id"
                           placeholder="Enter Student ID" value={this.state.student_id} onChange={this.handleChange}/>
                </div>
                <br/>
                <div className="form-group">
                    <label htmlFor="student_password">Password</label>
                    <input type="password" className="form-control" id="student_password" name="student_password"
                           placeholder="Enter Password"
                           value={this.state.student_password} onChange={this.handleChange}/>
                </div>
            </div>

        )
    }

    teacherLogin() {
        return (
            <div className="form-group" style={{paddingTop: 20, paddingLeft: 30, paddingRight: 30}}>
                <div>
                    <div className="form-group">
                        <label htmlFor="email">Username</label>
                        <input type="email" className="form-control" id="email" name="email"
                               placeholder="Enter Your email" value={this.state.email}
                        onChange={this.handleChange}/>
                    </div>
                    <div className="form-group">
                        <label htmlFor="teacher_password">Password</label>
                        <input type="password" className="form-control" id="teacher_password"
                               name="teacher_password"
                               placeholder="Enter password" value={this.state.teacher_password}
                        onChange={this.handleChange}/>
                    </div>
                </div>
            </div>
        )
    }

    render() {
        return (
            <div>
                <NavBarLogin/>
                <div className="container">
                    <div style={{paddingLeft: 20, paddingTop: 20}}>
                        <div className="row">
                            <div className="col-md-2">
                                <h3>Login As :</h3>
                            </div>
                            <div className="col-md-3">
                                <select className="form-control" value={this.state.mode}
                                        onChange={(e) => (this.setState({mode: e.target.value}))}>
                                    <option value="student">Student</option>
                                    <option value="teacher">Teacher</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    {this.state.mode === "student" ? this.studentLogin() : this.teacherLogin()}
                    <button type="button" className="btn btn-primary" style={{marginLeft: 25}}
                            onClick={this.handleSubmit}>Submit
                    </button>
                </div>
            </div>
        )
    }
}