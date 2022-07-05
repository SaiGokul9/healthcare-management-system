import React from "react";
import ReactDOM from "react-dom";
import thunk from "redux-thunk";
import { BrowserRouter } from "react-router-dom";
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";

import "./index.css";
import App from "./App";

import reducer from "./store/reducer";
import reportWebVitals from "./reportWebVitals";

const store = createStore(reducer, applyMiddleware(thunk));

{
    /* <React.StrictMode> */
}
ReactDOM.render(
    <Provider store={store}>
        <BrowserRouter>
            <App />
        </BrowserRouter>
    </Provider>,
    document.getElementById("root")
);
// </React.StrictMode>,

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
