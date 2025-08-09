import React, { useState } from 'react';
import './ChatWidget.css'; // You'll create this file in the next step

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { type: 'text', payload: { message: "Hello! I'm here to help with thermal-plant efficiency forecasting." } }
  ]);
  const [input, setInput] = useState('');

  const handleSend = async () => {
    if (input.trim() === '') return;

    const userMessage = { type: 'text', payload: { message: input, isUser: true } };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    try {
      // Send the user's message to your Flask backend
      const response = await fetch('http://127.0.0.1:8080/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const botResponse = await response.json();
      setMessages((prevMessages) => [...prevMessages, botResponse]);

    } catch (error) {
      console.error('Failed to fetch:', error);
      setMessages((prevMessages) => [...prevMessages, { type: 'text', payload: { message: "Sorry, something went wrong. Please try again." } }]);
    }

    setInput('');
  };

  const renderMessage = (msg, index) => {
    if (msg.type === 'simulation') {
      const { efficiency_change, new_generation_mw, message } = msg.payload;
      return (
        <div key={index} className="bot-message simulation-response">
          <p>
            **Simulation Results**
          </p>
          <p>{message}</p>
          <ul>
            <li>Efficiency Change: {efficiency_change}</li>
            <li>New Generation: {new_generation_mw} MW</li>
          </ul>
        </div>
      );
    } else {
      return (
        <div key={index} className={`message ${msg.payload.isUser ? 'user-message' : 'bot-message'}`}>
          {msg.payload.message}
        </div>
      );
    }
  };

  return (
    <div className="chat-container">
      <div className={`chat-widget ${isOpen ? 'open' : ''}`}>
        <div className="chat-header" onClick={() => setIsOpen(!isOpen)}>
          Chatbot
        </div>
        <div className="chat-body">
          <div className="message-list">
            {messages.map(renderMessage)}
          </div>
          <div className="chat-input-area">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Type your message..."
            />
            <button onClick={handleSend}>Send</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatWidget;