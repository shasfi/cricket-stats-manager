from flask import render_template, redirect, url_for, flash, request, jsonify, current_app as app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models import User, Player, PlayerStatistic, TopPerformance
from forms import LoginForm, RegisterForm, PlayerForm, PlayerStatisticForm, SearchForm, CompareForm
from utils import get_player_career_stats, get_top_performers, generate_comparison_data
from rankings import get_batting_rankings, get_bowling_rankings, get_all_rounder_rankings, get_team_rankings
from sqlalchemy import or_, and_
import logging

@app.route('/debug')
def debug():
    """Debug route to check database connection"""
    try:
        total_players = Player.query.count()
        players = Player.query.limit(5).all()
        player_names = [f"{p.name} ({p.country})" for p in players]
        
        return jsonify({
            'total_players': total_players,
            'sample_players': player_names,
            'database_url': app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/')
def index():
    """Home page with overview statistics"""
    total_players = Player.query.count()
    total_stats = PlayerStatistic.query.count()
    recent_players = Player.query.order_by(Player.created_at.desc()).limit(5).all()
    top_performers = get_top_performers()
    
    return render_template('index.html', 
                         total_players=total_players,
                         total_stats=total_stats,
                         recent_players=recent_players,
                         top_performers=top_performers)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.is_active and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            role=form.role.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with personalized content"""
    total_players = Player.query.count()
    total_stats = PlayerStatistic.query.count()
    recent_players = Player.query.order_by(Player.created_at.desc()).limit(10).all()
    top_performers = get_top_performers()
    
    return render_template('dashboard.html',
                         total_players=total_players,
                         total_stats=total_stats,
                         recent_players=recent_players,
                         top_performers=top_performers)

@app.route('/players')
def players():
    """Players listing with search and filtering"""
    form = SearchForm()
    
    # Get unique countries for filter dropdown
    countries = db.session.query(Player.country).distinct().order_by(Player.country).all()
    form.country.choices = [('', 'All Countries')] + [(c[0], c[0]) for c in countries]
    
    # Build query
    query = Player.query
    
    # Apply search filters
    if request.args.get('search'):
        search_term = request.args.get('search')
        query = query.filter(Player.name.contains(search_term))
    
    if request.args.get('country'):
        query = query.filter(Player.country == request.args.get('country'))
    
    if request.args.get('player_type'):
        query = query.filter(Player.player_type == request.args.get('player_type'))
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    players = query.order_by(Player.name).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Remove 'page' from request.args for safe pagination links
    args = request.args.to_dict()
    args.pop('page', None)
    return render_template('players.html', players=players, form=form, args=args)

@app.route('/player/<int:player_id>')
def player_detail(player_id):
    """Individual player statistics and details"""
    player = Player.query.get_or_404(player_id)
    career_stats = get_player_career_stats(player_id)
    
    # Get yearly statistics for charts
    yearly_stats = PlayerStatistic.query.filter_by(player_id=player_id)\
                                       .order_by(PlayerStatistic.year)\
                                       .all()
    
    return render_template('player_detail.html', 
                         player=player, 
                         career_stats=career_stats,
                         yearly_stats=yearly_stats)

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    """Player comparison tool"""
    form = CompareForm()
    
    # Populate player choices
    players = Player.query.order_by(Player.name).all()
    form.player1.choices = [(p.id, p.name) for p in players]
    form.player2.choices = [(p.id, p.name) for p in players]
    
    comparison_data = None
    if form.validate_on_submit():
        comparison_data = generate_comparison_data(
            form.player1.data, 
            form.player2.data, 
            form.format.data
        )
    
    return render_template('compare.html', form=form, comparison_data=comparison_data)

@app.route('/admin')
@login_required
def admin():
    """Admin panel - accessible only to admin users"""
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    total_users = User.query.count()
    total_players = Player.query.count()
    total_stats = PlayerStatistic.query.count()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_players = Player.query.order_by(Player.created_at.desc()).limit(5).all()
    
    return render_template('admin.html',
                         total_users=total_users,
                         total_players=total_players,
                         total_stats=total_stats,
                         recent_users=recent_users,
                         recent_players=recent_players)

@app.route('/admin/add_player', methods=['GET', 'POST'])
@login_required
def add_player():
    """Add new player - admin only"""
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = PlayerForm()
    if form.validate_on_submit():
        player = Player(
            name=form.name.data,
            country=form.country.data,
            debut_year=form.debut_year.data,
            player_type=form.player_type.data,
            birth_date=form.birth_date.data,
            batting_style=form.batting_style.data,
            bowling_style=form.bowling_style.data
        )
        db.session.add(player)
        db.session.commit()
        flash(f'Player {player.name} added successfully!', 'success')
        return redirect(url_for('players'))
    
    return render_template('add_player.html', form=form)

@app.route('/admin/edit_player/<int:player_id>', methods=['GET', 'POST'])
@login_required
def edit_player(player_id):
    """Edit player information - admin only"""
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    player = Player.query.get_or_404(player_id)
    form = PlayerForm(obj=player)
    
    if form.validate_on_submit():
        form.populate_obj(player)
        db.session.commit()
        flash(f'Player {player.name} updated successfully!', 'success')
        return redirect(url_for('player_detail', player_id=player.id))
    
    return render_template('add_player.html', form=form, player=player)

@app.route('/admin/add_stats/<int:player_id>', methods=['GET', 'POST'])
@login_required
def add_statistics(player_id):
    """Add player statistics - admin only"""
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    player = Player.query.get_or_404(player_id)
    form = PlayerStatisticForm()
    
    if form.validate_on_submit():
        # Check if statistics already exist for this player, format, and year
        existing_stat = PlayerStatistic.query.filter_by(
            player_id=player_id,
            format=form.format.data,
            year=form.year.data
        ).first()
        
        if existing_stat:
            flash(f'Statistics for {form.format.data} {form.year.data} already exist for this player.', 'warning')
        else:
            stat = PlayerStatistic(player_id=player_id)
            form.populate_obj(stat)
            db.session.add(stat)
            db.session.commit()
            flash(f'Statistics added for {player.name} - {form.format.data} {form.year.data}', 'success')
            return redirect(url_for('player_detail', player_id=player.id))
    
    return render_template('add_player.html', form=form, player=player, is_stats=True)

@app.route('/api/player_stats/<int:player_id>')
def api_player_stats(player_id):
    """API endpoint for player statistics (for charts)"""
    format_filter = request.args.get('format')
    
    query = PlayerStatistic.query.filter_by(player_id=player_id)
    if format_filter:
        query = query.filter_by(format=format_filter)
    
    stats = query.order_by(PlayerStatistic.year).all()
    
    data = {
        'years': [stat.year for stat in stats],
        'runs': [stat.runs for stat in stats],
        'average': [stat.average for stat in stats],
        'strike_rate': [stat.strike_rate for stat in stats],
        'wickets': [stat.wickets for stat in stats],
        'bowling_average': [stat.bowling_average for stat in stats],
        'economy_rate': [stat.economy_rate for stat in stats],
        'formats': [stat.format for stat in stats]
    }
    
    return jsonify(data)

@app.route('/rankings')
def rankings():
    """Cricket rankings for all formats"""
    format_name = request.args.get('format', 'Test')
    ranking_type = request.args.get('type', 'batting')
    
    if format_name not in ['Test', 'ODI', 'T20']:
        format_name = 'Test'
    
    if ranking_type not in ['batting', 'bowling', 'all-rounder', 'team']:
        ranking_type = 'batting'
    
    rankings_data = {}
    
    if ranking_type == 'batting':
        rankings_data = get_batting_rankings(format_name)
    elif ranking_type == 'bowling':
        rankings_data = get_bowling_rankings(format_name)
    elif ranking_type == 'all-rounder':
        rankings_data = get_all_rounder_rankings(format_name)
    elif ranking_type == 'team':
        team_rankings = get_team_rankings()
        rankings_data = team_rankings.get(format_name, [])
    
    return render_template('rankings.html',
                         rankings=rankings_data,
                         format=format_name,
                         ranking_type=ranking_type)

@app.route('/rankings/live')
def live_rankings():
    """Live rankings dashboard with all formats"""
    # Get rankings for all formats and types
    test_batting = get_batting_rankings('Test', 10)
    test_bowling = get_bowling_rankings('Test', 10)
    test_teams = get_team_rankings().get('Test', [])[:5]
    
    odi_batting = get_batting_rankings('ODI', 10)
    odi_bowling = get_bowling_rankings('ODI', 10)
    odi_teams = get_team_rankings().get('ODI', [])[:5]
    
    t20_batting = get_batting_rankings('T20', 10)
    t20_bowling = get_bowling_rankings('T20', 10)
    t20_teams = get_team_rankings().get('T20', [])[:5]
    
    return render_template('live_rankings.html',
                         test_batting=test_batting,
                         test_bowling=test_bowling,
                         test_teams=test_teams,
                         odi_batting=odi_batting,
                         odi_bowling=odi_bowling,
                         odi_teams=odi_teams,
                         t20_batting=t20_batting,
                         t20_bowling=t20_bowling,
                         t20_teams=t20_teams)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('base.html', error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('base.html', error_message="Internal server error"), 500
