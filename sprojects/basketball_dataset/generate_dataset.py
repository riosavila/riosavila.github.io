import numpy as np
import pandas as pd
import random
from faker import Faker
from sklearn.preprocessing import StandardScaler

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)
fake = Faker()

# Teams and their characteristics
TEAMS = [
    'Lakers', 'Celtics', 'Warriors', 'Bulls', 'Rockets', 
    'Spurs', 'Heat', 'Cavaliers', 'Raptors', 'Mavericks'
]

POSITIONS = ['PG', 'SG', 'SF', 'PF', 'C']

def generate_player_stats(num_players=300):
    """Generate synthetic player performance data."""
    players = []
    for _ in range(num_players):
        team = random.choice(TEAMS)
        position = random.choice(POSITIONS)
        
        # Correlated performance metrics
        base_skill = np.random.normal(0, 1)
        points = max(0, base_skill * 10 + np.random.normal(15, 5))
        rebounds = max(0, base_skill * 5 + np.random.normal(7, 3))
        assists = max(0, base_skill * 4 + np.random.normal(5, 2))
        
        # Shooting percentages with correlation
        fg_percentage = min(1, max(0, 0.45 + base_skill * 0.1 + np.random.normal(0.05, 0.02)))
        three_point_percentage = min(1, max(0, 0.35 + base_skill * 0.1 + np.random.normal(0.05, 0.02)))
        
        # Qualitative performance description
        performance_levels = [
            'Emerging Talent', 'Solid Performer', 'Star Player', 
            'Role Player', 'Veteran Leader'
        ]
        performance_desc = random.choices(performance_levels, weights=[0.3, 0.3, 0.2, 0.1, 0.1])[0]
        
        player = {
            'player_id': fake.uuid4(),
            'name': fake.name(),
            'team': team,
            'position': position,
            'points_per_game': points,
            'rebounds_per_game': rebounds,
            'assists_per_game': assists,
            'fg_percentage': fg_percentage,
            'three_point_percentage': three_point_percentage,
            'performance_description': performance_desc,
            'age': random.randint(19, 40),
            'years_experience': random.randint(0, 20)
        }
        players.append(player)
    
    return pd.DataFrame(players)

def generate_team_stats(players_df):
    """Generate team-level statistics from player data."""
    team_stats = players_df.groupby('team').agg({
        'points_per_game': 'sum',
        'rebounds_per_game': 'sum',
        'assists_per_game': 'sum',
        'fg_percentage': 'mean',
        'three_point_percentage': 'mean'
    }).reset_index()
    
    # Add win probability based on aggregated stats
    team_stats['win_probability'] = (
        team_stats['points_per_game'] / 100 + 
        team_stats['rebounds_per_game'] / 50 + 
        team_stats['assists_per_game'] / 25
    ) / 3
    
    team_stats['win_probability'] = StandardScaler().fit_transform(
        team_stats['win_probability'].values.reshape(-1, 1)
    )
    
    return team_stats

def generate_game_data(players_df, team_stats, num_games=500):
    """Generate game-level data with outcomes."""
    games = []
    for _ in range(num_games):
        home_team = random.choice(TEAMS)
        away_team = random.choice([t for t in TEAMS if t != home_team])
        
        home_team_stats = team_stats[team_stats['team'] == home_team].iloc[0]
        away_team_stats = team_stats[team_stats['team'] == away_team].iloc[0]
        
        # Game outcome probability
        home_win_prob = (home_team_stats['win_probability'] + 0.1 * np.random.normal())
        game_outcome = 1 if home_win_prob > 0 else 0
        
        game = {
            'game_id': fake.uuid4(),
            'home_team': home_team,
            'away_team': away_team,
            'home_team_score': max(80, int(home_team_stats['points_per_game'] + np.random.normal(10, 5))),
            'away_team_score': max(80, int(away_team_stats['points_per_game'] + np.random.normal(10, 5))),
            'home_team_win': game_outcome,
            'game_location': random.choice(['Home', 'Away', 'Neutral']),
            'game_summary': fake.paragraph(nb_sentences=3)
        }
        games.append(game)
    
    return pd.DataFrame(games)

def main():
    # Generate datasets
    players_df = generate_player_stats()
    team_stats = generate_team_stats(players_df)
    games_df = generate_game_data(players_df, team_stats)
    
    # Save datasets
    players_df.to_csv('players_data.csv', index=False)
    team_stats.to_csv('team_stats.csv', index=False)
    games_df.to_csv('games_data.csv', index=False)
    
    print("Datasets generated successfully!")

if __name__ == '__main__':
    main()