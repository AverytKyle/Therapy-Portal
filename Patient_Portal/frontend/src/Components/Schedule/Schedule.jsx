import { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";

const Schedule = () => {
    const user = useSelector((state) => state.session.user);
    const navigate = useNavigate();

    useEffect(() => {
        if (!user) {
            navigate("/");
        }
    }, [user, navigate]);

    return (
        <div>
            <h1>Schedule Page</h1>
            {/* Schedule content goes here */}
        </div>
    );
};

export default Schedule;