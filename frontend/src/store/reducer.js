import * as actionTypes from "./actions/actionTypes";

const initialState = {
    userId: null,
    username: null,
    // userEmail: null,
    userType: null,
    userProfile: {},

    authSuccess: null,
    authError: null,
    errorMsg: null,
    successMsg: null,

    sessions: [],
    session_details: null,
    appointment_details: null,
    area_of_diseases: [],
    related_doctors: [],

    all_medicines: [],
    all_treatments: [],
    all_doctors: [],

    // searchedNames: [],
    // searchError: null,

    // searchedProfile: null,
    // profileError: null,

    // messages: {},
    // notices: {},
    // positions: {},
    // unread_positions: {},
    // unreleasedpositions: {},
    // applications: {},
    // notifications: {},

    // currentPosApplications: [],
    // currentPosFeedbacks: [],
    // current_application: null,

    // notificationsInterval: null,
    // lastDataFetchStamp: 0,
};

const reducer = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.AUTH_START:
            return {
                ...state,
                userId: null,
                username: null,
                // email: null,
                userType: null,
                authError: null,
                successMsg: null,
            };

        case actionTypes.AUTH_FAIL:
            return {
                ...state,
                authError:
                    action.payload.message === undefined
                        ? "Try Again ! Not Connected to Internet."
                        : action.payload.message,
            };

        case actionTypes.NORMAL_FAIL:
            return {
                ...state,
                errorMsg:
                    action.payload.message === undefined
                        ? "Try Again ! Not Connected to Internet."
                        : action.payload.message,
            };

        case actionTypes.AUTH_LOGIN:
            localStorage.setItem(
                "authToken",
                JSON.stringify(action.payload.authToken)
            );
            return {
                ...state,
                username: action.payload.username,
                // userEmail: action.payload.userEmail,
                userId: action.payload.userId,
                userProfile: { ...action.payload.profile },
                userType: action.payload.userType,
                successMsg: action.payload.message,
            };

        case actionTypes.AUTH_LOGOUT:
            localStorage.removeItem("authToken");
            return {
                ...state,
                username: null,
                // userEmail: null,
                userId: null,
                userType: null,
                successMsg: action.payload.message,
                // messages: {},
                // notices: {},
                // positions: {},
                // applications: {},
                // notifications: {},
            };
        case actionTypes.LOAD_SESSIONS:
            return {
                ...state,
                sessions: action.payload.sessions,
            };
        case actionTypes.LOAD_SESSION_DETAILS:
            return {
                ...state,
                session_details: action.payload.session_details,
            };
        case actionTypes.LOAD_APPOINTMENT_DETAILS:
            return {
                ...state,
                appointment_details: action.payload.appointment_details,
            };
        case actionTypes.LOAD_DISEASE_AREAS:
            return {
                ...state,
                area_of_diseases: action.payload.area_of_diseases,
            };
        case actionTypes.LOAD_MEDICINES:
            return {
                ...state,
                all_medicines: action.payload.all_medicines,
            };
        case actionTypes.LOAD_TREATMENTS:
            return {
                ...state,
                all_treatments: action.payload.all_treatments,
            };
        case actionTypes.LOAD_RELATED_DOCTORS:
            return {
                ...state,
                related_doctors: action.payload.related_doctors,
            };
        case actionTypes.LOAD_ALL_DOCTORS:
            return {
                ...state,
                all_doctors: action.payload.all_doctors,
            };

        case actionTypes.CLEAR_ERROR:
            return {
                ...state,
                errorMsg: null,
            };

        case actionTypes.CREATE_SESSION:
            return {
                ...state,
                successMsg: action.payload.message,
            };
        case actionTypes.GENERATE_BILL:
            return {
                ...state,
                successMsg: action.payload.message,
            };

        case actionTypes.CREATE_APPOINTMENT:
            return {
                ...state,
                successMsg: action.payload.message,
            };

        case actionTypes.ADD_MEDICINE:
            return {
                ...state,
                successMsg: action.payload.message,
            };

        case actionTypes.ADD_TREATMENT:
            return {
                ...state,
                successMsg: action.payload.message,
            };

        default:
            return state;
    }
};

export default reducer;
