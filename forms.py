from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField, FloatField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, ValidationError
from models import User, Player
import datetime

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Role', choices=[('user', 'User'), ('analyst', 'Analyst')], default='user')
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please choose a different one.')

class PlayerForm(FlaskForm):
    name = StringField('Player Name', validators=[DataRequired(), Length(min=2, max=100)])
    country = StringField('Country', validators=[DataRequired(), Length(min=2, max=50)])
    debut_year = IntegerField('Debut Year', validators=[DataRequired(), NumberRange(min=1900, max=datetime.datetime.now().year)])
    player_type = SelectField('Player Type', choices=[
        ('batsman', 'Batsman'),
        ('bowler', 'Bowler'),
        ('all-rounder', 'All-rounder'),
        ('wicket-keeper', 'Wicket-keeper')
    ], validators=[DataRequired()])
    birth_date = DateField('Birth Date', validators=[Optional()])
    batting_style = SelectField('Batting Style', choices=[
        ('', 'Select Style'),
        ('right-handed', 'Right-handed'),
        ('left-handed', 'Left-handed')
    ], validators=[Optional()])
    bowling_style = StringField('Bowling Style', validators=[Optional(), Length(max=50)])
    submit = SubmitField('Save Player')

class PlayerStatisticForm(FlaskForm):
    format = SelectField('Format', choices=[('Test', 'Test'), ('ODI', 'ODI'), ('T20', 'T20')], validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=2014, max=datetime.datetime.now().year)])
    
    # Batting stats
    matches = IntegerField('Matches', validators=[Optional(), NumberRange(min=0)])
    innings = IntegerField('Innings', validators=[Optional(), NumberRange(min=0)])
    runs = IntegerField('Runs', validators=[Optional(), NumberRange(min=0)])
    not_outs = IntegerField('Not Outs', validators=[Optional(), NumberRange(min=0)])
    highest_score = IntegerField('Highest Score', validators=[Optional(), NumberRange(min=0)])
    average = FloatField('Batting Average', validators=[Optional(), NumberRange(min=0)])
    strike_rate = FloatField('Strike Rate', validators=[Optional(), NumberRange(min=0)])
    hundreds = IntegerField('Hundreds', validators=[Optional(), NumberRange(min=0)])
    fifties = IntegerField('Fifties', validators=[Optional(), NumberRange(min=0)])
    fours = IntegerField('Fours', validators=[Optional(), NumberRange(min=0)])
    sixes = IntegerField('Sixes', validators=[Optional(), NumberRange(min=0)])
    
    # Bowling stats
    balls_bowled = IntegerField('Balls Bowled', validators=[Optional(), NumberRange(min=0)])
    overs_bowled = FloatField('Overs Bowled', validators=[Optional(), NumberRange(min=0)])
    wickets = IntegerField('Wickets', validators=[Optional(), NumberRange(min=0)])
    runs_conceded = IntegerField('Runs Conceded', validators=[Optional(), NumberRange(min=0)])
    bowling_average = FloatField('Bowling Average', validators=[Optional(), NumberRange(min=0)])
    economy_rate = FloatField('Economy Rate', validators=[Optional(), NumberRange(min=0)])
    bowling_strike_rate = FloatField('Bowling Strike Rate', validators=[Optional(), NumberRange(min=0)])
    five_wickets = IntegerField('5-wicket Hauls', validators=[Optional(), NumberRange(min=0)])
    ten_wickets = IntegerField('10-wicket Hauls', validators=[Optional(), NumberRange(min=0)])
    best_bowling = StringField('Best Bowling', validators=[Optional(), Length(max=10)])
    
    # Fielding stats
    catches = IntegerField('Catches', validators=[Optional(), NumberRange(min=0)])
    stumpings = IntegerField('Stumpings', validators=[Optional(), NumberRange(min=0)])
    
    submit = SubmitField('Save Statistics')

class SearchForm(FlaskForm):
    search = StringField('Search Players', validators=[Optional()])
    country = SelectField('Country', choices=[('', 'All Countries')], validators=[Optional()])
    player_type = SelectField('Player Type', choices=[
        ('', 'All Types'),
        ('batsman', 'Batsman'),
        ('bowler', 'Bowler'),
        ('all-rounder', 'All-rounder'),
        ('wicket-keeper', 'Wicket-keeper')
    ], validators=[Optional()])
    format = SelectField('Format', choices=[
        ('', 'All Formats'),
        ('Test', 'Test'),
        ('ODI', 'ODI'),
        ('T20', 'T20')
    ], validators=[Optional()])
    submit = SubmitField('Search')

class CompareForm(FlaskForm):
    player1 = SelectField('Player 1', coerce=int, validators=[DataRequired()])
    player2 = SelectField('Player 2', coerce=int, validators=[DataRequired()])
    format = SelectField('Format', choices=[('Test', 'Test'), ('ODI', 'ODI'), ('T20', 'T20')], validators=[DataRequired()])
    submit = SubmitField('Compare Players')
    
    def validate_player2(self, player2):
        if self.player1.data == player2.data:
            raise ValidationError('Please select different players for comparison.')
