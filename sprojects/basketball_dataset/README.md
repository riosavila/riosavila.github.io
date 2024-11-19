# Basketball Performance Analysis Dataset

## Overview
This project provides a synthetic basketball dataset designed for advanced statistical analysis, suitable for master's level data science students.

## Dataset Contents
- `players_data.csv`: Individual player statistics
- `team_stats.csv`: Team-level performance metrics
- `games_data.csv`: Game outcomes and details
- `basketball_analysis_project.qmd`: Comprehensive project guidelines

## Project Structure
```
basketball_dataset/
│
├── generate_dataset.py    # Script to regenerate synthetic data
├── players_data.csv       # Player statistics
├── team_stats.csv         # Team performance data
├── games_data.csv         # Game-level information
└── basketball_analysis_project.qmd  # Project instructions
```

## Getting Started
1. Ensure you have Python 3.8+ installed
2. Install required libraries:
   ```
   pip install pandas numpy scikit-learn faker
   ```
3. Open the Quarto document for full project details

## Regenerating Data
To regenerate the dataset, run:
```
python generate_dataset.py
```

## Project Objectives
- Develop regression models
- Create logistic/probit models
- Perform comprehensive data analysis

## Recommended Environment
- Python 3.8+
- Jupyter/Quarto
- pandas, numpy, scikit-learn
- statsmodels

## License
Educational use only. Not for commercial purposes.