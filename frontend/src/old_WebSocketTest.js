import React, { useState, useEffect } from 'react';

const WebSocketTest = () => {
    const [message, setMessage] = useState('');
    const [ws, setWs] = useState(null);

    useEffect(() => {
        // Create WebSocket connection
        const socket = new WebSocket('wss://localhost/ws/test/');
        // Event listeners
        socket.onopen = () => {
            console.log('WebSocket is connected.');
            setWs(socket);
        };

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setMessage(data.message);
        };

        socket.onclose = () => {
            console.log('WebSocket is closed.');
        };

        return () => {
            socket.close();
        };
    }, []);

    const sendMessage = () => {
        if (ws) {
            ws.send(JSON.stringify({ 'message': 'gday mate heres a message from react' }));
        }
    };

    return (
        <div>
            <button onClick={sendMessage}>Send Message</button>
            <p>Received message: {message}</p>
        </div>
    );
};

export default WebSocketTest;
