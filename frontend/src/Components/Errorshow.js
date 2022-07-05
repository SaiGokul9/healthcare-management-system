import React from "react";
import { connect } from "react-redux";

import classes from "../App.module.css";

function ErrorShow(props) {

    console.log("Error rendering");
    return (
            <div
                className={[
                    classes.errorMsg,
                    props.errorMsg ? classes.show : classes.hide,
                ].join(" ")}
            >
                {props.errorMsg}
            </div>
    );
}

const mapStateToProps = (state) => {
    return {
        errorMsg: state.errorMsg,
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(ErrorShow);
