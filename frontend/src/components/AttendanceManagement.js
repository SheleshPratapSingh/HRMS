import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL;

const AttendanceManagement = () => {
  const [employees, setEmployees] = useState([]);
  const [selectedEmployee, setSelectedEmployee] = useState('');
  const [attendanceRecords, setAttendanceRecords] = useState([]);
  const [totalPresentDays, setTotalPresentDays] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [dateFilter, setDateFilter] = useState('');
  const [formData, setFormData] = useState({
    employee: '',
    date: new Date().toISOString().split('T')[0],
    status: 'Present'
  });

  useEffect(() => {
    fetchEmployees();
  }, []);

  const fetchEmployees = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/employees/`);
      setEmployees(response.data);
    } catch (error) {
      console.error('Error fetching employees:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      await axios.post(`${API_BASE_URL}/api/attendance/`, formData);
      setSuccess('Attendance marked successfully!');
      setFormData({
        employee: '',
        date: new Date().toISOString().split('T')[0],
        status: 'Present'
      });
      if (selectedEmployee) {
        fetchAttendance(selectedEmployee, dateFilter);
      }
      setTimeout(() => setSuccess(''), 3000);
    } catch (error) {
      if (error.response && error.response.data) {
        const errorData = error.response.data;
        if (typeof errorData === 'object') {
          const errorMessages = Object.entries(errorData)
            .map(([key, value]) => {
              if (Array.isArray(value)) {
                return `${key}: ${value.join(', ')}`;
              }
              return `${key}: ${value}`;
            })
            .join(' | ');
          setError(errorMessages || 'Failed to mark attendance');
        } else {
          setError(errorData.error || errorData.message || 'Failed to mark attendance');
        }
      } else {
        setError('Failed to mark attendance');
      }
    }
  };

  const fetchAttendance = async (employeeId, date = '') => {
    if (!employeeId) return;

    try {
      setLoading(true);
      const params = date ? { date } : {};
      const response = await axios.get(`${API_BASE_URL}/api/attendance/${employeeId}/`, { params });
      setAttendanceRecords(response.data.attendance);
      setTotalPresentDays(response.data.total_present_days);
    } catch (error) {
      setError('Failed to fetch attendance records');
    } finally {
      setLoading(false);
    }
  };

  const handleEmployeeSelect = (employeeId) => {
    setSelectedEmployee(employeeId);
    setDateFilter('');
    if (employeeId) {
      fetchAttendance(employeeId);
    } else {
      setAttendanceRecords([]);
      setTotalPresentDays(0);
    }
  };

  const handleDateFilterChange = (date) => {
    setDateFilter(date);
    if (selectedEmployee) {
      fetchAttendance(selectedEmployee, date);
    }
  };

  return (
    <div data-testid="attendance-management-page">
      <div className="page-header">
        <h1 className="page-title">Attendance Management</h1>
        <p className="page-subtitle">Track and manage employee attendance</p>
      </div>

      <div className="card" style={{ marginBottom: '2rem' }}>
        <div className="card-header">
          <h2 className="card-title">Mark Attendance</h2>
        </div>
        <div className="card-body">
          {error && (
            <div className="error-message" data-testid="attendance-error-message">
              <span>⚠️</span>
              {error}
            </div>
          )}
          {success && (
            <div className="success-message" data-testid="attendance-success-message">
              <span>✓</span>
              {success}
            </div>
          )}

          <form onSubmit={handleSubmit} data-testid="mark-attendance-form">
            <div className="form-grid">
              <div className="form-group">
                <label className="form-label">Employee</label>
                <select
                  name="employee"
                  className="form-select"
                  value={formData.employee}
                  onChange={(e) => setFormData({ ...formData, employee: e.target.value })}
                  required
                  data-testid="select-employee-attendance"
                >
                  <option value="">Select Employee</option>
                  {employees.map((emp) => (
                    <option key={emp.id} value={emp.id}>
                      {emp.employee_id} - {emp.full_name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Date</label>
                <input
                  type="date"
                  name="date"
                  className="form-input"
                  value={formData.date}
                  onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                  required
                  data-testid="input-attendance-date"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Status</label>
                <select
                  name="status"
                  className="form-select"
                  value={formData.status}
                  onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                  required
                  data-testid="select-attendance-status"
                >
                  <option value="Present">Present</option>
                  <option value="Absent">Absent</option>
                </select>
              </div>
            </div>

            <button type="submit" className="btn btn-primary" data-testid="btn-mark-attendance">
              Mark Attendance
            </button>
          </form>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Attendance Records</h2>
        </div>
        <div className="card-body">
          <div className="filter-group">
            <div className="form-group" style={{ flex: 1, marginBottom: 0 }}>
              <label className="form-label">Select Employee</label>
              <select
                className="form-select"
                value={selectedEmployee}
                onChange={(e) => handleEmployeeSelect(e.target.value)}
                data-testid="filter-employee-select"
              >
                <option value="">Select Employee</option>
                {employees.map((emp) => (
                  <option key={emp.id} value={emp.id}>
                    {emp.employee_id} - {emp.full_name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group" style={{ flex: 1, marginBottom: 0 }}>
              <label className="form-label">Filter by Date</label>
              <input
                type="date"
                className="form-input"
                value={dateFilter}
                onChange={(e) => handleDateFilterChange(e.target.value)}
                disabled={!selectedEmployee}
                data-testid="filter-date-input"
              />
            </div>

            {dateFilter && (
              <button
                className="btn btn-secondary"
                onClick={() => handleDateFilterChange('')}
                style={{ marginTop: '1.75rem' }}
                data-testid="btn-clear-date-filter"
              >
                Clear Filter
              </button>
            )}
          </div>

          {selectedEmployee && (
            <div className="stat-card" style={{ marginBottom: '1.5rem' }} data-testid="total-present-days-card">
              <div className="stat-label">Total Present Days</div>
              <div className="stat-value" style={{ color: '#10b981' }}>{totalPresentDays}</div>
            </div>
          )}

          {loading ? (
            <div className="loading" data-testid="attendance-records-loading">Loading attendance records...</div>
          ) : !selectedEmployee ? (
            <div className="empty-state" data-testid="attendance-empty-no-employee">
              <div className="empty-icon">📋</div>
              <div className="empty-text">Select an employee</div>
              <div className="empty-subtext">Choose an employee to view their attendance records</div>
            </div>
          ) : attendanceRecords.length === 0 ? (
            <div className="empty-state" data-testid="attendance-empty-no-records">
              <div className="empty-icon">📋</div>
              <div className="empty-text">No attendance records found</div>
              <div className="empty-subtext">Mark attendance to get started</div>
            </div>
          ) : (
            <div className="table-container">
              <table className="table" data-testid="attendance-records-table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Employee ID</th>
                    <th>Employee Name</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {attendanceRecords.map((record) => (
                    <tr key={record.id} data-testid={`attendance-record-${record.id}`}>
                      <td>{record.date}</td>
                      <td>{record.employee_id}</td>
                      <td>{record.employee_name}</td>
                      <td>
                        <span className={`badge ${record.status === 'Present' ? 'badge-success' : 'badge-danger'}`}>
                          {record.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AttendanceManagement;