import React, { useEffect } from 'react';
import { useOAuth2 } from '../contexts/OAuth2Context';

const OAuth2Callback = () => {
    const { handleCallback } = useOAuth2();

    useEffect(() => {
        const query = new URLSearchParams(window.location.search);
        const code = query.get('code');
        if (code) {
            handleCallback(code);
        }
    }, [handleCallback]);

    return <div>Processing...</div>;
};

export default OAuth2Callback;
