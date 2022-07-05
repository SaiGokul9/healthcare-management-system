import React, { useEffect } from "react";

import { NavLink } from "react-router-dom";
import { connect } from "react-redux";

import * as actionCreators from "../store/actions/actionCreators";

import classes from "./Main.module.css";

function Sessions(props) {
    document.title = "All Sessions | HealthCare ";
    useEffect(() => props.getSessions(), []);
    console.log("Sessions rendering");

    let sessions = props.sessions.reverse().map((obj) => {
        return (
            <NavLink
                key={obj.session_id}
                className={classes.note}
                to={`/session/${obj.session_id}`}
            >
                <div className={classes.timestamp}>
                    Discharge Date : {obj.last_updated_time ? obj.last_updated_time : "-"}
                </div>
                <div className={classes.timestamp}>
                    Session start time : {obj.session_start_time}
                </div>
                <div className={classes.heading}>
                    Session {obj.session_id} | Patient Name : {obj.patient_name}{" "}
                    | Patient ID : {obj.patient_id}
                </div>
                <div className={classes.content}>{obj.description}</div>
                {!obj.last_updated_time ? (
                    <button
                        className={[
                            classes.delete,
                            classes.button,
                            classes.solid,
                            classes.red,
                        ].join(" ")}
                    >
                        Active
                    </button>
                ) : (
                    ""
                )}
                <button
                    className={[
                        classes.goToRef,
                        classes.button,
                        classes.solid,
                        classes.contrast,
                    ].join(" ")}
                >
                    Take a look
                </button>
            </NavLink>
        );
    });

    return (
        <div className={[classes.homepage, classes.centerHome].join(" ")}>
            <div className={classes.notes}>
                <div className={classes.chatBox}>
                    <NavLink
                        to="/session/add"
                        className={[
                            classes.solid,
                            classes.orange,
                            classes.div,
                            classes.chatBtn,
                        ].join(" ")}
                    >
                        Add a new Session
                    </NavLink>
                </div>
                <h2 className={classes.savedNotesHead}>Active Sessions</h2>
                {sessions}
            </div>
        </div>
    );
}

const mapStateToProps = (state) => {
    return {
        userId: state.userId,
        userType: state.userType,
        sessions: state.sessions,
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        getSessions: () => dispatch(actionCreators.getAllSessions()),
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(Sessions);
