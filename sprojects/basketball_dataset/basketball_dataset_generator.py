import numpy as np
import pandas as pd
import random
import os
import sys
import traceback

def generate_basketball_performance_dataset(n_teams=30, n_players_per_team=15, n_seasons=5):
    """
    Generate a comprehensive synthetic basketball performance dataset
    
    Parameters:
    - n_teams: Number of teams in the league
    - n_players_per_team: Number of players per team
    - n_seasons: Number of seasons to simulate
    
    Returns:
    - DataFrame with comprehensive basketball performance metrics
    """
    
    # Random seed for reproducibility
    np.random.seed(42)
    
    # Team Names
    team_names = [
        f"City {chr(65+i)} {random.choice(['Hawks', 'Wolves', 'Eagles', 'Lions', 'Tigers'])}" 
        for i in range(n_teams)
    ]
    
    # Comprehensive Dataset
    data = []
    
    for season in range(2018, 2018 + n_seasons):
        # Track all teams' strength scores for this season
        season_team_strengths = []
        season_team_data = []
        
        for team_id, team_name in enumerate(team_names, 1):
            # Team-level features
            team_budget = np.random.normal(100, 20) * 1_000_000
            market_size = np.random.choice(['Small', 'Medium', 'Large'])
            conference = np.random.choice(['Eastern', 'Western'])
            
            # Team Performance Metrics
            total_wins = np.random.randint(10, 60)
            playoff_appearance = 1 if total_wins > 40 else 0
            
            # Team Star Power Calculation
            team_star_count = 0
            team_performance_scores = []
            team_players_data = []
            
            for player_num in range(1, n_players_per_team + 1):
                # Player-level features
                player_age = np.random.randint(19, 40)
                position = np.random.choice(['Guard', 'Forward', 'Center'])
                height = np.random.normal(200, 10)
                years_in_league = np.random.randint(0, 15)
                
                # Player Performance Metrics
                player_salary = np.random.normal(2, 1) * 1_000_000
                games_played = np.random.randint(0, 82)  # NBA season length
                points_per_game = np.random.normal(10, 5)
                assists_per_game = np.random.normal(3, 2)
                rebounds_per_game = np.random.normal(5, 3)
                
                # Performance Quality Metrics
                performance_score = (
                    points_per_game * 0.4 + 
                    assists_per_game * 0.3 + 
                    rebounds_per_game * 0.3
                )
                
                # Track team performance scores and star players
                team_performance_scores.append(performance_score)
                if performance_score > 15:
                    team_star_count += 1
                
                # Career Trajectory Indicator
                career_trajectory = (
                    1 if performance_score > 15 else
                    0 if performance_score > 10 else
                    -1
                )
                
                # Injury and Resilience
                injury_count = np.random.randint(0, 5)
                injury_impact = min(injury_count * 0.1, 1)
                
                # Qualitative Performance Description
                performance_narrative = (
                    f"A {position} with {points_per_game:.1f} PPG, "
                    f"showing {['declining', 'stable', 'emerging'][career_trajectory+1]} potential"
                )
                
                # Compile data point
                data_point = {
                    # Identifiers
                    'season': season,
                    'team_id': team_id,
                    'team_name': team_name,
                    'player_id': player_num,
                    
                    # Team Features
                    'team_budget': team_budget,
                    'market_size': market_size,
                    'conference': conference,
                    'total_team_wins': total_wins,
                    'playoff_appearance': playoff_appearance,
                    
                    # Player Demographics
                    'player_age': player_age,
                    'position': position,
                    'height_cm': height,
                    'years_in_league': years_in_league,
                    
                    # Performance Metrics
                    'player_salary': player_salary,
                    'games_played': games_played,
                    'points_per_game': points_per_game,
                    'assists_per_game': assists_per_game,
                    'rebounds_per_game': rebounds_per_game,
                    'performance_score': performance_score,
                    
                    # Career and Resilience Metrics
                    'career_trajectory': career_trajectory,
                    'injury_count': injury_count,
                    'injury_impact': injury_impact,
                    
                    # Qualitative Data
                    'performance_narrative': performance_narrative
                }
                
                team_players_data.append(data_point)
            
            # Calculate Team Strength Score
            avg_team_performance = np.mean(team_performance_scores)
            
            # Market size factor
            market_factor = {
                'Small': 0.8,
                'Medium': 1.0,
                'Large': 1.2
            }[market_size]
            
            # Calculate team strength (but not championship potential yet)
            team_strength = (
                (total_wins / 60) * 0.4 +  # Win contribution
                (avg_team_performance / 15) * 0.25 +  # Team performance
                (team_star_count / n_players_per_team) * 0.2 +  # Star power
                (playoff_appearance * 0.1) +  # Playoff bonus
                (market_factor * 0.05)  # Market influence
            )
            
            # Store team strength and data for later processing
            season_team_strengths.append(team_strength)
            season_team_data.append((team_strength, team_players_data))
        
        # Sort teams by strength and determine championship potential
        # Only top 20% of teams get championship potential
        strength_threshold = sorted(season_team_strengths, reverse=True)[int(n_teams * 0.2)]
        
        # Add all players to the dataset with appropriate championship potential
        for team_strength, team_players in season_team_data:
            # Binary championship potential based on team strength
            has_potential = 1 if team_strength >= 1.00*strength_threshold else 0
            
            # Update all players from this team with the championship potential
            for player_data in team_players:
                player_data['championship_potential'] = has_potential
                data.append(player_data)

    # Create DataFrame
    basketball_df = pd.DataFrame(data)
    
    return basketball_df

def main():
    # Open log file
    with open('C:/Users/Fernando/Desktop/basketball_dataset/dataset_generation.log', 'w') as log_file:
        try:
            # Redirect stdout and stderr to log file
            sys.stdout = log_file
            sys.stderr = log_file
            
            # Ensure the directory exists
            output_dir = 'C:/Users/Fernando/Desktop/basketball_dataset'
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate dataset
            basketball_performance_df = generate_basketball_performance_dataset()
            
            # Save dataset
            output_path = os.path.join(output_dir, 'basketball_performance_dataset.csv')
            basketball_performance_df.to_csv(output_path, index=False)
            
            # Print dataset information
            print("Dataset Generation Complete!")
            print(f"Dataset saved to: {output_path}")
            print(f"Dataset shape: {basketball_performance_df.shape}")
            print("\nColumns:")
            print(basketball_performance_df.columns.tolist())
            print("\nFirst few rows:")
            print(basketball_performance_df.head().to_string())
        
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc(file=log_file)

if __name__ == "__main__":
    main()
