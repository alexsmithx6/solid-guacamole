import React, { useEffect, useState } from 'react';

/**
 * Generate OAuth2 authorization URI.
 * @returns {string} - The fully constructed authorization URI.
 */
const SpotifyAuthUri = () => {
    const [authUri, setAuthUri] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchAuthUri = async () => {
            try {
                const response = await fetch('/api/users/spotify/auth_uri/');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const result = await response.json();
                setAuthUri(result.auth_uri);
            } catch (error) {
                setError(error);
            } finally {
                setLoading(false);
            }
        };

        fetchAuthUri();
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    return authUri;
}

export default SpotifyAuthUri;
