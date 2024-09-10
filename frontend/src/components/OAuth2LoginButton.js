import React from 'react';
import { useOAuth2 } from '../contexts/OAuth2Context';

const OAuth2LoginButton = () => {
    const { login } = useOAuth2();

    return (
        <button onClick={login}>
            Login with Spotify
        </button>
    );
};

export default OAuth2LoginButton;
