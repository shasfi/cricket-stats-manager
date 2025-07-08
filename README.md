# CricStats - Cricket Statistics Management System

A comprehensive Flask-based web application for managing cricket player statistics, rankings, and analysis.

## Features

- **Player Management**: Add, edit, and manage cricket players
- **Statistics Tracking**: Comprehensive batting and bowling statistics
- **Rankings System**: Live rankings for different formats
- **Comparison Tool**: Compare players across different metrics
- **Admin Panel**: Full administrative control
- **User Authentication**: Secure login system
- **Data Visualization**: Charts and graphs for statistics
- **PostgreSQL Support**: Robust database backend

## Prerequisites

- Python 3.11 or higher
- PostgreSQL 12 or higher
- pip (Python package installer)

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd FlaskDataManager
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. PostgreSQL Setup

#### Option A: Using the Setup Script (Recommended)

```bash
python setup_postgresql.py
```

This script will:
- Create a PostgreSQL user and database
- Set up environment variables
- Test the database connection

#### Option B: Manual PostgreSQL Setup

1. **Install PostgreSQL** (if not already installed)
   - Download from: https://www.postgresql.org/download/
   - Or use package manager:
     ```bash
     # Ubuntu/Debian
     sudo apt-get install postgresql postgresql-contrib
     
     # macOS
     brew install postgresql
     
     # Windows
     # Download installer from PostgreSQL website
     ```

2. **Create Database and User**
   ```sql
   -- Connect to PostgreSQL as superuser
   psql -U postgres
   
   -- Create user and database
   CREATE USER cricstats_user WITH PASSWORD 'your_password';
   CREATE DATABASE cricstats_db OWNER cricstats_user;
   GRANT ALL PRIVILEGES ON DATABASE cricstats_db TO cricstats_user;
   \q
   ```

3. **Configure Environment Variables**
   Create a `.env` file in the project root:
   ```env
   FLASK_APP=app.py
   FLASK_ENV=development
   FLASK_CONFIG=postgresql
   
   DATABASE_URL=postgresql://cricstats_user:your_password@localhost:5432/cricstats_db
   
   SECRET_KEY=your-secret-key-here
   
   POSTGRES_USER=cricstats_user
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=cricstats_db
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   ```

### 5. Run the Application

```bash
# Option 1: Using the run script
python run.py

# Option 2: Direct execution
python app.py

# Option 3: Using Flask CLI
flask run
```

### 6. Access the Application

- **URL**: http://localhost:5000
- **Admin Login**: 
  - Username: `admin`
  - Password: `admin123`

## Configuration Options

### Database Configuration

The application supports multiple database configurations:

- **SQLite** (default for development)
- **PostgreSQL** (recommended for production)

Set the `FLASK_CONFIG` environment variable:
- `development`: Uses SQLite
- `postgresql`: Uses PostgreSQL
- `production`: Uses PostgreSQL with production settings

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_CONFIG` | Application configuration | `default` |
| `DATABASE_URL` | Database connection string | SQLite file |
| `SECRET_KEY` | Flask secret key | Auto-generated |
| `POSTGRES_USER` | PostgreSQL username | `cricstats_user` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `cricstats_password` |
| `POSTGRES_DB` | PostgreSQL database name | `cricstats_db` |
| `POSTGRES_HOST` | PostgreSQL host | `localhost` |
| `POSTGRES_PORT` | PostgreSQL port | `5432` |

## Project Structure

```
FlaskDataManager/
├── app.py                 # Main application file
├── config.py              # Configuration classes
├── models.py              # Database models
├── routes.py              # Application routes
├── forms.py               # WTForms definitions
├── utils.py               # Utility functions
├── rankings.py            # Rankings logic
├── setup_postgresql.py    # PostgreSQL setup script
├── run.py                 # Application runner
├── requirements.txt       # Python dependencies
├── static/                # Static files (CSS, JS, images)
├── templates/             # HTML templates
└── instance/              # Instance-specific files
```

## Features Overview

### Player Management
- Add new players with detailed information
- Edit existing player details
- Bulk player import functionality
- Player search and filtering

### Statistics Tracking
- Batting statistics (runs, average, strike rate, etc.)
- Bowling statistics (wickets, economy, average, etc.)
- Year-wise statistics tracking
- Multiple format support (Test, ODI, T20)

### Rankings System
- Live batting rankings
- Live bowling rankings
- All-rounder rankings
- Team rankings

### Comparison Tool
- Side-by-side player comparison
- Statistical analysis
- Visual charts and graphs

### Admin Panel
- User management
- Database administration
- System statistics
- Bulk operations

## API Endpoints

- `GET /` - Home page
- `GET /login` - Login page
- `POST /login` - Login authentication
- `GET /register` - Registration page
- `GET /dashboard` - User dashboard
- `GET /players` - Players listing
- `GET /player/<id>` - Player details
- `GET /compare` - Player comparison
- `GET /rankings` - Rankings page
- `GET /admin` - Admin panel

## Development

### Running in Development Mode

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python run.py
```

### Database Migrations

The application uses SQLAlchemy with automatic table creation. For production, consider using Flask-Migrate for database migrations.

### Testing

```bash
# Run tests (if test files exist)
python -m pytest tests/
```

## Deployment

### Production Setup

1. **Set Production Environment Variables**
   ```env
   FLASK_CONFIG=production
   DATABASE_URL=postgresql://user:pass@host:port/db
   SECRET_KEY=your-secure-secret-key
   ```

2. **Use Gunicorn for Production**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Set up Reverse Proxy** (Nginx/Apache)

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify PostgreSQL is running
   - Check database credentials in `.env`
   - Ensure database and user exist

2. **Import Errors**
   - Activate virtual environment
   - Install all dependencies: `pip install -r requirements.txt`

3. **Permission Errors**
   - Check PostgreSQL user permissions
   - Verify database ownership

### Logs

Application logs are written to console. For production, configure proper logging:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**Note**: This application is designed for educational and demonstration purposes. For production use, ensure proper security measures, data validation, and backup strategies are implemented.