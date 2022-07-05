import React, { useState } from "react";

// import { auth, firestore } from "./Firebase";

import classes from "./Main.module.css";

// import { useAuthState } from "react-firebase-hooks/auth";
import { Redirect } from "react-router";

import logo from "../logo.png";
function Register(props) {
    // const [user] = useAuthState(auth);

    const [fullname, setFullname] = useState("");
    const [uname, setuname] = useState("");
    const [password, setPassword] = useState("");
    const [rePassword, setRePassword] = useState("");
    const [acType, setAcType] = useState("");
    const [authError, setAuthError] = useState("");
    const [authSuccess, setAuthSuccess] = useState("");
    const [authComplete, setAuthComplete] = useState(false);

    // if (authComplete) {
    //     return <Redirect to="/" />;
    // }
    document.title = "Register to HealthCare | Hospital Management System";
    // const usersRef = firestore.collection("users");

    const register = async () => {
        try {
            // if (acType == "") throw { message: "Please select a user type." };
            if (fullname == "")
                throw { message: "Please enter your full name." };
            else if (uname == "")
                throw { message: "Please enter your username." };
            else if (password != rePassword)
                throw { message: "Passwords do not match." };
            else if (password == "")
                throw { message: "Please enter the password." };
            else if (password.length < 4)
                throw { message: "Please use password of length atleast 4." };

            // await auth.createUserWithEmailAndPassword(email, password);
            // await auth.currentUser.updateProfile({
            //     displayName: fullname,
            // });

            // await usersRef.doc(auth.currentUser.uid).set({
            //     fullname: fullname,
            //     acType: acType,
            //     email: email,
            // });

            setAuthSuccess("Succesfully registered. Login to Continue.");
            setAuthError("");
            setFullname("");
            setuname("");
            setPassword("");
            setRePassword("");
            setAcType("");
            setAuthError("");
            setAuthComplete(true);
        } catch (e) {
            setAuthSuccess("");
            setAuthError(e.message);
        }
    };

    return (
        <div className={[classes.homepage, classes.centerHome].join(" ")}>
            <div className={classes.authBox}>
                <div className={classes.brandBox}>
                    <img className={classes.brandLogo} src={logo} alt="title" />
                    <div className={classes.brandName}>
                        Register to HealthCare
                    </div>
                </div>
                <form
                    className={classes.formBox}
                    onSubmit={(e) => {
                        e.preventDefault();
                        register();
                    }}
                >
                    <div
                        className={[
                            classes.smallHeadEntry,
                            fullname ? classes.show : classes.hide,
                        ].join(" ")}
                    >
                        Full Name :{" "}
                    </div>
                    <input
                        className={classes.authEntry}
                        type="text"
                        placeholder="Full Name"
                        value={fullname}
                        onChange={(e) => {
                            setAuthError("");
                            setFullname(e.target.value);
                        }}
                    />

                    <div
                        className={[
                            classes.smallHeadEntry,
                            uname ? classes.show : classes.hide,
                        ].join(" ")}
                    >
                        Username :{" "}
                    </div>
                    <input
                        className={classes.authEntry}
                        type="text"
                        placeholder="Username"
                        value={uname}
                        onChange={(e) => {
                            setAuthError("");
                            setuname(e.target.value);
                        }}
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
                        onChange={(e) => {
                            setAuthError("");
                            setPassword(e.target.value);
                        }}
                    />
                    <div
                        className={[
                            classes.smallHeadEntry,
                            rePassword ? classes.show : classes.hide,
                        ].join(" ")}
                    >
                        Re-enter Password :{" "}
                    </div>
                    <input
                        className={classes.authEntry}
                        type="password"
                        placeholder="Re-enter Password"
                        value={rePassword}
                        onChange={(e) => {
                            setAuthError("");
                            setRePassword(e.target.value);
                        }}
                    />
                    <div className={classes.authError}>{authError}</div>
                    <div className={classes.authSuccess}>{authSuccess}</div>
                    <input
                        className={[
                            classes.button,
                            classes.hollow,
                            classes.authSubmit,
                        ].join(" ")}
                        type="submit"
                        value="Register"
                    />
                </form>
            </div>
        </div>
    );
}

export default Register;
