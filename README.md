# HRMS Lite - HR Management System

A modern, production-ready HRMS (Human Resource Management System) built with Django REST Framework and React. This system allows administrators to manage employee records and track daily attendance.

## 🚀 Features

### Employee Management
- Add new employees with unique employee IDs
- View all employees in a clean, organized table
- Delete employees with confirmation
- Automatic validation for duplicate employee IDs and emails
- Email format validation

### Attendance Management
- Mark daily attendance (Present/Absent)
- View attendance records per employee
- Filter attendance by date
- Track total present days for each employee
- Prevent duplicate attendance entries for same employee and date

### Dashboard
- Real-time statistics overview
- Total employees count
- Total attendance records
- Daily present/absent counts
- Date-based filtering for attendance stats

## 🛠️ Tech Stack

### Backend
- **Python 3.11**
- **Django 5.0.6** - Web framework
- **Django REST Framework 3.15.1** - RESTful API
- **PostgreSQL** - Production database (SQLite for local dev)
- **Gunicorn** - WSGI HTTP Server

### Frontend
- **React 19** - UI library
- **React Router DOM** - Navigation
- **Axios** - HTTP client
- **CSS3** - Modern minimal design
- **Google Fonts** (Manrope, Inter) - Typography

## 📁 Project Structure

```
/app/
├── backend/
│   ├── hrms/                    # Django project
│   │   ├── settings.py         # Configuration
│   │   ├── urls.py             # URL routing
│   │   ├── wsgi.py             # WSGI config
│   │   └── exception_handler.py # Custom error handling
│   ├── employees/              # Employee app
│   │   ├── models.py           # Employee model
│   │   ├── serializers.py      # DRF serializers
│   │   ├── views.py            # API views
│   │   └── urls.py             # Employee routes
│   ├── attendance/             # Attendance app
│   │   ├── models.py           # Attendance model
│   │   ├── serializers.py      # DRF serializers
│   │   ├── views.py            # API views
│   │   └── urls.py             # Attendance routes
│   ├── manage.py               # Django CLI
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # Environment variables
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.js
│   │   │   ├── EmployeeManagement.js
│   │   │   └── AttendanceManagement.js
│   │   ├── App.js              # Main component
│   │   ├── App.css             # Global styles
│   │   └── index.js            # Entry point
│   ├── package.json            # Node dependencies
│   └── .env                    # Frontend config
└── README.md
```

## 🔌 API Endpoints

### Employees
- `GET /api/employees/` - Get all employees
- `POST /api/employees/` - Create new employee
- `DELETE /api/employees/<id>/` - Delete employee

### Attendance
- `POST /api/attendance/` - Mark attendance
- `GET /api/attendance/<employee_id>/` - Get employee attendance records
  - Query param: `?date=YYYY-MM-DD` (optional filter)
- `GET /api/attendance/stats/` - Get dashboard statistics
  - Query param: `?date=YYYY-MM-DD` (for daily stats)

## 🚀 Local Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (or SQLite for quick start)

### Backend Setup

1. Navigate to backend directory:
```bash
cd /app/backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables in `.env`:
```env
# For local development with SQLite
USE_POSTGRESQL=False
DEBUG=True
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=*

# For PostgreSQL (production)
USE_POSTGRESQL=True
DATABASE_NAME=hrms_db
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password
DATABASE_HOST=your_host
DATABASE_PORT=5432
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Start development server:
```bash
python manage.py runserver 0.0.0.0:8001
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd /app/frontend
```

2. Install dependencies:
```bash
yarn install
```

3. Configure environment in `.env`:
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

4. Start development server:
```bash
yarn start
```

The application will be available at `http://localhost:3000`

## 🌐 Deployment

### Backend Deployment (Render)

1. **Create New Web Service on Render**
   - Connect your Git repository
   - Select Python environment

2. **Configure Build & Start Commands**
   - Build Command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - Start Command: `gunicorn hrms.wsgi:application --bind 0.0.0.0:$PORT`

3. **Set Environment Variables**
   ```
   USE_POSTGRESQL=True
   DATABASE_NAME=<from_render_postgres>
   DATABASE_USER=<from_render_postgres>
   DATABASE_PASSWORD=<from_render_postgres>
   DATABASE_HOST=<from_render_postgres>
   DATABASE_PORT=5432
   SECRET_KEY=<generate_strong_secret>
   DEBUG=False
   CORS_ORIGINS=https://your-frontend-domain.vercel.app
   ```

4. **Create PostgreSQL Database**
   - Add PostgreSQL addon in Render
   - Copy connection details to environment variables

### Frontend Deployment (Vercel)

1. **Deploy to Vercel**
   - Connect your Git repository
   - Select the `frontend` directory as root

2. **Environment Variables**
   ```
   REACT_APP_BACKEND_URL=https://your-backend.onrender.com
   ```

3. **Build Settings**
   - Framework Preset: Create React App
   - Build Command: `yarn build`
   - Output Directory: `build`

### Alternative: Railway/Supabase for Database

**Railway:**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and create PostgreSQL
railway login
railway init
railway add --database postgresql
```

**Supabase:**
1. Create project at supabase.com
2. Copy PostgreSQL connection string
3. Add to environment variables

## 📋 Environment Variables Reference

### Backend (.env)
```env
USE_POSTGRESQL=True/False
DATABASE_NAME=hrms_db
DATABASE_USER=user
DATABASE_PASSWORD=password
DATABASE_HOST=localhost
DATABASE_PORT=5432
SECRET_KEY=django-secret-key
DEBUG=True/False
CORS_ORIGINS=*
```

### Frontend (.env)
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

## 🔒 Security Features

- Server-side validation for all inputs
- Email format validation
- Unique constraint enforcement
- CORS configuration
- SQL injection prevention (Django ORM)
- XSS protection (React escaping)
- CSRF protection

## 🧪 Testing

### Backend API Testing
```bash
# Test employee creation
curl -X POST http://localhost:8001/api/employees/ \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "EMP001",
    "full_name": "John Doe",
    "email": "john@example.com",
    "department": "Engineering"
  }'

# Get all employees
curl http://localhost:8001/api/employees/

# Mark attendance
curl -X POST http://localhost:8001/api/attendance/ \
  -H "Content-Type: application/json" \
  -d '{
    "employee": 1,
    "date": "2026-02-05",
    "status": "Present"
  }'
```

## 🎨 Design System

### Colors
- Primary: `#667eea` (Purple-blue gradient)
- Success: `#10b981` (Green)
- Danger: `#ef4444` (Red)
- Background: `#fafafa` (Light gray)
- Text: `#1a1a1a` (Dark)

### Typography
- Headings: Manrope (700 weight)
- Body: Inter (400-600 weight)

### Components
- Modern card-based layout
- Subtle shadows and borders
- Smooth transitions
- Responsive design

## 📝 Database Models

### Employee
```python
- id: Primary Key
- employee_id: Unique identifier
- full_name: String
- email: Unique email
- department: String
- created_at: Timestamp
- updated_at: Timestamp
```

### Attendance
```python
- id: Primary Key
- employee: Foreign Key to Employee
- date: Date
- status: Choice (Present/Absent)
- created_at: Timestamp
- updated_at: Timestamp
- Unique constraint: (employee, date)
```

## 🐛 Error Handling

### HTTP Status Codes
- `200 OK` - Successful GET/DELETE
- `201 Created` - Successful POST
- `400 Bad Request` - Validation error
- `404 Not Found` - Resource not found
- `409 Conflict` - Duplicate entry
- `500 Internal Server Error` - Server error

### Error Response Format
```json
{
  "error": "Error message here"
}
```

or

```json
{
  "field_name": ["Error message for this field"]
}
```

## 🔄 Database Migrations

```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Rollback migration
python manage.py migrate app_name migration_name
```

## 🚦 Status Monitoring

### Check Backend
```bash
curl http://localhost:8001/api/employees/
```

### Check Frontend
```bash
curl http://localhost:3000
```

## 📦 Dependencies

### Backend Requirements
- Django==5.0.6
- djangorestframework==3.15.1
- django-cors-headers==4.3.1
- psycopg2-binary==2.9.9
- python-dotenv==1.0.1
- gunicorn==22.0.0

### Frontend Dependencies
- react: ^19.0.0
- react-router-dom: ^7.5.1
- axios: ^1.8.4

## 🤝 Contributing

This is a production-ready HRMS system. Follow these guidelines:

1. Write clean, modular code
2. Add proper validation
3. Handle errors gracefully
4. Write meaningful comments
5. Test before committing

## 📄 License

MIT License - feel free to use this project for your organization.

## 🆘 Support

For issues or questions:
1. Check the API endpoints are correct
2. Verify environment variables
3. Check Django/React logs
4. Ensure database is running

## 🎯 Future Enhancements

- Add user authentication
- Export attendance reports (CSV/PDF)
- Email notifications
- Advanced filtering and search
- Role-based access control
- Mobile app
- Real-time updates with WebSockets

---

**Built with Django REST Framework + React**  
**Production-ready HRMS solution**