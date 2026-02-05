import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL;

const Dashboard = () => {
  const [stats, setStats] = useState({
    total_employees: 0,
    total_attendance_records: 0,
    today_present: 0,
    today_absent: 0
  });
  const [loading, setLoading] = useState(true);
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);

  useEffect(() => {
    fetchStats();
  }, [selectedDate]);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/api/attendance/stats/`, {
        params: { date: selectedDate }
      });
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading" data-testid="dashboard-loading">Loading dashboard...</div>;
  }

  return (
    <div data-testid="dashboard-page">
      <div className="page-header">
        <h1 className="page-title">Dashboard</h1>
        <p className="page-subtitle">Overview of your HR management system</p>
      </div>

      <div className="card" style={{ marginBottom: '2rem' }}>
        <div className="card-body">
          <div className="form-group" style={{ marginBottom: 0, maxWidth: '300px' }}>
            <label className="form-label">Select Date</label>
            <input
              type="date"
              className="form-input"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
              data-testid="dashboard-date-filter"
            />
          </div>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card" data-testid="stat-total-employees">
          <div className="stat-label">Total Employees</div>
          <div className="stat-value" style={{ color: '#667eea' }}>{stats.total_employees}</div>
        </div>
        
        <div className="stat-card" data-testid="stat-total-records">
          <div className="stat-label">Total Records</div>
          <div className="stat-value" style={{ color: '#764ba2' }}>{stats.total_attendance_records}</div>
        </div>
        
        <div className="stat-card" data-testid="stat-present-today">
          <div className="stat-label">Present ({selectedDate})</div>
          <div className="stat-value" style={{ color: '#10b981' }}>{stats.today_present}</div>
        </div>
        
        <div className="stat-card" data-testid="stat-absent-today">
          <div className="stat-label">Absent ({selectedDate})</div>
          <div className="stat-value" style={{ color: '#ef4444' }}>{stats.today_absent}</div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;