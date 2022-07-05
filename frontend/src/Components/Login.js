import React, { useState } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router";

import * as actionCreators from "../store/actions/actionCreators";

import logo from "../logo.png";
import classes from "./Main.module.css";

function Login(props) {
    // const [user] = useAuthState(auth);
    document.title = "Login to Healthcare | Hospital Management System ";
    console.log("Login", props);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    // const [authError, setAuthErrorState] = useState("");
    // const [authSuccess, setAuthSuccessState] = useState("");

    // if (auth.currentUser) {
    //     return <Redirect to="/" />;
    // }
    const login = () => {
        let isValid = true;

        props.setAuthError("");

        if (username === "") {
            props.setAuthError("All fields are required!");
            isValid = false;
        }
        if (password === "") {
            props.setAuthError("All fields are required!");
            isValid = false;
        }

        if (isValid) props.login(username, password);
    };

    // if (props.userId === null) {
    //     return <Redirect to="/login" />;
    // }
    return (
        <div className={[classes.homepage, classes.centerHome].join(" ")}>
            <div className={classes.authBox}>
                <div className={classes.brandBox}>
                    <img className={classes.brandLogo} src={logo} alt="title" />
                    <div className={classes.brandName}>
                        Login to HealthCare&trade;
                    </div>
                </div>
                <form
                    className={classes.formBox}
                    onSubmit={(e) => {
                        e.preventDefault();
                        login();
                    }}
                >
                    <div
                        className={[
                            classes.smallHeadEntry,
                            username ? classes.show : classes.hide,
                        ].join(" ")}
                    >
                        Username :{" "}
                    </div>
                    <input
                        className={classes.authEntry}
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                    <div
                        className={[
                            classes.smallHeadEntry,
                            password ? classes.show : classes.hide,
                        ].join(" ")}
                    >
                        Password :{" "}
                    </div>
                    <input
                        className={classes.authEntry}
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <div className={classes.authError}>{props.errorMsg}</div>
                    {/* <div className={classes.authSuccess}>{authSuccess}</div> */}
                    <input
                        className={[
                            classes.button,
                            classes.hollow,
                            classes.authSubmit,
                        ].join(" ")}
                        type="submit"
                        value="Login"
                    />
                </form>
            </div>
        </div>
    );
}

const mapStateToProps = (state) => {
    return {
        userId: state.userId,
        errorMsg: state.authError,
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        login: (uname, pass) => dispatch(actionCreators.login(uname, pass)),
        setAuthError: (message) =>
            dispatch(actionCreators.setAuthError(message)),
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(Login);
