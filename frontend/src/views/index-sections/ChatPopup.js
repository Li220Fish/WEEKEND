import React, { useState, useEffect } from 'react';
import 'D:/weekend/frontend/src/assets/css/ChatPopup.css'; // Import the CSS file for styling

const ChatPopup = ({ onClose }) => {
    const [inputValue, setInputValue] = useState(''); // State to store input value
    const [messages, setMessages] = useState([]); // State to store chat messages
    const [inputSp, setInputSp] = useState('#0');

    useEffect(() => {
        const storedMessages = localStorage.getItem('chatMessages');
        if (storedMessages) {
            setMessages(JSON.parse(storedMessages));
        }
    }, []); // Load stored messages on component mount

    useEffect(() => {
        // Clear chat messages from local storage when the component mounts for the first time
        localStorage.removeItem('chatMessages');
    }, []); // Run only on component mount

    useEffect(() => {
        // Scroll to the bottom of the chat messages container when messages change
        const chatMessagesContainer = document.getElementById('chat-messages-container');
        if (chatMessagesContainer) {
            chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
        }
    }, [messages]); // Scroll on messages change

    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (inputValue.trim() !== '') {
            const newUserMessage = inputValue;
            const newMessages = [...messages, { text: newUserMessage, type: 'user' }];
            setMessages(newMessages);
            try {
                const response = await fetch('/chat_bot', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ "message": inputSp + newUserMessage, "Sp": inputSp })
                });

                if (response.ok) {
                    const data = await response.json();
                    const newReplyMessage = { text: data.Message, type: 'reply' };
                    setInputSp(data.Special);
                    setMessages(prevMessages => [...prevMessages, newReplyMessage]);
                    localStorage.setItem('chatMessages', JSON.stringify([...newMessages, newReplyMessage]));
                } else {
                    console.error('Failed to fetch reply from server.');
                }
            } catch (error) {
                console.error('Error fetching reply from server:', error);
            }

            setInputValue('');
        }
    };

    const handleClose = () => {
        onClose();
    };

    return (
        <div className="chat-popup">
            <div className="chat-header">
                <span>Chat</span>
                <button className="close-btn" onClick={handleClose}>×</button>
            </div>

            <div id="chat-messages-container" className="chat-messages">
                {messages.map((message, index) => (
                    <div className={message.type === 'user' ? 'user-message' : 'reply-message'} key={index}>
                        {message.text}
                    </div>
                ))}
            </div>

            <form onSubmit={handleSubmit} className="chat-form">
                <input
                    type="text"
                    value={inputValue}
                    onChange={handleInputChange}
                    placeholder="Type your message..."
                />
                <button type="submit">Send</button>
            </form>
        </div>
    );
};

export default ChatPopup;
