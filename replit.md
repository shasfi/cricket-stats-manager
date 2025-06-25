# CricStats - Cricket Statistics Analysis System

## Overview

CricStats is a comprehensive web application for cricket statistics analysis and management, built with Flask and designed to handle 10 years of player performance data across different cricket formats (Test, ODI, T20). The system provides player management, statistical analysis, comparison tools, and visualization capabilities.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with support for SQLite (development) and PostgreSQL (production)
- **Authentication**: Flask-Login for user session management
- **Forms**: Flask-WTF with WTForms for form handling and validation
- **Deployment**: Gunicorn WSGI server with auto-scaling deployment target

### Frontend Architecture
- **UI Framework**: Bootstrap 5 with dark theme support
- **Icons**: Font Awesome 6.0
- **Charts**: Chart.js for data visualization
- **Template Engine**: Jinja2 (Flask's default)
- **Responsive Design**: Mobile-first Bootstrap grid system

### Data Storage
- **Primary Database**: PostgreSQL (production) / SQLite (development)
- **ORM**: SQLAlchemy with declarative base model
- **Migration Strategy**: Built-in Flask-SQLAlchemy table creation

## Key Components

### User Management
- **Role-based Access Control**: Three user roles (admin, analyst, user)
- **Authentication System**: Username/password authentication with session management
- **Registration/Login**: Form-based user registration and login

### Player Management
- **Player Profiles**: Comprehensive player information including personal details, playing style, and career information
- **Statistics Tracking**: Year-wise performance statistics across all cricket formats
- **CRUD Operations**: Full create, read, update, delete operations for players and statistics

### Analytics & Visualization
- **Player Comparison**: Side-by-side comparison tool for analyzing player performance
- **Statistical Charts**: Interactive charts for performance trends and comparisons
- **Top Performers**: Automated identification and display of top-performing players

### Search & Filtering
- **Advanced Search**: Multi-criteria search functionality for players
- **Filter Options**: Country, player type, and format-based filtering
- **Pagination**: Efficient handling of large datasets

## Data Flow

### User Authentication Flow
1. User submits login/registration form
2. Flask-WTF validates form data
3. Password hashing/verification using Werkzeug security
4. Flask-Login manages user sessions
5. Role-based access control determines available features

### Player Data Management Flow
1. Authorized users (admin/analyst) input player data via forms
2. Form validation ensures data integrity
3. SQLAlchemy ORM persists data to database
4. Statistics calculations performed in utils module
5. Data presented through templated views

### Comparison & Analytics Flow
1. User selects players and format for comparison
2. Backend aggregates statistics using SQLAlchemy queries
3. Utils module processes data for visualization
4. Chart.js renders interactive comparisons
5. Results displayed with responsive design

## External Dependencies

### Python Dependencies
- **Flask**: Web framework and core functionality
- **SQLAlchemy**: Database ORM and management
- **Flask-Login**: User authentication and session management
- **Flask-WTF**: Form handling and CSRF protection
- **Matplotlib**: Statistical data visualization (server-side)
- **Gunicorn**: Production WSGI server
- **psycopg2-binary**: PostgreSQL database adapter

### Frontend Dependencies
- **Bootstrap 5**: UI framework with dark theme support
- **Font Awesome**: Icon library for enhanced UX
- **Chart.js**: Client-side data visualization library

### System Dependencies (via Nix)
- **PostgreSQL**: Production database server
- **Cairo/FFmpeg**: Graphics and media processing support
- **OpenSSL**: Security and encryption support

## Deployment Strategy

### Development Environment
- **Local Server**: Flask development server with debug mode
- **Database**: SQLite for local development
- **Hot Reload**: Automatic restart on code changes

### Production Environment
- **Server**: Gunicorn with multiple worker processes
- **Database**: PostgreSQL with connection pooling
- **Scaling**: Auto-scaling deployment target on Replit
- **Port Configuration**: Bound to 0.0.0.0:5000 with port reuse
- **Security**: ProxyFix middleware for proper header handling

### Environment Configuration
- **Database URL**: Environment variable for database connection
- **Session Secret**: Environment variable for session security
- **Debug Mode**: Disabled in production environment

## Changelog
- June 25, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.