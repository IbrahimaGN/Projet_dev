import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';
import PromptDetail from './components/PromptDetail';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/consulter/:id" element={<PromptDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
