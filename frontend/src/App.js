import React, { useEffect } from "react";
import { Switch, Route, Redirect } from "react-router-dom";
import { connect } from "react-redux";

import * as actionCreators from "./store/actions/actionCreators";

import classes from "./App.module.css";
import Errorshow from "./Components/Errorshow";
import SuccessShow from "./Components/SuccessShow";
import Header from "./Components/Header";
import MainPart from "./Components/MainPart";

class App extends React.Component {
    constructor(props) {
        super(props);
    }

    componentDidMount() {
        document.title = `Welcome to Healthcare | Hospital Management System `;
        try {
            console.log("Trying", localStorage.getItem("authToken"));
            if (JSON.parse(localStorage.getItem("authToken"))) {
                this.props.autoLogin();
            }
        } catch {
            console.log("No need of logging in automatically");
        }
        console.log("App rendering");
    }
    render() {
        return (
            <div className={classes.App}>
                <Header />
                <Errorshow />
                <SuccessShow />
                <MainPart />
            </div>
        );
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        autoLogin: () => dispatch(actionCreators.autoLogin()),
    };
};

export default connect(null, mapDispatchToProps)(App);
