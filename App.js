import React from 'react';
import './App.css';
import ChatWidget from './ChatWidget';

function App() {
  return (
    <div className="App">
      {/* Your main web application content goes here */}
      <header className="App-header">
        <h1>My Thermal Plant Simulator</h1>
      </header>
      <ChatWidget />
    </div>
  );
}

export default App;