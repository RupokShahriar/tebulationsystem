import React, {Component} from "react"

import TopBar from "./TopBar"
import UserService from "../services/User";


export default class Home extends Component {

    constructor(props) {
        super(props);

        this.loadUserDataOrRedirect = this.loadUserDataOrRedirect.bind(this);
        this.userService = new UserService();
    }

    componentWillMount() {
        document.title = "Tabulation System KU";
        this.loadUserDataOrRedirect()
    }

    loadUserDataOrRedirect() {
        const user = this.userService.getUser();
        if (!user) {
            this.props.history.push("/login");
        }
    }

    render() {
        return (
            <div>
                <TopBar/>
                <h1 className="text text-center text-info" style={{paddingTop: "20px"}}>Welcome to Khulna University
                    Tabulation System</h1>

                <div>
                    <div id="carouselControls" className="carousel slide" data-ride="carousel">
                        <div className="carousel-inner">
                            <div className="carousel-item active">
                                <img className="d-block w-100" src={require("../images/carousel1.jpg")}
                                     alt="First slide" height="800px" width="800px"/>
                            </div>
                        </div>
                        <a className="carousel-control-prev" href="#carouselControls" role="button"
                           data-slide="prev">
                            <span className="carousel-control-prev-icon" aria-hidden="true"></span>
                            <span className="sr-only">Previous</span>
                        </a>
                        <a className="carousel-control-next" href="#carouselControls" role="button"
                           data-slide="next">
                            <span className="carousel-control-next-icon" aria-hidden="true"></span>
                            <span className="sr-only">Next</span>
                        </a>
                    </div>
                </div>

            </div>

        )
    }

}