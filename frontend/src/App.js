import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { OAuth2Provider, useOAuth2 } from './contexts/OAuth2Context';
import OAuth2LoginButton from './components/OAuth2LoginButton';
import OAuth2Callback from './pages/OAuth2Callback';

const HomePage = () => {
    const { authState, logout } = useOAuth2();

    return (
        <div>
            <h1>Welcome, {authState.user ? authState.user.name : 'User'}</h1>
            <button onClick={logout}>Logout</button>
        </div>
    );
};

const App = () => {

    return (
        <OAuth2Provider>
            <Router>
                <Routes>
                    <Route path="/login" element={<OAuth2LoginButton />} />
                    <Route path="/callback" element={<OAuth2Callback />} />
                    <Route path="/home" element={<HomePage />} />
                    <Route path="*" element={<Navigate to="/home" replace />} />
                </Routes>
            </Router>
        </OAuth2Provider>
    );
};

export default App;
