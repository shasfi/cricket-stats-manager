from app import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Index

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')  # admin, analyst, user
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    debut_year = db.Column(db.Integer, nullable=False)
    player_type = db.Column(db.String(20), nullable=False)  # batsman, bowler, all-rounder, wicket-keeper
    birth_date = db.Column(db.Date)
    batting_style = db.Column(db.String(20))  # right-handed, left-handed
    bowling_style = db.Column(db.String(50))  # right-arm fast, left-arm spin, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    statistics = db.relationship('PlayerStatistic', backref='player', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Player {self.name}>'

class PlayerStatistic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    format = db.Column(db.String(10), nullable=False)  # Test, ODI, T20
    year = db.Column(db.Integer, nullable=False)
    
    # Batting statistics
    matches = db.Column(db.Integer, default=0)
    innings = db.Column(db.Integer, default=0)
    runs = db.Column(db.Integer, default=0)
    not_outs = db.Column(db.Integer, default=0)
    highest_score = db.Column(db.Integer, default=0)
    average = db.Column(db.Float, default=0.0)
    strike_rate = db.Column(db.Float, default=0.0)
    hundreds = db.Column(db.Integer, default=0)
    fifties = db.Column(db.Integer, default=0)
    fours = db.Column(db.Integer, default=0)
    sixes = db.Column(db.Integer, default=0)
    
    # Bowling statistics
    balls_bowled = db.Column(db.Integer, default=0)
    overs_bowled = db.Column(db.Float, default=0.0)
    wickets = db.Column(db.Integer, default=0)
    runs_conceded = db.Column(db.Integer, default=0)
    bowling_average = db.Column(db.Float, default=0.0)
    economy_rate = db.Column(db.Float, default=0.0)
    bowling_strike_rate = db.Column(db.Float, default=0.0)
    five_wickets = db.Column(db.Integer, default=0)
    ten_wickets = db.Column(db.Integer, default=0)
    best_bowling = db.Column(db.String(10))  # e.g., "7/46"
    
    # Fielding statistics
    catches = db.Column(db.Integer, default=0)
    stumpings = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes for better query performance
    __table_args__ = (
        Index('idx_player_format_year', 'player_id', 'format', 'year'),
        Index('idx_format_year', 'format', 'year'),
    )
    
    def __repr__(self):
        return f'<PlayerStatistic {self.player.name} {self.format} {self.year}>'

class TopPerformance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    format = db.Column(db.String(10), nullable=False)
    performance_type = db.Column(db.String(20), nullable=False)  # highest_score, best_bowling, etc.
    value = db.Column(db.String(20), nullable=False)
    match_details = db.Column(db.String(200))
    date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    player = db.relationship('Player', backref='top_performances')
    
    def __repr__(self):
        return f'<TopPerformance {self.player.name} {self.performance_type}: {self.value}>'
