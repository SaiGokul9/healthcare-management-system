import React, { useEffect, useState } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import { withRouter, NavLink } from "react-router-dom";
import Select from "react-select";

import * as actionCreators from "../store/actions/actionCreators";

import classes from "./Main.module.css";

function ViewAppointment(props) {
    let appointment_id = props.match.params.id;
    document.title = `Appointment ${appointment_id} | Details`;
    console.log("View appointment rendering", props);

    useEffect(() => props.getAppointmentDetails(appointment_id), [
        appointment_id,
    ]);
    useEffect(() => {
        setTimeout(() => {
            props.getMedicines();
        }, 200);
        setTimeout(() => {
            props.getTreatments();
            // props.getMedicines();
        }, 400);
    }, []);

    let appointment_details = props.appointment_details;

    const [medicine, setmedicine] = useState();
    const [treatment, settreatment] = useState();
    const [quantity, setquantity] = useState();
    const [description, setdescription] = useState("");
    
    if (!props.appointment_details) {
        return (
            <div
                className={[classes.homepage, classes.centerHome].join(" ")}
            ></div>
        );
    }

    let all_medicines = props.all_medicines.map((obj) => {
        return { value: obj.medicine_id, label: obj.medicine_name };
    });
    let all_treatments = props.all_treatments.map((obj) => {
        return { value: obj.treatment_id, label: obj.treatment_name };
    });

    return (
        <div className={[classes.homepage, classes.centerHome].join(" ")}>
            <div /* className={} */>
                <div className={classes.notes}>
                    <div>
                        <NavLink
                            to={`/sessions`}
                            className={[
                                classes.backRef,
                                classes.button,
                                classes.hollow,
                                classes.teal,
                            ].join(" ")}
                        >
                            Back to the Session
                        </NavLink>
                    </div>
                    <h2 className={classes.mainHead}>
                        Details of Appointment {appointment_details.app_id} |
                        Patient Name : {appointment_details.patient_name} |
                        Doctor : {appointment_details.doctor_name}
                    </h2>
                    <div className={classes.sessionDetails}>
                        <h2 className={classes.appsHeadDouble}>General Info</h2>

                        <div className={classes.timestamp}>
                            Appointment time :{" "}
                            <div className={classes.contentFillDetails}>
                                {appointment_details.appointment_time}
                            </div>
                        </div>

                        <div className={classes.timestamp}>
                            Appointment Description :{" "}
                            <div className={classes.contentFillDetails}>
                                {appointment_details.doctor_description}
                            </div>
                            <textarea
                                placeholder="Edit Appointment Description .."
                                rows="5"
                                className={classes.noteEntryContent}
                                value={description}
                                onChange={(e) => {
                                    setdescription(e.target.value);
                                }}
                            />
                        </div>

                        <button
                            to="/sessions"
                            className={[
                                classes.viewProfile,
                                classes.button,
                                classes.hollow,
                                classes.orange,
                            ].join(" ")}
                            onClick={() =>
                                props.editDescrip(appointment_id, description)
                            }
                        >
                            Edit Description
                        </button>
                    </div>
                    <h2 className={classes.appsHeadDouble}>Treatments</h2>
                    <div
                        className={[
                            classes.smallHeadEntry,
                            classes.normal,
                        ].join(" ")}
                    >
                        Add a treatment :{" "}
                    </div>

                    <Select
                        defaultValue={[]}
                        isDisabled={false}
                        isLoading={false}
                        isClearable={true}
                        isRtl={false}
                        isSearchable={false}
                        name="treatment"
                        options={all_treatments}
                        className={["basic-single", classes.react_select].join(
                            " "
                        )}
                        classNamePrefix="select"
                        value={treatment}
                        onChange={(e) => {
                            console.log(treatment);
                            settreatment(e);
                        }}
                    />
                    <button
                        className={[
                            classes.saveNoteBtn,
                            classes.button,
                            classes.hollow,
                            classes.blue,
                        ].join(" ")}
                        onClick={() => {
                            if (treatment) {
                                props.addTreatment(
                                    appointment_id,
                                    treatment.value
                                );
                                settreatment([]);
                            }
                        }}
                    >
                        Add treatment
                    </button>
                    {appointment_details.treatments.length ? (
                        appointment_details.treatments.map((obj) => {
                            return (
                                <div key={obj.trmrt_id}>
                                    <div className={classes.note}>
                                        <div className={classes.timestamp}>
                                            Treatment time : {obj.trmrt_time}
                                        </div>
                                        <div className={classes.heading}>
                                            {obj.trmrt_name}
                                        </div>
                                    </div>
                                </div>
                            );
                        })
                    ) : (
                        <div>No treatments done in this appointment</div>
                    )}
                    {/*                         
                    <h2 className={classes.appsHeadDouble}>Tests</h2>
                    <NavLink className={classes.note} to="/test/1">
                        <div className={classes.timestamp}>
                            Test time : 09:54:12, 7 March 2022
                        </div>
                        <div className={classes.heading}>
                            RTPCR - Covid Test
                        </div>
                        <div className={classes.content}>Result : Negative</div>
                    </NavLink> */}
                    <h2 className={classes.appsHeadDouble}>
                        Medicines prescribed
                    </h2>
                    <div
                        className={[
                            classes.smallHeadEntry,
                            classes.normal,
                        ].join(" ")}
                    >
                        Add a medicine :{" "}
                    </div>

                    <Select
                        defaultValue={[]}
                        isDisabled={false}
                        isLoading={false}
                        isClearable={true}
                        isRtl={false}
                        isSearchable={false}
                        name="medicine"
                        options={all_medicines}
                        className={["basic-single", classes.react_select].join(
                            " "
                        )}
                        classNamePrefix="select"
                        value={medicine}
                        onChange={(e) => {
                            console.log(medicine);
                            setmedicine(e);
                        }}
                    />
                    <div
                        className={[
                            classes.smallHeadEntry,
                            classes.normal,
                            quantity ? classes.show : classes.hide,
                        ].join(" ")}
                    >
                        Quantity of the medicine :{" "}
                    </div>
                    <input
                        className={classes.noteEntryHead}
                        type="number"
                        placeholder="Quantity of the medicine"
                        value={quantity}
                        onChange={(e) => {
                            setquantity(e.target.value);
                        }}
                    />
                    <button
                        className={[
                            classes.saveNoteBtn,
                            classes.button,
                            classes.hollow,
                            classes.blue,
                        ].join(" ")}
                        onClick={() => {
                            if (medicine) {
                                props.addMedicine(
                                    appointment_id,
                                    medicine.value,
                                    quantity
                                );
                                setmedicine([]);
                            }
                        }}
                    >
                        Add medicine
                    </button>
                    {appointment_details.medicines.length ? (
                        appointment_details.medicines.map((obj) => {
                            return (
                                <div key={obj.trmrt_id}>
                                    <div className={classes.note}>
                                        <div className={classes.timestamp}>
                                            Medicine quantity : {obj.quantity}
                                        </div>
                                        <div className={classes.heading}>
                                            {obj.trmrt_name}
                                        </div>
                                    </div>
                                </div>
                            );
                        })
                    ) : (
                        <div>No medicines done in this appointment</div>
                    )}
                </div>
            </div>
        </div>
    );
}

const mapStateToProps = (state) => {
    return {
        userId: state.userId,
        appointment_details: state.appointment_details,
        all_medicines: state.all_medicines,
        all_treatments: state.all_treatments,
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        editDescrip: (appointment_id, description) =>
            dispatch(actionCreators.editDescrip(appointment_id, description)),
        getAppointmentDetails: (appointment_id) =>
            dispatch(actionCreators.getAppointmentDetails(appointment_id)),
        getMedicines: () => dispatch(actionCreators.getMedicines()),
        getTreatments: () => dispatch(actionCreators.getTreatments()),
        addMedicine: (appointment_id, medicine_id, quantity) =>
            dispatch(
                actionCreators.addMedicine(
                    appointment_id,
                    medicine_id,
                    quantity
                )
            ),
        addTreatment: (appointment_id, treatment_id) =>
            dispatch(actionCreators.addTreatment(appointment_id, treatment_id)),
    };
};

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(withRouter(ViewAppointment));
