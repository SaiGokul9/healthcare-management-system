import React from "react";
import { NavLink } from "react-router-dom";
import { Switch, Route, Redirect } from "react-router-dom";
import { connect } from "react-redux";

import * as actionCreators from "../store/actions/actionCreators";
import classes1 from "./Header.module.css";
import classes2 from "./Main.module.css";
// import { auth, firestore } from "./Firebase";
// import { useAuthState } from "react-firebase-hooks/auth";

import logo from "../logo.png";
import userImg from "../user.png";
// import { useDocumentDataOnce } from "react-firebase-hooks/firestore";
// import UserDetails from "./UserDetails";

function Header(props) {
    // const [user] = useAuthState(auth);

    let classes = { ...classes1, ...classes2 };

    let data = props.usertype;
    if (props.usertype === "staff") {
        data = (
            <div>
                <NavLink
                    to="/sessions"
                    className={[
                        classes.button,
                        classes.orange,
                        classes.hollow,
                    ].join(" ")}
                >
                    Sessions
                </NavLink>
                <NavLink
                    to="/logout"
                    className={[
                        classes.button,
                        classes.orange,
                        classes.hollow,
                    ].join(" ")}
                >
                    Logout
                </NavLink>
                <NavLink
                    to="/register"
                    className={[
                        classes.button,
                        classes.red,
                        classes.hollow,
                    ].join(" ")}
                >
                    New Register
                </NavLink>
            </div>
        );
    } else if (props.usertype === "doctor") {
        data = (
            <div>
                <NavLink
                    to="/sessions"
                    className={[
                        classes.button,
                        classes.orange,
                        classes.hollow,
                    ].join(" ")}
                >
                    Sessions
                </NavLink>
                <NavLink
                    to="/logout"
                    className={[
                        classes.button,
                        classes.orange,
                        classes.hollow,
                    ].join(" ")}
                >
                    Logout
                </NavLink>
            </div>
        );
    } else if (props.usertype === "patient") {
        data = (
            <div>
                <NavLink
                    to="/sessions"
                    className={[
                        classes.button,
                        classes.orange,
                        classes.hollow,
                    ].join(" ")}
                >
                    Sessions
                </NavLink>
                <NavLink
                    to="/logout"
                    className={[
                        classes.button,
                        classes.orange,
                        classes.hollow,
                    ].join(" ")}
                >
                    Logout
                </NavLink>
            </div>
        );
    }
    return (
        <div>
            <div
                id="header"
                className={[classes["fixed-top"], classes["header"]].join(" ")}
            >
                <div className={classes["row"]}>
                    <nav
                        className={[
                            classes["navbar-expand-xl"],
                            classes["bg-light"],
                            classes["navbar-default"],
                            classes["navbar"],
                            classes["navbar-expand-xl"],
                            classes["navbar-light"],
                            classes["scrolled"],
                        ].join(" ")}
                    >
                        <NavLink
                            to="/"
                            className={[
                                classes["ml-3"],
                                classes["navbar-brand"],
                            ].join(" ")}
                        >
                            <img
                                className={[
                                    classes["logo"],
                                    classes["mt-n4"],
                                    classes["mr-auto"],
                                ].join(" ")}
                                src={logo}
                                alt="logo"
                            />
                            <span
                                className={[
                                    classes["missioned-nav"],
                                    classes["font-weight-bold"],
                                ].join(" ")}
                            >
                                Health
                                <span className={classes["ed"]}>Care</span>
                                <span className={classes["classes"]}>
                                    &trade;
                                </span>
                            </span>
                        </NavLink>

                        {/* <div className={classes.flex}>
                            <NavLink to="/" className={classes.navlink}>
                                Home
                            </NavLink>
                            <NavLink to="/course/1" className={classes.navlink}>
                                Course
                            </NavLink>
                        </div> */}

                        {/* {!auth.currentUser || !user ? ( */}

                        {props.usertype !== null ? (
                            data
                        ) : (
                            <NavLink
                                to="/login"
                                className={[
                                    classes.button,
                                    classes.orange,
                                    classes.hollow,
                                ].join(" ")}
                            >
                                Login
                            </NavLink>
                        )}
                        {/* ) : (
                            <UserDetails />
                        )} */}
                    </nav>
                </div>
            </div>
        </div>
    );
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

export default connect(mapStateToProps, mapDispatchToProps)(Header);