# HRMS Lite - Human Resource Management System

A lightweight, production-ready Human Resource Management System built with FastAPI, React, and PostgreSQL.

## 🚀 Features

- **Employee Management**: Add, view, and delete employee records
- **Attendance Tracking**: Mark and view daily attendance with date filtering
- **Dashboard**: Real-time statistics and metrics
- **Responsive UI**: Modern, professional interface built with React and Tailwind CSS
- **RESTful API**: Well-documented FastAPI backend with automatic Swagger docs
- **Production Ready**: Docker support, error handling, validation, and security headers

## 🛠️ Tech Stack

### Frontend
- React 18
- React Router v6
- Axios for API calls
- Tailwind CSS for styling
- Vite for build tooling
- Lucide React for icons
- date-fns for date formatting

### Backend
- Python 3.11
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- Pydantic for validation
- Uvicorn (ASGI server)

### DevOps
- Docker & Docker Compose
- Multi-stage builds
- Nginx for frontend serving
- Health checks

## 📋 Prerequisites

- Docker and Docker Compose installed
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)
- PostgreSQL 16+ (for local development without Docker)

3. **Access the application**
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs

## 💻 Local Development Setup

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. **Run the backend**
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API URL
```

4. **Run the development server**
```bash
npm run dev
```

## 🗄️ Database Schema

### Employees Table
- `id` (UUID, Primary Key)
- `employee_id` (String, Unique)
- `full_name` (String)
- `email` (String, Unique)
- `department` (String)

**Indexes**: employee_id, email, full_name, department

### Attendance Table
- `id` (UUID, Primary Key)
- `employee_id` (UUID, Foreign Key → employees.id, CASCADE)
- `date` (Date)
- `status` (Enum: Present/Absent)

**Constraints**: 
- Unique constraint on (employee_id, date)
- Foreign key with CASCADE delete

**Indexes**: date, status, (employee_id, date)

## 📡 API Endpoints

### Employees
- `GET /api/employees` - Get all employees
- `GET /api/employees/with-stats` - Get employees with attendance stats
- `GET /api/employees/{id}` - Get employee by ID
- `POST /api/employees` - Create new employee
- `DELETE /api/employees/{id}` - Delete employee

### Attendance
- `GET /api/attendance` - Get all attendance records
- `GET /api/attendance?date_filter=2024-01-01` - Filter by date
- `GET /api/attendance/employee/{id}` - Get employee attendance
- `POST /api/attendance` - Mark attendance
- `GET /api/attendance/dashboard` - Get dashboard statistics

### Health
- `GET /health` - Health check endpoint

## 🔒 Security Features

- CORS configuration
- Input validation with Pydantic
- SQL injection prevention (SQLAlchemy ORM)
- XSS protection headers
- Email format validation
- Unique constraint enforcement

## 🏗️ Project Structure

```
hrms-lite/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── employees.py
│   │   │   └── attendance.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud_employee.py
│   │   ├── crud_attendance.py
│   │   └── main.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Button.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Input.jsx
│   │   │   ├── Modal.jsx
│   │   │   ├── Layout.jsx
│   │   │   ├── Loading.jsx
│   │   │   ├── EmptyState.jsx
│   │   │   └── ErrorMessage.jsx
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Employees.jsx
│   │   │   └── Attendance.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── vite.config.js
└── docker-compose.yml
```

## 🎯 Key Features Implementation

### UUID Primary Keys
All tables use UUID for distributed system compatibility and security.

### Foreign Key Constraints
Attendance records cascade delete when employee is removed.

### Indexes
Strategic indexes on frequently queried columns for optimal performance.

### Multi-stage Docker Builds
Both frontend and backend use multi-stage builds to minimize image size.

### Error Handling
- Global exception handlers
- Validation error messages
- User-friendly error states in UI

### Loading & Empty States
- Loading indicators during API calls
- Empty state messages when no data
- Error boundaries for failed requests

## 🚀 Deployment

### Backend Deployment (Render/Railway)

1. Create a new Web Service
2. Connect your GitHub repository
3. Set environment variables:
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `CORS_ORIGINS`: Your frontend URL
   - `ENVIRONMENT`: production

4. Deploy command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Frontend Deployment (Vercel/Netlify)

1. Create a new project
2. Connect your GitHub repository
3. Set build settings:
   - Build command: `npm run build`
   - Output directory: `dist`
   - Environment variable: `VITE_API_URL` = your backend URL

### Database (Render PostgreSQL / Neon)

1. Create a PostgreSQL instance
2. Copy the connection string
3. Use it in backend's `DATABASE_URL`

## ⚙️ Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
CORS_ORIGINS=http://localhost:3000,https://your-frontend.com
ENVIRONMENT=production
```

### Frontend (.env)
```
VITE_API_URL=https://your-backend-api.com
```

## 📊 Performance Optimizations

- Database query optimization with eager loading
- Frontend code splitting
- Static asset caching with Nginx
- Gzip compression
- Connection pooling in database

## 🧪 Testing the Application

1. **Add an employee**
   - Go to Employees page
   - Click "Add Employee"
   - Fill in the form
   - Submit

2. **Mark attendance**
   - Go to Attendance page
   - Click "Mark Attendance"
   - Select employee, date, and status
   - Submit

3. **View dashboard**
   - Go to Dashboard
   - See real-time statistics

4. **Filter attendance**
   - Go to Attendance page
   - Use date filter to view specific dates

## 🐛 Troubleshooting

### Database connection issues
- Ensure PostgreSQL is running
- Check DATABASE_URL format
- Verify network connectivity

### CORS errors
- Add frontend URL to CORS_ORIGINS
- Check API URL in frontend .env

### Docker build failures
- Clear Docker cache: `docker-compose down -v`
- Rebuild: `docker-compose up --build --force-recreate`

## 📝 Assumptions & Limitations

- Single admin user (no authentication)
- No leave management
- No payroll features
- Attendance can only be marked for past/present dates
- One attendance record per employee per day

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📄 License

This project is licensed under the MIT License.

## 👥 Author

Shreya Sai - Full Stack Developer

## 🙏 Acknowledgments

- FastAPI documentation
- React documentation
- Tailwind CSS
- PostgreSQL community
