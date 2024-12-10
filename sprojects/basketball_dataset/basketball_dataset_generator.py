import numpy as np
import pandas as pd
import random
import os
import sys
import traceback
from scipy.stats import multivariate_normal

class BasketballDatasetGenerator:
    def __init__(self, n_teams=30, n_players_per_team=15, n_seasons=5):
        """
        Initialize dataset generation with correlated variables
        """
        np.random.seed(42)
        self.n_teams = n_teams
        self.n_players_per_team = n_players_per_team
        self.n_seasons = n_seasons
        
        # Correlation matrix for key variables
        self.correlation_matrix = np.array([
            [1.0,   0.7,   0.5,  -0.3],  # Performance Score
            [0.7,   1.0,   0.6,  -0.4],  # Salary
            [0.5,   0.6,   1.0,  -0.2],  # Years in League
            [-0.3, -0.4,  -0.2,   1.0]   # Injury Count
        ])
        
        # Salary tiers with more nuanced probabilities
        self.salary_tiers = {
            'minimum': {
                'range': (1_000_000, 2_500_000),
                'probability': 0.65
            },
            'mid_level': {
                'range': (2_500_000, 10_000_000),
                'probability': 0.25
            },
            'high_performance': {
                'range': (10_000_000, 25_000_000),
                'probability': 0.08
            },
            'max_contract': {
                'range': (25_000_000, 45_000_000),
                'probability': 0.02
            }
        }
        
        # Performance and experience constraints
        self.constraints = {
            'age': {
                'min': 19,
                'max': 40,
                'peak_start': 23,
                'peak_end': 30
            },
            'performance': {
                'points_per_game': {
                    'mean': 10,
                    'std': 5,
                    'min': 0,
                    'max': 35
                },
                'assists_per_game': {
                    'mean': 3,
                    'std': 2,
                    'min': 0,
                    'max': 15
                },
                'rebounds_per_game': {
                    'mean': 5,
                    'std': 3,
                    'min': 0,
                    'max': 20
                }
            }
        }
    
    def generate_correlated_variables(self):
        """
        Generate correlated variables using multivariate normal distribution
        """
        # Mean values for performance score, salary, years in league, injury count
        means = [15, 5_000_000, 5, 2]
        
        # Generate correlated samples
        samples = multivariate_normal.rvs(
            mean=means, 
            cov=self.correlation_matrix, 
            size=1
        )
        
        return {
            'performance_score': np.clip(samples[0], 0, 30),
            'salary': np.clip(samples[1], 1_000_000, 45_000_000),
            'years_in_league': np.clip(samples[2], 0, 20),
            'injury_count': np.clip(samples[3], 0, 10)
        }
    
    def generate_realistic_salary(self, performance_score, years_in_league, position, market_size):
        """
        Generate salary with correlated performance and experience
        """
        # Use correlated variables to influence salary
        correlated_vars = self.generate_correlated_variables()
        
        # Blend generated salary with performance-based calculation
        base_salary = correlated_vars['salary']
        
        # Performance and experience adjustments
        performance_factor = np.clip(performance_score / 20, 0, 1.5)
        experience_factor = np.log1p(years_in_league) * 0.2
        
        # Market size and position multipliers
        market_multipliers = {
            'Small': 0.8,
            'Medium': 1.0,
            'Large': 1.2
        }
        position_multipliers = {
            'Guard': 1.1,
            'Forward': 1.0,
            'Center': 1.2
        }
        
        # Final salary calculation
        salary = (
            base_salary * 
            (1 + performance_factor) * 
            (1 + experience_factor) * 
            market_multipliers.get(market_size, 1.0) *
            position_multipliers.get(position, 1.0)
        )
        
        return int(np.clip(salary, 1_000_000, 45_000_000))
    
    def generate_performance_metrics(self, years_in_league):
        """
        Generate performance metrics with age and experience correlation
        """
        metrics = {}
        experience_penalty = max(0, 1 - (years_in_league / 15))  # Performance decline with age
        
        for metric, config in self.constraints['performance'].items():
            base_value = np.random.normal(config['mean'], config['std'])
            adjusted_value = base_value * (1 - (0.3 * experience_penalty))
            
            if metric == 'points_per_game':
                metrics[metric] = round(np.clip(adjusted_value, config['min'], config['max']))
            else:
                metrics[metric] = round(np.clip(adjusted_value, config['min'], config['max']), 1)
        
        return metrics
    
    def generate_basketball_performance_dataset(self):
        """
        Generate comprehensive synthetic basketball performance dataset
        """
        data = []
        
        for season in range(2018, 2018 + self.n_seasons):
            team_names = [
                f"City {chr(65+i)} {random.choice(['Hawks', 'Wolves', 'Eagles', 'Lions', 'Tigers'])}" 
                for i in range(self.n_teams)
            ]
            
            for team_id, team_name in enumerate(team_names, 1):
                market_size = np.random.choice(['Small', 'Medium', 'Large'])
                conference = np.random.choice(['Eastern', 'Western'])
                total_wins = np.random.randint(10, 60)
                playoff_appearance = 1 if total_wins > 40 else 0
                
                team_performance_scores = []
                
                for player_num in range(1, self.n_players_per_team + 1):
                    # Age and experience with correlation
                    player_age = np.random.randint(19, 40)
                    years_in_league = max(0, player_age - 19)
                    position = np.random.choice(['Guard', 'Forward', 'Center'])
                    
                    # Performance metrics with experience correlation
                    perf_metrics = self.generate_performance_metrics(years_in_league)
                    
                    performance_score = round(
                        perf_metrics['points_per_game'] * 0.4 + 
                        perf_metrics['assists_per_game'] * 0.3 + 
                        perf_metrics['rebounds_per_game'] * 0.3,
                        1
                    )
                    
                    # Salary generation with correlated factors
                    player_salary = self.generate_realistic_salary(
                        performance_score, 
                        years_in_league, 
                        position,
                        market_size
                    )
                    
                    # Career trajectory with performance correlation
                    career_trajectory = (
                        1 if performance_score > 15 else
                        0 if performance_score > 10 else
                        -1
                    )
                    
                    # Injury count with performance impact
                    injury_count = np.random.binomial(5, 0.2)
                    
                    data_point = {
                        'season': season,
                        'team_id': team_id,
                        'team_name': team_name,
                        'player_id': player_num,
                        'market_size': market_size,
                        'conference': conference,
                        'total_team_wins': total_wins,
                        'playoff_appearance': playoff_appearance,
                        
                        'player_age': player_age,
                        'position': position,
                        'years_in_league': years_in_league,
                        
                        'player_salary': player_salary,
                        'points_per_game': perf_metrics['points_per_game'],
                        'assists_per_game': perf_metrics['assists_per_game'],
                        'rebounds_per_game': perf_metrics['rebounds_per_game'],
                        'performance_score': performance_score,
                        
                        'career_trajectory': career_trajectory,
                        'injury_count': injury_count
                    }
                    
                    team_performance_scores.append(performance_score)
                    data.append(data_point)
        
        return pd.DataFrame(data)

def main():
    generator = BasketballDatasetGenerator()
    basketball_performance_df = generator.generate_basketball_performance_dataset()
    
    output_dir = 'C:/Users/Fernando/Desktop/basketball_dataset'
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'basketball_performance_dataset.csv')
    basketball_performance_df.to_csv(output_path, index=False)
    
    print("Dataset Generation Complete!")
    print(f"Dataset saved to: {output_path}")
    print(f"Dataset shape: {basketball_performance_df.shape}")
    
    # Correlation analysis
    print("\nVariable Correlations:")
    correlation_columns = [
        'player_salary', 
        'performance_score', 
        'years_in_league', 
        'injury_count', 
        'points_per_game'
    ]
    print(basketball_performance_df[correlation_columns].corr())

if __name__ == "__main__":
    main()