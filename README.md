# School Information System (SIS)

A comprehensive Django-based School Information System with role-based access control for Admins, Students, and Staff.

## Features

### User Roles & Permissions
- **Admin**: Full CRUD access to all modules (Users, Courses, Events, Results, Announcements, Timetable)
- **Student**: View access to Dashboard, Results, Announcements, Profile (with edit), Timetable, Events
- **Staff**: Limited access to relevant modules
- **Guest**: View access to Announcements

### Core Modules
1. **User Management** - Custom user model with role-based permissions
2. **Course Management** - CRUD operations for courses and enrollments
3. **Event Management** - School events with registration system
4. **Results Management** - Academic results with grades and GPA
5. **Announcements** - Priority-based announcement system
6. **Timetable Management** - Class scheduling system
7. **Dashboard** - Role-specific dashboards with statistics

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Neon PostgreSQL connection string
# DATABASE_URL=postgresql://username:password@ep-example-123456.us-east-1.aws.neon.tech/dbname?sslmode=require
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## Technology Stack
- **Backend**: Django 4.2.7
- **Frontend**: Bootstrap 5.1.3, Font Awesome 6.0
- **Database**: PostgreSQL (Neon) with SQLite fallback
- **Authentication**: Django's built-in authentication system

## Project Structure
```
SE_SMP/
├── accounts/          # User management and authentication
├── announcements/     # Announcement system
├── courses/          # Course management
├── dashboard/        # Dashboard views
├── events/           # Event management
├── results/          # Academic results
├── timetable/        # Class scheduling
├── templates/        # HTML templates
├── static/           # CSS, JS, images
└── school_system/    # Main project settings
```

## Usage

1. Access the application at `http://localhost:8000`
2. Register a new account or login with existing credentials
3. Navigate through different modules based on your user role
4. Admins can access the Django admin panel at `/admin/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
Software Engineering School Management Project
