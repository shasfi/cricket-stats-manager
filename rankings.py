"""
Real-time Cricket Rankings System
Calculates and provides rankings for Test, ODI, and T20 formats
"""

from app import db
from models import Player, PlayerStatistic
from sqlalchemy import func, desc, and_
from datetime import datetime, timedelta
import logging

def get_batting_rankings(format_name, limit=50):
    """Get batting rankings for a specific format based on recent performance"""
    try:
        # Calculate batting rankings based on runs, average, and recent form
        # Weight recent performances more heavily
        current_year = datetime.now().year
        recent_cutoff = current_year - 2  # Last 2 years for recent form
        
        batting_stats = db.session.query(
            Player.id,
            Player.name,
            Player.country,
            Player.player_type,
            func.sum(PlayerStatistic.runs).label('total_runs'),
            func.sum(PlayerStatistic.innings).label('total_innings'),
            func.sum(PlayerStatistic.not_outs).label('total_not_outs'),
            func.avg(PlayerStatistic.average).label('avg_average'),
            func.avg(PlayerStatistic.strike_rate).label('avg_strike_rate'),
            func.sum(PlayerStatistic.hundreds).label('total_hundreds'),
            func.sum(PlayerStatistic.fifties).label('total_fifties'),
            func.sum(PlayerStatistic.matches).label('total_matches'),
            func.max(PlayerStatistic.year).label('last_active_year')
        ).join(PlayerStatistic).filter(
            PlayerStatistic.format == format_name,
            PlayerStatistic.runs > 0,
            PlayerStatistic.innings > 0
        ).group_by(Player.id).having(
            func.sum(PlayerStatistic.innings) >= 5  # Minimum 5 innings
        ).all()
        
        rankings = []
        for stat in batting_stats:
            # Calculate batting average
            effective_innings = stat.total_innings - stat.total_not_outs
            if effective_innings > 0:
                batting_avg = stat.total_runs / effective_innings
            else:
                batting_avg = stat.total_runs  # All not out
            
            # Calculate ranking points
            # Base points from runs and average
            base_points = min(stat.total_runs * 0.1, 500)  # Max 500 from runs
            avg_points = min(batting_avg * 10, 400)  # Max 400 from average
            
            # Bonus points for hundreds and fifties
            milestone_points = (stat.total_hundreds * 20) + (stat.total_fifties * 10)
            
            # Strike rate bonus (for limited overs)
            strike_rate_bonus = 0
            if format_name in ['ODI', 'T20'] and stat.avg_strike_rate:
                if format_name == 'ODI':
                    strike_rate_bonus = max(0, (stat.avg_strike_rate - 70) * 2)
                elif format_name == 'T20':
                    strike_rate_bonus = max(0, (stat.avg_strike_rate - 100) * 1.5)
            
            # Recent form bonus
            recent_form_bonus = 0
            if stat.last_active_year >= recent_cutoff:
                recent_form_bonus = 50
            
            total_points = base_points + avg_points + milestone_points + strike_rate_bonus + recent_form_bonus
            
            rankings.append({
                'rank': 0,  # Will be set after sorting
                'player_id': stat.id,
                'player_name': stat.name,
                'country': stat.country,
                'player_type': stat.player_type,
                'matches': stat.total_matches,
                'innings': stat.total_innings,
                'runs': stat.total_runs,
                'average': round(batting_avg, 2),
                'strike_rate': round(stat.avg_strike_rate or 0, 2),
                'hundreds': stat.total_hundreds,
                'fifties': stat.total_fifties,
                'points': round(total_points, 2),
                'last_active': stat.last_active_year
            })
        
        # Sort by points and assign ranks
        rankings.sort(key=lambda x: x['points'], reverse=True)
        for i, player in enumerate(rankings[:limit]):
            player['rank'] = i + 1
        
        return rankings[:limit]
        
    except Exception as e:
        logging.error(f"Error calculating batting rankings for {format_name}: {str(e)}")
        return []

def get_bowling_rankings(format_name, limit=50):
    """Get bowling rankings for a specific format"""
    try:
        current_year = datetime.now().year
        recent_cutoff = current_year - 2
        
        bowling_stats = db.session.query(
            Player.id,
            Player.name,
            Player.country,
            Player.player_type,
            func.sum(PlayerStatistic.wickets).label('total_wickets'),
            func.sum(PlayerStatistic.overs_bowled).label('total_overs'),
            func.sum(PlayerStatistic.runs_conceded).label('total_runs_conceded'),
            func.avg(PlayerStatistic.bowling_average).label('avg_bowling_average'),
            func.avg(PlayerStatistic.economy_rate).label('avg_economy_rate'),
            func.sum(PlayerStatistic.five_wickets).label('total_five_wickets'),
            func.sum(PlayerStatistic.matches).label('total_matches'),
            func.max(PlayerStatistic.year).label('last_active_year')
        ).join(PlayerStatistic).filter(
            PlayerStatistic.format == format_name,
            PlayerStatistic.wickets > 0
        ).group_by(Player.id).having(
            func.sum(PlayerStatistic.wickets) >= 5  # Minimum 5 wickets
        ).all()
        
        rankings = []
        for stat in bowling_stats:
            # Calculate bowling average
            bowling_avg = stat.total_runs_conceded / stat.total_wickets if stat.total_wickets > 0 else 999
            
            # Calculate economy rate
            economy_rate = stat.total_runs_conceded / stat.total_overs if stat.total_overs > 0 else 999
            
            # Calculate ranking points
            # Base points from wickets
            base_points = min(stat.total_wickets * 2, 400)  # Max 400 from wickets
            
            # Average bonus (lower is better)
            if bowling_avg <= 50:
                avg_points = max(0, 200 - (bowling_avg * 3))
            else:
                avg_points = 0
            
            # Economy rate bonus (format specific)
            economy_bonus = 0
            if format_name == 'Test' and economy_rate <= 3.5:
                economy_bonus = max(0, (3.5 - economy_rate) * 50)
            elif format_name == 'ODI' and economy_rate <= 5.5:
                economy_bonus = max(0, (5.5 - economy_rate) * 40)
            elif format_name == 'T20' and economy_rate <= 8.0:
                economy_bonus = max(0, (8.0 - economy_rate) * 30)
            
            # Five-wicket haul bonus
            milestone_points = stat.total_five_wickets * 30
            
            # Recent form bonus
            recent_form_bonus = 0
            if stat.last_active_year >= recent_cutoff:
                recent_form_bonus = 50
            
            total_points = base_points + avg_points + economy_bonus + milestone_points + recent_form_bonus
            
            rankings.append({
                'rank': 0,
                'player_id': stat.id,
                'player_name': stat.name,
                'country': stat.country,
                'player_type': stat.player_type,
                'matches': stat.total_matches,
                'wickets': stat.total_wickets,
                'bowling_average': round(bowling_avg, 2),
                'economy_rate': round(economy_rate, 2),
                'five_wickets': stat.total_five_wickets,
                'points': round(total_points, 2),
                'last_active': stat.last_active_year
            })
        
        # Sort by points and assign ranks
        rankings.sort(key=lambda x: x['points'], reverse=True)
        for i, player in enumerate(rankings[:limit]):
            player['rank'] = i + 1
        
        return rankings[:limit]
        
    except Exception as e:
        logging.error(f"Error calculating bowling rankings for {format_name}: {str(e)}")
        return []

def get_all_rounder_rankings(format_name, limit=25):
    """Get all-rounder rankings combining batting and bowling performance"""
    try:
        # Get players with both batting and bowling statistics
        all_rounder_stats = db.session.query(
            Player.id,
            Player.name,
            Player.country,
            Player.player_type,
            func.sum(PlayerStatistic.runs).label('total_runs'),
            func.sum(PlayerStatistic.innings).label('total_innings'),
            func.sum(PlayerStatistic.not_outs).label('total_not_outs'),
            func.sum(PlayerStatistic.wickets).label('total_wickets'),
            func.sum(PlayerStatistic.runs_conceded).label('total_runs_conceded'),
            func.avg(PlayerStatistic.average).label('avg_batting_average'),
            func.avg(PlayerStatistic.bowling_average).label('avg_bowling_average'),
            func.sum(PlayerStatistic.matches).label('total_matches'),
            func.max(PlayerStatistic.year).label('last_active_year')
        ).join(PlayerStatistic).filter(
            PlayerStatistic.format == format_name,
            PlayerStatistic.runs > 0,
            PlayerStatistic.wickets > 0
        ).group_by(Player.id).having(
            and_(
                func.sum(PlayerStatistic.runs) >= 200,  # Minimum runs
                func.sum(PlayerStatistic.wickets) >= 10  # Minimum wickets
            )
        ).all()
        
        rankings = []
        for stat in all_rounder_stats:
            # Calculate batting points
            effective_innings = stat.total_innings - stat.total_not_outs
            batting_avg = stat.total_runs / effective_innings if effective_innings > 0 else stat.total_runs
            batting_points = min(stat.total_runs * 0.05, 200) + min(batting_avg * 5, 150)
            
            # Calculate bowling points
            bowling_avg = stat.total_runs_conceded / stat.total_wickets if stat.total_wickets > 0 else 999
            bowling_points = min(stat.total_wickets * 1.5, 150) + max(0, 100 - (bowling_avg * 2))
            
            # Recent form bonus
            current_year = datetime.now().year
            recent_form_bonus = 50 if stat.last_active_year >= (current_year - 2) else 0
            
            total_points = batting_points + bowling_points + recent_form_bonus
            
            rankings.append({
                'rank': 0,
                'player_id': stat.id,
                'player_name': stat.name,
                'country': stat.country,
                'player_type': stat.player_type,
                'matches': stat.total_matches,
                'runs': stat.total_runs,
                'batting_average': round(batting_avg, 2),
                'wickets': stat.total_wickets,
                'bowling_average': round(bowling_avg, 2),
                'points': round(total_points, 2),
                'last_active': stat.last_active_year
            })
        
        # Sort by points and assign ranks
        rankings.sort(key=lambda x: x['points'], reverse=True)
        for i, player in enumerate(rankings[:limit]):
            player['rank'] = i + 1
        
        return rankings[:limit]
        
    except Exception as e:
        logging.error(f"Error calculating all-rounder rankings for {format_name}: {str(e)}")
        return []

def get_team_rankings():
    """Get team rankings based on player performance"""
    try:
        team_stats = {}
        formats = ['Test', 'ODI', 'T20']
        
        for format_name in formats:
            # Get top players from each country
            country_performance = db.session.query(
                Player.country,
                func.count(Player.id).label('player_count'),
                func.avg(PlayerStatistic.average).label('avg_batting'),
                func.avg(PlayerStatistic.bowling_average).label('avg_bowling'),
                func.sum(PlayerStatistic.runs).label('total_runs'),
                func.sum(PlayerStatistic.wickets).label('total_wickets')
            ).join(PlayerStatistic).filter(
                PlayerStatistic.format == format_name
            ).group_by(Player.country).having(
                func.count(Player.id) >= 3  # At least 3 players
            ).all()
            
            team_rankings = []
            for country_data in country_performance:
                country, player_count, avg_batting, avg_bowling, total_runs, total_wickets = country_data
                
                # Calculate team strength points
                batting_strength = (avg_batting or 0) * 2 + (total_runs or 0) * 0.01
                bowling_strength = max(0, 100 - (avg_bowling or 50)) + (total_wickets or 0) * 0.5
                depth_bonus = min(player_count * 10, 100)  # Bonus for squad depth
                
                total_strength = batting_strength + bowling_strength + depth_bonus
                
                team_rankings.append({
                    'country': country,
                    'player_count': player_count,
                    'batting_strength': round(batting_strength, 2),
                    'bowling_strength': round(bowling_strength, 2),
                    'total_strength': round(total_strength, 2),
                    'avg_batting': round(avg_batting or 0, 2),
                    'avg_bowling': round(avg_bowling or 0, 2)
                })
            
            # Sort by total strength
            team_rankings.sort(key=lambda x: x['total_strength'], reverse=True)
            for i, team in enumerate(team_rankings):
                team['rank'] = i + 1
            
            team_stats[format_name] = team_rankings[:10]  # Top 10 teams
        
        return team_stats
        
    except Exception as e:
        logging.error(f"Error calculating team rankings: {str(e)}")
        return {'Test': [], 'ODI': [], 'T20': []}