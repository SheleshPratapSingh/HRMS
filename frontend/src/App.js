import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import EmployeeManagement from './components/EmployeeManagement';
import AttendanceManagement from './components/AttendanceManagement';
import './App.css';

function Navigation() {
  const location = useLocation();
  
  const isActive = (path) => location.pathname === path;
  
  return (
    <nav className="nav-container">
      <div className="nav-content">
        <div className="nav-brand">
          <div className="brand-icon">H</div>
          <span className="brand-text">HRMS Lite</span>
        </div>
        <div className="nav-links">
          <Link 
            to="/" 
            className={`nav-link ${isActive('/') ? 'active' : ''}`}
            data-testid="nav-dashboard"
          >
            Dashboard
          </Link>
          <Link 
            to="/employees" 
            className={`nav-link ${isActive('/employees') ? 'active' : ''}`}
            data-testid="nav-employees"
          >
            Employees
          </Link>
          <Link 
            to="/attendance" 
            className={`nav-link ${isActive('/attendance') ? 'active' : ''}`}
            data-testid="nav-attendance"
          >
            Attendance
          </Link>
        </div>
      </div>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="app">
        <Navigation />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/employees" element={<EmployeeManagement />} />
            <Route path="/attendance" element={<AttendanceManagement />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;