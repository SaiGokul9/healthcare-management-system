import React from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router";

import * as actionCreators from "../store/actions/actionCreators";

class Logout extends React.Component {
    componentDidMount() {
        this.props.logout();
    }

    render() {
        // return <Redirect to="/login" exact />;
        return <div>""</div>
    }
}

const mapStateToProps = (state) => {
    return {};
};

const mapDispatchToProps = (dispatch) => {
    return {
        logout: () => {
            dispatch(actionCreators.logout());
        },
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(Logout);
