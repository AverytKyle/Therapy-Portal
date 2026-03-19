import { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { login } from "../../redux/session"; // Import the login action creator
import "./LoginPage.css";

const LoginPage = () => {
    const user = useSelector((state) => state.session.user);
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [pin, setPin] = useState("");
    const [error, setError] = useState(null);
    const dispatch = useDispatch();

    useEffect(() => {
        if (user) {
            navigate("/dashboard");
        }
    }, [user, navigate]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        const loginAction = await dispatch(login(username, pin));
        if (loginAction) {
            if (user.role === "SCHEDULER" || user.role === "PROVIDER") {
                navigate("/schedule");
            } else {
                navigate("/dashboard");
            }
        } else {
            setError("Invalid username or PIN. Please try again.");
        }
    };

    return (
        <div className="login-page">
            <h2>Login</h2>
            <form onSubmit={handleSubmit} className="login-form">
                <div className="form-group">
                    <label htmlFor="username">Username:</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="pin">PIN:</label>
                    <input
                        type="password"
                        id="pin"
                        value={pin}
                        onChange={(e) => setPin(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="login-button">Login</button>
            </form>
        </div>
    );
};

export default LoginPage;