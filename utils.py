from models import Player, PlayerStatistic, TopPerformance
from sqlalchemy import func, desc
import logging

def get_player_career_stats(player_id):
    """Calculate career statistics for a player across all formats"""
    try:
        player = Player.query.get(player_id)
        if not player:
            return None
        
        career_stats = {}
        formats = ['Test', 'ODI', 'T20']
        
        for format_name in formats:
            stats = PlayerStatistic.query.filter_by(
                player_id=player_id, 
                format=format_name
            ).all()
            
            if stats:
                # Aggregate statistics
                total_matches = sum(stat.matches or 0 for stat in stats)
                total_runs = sum(stat.runs or 0 for stat in stats)
                total_innings = sum(stat.innings or 0 for stat in stats)
                total_not_outs = sum(stat.not_outs or 0 for stat in stats)
                total_wickets = sum(stat.wickets or 0 for stat in stats)
                total_runs_conceded = sum(stat.runs_conceded or 0 for stat in stats)
                total_overs = sum(stat.overs_bowled or 0 for stat in stats)
                
                # Calculate averages
                batting_avg = total_runs / (total_innings - total_not_outs) if (total_innings - total_not_outs) > 0 else 0
                bowling_avg = total_runs_conceded / total_wickets if total_wickets > 0 else 0
                economy = total_runs_conceded / total_overs if total_overs > 0 else 0
                
                career_stats[format_name] = {
                    'matches': total_matches,
                    'runs': total_runs,
                    'batting_average': round(batting_avg, 2),
                    'highest_score': max((stat.highest_score or 0 for stat in stats), default=0),
                    'hundreds': sum(stat.hundreds or 0 for stat in stats),
                    'fifties': sum(stat.fifties or 0 for stat in stats),
                    'wickets': total_wickets,
                    'bowling_average': round(bowling_avg, 2),
                    'economy_rate': round(economy, 2),
                    'five_wickets': sum(stat.five_wickets or 0 for stat in stats),
                    'catches': sum(stat.catches or 0 for stat in stats)
                }
            else:
                career_stats[format_name] = None
        
        return career_stats
    except Exception as e:
        logging.error(f"Error calculating career stats for player {player_id}: {str(e)}")
        return None

def get_top_performers():
    """Get top performers across different categories"""
    try:
        top_performers = {
            'batting': {
                'most_runs': [],
                'highest_average': [],
                'most_hundreds': []
            },
            'bowling': {
                'most_wickets': [],
                'best_average': [],
                'best_economy': []
            }
        }
        
        # Most runs in each format
        for format_name in ['Test', 'ODI', 'T20']:
            # Top run scorers
            top_runs = db.session.query(
                Player.name,
                Player.country,
                func.sum(PlayerStatistic.runs).label('total_runs')
            ).join(PlayerStatistic).filter(
                PlayerStatistic.format == format_name
            ).group_by(Player.id).order_by(
                desc('total_runs')
            ).limit(5).all()
            
            top_performers['batting']['most_runs'].extend([
                {
                    'player': player_name,
                    'country': country,
                    'value': total_runs,
                    'format': format_name
                }
                for player_name, country, total_runs in top_runs
            ])
            
            # Top wicket takers
            top_wickets = db.session.query(
                Player.name,
                Player.country,
                func.sum(PlayerStatistic.wickets).label('total_wickets')
            ).join(PlayerStatistic).filter(
                PlayerStatistic.format == format_name,
                PlayerStatistic.wickets > 0
            ).group_by(Player.id).order_by(
                desc('total_wickets')
            ).limit(5).all()
            
            top_performers['bowling']['most_wickets'].extend([
                {
                    'player': player_name,
                    'country': country,
                    'value': total_wickets,
                    'format': format_name
                }
                for player_name, country, total_wickets in top_wickets
            ])
        
        return top_performers
    except Exception as e:
        logging.error(f"Error getting top performers: {str(e)}")
        return {'batting': {'most_runs': [], 'highest_average': [], 'most_hundreds': []}, 
                'bowling': {'most_wickets': [], 'best_average': [], 'best_economy': []}}

def generate_comparison_data(player1_id, player2_id, format_name):
    """Generate comparison data for two players in a specific format"""
    try:
        player1 = Player.query.get(player1_id)
        player2 = Player.query.get(player2_id)
        
        if not player1 or not player2:
            return None
        
        # Get statistics for both players
        player1_stats = PlayerStatistic.query.filter_by(
            player_id=player1_id, 
            format=format_name
        ).all()
        
        player2_stats = PlayerStatistic.query.filter_by(
            player_id=player2_id, 
            format=format_name
        ).all()
        
        def aggregate_stats(stats):
            if not stats:
                return None
            
            total_matches = sum(stat.matches or 0 for stat in stats)
            total_runs = sum(stat.runs or 0 for stat in stats)
            total_innings = sum(stat.innings or 0 for stat in stats)
            total_not_outs = sum(stat.not_outs or 0 for stat in stats)
            total_wickets = sum(stat.wickets or 0 for stat in stats)
            total_runs_conceded = sum(stat.runs_conceded or 0 for stat in stats)
            total_overs = sum(stat.overs_bowled or 0 for stat in stats)
            
            batting_avg = total_runs / (total_innings - total_not_outs) if (total_innings - total_not_outs) > 0 else 0
            bowling_avg = total_runs_conceded / total_wickets if total_wickets > 0 else 0
            economy = total_runs_conceded / total_overs if total_overs > 0 else 0
            
            return {
                'matches': total_matches,
                'runs': total_runs,
                'innings': total_innings,
                'batting_average': round(batting_avg, 2),
                'highest_score': max((stat.highest_score or 0 for stat in stats), default=0),
                'hundreds': sum(stat.hundreds or 0 for stat in stats),
                'fifties': sum(stat.fifties or 0 for stat in stats),
                'wickets': total_wickets,
                'bowling_average': round(bowling_avg, 2),
                'economy_rate': round(economy, 2),
                'five_wickets': sum(stat.five_wickets or 0 for stat in stats),
                'catches': sum(stat.catches or 0 for stat in stats)
            }
        
        comparison_data = {
            'player1': {
                'info': player1,
                'stats': aggregate_stats(player1_stats)
            },
            'player2': {
                'info': player2,
                'stats': aggregate_stats(player2_stats)
            },
            'format': format_name
        }
        
        return comparison_data
    except Exception as e:
        logging.error(f"Error generating comparison data: {str(e)}")
        return None

from app import db
