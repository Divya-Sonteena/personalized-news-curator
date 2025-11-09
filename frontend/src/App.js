import React, { useState, useEffect } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import LandingPage from "./components/LandingPage";
import Register from "./components/Register";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import { getToken, setToken, clearToken, getUserId } from "./api/api";

function App() {
  const [userId, setUserId] = useState(getUserId());
  const navigate = useNavigate();

  useEffect(() => {
    setUserId(getUserId());
  }, []);

  function handleLogin(token, uid) {
    setToken(token, uid);
    setUserId(uid);
    navigate("/dashboard");
  }

  function handleLogout() {
    clearToken();
    setUserId(null);
    navigate("/");
  }

  return (
    <div className="app-root">
      <Routes>
        <Route path="/" element={<LandingPage user={userId} onLogout={handleLogout} />} />
        <Route path="/register" element={<Register onRegistered={handleLogin} />} />
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route path="/dashboard" element={<Dashboard userId={userId} onLogout={handleLogout} />} />
      </Routes>
    </div>
  );
}

export default App;
