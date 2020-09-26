import React, {Component} from "react";
import APICalls from "../services/APICalls";

export default class YearTermSessionBatchComponent extends Component {

    constructor(props) {
        super(props);
        this.state = {
            session: "",
            year: "",
            term: "",
            batch: "",

            sessions: [],
            years: [],
            terms: [],
            batches: []
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.load_data = this.load_data.bind(this);

        this.apiCalls = new APICalls();
    }

    componentWillMount() {
        this.load_data();
    }

    async load_data() {
        const response = await this.apiCalls.get_sessions_years_terms_batches();
        const data = response.data;

        const sessions = data.sessions;
        const years = data.years;
        const terms = data.terms;
        const batches = data.batches;

        this.setState({sessions, years, terms, batches});

    }

    handleChange(event) {
        this.setState({[event.target.name]: event.target.value});

    }

    handleSubmit() {
        this.props.load(this.state.session, this.state.year, this.state.term, this.state.batch);
    }


    render() {
        return (
            <div style={{paddingTop: '20px'}}>

                <div className={"row container justify-content-md-center"} style={{"margin": "0 auto"}}>
                    <div className={"col-md-3"}>
                        <div className="row">
                            <div className="col-md-4">
                                <label id="year-label">Session</label>
                            </div>
                            <div className="col-md-8">
                                <select id="session" name="session"
                                        className="form-control" value={this.state.session}
                                        onChange={this.handleChange}>
                                    <option value={""}>(Select Session)</option>
                                    {
                                        this.state.sessions.map((session) => {
                                            return <option key={session} value={session}>{session}</option>
                                        })
                                    }

                                    {/*<option value="2017-2018">2017-2018</option>*/}
                                </select>

                            </div>
                        </div>
                    </div>
                    <div className={"col-md-2 "}>
                        <div className="row">
                            <div className="col-md-4">
                                <label id="year-label" style={{paddingTop: "3px"}}>Year</label>
                            </div>
                            <div className="col-md-8"><select id="year" name="year" aria-labelledby="year-label"
                                                              className="form-control" value={this.state.year}
                                                              onChange={this.handleChange}>
                                <option value={""}>(Select Year)</option>

                                {
                                    this.state.years.map((year) => {
                                        return <option key={year} value={year}>{year}</option>
                                    })
                                }
                            </select>
                            </div>
                        </div>
                    </div>
                    <div className={"col-md-2"}>
                        <div className="row">
                            <div className="col-md-4">
                                <label id="year-label" style={{paddingTop: "3px"}}>Term</label>
                            </div>
                            <div className="col-md-8"><select id="term" name="term" aria-labelledby="term-label"
                                                              className="form-control" value={this.state.term}
                                                              onChange={this.handleChange}>
                                <option value={""}>(Select Term)</option>
                                {
                                    this.state.terms.map((term) => {
                                        return <option key={term} value={term}>{term}</option>
                                    })
                                }
                            </select>
                            </div>
                        </div>
                    </div>
                    <div className={"col-md-3"}>
                        <div className="row">
                            <div className="col-md-6">
                                <label id="batch-label" style={{paddingTop: "3px"}}>Registration With Batch</label>
                            </div>
                            <div className="col-md-6"><select id="batch" name={"batch"} aria-labelledby="batch-label"
                                                              className="form-control" value={this.state.batch}
                                                              onChange={this.handleChange}>
                                <option value={""}>(Select Batch)</option>
                                {
                                    this.state.batches.map((batch) => {
                                        return <option key={batch} value={batch}>{batch}</option>
                                    })
                                }


                            </select>
                            </div>
                        </div>
                    </div>

                    <div className={"col-md-2"}>
                        <button className="btn btn-primary" type="button"
                                onClick={this.handleSubmit}>
                            SEARCH
                        </button>

                    </div>
                </div>
            </div>
        )
    }
}