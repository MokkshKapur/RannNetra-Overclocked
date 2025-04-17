import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import IntroSection from './components/IntroSection';
import MapSection from './components/MapSection';
import StaticImageSection from './components/StaticImageSection';
import AnalyticsSection from './components/AnalyticsSection';
import ScanningPage from './components/ScanningPage';

function App() {
  return (
    <Router>
      <div className="background-animation" />
      <div className="app-container">
        <nav className="main-nav">
          <Link to="/">Home</Link>
          <Link to="/scanning">Scanning</Link>
        </nav>
        
        <Routes>
          <Route path="/scanning" element={<ScanningPage />} />
          <Route path="/" element={
            <>
              <IntroSection />
              <MapSection />
              <StaticImageSection />
              <div className="analytics-section">
                <AnalyticsSection />
              </div>
            </>
          } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;