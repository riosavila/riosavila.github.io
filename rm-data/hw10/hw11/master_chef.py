import numpy as np
import pandas as pd

np.random.seed(42)  # For reproducibility

# Number of chefs
n = 3000

# Correlation matrix for continuous variables
# Variables: [Age, Experience, Knife Skills, Plating Aesthetics, Creativity, Challenge Win Rate, Judges Feedback, Stress Management, Social Media Following]
correlation_matrix = np.array([
    [1.0,  0.7,  0.2,  0.1,  0.1,  0.1,  0.0,  0.0,  0.1],  # Age
    [0.7,  1.0,  0.3,  0.2,  0.2,  0.2,  0.1,  0.1,  0.2],  # Experience
    [0.2,  0.3,  1.0,  0.5,  0.4,  0.3,  0.3,  0.2,  0.0],  # Knife Skills
    [0.1,  0.2,  0.5,  1.0,  0.4,  0.3,  0.4,  0.2,  0.1],  # Plating Aesthetics
    [0.1,  0.2,  0.4,  0.4,  1.0,  0.2,  0.2,  0.1,  0.1],  # Creativity
    [0.1,  0.2,  0.3,  0.3,  0.2,  1.0,  0.5,  0.2,  0.3],  # Challenge Win Rate
    [0.0,  0.1,  0.3,  0.4,  0.2,  0.5,  1.0,  0.2,  0.3],  # Judges Feedback
    [0.0,  0.1,  0.2,  0.2,  0.1,  0.2,  0.2,  1.0,  0.3],  # Stress Management
    [0.1,  0.2,  0.0,  0.1,  0.1,  0.3,  0.3,  0.3,  1.0],  # Social Media Following
])

# Ensure the matrix is positive-definite
assert np.all(np.linalg.eigvals(correlation_matrix) > 0), "Correlation matrix is not positive-definite!"

# Mean and standard deviation for each variable
means = [35, 10, 6, 7, 8, 20, 6.5, 5, 5]  # Approximate means
std_devs = [10, 5, 2, 1.5, 2, 10, 1, 3, 2]  # Approximate standard deviations

# Generate multivariate normal data
data = np.random.multivariate_normal(means, np.diag(std_devs) @ correlation_matrix @ np.diag(std_devs), n)

# Split data into variables
age, experience, knife_skills, plating_aesthetics, creativity, challenge_win_rate, judges_feedback, stress_management, social_media_following = data.T

# Other categorical variables
education_levels = ["High School", "Associate's", "Bachelor's", "Culinary School"]
education_probs = [0.4, 0.3, 0.2, 0.1]
education = np.random.choice(education_levels, n, p=education_probs)

# Map education levels to scores
education_boost = {
    "High School": 0,
    "Associate's": 0.5,
    "Bachelor's": 1.0,
    "Culinary School": 1.5,
}

# Map countries and cuisine specialties
countries = ["USA", "France", "Japan", "India", "Mexico", "Italy", "UK", "Germany", "China", "Brazil"]
country = np.random.choice(countries, n)

cuisine_specialties = ["Italian", "French", "Japanese", "Indian", "Mexican"]
cuisine_specialty = np.random.choice(cuisine_specialties, n)

# Additional variables
audience_popularity = np.random.uniform(0, 10, n)
signature_dishes = np.random.poisson(3, n)
unique_ingredients = np.random.poisson(5, n)
hours_practiced = np.random.normal(20, 5, n).clip(0, 40)

# Score for Top 10% (more comprehensive)
score = (
    0.3 * judges_feedback +
    0.25 * challenge_win_rate +
    0.2 * (creativity * plating_aesthetics) +
    0.1 * knife_skills +
    0.05 * social_media_following * audience_popularity +
    0.05 * stress_management +
    0.05 * education_boost[education[np.random.randint(0, n)]]
)

# Normalize scores and assign top 10%
top_10_percent = (score >= np.percentile(score, 90)).astype(int)

# Generate fake names
first_names = ["James", "Mary", "John", "Patricia", "Robert", "Linda", "Michael", "Barbara", "William", "Elizabeth"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]

names = [
    f"{np.random.choice(first_names)} {np.random.choice(last_names)}"
    for _ in range(n)
]

# Create DataFrame
df = pd.DataFrame({
    "Name": names, "Age": age, "Experience": experience, "KnifeSkills": knife_skills,
    "PlatingAesthetics": plating_aesthetics, "Creativity": creativity,
    "ChallengeWinRate": challenge_win_rate, "JudgesFeedback": judges_feedback,
    "StressManagement": stress_management, "SocialMediaFollowing": social_media_following,
    "Education": education, "Country": country, "CuisineSpecialty": cuisine_specialty,
    "AudiencePopularity": audience_popularity, "SignatureDishes": signature_dishes,
    "UniqueIngredients": unique_ingredients, "HoursPracticed": hours_practiced,
    "Top10Percent": top_10_percent
})

# Save to CSV
df.to_csv("master_chef_simulated_data_with_names.csv", index=False)
