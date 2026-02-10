import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.detail || error.message || 'An error occurred';
    return Promise.reject(new Error(message));
  }
);

// Employee API
export const employeeAPI = {
  getAll: () => api.get('/employees'),
  getAllWithStats: () => api.get('/employees/with-stats'),
  getById: (id) => api.get(`/employees/${id}`),
  create: (data) => api.post('/employees', data),
  delete: (id) => api.delete(`/employees/${id}`),
};

// Attendance API
export const attendanceAPI = {
  getAll: (params) => api.get('/attendance', { params }),
  getByEmployee: (employeeId) => api.get(`/attendance/employee/${employeeId}`),
  create: (data) => api.post('/attendance', data),
  getDashboard: () => api.get('/attendance/dashboard'),
};

export default api;
