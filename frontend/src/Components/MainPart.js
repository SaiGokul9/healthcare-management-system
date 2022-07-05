import React, { useEffect } from "react";
import { Switch, Route, Redirect } from "react-router-dom";
import { connect } from "react-redux";

import * as actionCreators from "../store/actions/actionCreators";

import Session from "./ViewSession";
import Sessions from "./Sessions";
import Header from "./Header";
import Login from "./Login";
import Register from "./Register";
import AddSession from "./AddSession";

import classes from "../App.module.css";
import ViewAppointment from "./ViewAppointment";
import Logout from "./Logout";

class MainPart extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        let data = this.props.usertype;
        if (this.props.usertype === "staff") {
            data = (
                <Switch>
                    <Route path="/logout">
                        <Logout />
                    </Route>
                    <Route path="/register">
                        <Register />
                    </Route>
                    <Route path="/sessions">
                        <Sessions />
                    </Route>
                    <Route path="/session/add" exact>
                        <AddSession />
                    </Route>
                    <Route path="/session/:id">
                        <Session />
                    </Route>
                    <Route path="/appointment/:id">
                        <ViewAppointment />
                    </Route>
                    <Redirect from="/" to="/sessions" />
                </Switch>
            );
        } else if (this.props.usertype === "doctor") {
            data = (
                <Switch>
                    <Route path="/logout">
                        <Logout />
                    </Route>
                    <Route path="/sessions">
                        <Sessions />
                    </Route>
                    <Route path="/session/:id">
                        <Session />
                    </Route>
                    <Route path="/appointment/:id">
                        <ViewAppointment />
                    </Route>
                    <Redirect from="/" to="/sessions" />
                </Switch>
            );
        } else if (this.props.usertype === "patient") {
            data = (
                <Switch>
                    <Route path="/logout">
                        <Logout />
                    </Route>
                    <Route path="/sessions">
                        <Sessions />
                    </Route>
                    <Route path="/session/:id">
                        <Session />
                    </Route>
                    <Route path="/appointment/:id">
                        <ViewAppointment />
                    </Route>
                    <Redirect from="/" to="/sessions" />
                </Switch>
            );
        } 
        return (
            <div>
                {this.props.usertype !== null ? (
                    data
                ) : (
                    <Switch>
                        <Route path="/login" exact component={Login} />
                        <Route path="/register" exact component={Register} />
                        <Redirect from="/" to="/login" />
                    </Switch>
                )}
            </div>
        );
    }
}

const mapStateToProps = (state) => {
    return {
        usertype: state.userType,
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        // getdata: () => dispatch(actionCreators.getData()),
        autoLogin: () => dispatch(actionCreators.autoLogin()),
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(MainPart);
