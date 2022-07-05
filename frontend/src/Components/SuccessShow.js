import React from "react";
import { connect } from "react-redux";

import classes from "../App.module.css";

function SuccessShow(props) {

    console.log("Success rendering");
    return (
            <div
                className={[
                    classes.successMsg,
                    props.successMsg ? classes.show : classes.hide,
                ].join(" ")}
            >
                {props.successMsg}
            </div>
    );
}

const mapStateToProps = (state) => {
    return {
        successMsg: state.successMsg,
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(SuccessShow);
