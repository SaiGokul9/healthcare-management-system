import React, { useEffect, useState } from "react";
import { connect } from "react-redux";
import { NavLink } from "react-router-dom";
import Select from "react-select";

import * as actionCreators from "../store/actions/actionCreators";

import classes from "./Main.module.css";
// import classes from "./Course.module.css";

function AddSession(props) {
    document.title = "Add a Session | HealthCare";

    useEffect(() => {
        props.getDiseases();
    }, []);

    const optionsb = [
        { value: "male", label: "Male" },
        { value: "female", label: "Female" },
    ];
    const options = props.area_of_diseases.map((obj) => {
        return { value: obj.disease_id, label: obj.disease_name };
    });
    const optionas = props.related_doctors.map((obj) => {
        return {
            value: obj.doctor_id,
            label:
                (obj.doctor_name ? obj.doctor_name : obj.doctor_id) +
                " | Department : " +
                obj.department,
        };
    });

    const [username, setUsername] = useState("");
    const [newusername, setNewUsername] = useState("");
    const [newname, setNewname] = useState("");
    const [dob, setdob] = useState("");
    const [gender, setgender] = useState(optionsb[0]);
    const [mobile, setmobile] = useState("");
    const [description, setdescription] = useState("");
    const [diseases, setdiseases] = useState([]);
    const [doctor, setdoctor] = useState([]);
    // {"related_doctors":[{"appointment_fee":null,"department":"('ortho',)","doctor_id":3,"doctor_name":"None","room_no":"None","specialisation":[]},{"appointment_fee":null,"department":"('ortho',)","doctor_id":5,"doctor_name":"None","room_no":"None","specialisation":[]}]}

    return (
        <div className={[classes.homepage, classes.centerHome].join(" ")}>
            <div className={classes.notes}>
                <h2 className={classes.savedNotesHead}>Add a New Session</h2>
                <div className={classes.noteAddSection}>
                    <h2 className={classes.appsHeadDouble}>
                        For exisiting patient:
                    </h2>
                    <div
                        className={[
                            classes.smallHeadEntry,
                            classes.normal,
                            username ? classes.show : classes.hide,
                        ].join(" ")}
                    >
                        Username of the patient :{" "}
                    </div>
                    <input
                        className={classes.noteEntryHead}
                        type="text"
                        placeholder="Username of the patient"
                        value={username}
                        onChange={(e) => {
                            setUsername(e.target.value);
                            setNewUsername("");
                            setNewname("");
                            setdob("");
                        }}
                    />
                    {/*  */}
                    <h2 className={classes.appsHeadDouble}>For new patient:</h2>
                    <div
                        className={[
                            classes.smallHeadEntry,
                            classes.normal,
                            newname ? classes.show : classes.hide,
                        ].join(" ")}
                    >
                        Name of the patient :{" "}
                    </div>
                    <input
                        className={classes.noteEntryHead}
                        type="text"
                        placeholder="Name of the patient"
                        value={newname}
                        onChange={(e) => {
                            setNewname(e.target.value);
                            setUsername("");
                        }}
                    />
                    <div
                        className={[
                            classes.smallHeadEntry,
                            classes.normal,
                            newusername ? classes.show : classes.hide,
                        ].join(" ")}
                    >
                        Username :{" "}
                    </div>
                    <input
                        className={classes.noteEntryHead}
                        type="text"
                        placeholder="Username"
                        value={newusername}
                        onChange={(e) => {
                            setNewUsername(e.target.value);
                            setUsername("");
                        }}
                    />
                    <div
                        className={[
                            classes.smallHeadEntry,
                            classes.normal,
                        ].join(" ")}
                    >
                        Date of Birth :{" "}
                    </div>
                    <input
                        className={classes.noteEntryHead}
                        type="date"
                        placeholder="Date of birth"
                        value={dob}
                        onChange={(e) => {
                            setdob(e.target.value);
                            setUsername("");
                        }}
                    />
                    <div
                        className={[
                            classes.smallHeadEntry,
                            classes.normal,
                        ].join(" ")}
                    >
                        Gender :{" "}
                    </div>
                    <Select
                        defaultValue={optionsb[0]}
                        isDisabled={false}
                        isLoading={false}
                        isClearable={true}
                        isRtl={false}
                        isSearchable={false}
                        name="gender"
                        options={optionsb}
                        className={["basic-single", classes.react_select].join(
                            " "
                        )}
                        classNamePrefix="select"
                        value={gender}
                        onChange={(e) => {
                            console.log(gender);
                            setgender(e);
                        }}
                    />
                    <div
                        className={[
                            classes.smallHeadEntry,
                            classes.normal,
                            mobile ? classes.show : classes.hide,
                        ].join(" ")}
                    >
                        Mobile number :{" "}
                    </div>
                    <input
                        className={classes.noteEntryHead}
                        type="mobile"
                        placeholder="Mobile number"
                        value={mobile}
                        onChange={(e) => {
                            setmobile(e.target.value);
                            setUsername("");
                        }}
                    />
                    {/*  */}
                    <h2 className={classes.appsHeadDouble}>Session Details:</h2>

                    <div
                        className={[
                            classes.smallHeadEntry,
                            classes.normal,
                            description ? classes.show : classes.hide,
                        ].join(" ")}
                    >
                        Patient general description :{" "}
                    </div>
                    <textarea
                        placeholder="Patient general description .."
                        rows="5"
                        className={classes.noteEntryContent}
                        value={description}
                        onChange={(e) => {
                            console.log(description);
                            setdescription(e.target.value);
                        }}
                    />

                    <div
                        className={[
                            classes.smallHeadEntry,
                            classes.normal,
                        ].join(" ")}
                    >
                        Select Area of Diseases :{" "}
                    </div>

                    <Select
                        defaultValue={[]}
                        isDisabled={false}
                        isLoading={false}
                        isClearable={true}
                        isRtl={false}
                        isSearchable={false}
                        name="diseases"
                        options={options}
                        isMulti
                        className={[
                            "basic-multi-select",
                            classes.react_select,
                        ].join(" ")}
                        classNamePrefix="select"
                        value={diseases}
                        onChange={(e) => {
                            console.log(diseases);
                            setdiseases(e);
                        }}
                    />

                    {/* <div className={classes.doctorList}>doctorList</div> */}
                    <button
                        className={[
                            classes.saveNoteBtn,
                            classes.button,
                            classes.hollow,
                            classes.blue,
                        ].join(" ")}
                        onClick={() =>
                            props.getDoctors(diseases.map((obj) => obj.value))
                        }
                    >
                        Search Doctors
                    </button>
                    <div
                        className={[
                            classes.smallHeadEntry,
                            classes.normal,
                        ].join(" ")}
                    >
                        Select primary doctor :{" "}
                    </div>

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
                    <div>
                        <button
                            className={[
                                classes.saveNoteBtn,
                                classes.button,
                                classes.hollow,
                                classes.blue,
                            ].join(" ")}
                            onClick={(e) => {
                                props.createSession(
                                    props.userId,
                                    username,
                                    newname,
                                    newusername,
                                    gender.value,
                                    mobile,
                                    dob,
                                    description,
                                    diseases.map((obj) => obj.value),
                                    doctor.value
                                );
                            }}
                        >
                            Add Session
                        </button>
                        <NavLink
                            to="/sessions"
                            className={[
                                classes.discardButton,
                                classes.button,
                                classes.hollow,
                                classes.red,
                            ].join(" ")}
                        >
                            Discard
                        </NavLink>
                    </div>
                </div>
            </div>
        </div>
    );
}

const mapStateToProps = (state) => {
    return {
        userId: state.userId,
        area_of_diseases: state.area_of_diseases,
        related_doctors: state.related_doctors,
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        getDiseases: () => dispatch(actionCreators.getDiseaseAreas()),
        getDoctors: (list_of_diseases) =>
            dispatch(actionCreators.getRelatedDoctors(list_of_diseases)),
        createSession: (
            userId,
            paitent_username,
            patient_newname,
            patient_newusername,
            patient_gender,
            patient_mobile,
            patient_dob,
            patient_description,
            disease_ids,
            primary_doctor_id
        ) =>
            dispatch(
                actionCreators.createSession(
                    userId,
                    paitent_username,
                    patient_newname,
                    patient_newusername,
                    patient_gender,
                    patient_mobile,
                    patient_dob,
                    patient_description,
                    disease_ids,
                    primary_doctor_id
                )
            ),
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(AddSession);
