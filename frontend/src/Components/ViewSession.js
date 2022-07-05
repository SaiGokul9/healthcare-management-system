import React, { useEffect, useState } from "react";
import { connect } from "react-redux";
import { withRouter, NavLink, Redirect } from "react-router-dom";
import Select from "react-select";

import * as actionCreators from "../store/actions/actionCreators";

import classes from "./Main.module.css";

function ViewSession(props) {
    let session_id = props.match.params.id;
    document.title = `Session ${session_id} | Details `;
    useEffect(() => {
        setTimeout(() => {
            props.getAllDoctors();
        }, 200);
    }, []);
    useEffect(() => {
        if (session_id) {
            props.getSessionDetails(session_id);
        }
    }, [session_id]);
    console.log("View session rendering", props);

    const optionas = props.all_doctors.map((obj) => {
        return {
            value: obj.doctor_id,
            label:
                (obj.doctor_name ? obj.doctor_name : obj.doctor_id) +
                " | Department : " +
                obj.department,
        };
    });
    // if (!props.session_details) {
    //     return <Redirect to="/sessions" />;
    // }
    // useEffect(() => props.getSessionDetails(session_id), [props]);
    const [doctor, setdoctor] = useState([]);

    let details_obj = props.session_details;
    if (details_obj == null) {
        return (
            <div
                className={[classes.homepage, classes.centerHome].join(" ")}
            ></div>
        );
    }
    return (
        <div className={[classes.homepage, classes.centerHome].join(" ")}>
            <div /* className={} */>
                <div className={classes.notes}>
                    <div>
                        <NavLink
                            to="/sessions"
                            className={[
                                classes.backRef,
                                classes.button,
                                classes.hollow,
                                classes.teal,
                            ].join(" ")}
                        >
                            Back to All Sessions
                        </NavLink>
                    </div>
                    <h2 className={classes.mainHead}>
                        Details of Session {details_obj.session_id} | Patient
                        Name : {details_obj.patient_name}
                    </h2>
                    <div className={classes.sessionDetails}>
                        <h2 className={classes.appsHeadDouble}>General Info</h2>
                        <div className={classes.sessionDetail}>
                            Patient session started by :{" "}
                            <div className={classes.contentFillDetails}>
                                {details_obj.staff_name}
                            </div>
                        </div>
                        <div className={classes.sessionDetail}>
                            Patient joined with area of diseases :{" "}
                            <div className={classes.contentFillDetails}>
                                {details_obj.area_of_disease.join(", ")}
                            </div>
                        </div>
                        <div className={classes.sessionDetail}>
                            Patient description given on his own :{" "}
                            <div className={classes.contentFillDetails}>
                                {details_obj.description}
                            </div>
                        </div>
                        <div className={classes.timestamp}>
                            Session start time :{" "}
                            <div className={classes.contentFillDetails}>
                                {details_obj.session_start_time}
                            </div>
                        </div>
                        <div className={classes.timestamp}>
                            Last updated :{" "}
                            <div className={classes.contentFillDetails}>
                                {details_obj.last_updated_time || "-"}
                            </div>
                        </div>
                    </div>
                    <h2 className={classes.appsHeadDouble}>Appointments</h2>
                    <Select
                        defaultValue={[]}
                        isDisabled={false}
                        isLoading={false}
                        isClearable={true}
                        isRtl={false}
                        isSearchable={false}
                        name="doctor"
                        options={optionas}
                        className={["basic-single", classes.react_select].join(
                            " "
                        )}
                        classNamePrefix="select"
                        value={doctor}
                        onChange={(e) => {
                            console.log(doctor);
                            setdoctor(e);
                        }}
                    />
                    <button
                        className={[
                            classes.saveNoteBtn,
                            classes.button,
                            classes.hollow,
                            classes.blue,
                        ].join(" ")}
                        onClick={(e) => {
                            props.createAppointment(session_id, doctor.value);
                        }}
                    >
                        Add appointment
                    </button>
                    {details_obj.appointments.length > 0
                        ? details_obj.appointments.map((obj) => (
                              <div key={obj.appointment_id}>
                                  <NavLink
                                      className={classes.note}
                                      to={`/appointment/${obj.appointment_id}`}
                                  >
                                      <div className={classes.timestamp}>
                                          Appointment time :{" "}
                                          {obj.appointment_time}
                                      </div>
                                      <div className={classes.heading}>
                                          Appointment with {obj.doctor_name}|
                                          Appointment ID : {obj.appointment_id}
                                      </div>

                                      <div className={classes.content}>
                                          {obj.description}
                                      </div>
                                      {/* <button
                                          className={[
                                              classes.delete,
                                              classes.button,
                                              classes.solid,
                                              classes.red,
                                          ].join(" ")}
                                      >
                                          Active
                                      </button> */}
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
                              </div>
                          ))
                        : "No Appointments in the current session"}
                    <h2 className={classes.appsHeadDouble}>
                        Payment Details
                        {details_obj.bill_generation_status
                            ? " | The billed amount is : Rs." +
                              details_obj.billed_amount
                            : ""}
                    </h2>
                    {details_obj.bill_generation_status ? (
                        <div>
                            <div></div>
                            {details_obj.last_updated_time ? (
                                <div>
                                    <button
                                        className={[
                                            classes.generateBill,
                                            classes.button,
                                            classes.solid,
                                            classes.blue,
                                        ].join(" ")}
                                    >
                                        Bill Paid Already
                                    </button>
                                </div>
                            ) : (
                                <div>
                                    <button
                                        className={[
                                            classes.generateBill,
                                            classes.button,
                                            classes.solid,
                                            classes.red,
                                        ].join(" ")}
                                        onClick={() =>
                                            props.markAsPaid(session_id)
                                        }
                                    >
                                        Mark as paid and terminate the session
                                    </button>
                                </div>
                            )}{" "}
                        </div>
                    ) : (
                        <div>
                            <button
                                className={[
                                    classes.generateBill,
                                    classes.button,
                                    classes.solid,
                                    classes.orange,
                                ].join(" ")}
                                onClick={() => props.generateBill(session_id)}
                            >
                                Generate Bill
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

const mapStateToProps = (state) => {
    return {
        userId: state.userId,
        session_details: state.session_details,
        all_doctors: state.all_doctors,
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        getSessionDetails: (session_id) =>
            dispatch(actionCreators.getSessionDetails(session_id)),
        getAllDoctors: () => dispatch(actionCreators.getAllDoctors()),
        createAppointment: (session_id, doctor_id) =>
            dispatch(actionCreators.createAppointment(session_id, doctor_id)),
        generateBill: (session_id) =>
            dispatch(actionCreators.generateBill(session_id)),
        markAsPaid: (session_id) =>
            dispatch(actionCreators.markAsPaid(session_id)),
    };
};

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(withRouter(ViewSession));
