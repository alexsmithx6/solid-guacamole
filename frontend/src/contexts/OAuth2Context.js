import React, { createContext, useContext, useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import axios from 'axios';
import { generateSpotifyAuthUri } from '../utils/OAuth2Utils';

const OAuth2Context = createContext();

export const OAuth2Provider = ({ children }) => {
    const [authState, setAuthState] = useState({
        accessToken: null,
        isAuthenticated: false,
        user: null,
    });

    useEffect(() => {
        const fetchUser = async () => {
            const token = localStorage.getItem('accessToken');
            if (token) {
                try {
                    const response = await axios.get('/api/me', {
                        headers: { Authorization: `Bearer ${token}` },
                    });
                    setAuthState({
                        accessToken: token,
                        isAuthenticated: true,
                        user: response.data,
                    });
                } catch (error) {
                    console.error('Failed to fetch user data:', error);
                    setAuthState({ accessToken: null, isAuthenticated: false, user: null });
                }
            }
        };

        fetchUser();
    }, []);

    const login = () => {
        return <Navigate to={generateSpotifyAuthUri()} />;
    };

    const handleCallback = async (code) => {
        try {
            const response = await axios.post('/api/token', { code });
            localStorage.setItem('accessToken', response.data.access_token);
            const userResponse = await axios.get('/api/me', {
                headers: { Authorization: `Bearer ${response.data.access_token}` },
            });
            setAuthState({
                accessToken: response.data.access_token,
                isAuthenticated: true,
                user: userResponse.data,
            });
        } catch (error) {
            console.error('Failed to handle OAuth2 callback:', error);
            setAuthState({ accessToken: null, isAuthenticated: false, user: null });
        }
    };

    const logout = () => {
        localStorage.removeItem('accessToken');
        setAuthState({ accessToken: null, isAuthenticated: false, user: null });
    };

    return (
        <OAuth2Context.Provider value={{ authState, login, handleCallback, logout }}>
            {children}
        </OAuth2Context.Provider>
    );
};

export const useOAuth2 = () => useContext(OAuth2Context);
