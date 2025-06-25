# CricStats - Cricket Statistics Analysis System

A comprehensive web application for cricket statistics analysis and management, built with Flask and designed to handle player performance data across different cricket formats (Test, ODI, T20).

## Features

- **Real-time Rankings**: Live rankings for Test, ODI, and T20 formats
- **Player Management**: Comprehensive player profiles and statistics
- **Performance Analytics**: Statistical analysis and player comparisons
- **User Authentication**: Secure login system with role-based access
- **Interactive Visualizations**: Charts and graphs using Chart.js
- **Responsive Design**: Mobile-friendly Bootstrap interface

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**: Bootstrap 5, Chart.js, Font Awesome
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF with validation

## Installation

### Prerequisites
- Python 3.11+
- PostgreSQL database

### Setup

1. **Clone or download the project files**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set environment variables**:
```bash
export DATABASE_URL="postgresql://username:password@localhost/cricstats"
export SESSION_SECRET="your-secret-key-here"
```

4. **Initialize the database**:
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

5. **Run the application**:
```bash
python main.py
# or
gunicorn --bind 0.0.0.0:5000 main:app
```

6. **Access the application**:
Open your browser and go to `http://localhost:5000`

## Quick Start

1. Register a new user account
2. Browse the 40+ authentic cricket players in the database
3. View live rankings across Test, ODI, and T20 formats
4. Compare player performances
5. Explore detailed player statistics and visualizations

## Project Structure

```
cricstats/
├── app.py              # Flask application setup
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # Application routes
├── forms.py            # Form definitions
├── rankings.py         # Ranking calculation logic
├── utils.py            # Utility functions
├── templates/          # HTML templates
├── static/             # CSS, JS, and assets
└── requirements.txt    # Python dependencies
```

## Usage

### Admin Functions
- Add new players and statistics
- Manage user accounts
- Access admin dashboard

### User Functions
- Browse player database
- View rankings and statistics
- Compare players
- View interactive charts

## Database Schema

- **Users**: Authentication and role management
- **Players**: Player profiles and basic information
- **Player Statistics**: Performance data by format and year
- **Top Performances**: Notable achievements

## Rankings System

The ranking system calculates points based on:
- **Batting**: Runs, average, strike rate, centuries, recent form
- **Bowling**: Wickets, average, economy rate, five-wicket hauls
- **All-rounders**: Combined batting and bowling performance
- **Teams**: Collective player strength by country

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please check the documentation or create an issue in the project repository.