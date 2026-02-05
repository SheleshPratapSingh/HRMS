import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL;

const EmployeeManagement = () => {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [formData, setFormData] = useState({
    employee_id: '',
    full_name: '',
    email: '',
    department: ''
  });

  useEffect(() => {
    fetchEmployees();
  }, []);

  const fetchEmployees = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/api/employees/`);
      setEmployees(response.data);
    } catch (error) {
      setError('Failed to fetch employees');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      await axios.post(`${API_BASE_URL}/api/employees/`, formData);
      setSuccess('Employee added successfully!');
      setFormData({
        employee_id: '',
        full_name: '',
        email: '',
        department: ''
      });
      fetchEmployees();
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
          setError(errorMessages || 'Failed to add employee');
        } else {
          setError(errorData.error || errorData.message || 'Failed to add employee');
        }
      } else {
        setError('Failed to add employee');
      }
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this employee?')) {
      return;
    }

    try {
      await axios.delete(`${API_BASE_URL}/api/employees/${id}/`);
      setSuccess('Employee deleted successfully!');
      fetchEmployees();
      setTimeout(() => setSuccess(''), 3000);
    } catch (error) {
      setError('Failed to delete employee');
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div data-testid="employee-management-page">
      <div className="page-header">
        <h1 className="page-title">Employee Management</h1>
        <p className="page-subtitle">Manage your organization's employees</p>
      </div>

      <div className="card" style={{ marginBottom: '2rem' }}>
        <div className="card-header">
          <h2 className="card-title">Add New Employee</h2>
        </div>
        <div className="card-body">
          {error && (
            <div className="error-message" data-testid="employee-error-message">
              <span>⚠️</span>
              {error}
            </div>
          )}
          {success && (
            <div className="success-message" data-testid="employee-success-message">
              <span>✓</span>
              {success}
            </div>
          )}

          <form onSubmit={handleSubmit} data-testid="add-employee-form">
            <div className="form-grid">
              <div className="form-group">
                <label className="form-label">Employee ID</label>
                <input
                  type="text"
                  name="employee_id"
                  className="form-input"
                  value={formData.employee_id}
                  onChange={handleChange}
                  placeholder="EMP001"
                  required
                  data-testid="input-employee-id"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Full Name</label>
                <input
                  type="text"
                  name="full_name"
                  className="form-input"
                  value={formData.full_name}
                  onChange={handleChange}
                  placeholder="John Doe"
                  required
                  data-testid="input-full-name"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Email</label>
                <input
                  type="email"
                  name="email"
                  className="form-input"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="john.doe@company.com"
                  required
                  data-testid="input-email"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Department</label>
                <input
                  type="text"
                  name="department"
                  className="form-input"
                  value={formData.department}
                  onChange={handleChange}
                  placeholder="Engineering"
                  required
                  data-testid="input-department"
                />
              </div>
            </div>

            <button type="submit" className="btn btn-primary" data-testid="btn-add-employee">
              Add Employee
            </button>
          </form>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">All Employees</h2>
        </div>
        <div className="card-body" style={{ padding: 0 }}>
          {loading ? (
            <div className="loading" data-testid="employees-loading">Loading employees...</div>
          ) : employees.length === 0 ? (
            <div className="empty-state" data-testid="employees-empty-state">
              <div className="empty-icon">👥</div>
              <div className="empty-text">No employees found</div>
              <div className="empty-subtext">Add your first employee to get started</div>
            </div>
          ) : (
            <div className="table-container">
              <table className="table" data-testid="employees-table">
                <thead>
                  <tr>
                    <th>Employee ID</th>
                    <th>Full Name</th>
                    <th>Email</th>
                    <th>Department</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {employees.map((employee) => (
                    <tr key={employee.id} data-testid={`employee-row-${employee.id}`}>
                      <td>{employee.employee_id}</td>
                      <td>{employee.full_name}</td>
                      <td>{employee.email}</td>
                      <td>{employee.department}</td>
                      <td>
                        <button
                          onClick={() => handleDelete(employee.id)}
                          className="btn btn-danger"
                          style={{ padding: '0.5rem 1rem', fontSize: '0.875rem' }}
                          data-testid={`btn-delete-employee-${employee.id}`}
                        >
                          Delete
                        </button>
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

export default EmployeeManagement;