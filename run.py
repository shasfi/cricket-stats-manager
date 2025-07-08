#!/usr/bin/env python3
"""
Run script for CricStats Flask Application
This script starts the Flask application with proper configuration.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    """Main function to run the Flask application"""
    
    # Set default configuration if not specified
    if not os.environ.get('FLASK_CONFIG'):
        os.environ['FLASK_CONFIG'] = 'postgresql'
    
    # Import and run the app
    from app import app
    
    print("Starting CricStats Application...")
    print(f"Configuration: {os.environ.get('FLASK_CONFIG', 'default')}")
    print(f"Database: {os.environ.get('DATABASE_URL', 'Not set')}")
    print("Access the application at: http://localhost:5000")
    print("Admin login: admin / admin123")
    print("Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main() 