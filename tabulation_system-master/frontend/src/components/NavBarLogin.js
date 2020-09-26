import React, {Component} from "react";

export default class NavBarLogin extends Component{

    render()
    {
        return(
           <nav className="navbar navbar-expand-lg  navbar-dark bg-dark">
                <a className="navbar-brand" href="/">Khulna University Tabulation System</a>
                <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown"
                        aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
            </nav>
        )
    }
}