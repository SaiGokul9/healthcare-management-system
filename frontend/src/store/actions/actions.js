import axios from "axios";

import * as actionTypes from "./actionTypes";
import * as LinkConstants from "../../LinkNames";

export const getAllSessions = () => {
    return (dispatch, getState) => {
        dispatch({ type: actionTypes.CLEAR_ERROR });
        let axiosOptions = {
            method: "POST",
            url: `${process.env.REACT_APP_DATABASE_URI}/getallsessions`,
            data: {},
            headers: {
                authorization: `Basic ${JSON.parse(
                    localStorage.getItem("authToken")
                )}`,
            },
        };

        axios(axiosOptions)
            .then((response) => {
                let sessions = response.data.sessions;

                dispatch({
                    type: actionTypes.LOAD_SESSIONS,
                    payload: {
                        sessions: sessions,
                    },
                });
            })
            .catch((error) => {
                let message = null;
                try {
                    message = error.response.data.message;
                } catch {
                    message = "Sorry, some error occured, Please Try again.";
                }

                dispatch({
                    type: actionTypes.NORMAL_FAIL,
                    payload: {
                        message: message,
                    },
                });
            });
    };
};

export const getSessionDetails = (session_id) => {
    return (dispatch, getState) => {
        dispatch({
            type: actionTypes.CREATE_SESSION,
            payload: {
                message: "Succesful",
            },
        });
        dispatch({ type: actionTypes.CLEAR_ERROR });
        let axiosOptions = {
            method: "POST",
            url: `${process.env.REACT_APP_DATABASE_URI}/getsessiondetails`,
            data: {
                session_id: session_id,
            },
            headers: {
                authorization: `Basic ${JSON.parse(
                    localStorage.getItem("authToken")
                )}`,
            },
        };

        axios(axiosOptions)
            .then((response) => {
                let session_details = response.data.session_details;
                dispatch({
                    type: actionTypes.LOAD_SESSION_DETAILS,
                    payload: {
                        session_details: session_details,
                    },
                });
            })
            .catch((error) => {
                let message = null;
                try {
                    message = error.response.data.message;
                } catch {
                    message = "Sorry, some error occured, Please Try again.";
                }

                dispatch({
                    type: actionTypes.NORMAL_FAIL,
                    payload: {
                        message: message,
                    },
                });
            });
    };
};

export const getDiseaseAreas = () => {
    return (dispatch, getState) => {
        dispatch({ type: actionTypes.CLEAR_ERROR });
        let axiosOptions = {
            method: "POST",
            url: `${process.env.REACT_APP_DATABASE_URI}/getareaofdiseases`,
            data: {},
            headers: {
                authorization: `Basic ${JSON.parse(
                    localStorage.getItem("authToken")
                )}`,
            },
        };

        axios(axiosOptions)
            .then((response) => {
                let area_of_diseases = response.data.area_of_diseases;
                dispatch({
                    type: actionTypes.LOAD_DISEASE_AREAS,
                    payload: {
                        area_of_diseases: area_of_diseases,
                    },
                });
            })
            .catch((error) => {
                let message = null;
                try {
                    message = error.response.data.message;
                } catch {
                    message = "Sorry, some error occured, Please Try again.";
                }

                dispatch({
                    type: actionTypes.NORMAL_FAIL,
                    payload: {
                        message: message,
                    },
                });
            });
    };
};

export const getMedicines = () => {
    return (dispatch, getState) => {
        dispatch({ type: actionTypes.CLEAR_ERROR });
        let axiosOptions = {
            method: "POST",
            url: `${process.env.REACT_APP_DATABASE_URI}/getallmedicine`,
            data: {},
            headers: {
                authorization: `Basic ${JSON.parse(
                    localStorage.getItem("authToken")
                )}`,
            },
        };

        axios(axiosOptions)
            .then((response) => {
                let all_medicines = response.data.all_medicines;
                dispatch({
                    type: actionTypes.LOAD_MEDICINES,
                    payload: {
                        all_medicines: all_medicines,
                    },
                });
            })
            .catch((error) => {
                let message = null;
                try {
                    message = error.response.data.message;
                } catch {
                    message = "Sorry, some error occured, Please Try again.";
                }

                dispatch({
                    type: actionTypes.NORMAL_FAIL,
                    payload: {
                        message: message,
                    },
                });
            });
    };
};

export const getTreatments = () => {
    return (dispatch, getState) => {
        dispatch({ type: actionTypes.CLEAR_ERROR });
        let axiosOptions = {
            method: "POST",
            url: `${process.env.REACT_APP_DATABASE_URI}/getalltreatment`,
            data: {},
            headers: {
                authorization: `Basic ${JSON.parse(
                    localStorage.getItem("authToken")
                )}`,
            },
        };

        axios(axiosOptions)
            .then((response) => {
                let all_treatments = response.data.all_treatments;
                dispatch({
                    type: actionTypes.LOAD_TREATMENTS,
                    payload: {
                        all_treatments: all_treatments,
                    },
                });
            })
            .catch((error) => {
                let message = null;
                try {
                    message = error.response.data.message;
                } catch {
                    message = "Sorry, some error occured, Please Try again.";
                }

                dispatch({
                    type: actionTypes.NORMAL_FAIL,
                    payload: {
                        message: message,
                    },
                });
            });
    };
};

export const getRelatedDoctors = (disease_ids) => {
    return (dispatch, getState) => {
        dispatch({ type: actionTypes.CLEAR_ERROR });
        let axiosOptions = {
            method: "POST",
            url: `${process.env.REACT_APP_DATABASE_URI}/getrelateddoctors`,
            data: {
                disease_ids: disease_ids, // For example it is a list of [1, 2, 3]
            },
            headers: {
                authorization: `Basic ${JSON.parse(
                    localStorage.getItem("authToken")
                )}`,
            },
        };

        axios(axiosOptions)
            .then((response) => {
                let related_doctors = response.data.related_doctors;
                dispatch({
                    type: actionTypes.LOAD_RELATED_DOCTORS,
                    payload: {
                        related_doctors: related_doctors,
                    },
                });
            })
            .catch((error) => {
                let message = null;
                try {
                    message = error.response.data.message;
                } catch {
                    message = "Sorry, some error occured, Please Try again.";
                }

                dispatch({
                    type: actionTypes.NORMAL_FAIL,
                    payload: {
                        message: message,
                    },
                });
            });
    };
};

export const getAllDoctors = () => {
    return (dispatch, getState) => {
        dispatch({ type: actionTypes.CLEAR_ERROR });
        let axiosOptions = {
            method: "POST",
            url: `${process.env.REACT_APP_DATABASE_URI}/getalldoctors`,
            data: {},
            headers: {
                authorization: `Basic ${JSON.parse(
                    localStorage.getItem("authToken")
                )}`,
            },
        };

        axios(axiosOptions)
            .then((response) => {
                let all_doctors = response.data.all_doctors;
                dispatch({
                    type: actionTypes.LOAD_ALL_DOCTORS,
                    payload: {
                        all_doctors: all_doctors,
                    },
                });
            })
            .catch((error) => {
                let message = null;
                try {
                    message = error.response.data.message;
                } catch {
                    message = "Sorry, some error occured, Please Try again.";
                }

                dispatch({
                    type: actionTypes.NORMAL_FAIL,
                    payload: {
                        message: message,
                    },
                });
            });
    };
};

export const createSession = (
    staff_id,
    patient_username,
    patient_newname,
    patient_newusername,
    patient_gender,
    patient_mobile,
    patient_dob,
    patient_description,
    disease_ids,
    primary_doctor_id
) => {
    return (dispatch, getState) => {
        dispatch({ type: actionTypes.CLEAR_ERROR });
        let axiosOptions = {
            method: "POST",
            url: `${process.env.REACT_APP_DATABASE_URI}/createsession`,
            data: {
                staff_id: staff_id,
                patient_username: patient_username,
                patient_newname: patient_newname,
                patient_newusername: patient_newusername,
                patient_dob: patient_dob,
                patient_gender: patient_gender,
                patient_mobile: patient_mobile,
                description: patient_description,
                disease_ids: disease_ids, // For example it is a list of [1, 2, 3]
                primary_doctor_id: primary_doctor_id,
            },
            headers: {
                authorization: `Basic ${JSON.parse(
                    localStorage.getItem("authToken")
                )}`,
            },
        };

        axios(axiosOptions)
            .then((response) => {
                let message = response.data.message;
                dispatch({
                    type: actionTypes.CREATE_SESSION,
                    payload: {
                        message: message,
                    },
                });
            })
            .catch((error) => {
                let message = null;
                try {
                    message = error.response.data.message;
                } catch {
                    message = "Sorry, some error occured, Please Try again.";
                }

                dispatch({
                    type: actionTypes.NORMAL_FAIL,
                    payload: {
                        message: message,
                    },
                });
            });
    };
};

export const createAppointment = (session_id, doctor_id) => {
    return (dispatch, getState) => {
        dispatch({ type: actionTypes.CLEAR_ERROR });
        let axiosOptions = {
            method: "POST",
            url: `${process.env.REACT_APP_DATABASE_URI}/addappointment`,
            data: {
                session_id: session_id,
                doctor_id: doctor_id,
            },
            headers: {
                authorization: `Basic ${JSON.parse(
                    localStorage.getItem("authToken")
                )}`,
            },
        };

        axios(axiosOptions)
            .then((response) => {
                let message = response.data.message;
                dispatch({
                    type: actionTypes.CREATE_APPOINTMENT,
                    payload: {
                        message: message,
                    },
                });
            })
            .catch((error) => {
                let message = null;
                try {
                    message = error.response.data.message;
                } catch {
                    message = "Sorry, some error occured, Please Try again.";
                }

                dispatch({
                    type: actionTypes.NORMAL_FAIL,
                    payload: {
                        message: message,
                    },
                });
            });
    };
};

export const addMedicine = (appointment_id, medicine_id, quantity) => {
    return (dispatch, getState) => {
        dispatch({ type: actionTypes.CLEAR_ERROR });
        let axiosOptions = {
            method: "POST",
            url: `${process.env.REACT_APP_DATABASE_URI}/addmedicine`,
            data: {
                app_id: appointment_id,
                medicine_id: medicine_id,
                quantity: quantity,
            },
            headers: {
                authorization: `Basic ${JSON.parse(
                    localStorage.getItem("authToken")
                )}`,
            },
        };

        axios(axiosOptions)
            .then((response) => {
                let message = response.data.message;
                dispatch({
                    type: actionTypes.ADD_MEDICINE,
                    payload: {
                        message: message,
                    },
                });
            })
            .catch((error) => {
                let message = null;
                try {
                    message = error.response.data.message;
                } catch {
                    message = "Sorry, some error occured, Please Try again.";
                }

                dispatch({
                    type: actionTypes.NORMAL_FAIL,
                    payload: {
                        message: message,
                    },
                });
            });
    };
};

export const addTreatment = (appointment_id, treatment_id) => {
    return (dispatch, getState) => {
        dispatch({ type: actionTypes.CLEAR_ERROR });
        let axiosOptions = {
            method: "POST",
            url: `${process.env.REACT_APP_DATABASE_URI}/addtreatment`,
            data: {
                app_id: appointment_id,
                trmrt_id: treatment_id,
            },
            headers: {
                authorization: `Basic ${JSON.parse(
                    localStorage.getItem("authToken")
                )}`,
            },
        };

        axios(axiosOptions)
            .then((response) => {
                let message = response.data.message;
                dispatch({
                    type: actionTypes.ADD_TREATMENT,
                    payload: {
                        message: message,
                    },
                });
            })
            .catch((error) => {
                let message = null;
                try {
                    message = error.response.data.message;
                } catch {
                    message = "Sorry, some error occured, Please Try again.";
                }

                dispatch({
                    type: actionTypes.NORMAL_FAIL,
                    payload: {
                        message: message,
                    },
                });
            });
    };
};

export const editDescrip = (appointment_id, description) => {
    return (dispatch, getState) => {
        dispatch({ type: actionTypes.CLEAR_ERROR });
        let axiosOptions = {
            method: "POST",
            url: `${process.env.REACT_APP_DATABASE_URI}/editdescription`,
            data: {
                app_id: appointment_id,
                description: description,
            },
            headers: {
                authorization: `Basic ${JSON.parse(
                    localStorage.getItem("authToken")
                )}`,
            },
        };

        axios(axiosOptions)
            .then((response) => {
                let message = response.data.message;
                dispatch({
                    type: actionTypes.ADD_TREATMENT,
                    payload: {
                        message: message,
                    },
                });
            })
            .catch((error) => {
                let message = null;
                try {
                    message = error.response.data.message;
                } catch {
                    message = "Sorry, some error occured, Please Try again.";
                }

                dispatch({
                    type: actionTypes.NORMAL_FAIL,
                    payload: {
                        message: message,
                    },
                });
            });
    };
};

export const generateBill = (session_id) => {
    return (dispatch, getState) => {
        dispatch({
            type: actionTypes.CREATE_SESSION,
            payload: {
                message: "Succesful",
            },
        });
        dispatch({ type: actionTypes.CLEAR_ERROR });
        let axiosOptions = {
            method: "POST",
            url: `${process.env.REACT_APP_DATABASE_URI}/generatebill`,
            data: {
                session_id: session_id,
            },
            headers: {
                authorization: `Basic ${JSON.parse(
                    localStorage.getItem("authToken")
                )}`,
            },
        };

        axios(axiosOptions)
            .then((response) => {
                let message = response.data.message;
                dispatch({
                    type: actionTypes.GENERATE_BILL,
                    payload: {
                        message: message,
                    },
                });
            })
            .catch((error) => {
                let message = null;
                try {
                    message = error.response.data.message;
                } catch {
                    message = "Sorry, some error occured, Please Try again.";
                }

                dispatch({
                    type: actionTypes.NORMAL_FAIL,
                    payload: {
                        message: message,
                    },
                });
            });
    };
};

export const markAsPaid = (session_id) => {
    return (dispatch, getState) => {
        dispatch({
            type: actionTypes.CREATE_SESSION,
            payload: {
                message: "Succesful",
            },
        });
        dispatch({ type: actionTypes.CLEAR_ERROR });
        let axiosOptions = {
            method: "POST",
            url: `${process.env.REACT_APP_DATABASE_URI}/marksessionpaid`,
            data: {
                session_id: session_id,
            },
            headers: {
                authorization: `Basic ${JSON.parse(
                    localStorage.getItem("authToken")
                )}`,
            },
        };

        axios(axiosOptions)
            .then((response) => {
                let message = response.data.message;
                dispatch({
                    type: actionTypes.GENERATE_BILL,
                    payload: {
                        message: message,
                    },
                });
            })
            .catch((error) => {
                let message = null;
                try {
                    message = error.response.data.message;
                } catch {
                    message = "Sorry, some error occured, Please Try again.";
                }

                dispatch({
                    type: actionTypes.NORMAL_FAIL,
                    payload: {
                        message: message,
                    },
                });
            });
    };
};

export const getAppointmentDetails = (appointment_id) => {
    return (dispatch, getState) => {
        dispatch({ type: actionTypes.CLEAR_ERROR });

        let axiosOptions = {
            method: "POST",
            url: `${process.env.REACT_APP_DATABASE_URI}/getappointmentdetails`,
            data: {
                app_id: appointment_id,
            },
            headers: {
                authorization: `Basic ${JSON.parse(
                    localStorage.getItem("authToken")
                )}`,
            },
        };

        axios(axiosOptions)
            .then((response) => {
                let appointment_details = response.data.appointment_details;
                dispatch({
                    type: actionTypes.LOAD_APPOINTMENT_DETAILS,
                    payload: {
                        appointment_details: appointment_details,
                    },
                });
            })
            .catch((error) => {
                let message = null;
                try {
                    message = error.response.data.message;
                } catch {
                    message = "Sorry, some error occured, Please Try again.";
                }

                dispatch({
                    type: actionTypes.NORMAL_FAIL,
                    payload: {
                        message: message,
                    },
                });
            });
    };
};

let related_doctors = [
    {
        doctor_id: 1,
        doctor_name: "Ironman",
        department: "Dental",
        experience: 2, // has to be calculated from the joining date
        room_no: 101,
        appointment_fee: 100,
        specialisation: ["Tooth Replacement", "Tooth filling"],
    },
    {
        doctor_id: 2,
        doctor_name: "Steve",
        department: "Ortho",
        experience: 2, // has to be calculated from the joining date
        room_no: 102,
        appointment_fee: 200,
        specialisation: ["Bone fractures", "NonHuman leg fitment"],
    },
    {
        doctor_id: 3,
        doctor_name: "Steven",
        department: "Nephrology",
        experience: 2, // has to be calculated from the joining date
        room_no: 103,
        appointment_fee: 300,
        specialisation: ["Kideny Osmosliss", "Kidney Replacement"],
    },
];

let area_of_diseases = [
    {
        disease_id: 1,
        disease_name: "Leg Bone Ortho",
    },
    {
        disease_id: 2,
        disease_name: "Kidney Malfunction",
    },
];

let sample_session_details_obj = {
    session_id: 1,
    last_updated_time: "09:54:12, 8 March 2022",
    session_start_time: "09:54:12, 7 March 2022",
    patient_name: "Robert",
    patient_id: 8965,
    area_of_diseases: "Respiratory problems, Eye Infection, Joint Problems",
    description: `Details regarding the session : Like the description that is given by
    the patient etc.. Lorem Ipsum has been the industry's standard dummy
    text ever since the 1500s, when an unknown printer took a galley of type
    and scrambled it to make a type specimen book. It has survived not only
    five centuries, but also the leap into electronic typesetting, remaining
    essentially unchanged.`,
    appointments: [
        {
            appointment_time: "09:54:12, 7 March 2022",
            doctor_name: "Dr. Surapaneni Ramesh Babu",
            appointment_id: 13414,
            description: `Details regarding the appointment : Like the
                description that is given by the doctor etc.. Lorem
                Ipsum has been the industry's standard dummy text
                ever since the 1500s, when an unknown printer took a
                galley of type and scrambled it to make a type
                specimen book. It has survived not only five
                centuries, but also the leap into electronic
                typesetting, remaining essentially unchanged.`,
            active_or_not: false,
        },
        {
            appointment_time: "09:54:12, 7 March 2022",
            doctor_name: "Dr. Shoban Babu",
            appointment_id: 41413,
            description: `Details regarding the appointment : Like the
                description that is given by the doctor etc.. Lorem
                Ipsum has been the industry's standard dummy text
                ever since the 1500s, when an unknown printer took a
                galley of type and scrambled it to make a type
                specimen book. It has survived not only five
                centuries, but also the leap into electronic
                typesetting, remaining essentially unchanged.`,
            active_or_not: false,
        },
    ],
    bill_generation_status: false,
    bill_payment_status: false,
};

let sample_session_obj = {
    session_id: 1,
    last_updated_time: "09:54:12, 8 March 2022",
    session_start_time: "09:54:12, 7 March 2022",
    patient_name: "Robert",
    patient_id: 8965,
    description: `Details regarding the session : Like the description that is given by
    the patient etc.. Lorem Ipsum has been the industry's standard dummy
    text ever since the 1500s, when an unknown printer took a galley of type
    and scrambled it to make a type specimen book. It has survived not only
    five centuries, but also the leap into electronic typesetting, remaining
    essentially unchanged.`,
    active_or_not: false,
};
