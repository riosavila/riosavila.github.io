import numpy as np
import pandas as pd

np.random.seed(42)  # For reproducibility

# Number of chefs
n = 3000

# Correlation matrix for continuous variables
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

# Ensure integer values for relevant variables
age = np.clip(np.round(age).astype(int), 18, 65)  # Age between 18 and 65
experience = np.clip(np.round(experience).astype(int), 0, 40)  # Experience between 0 and 40

# Limit decimals for continuous variables
knife_skills = np.clip(np.round(knife_skills, 2), 1, 10)  # Knife skills between 1 and 10
plating_aesthetics = np.clip(np.round(plating_aesthetics, 2), 1, 10)  # Plating aesthetics between 1 and 10
creativity = np.clip(np.round(creativity, 2), 1, 10)  # Creativity between 1 and 10
challenge_win_rate = np.clip(np.round(challenge_win_rate, 2), 0, 100)  # Win rate between 0 and 100
judges_feedback = np.clip(np.round(judges_feedback, 2), 1, 10)  # Feedback between 1 and 10
stress_management = np.clip(np.round(stress_management, 2), 1, 10)  # Stress management between 1 and 10
social_media_following = np.clip(np.round(social_media_following, 2), 0, 10)  # Social media following between 0 and 10

# Categorical variables
education_levels = ["High School", "Associate's", "Bachelor's", "Culinary School"]
education_probs = [0.4, 0.3, 0.2, 0.1]
education = np.random.choice(education_levels, n, p=education_probs)

countries = ["USA", "France", "Japan", "India", "Mexico", "Italy", "UK", "Germany", "China", "Brazil"]
country = np.random.choice(countries, n)

cuisine_specialties = ["Italian", "French", "Japanese", "Indian", "Mexican"]
cuisine_specialty = np.random.choice(cuisine_specialties, n)

# Additional variables
audience_popularity = np.clip(np.round(np.random.uniform(0, 10, n), 2), 0, 10)
signature_dishes = np.random.poisson(3, n).clip(0, 15)
unique_ingredients = np.random.poisson(5, n).clip(0, 20)
hours_practiced = np.clip(np.round(np.random.normal(20, 5, n), 2), 0, 40)

# Compute scores and assign Top 10%
#score = (
#    0.3 * judges_feedback +
#    0.25 * challenge_win_rate +
#    0.2 * (creativity * plating_aesthetics) +
#    0.1 * knife_skills +
#    0.05 * social_media_following * audience_popularity +
#    0.05 * stress_management + np.random.normal(0, 14) 
#)

score = (
    # Linear contributions
    0.15 * judges_feedback +
    0.10 * knife_skills +
    0.10 * creativity +
    0.08 * plating_aesthetics +
    0.07 * social_media_following +
    0.05 * experience +
    
    # Nonlinear contributions
    0.15 * judges_feedback**2 +                             # Reward extreme feedback
    0.10 * np.sqrt(challenge_win_rate) +                    # Diminished returns on win rate
    0.08 * (creativity * plating_aesthetics) +              # Interaction: Creativity × Presentation
    0.05 * (unique_ingredients**2 / (signature_dishes + 1)) + # Creative use of ingredients
    0.05 * stress_management**1.5 +                         # Amplify stress management at high levels

    # Threshold-based contributions
    0.07 * (audience_popularity > 7) * audience_popularity + # Extra weight for high popularity
    0.05 * (age > 40) * (stress_management * experience) +   # Older chefs with experience and calmness

    # Interaction and inverses
    0.10 * (hours_practiced / (experience + 1)) +            # Efficiency in practice
    0.05 * np.log1p(social_media_following * audience_popularity) # Amplify online popularity
)

# Normalize the score to a 0-100 range
score = (score - score.min()) / (score.max() - score.min()) * 100

top_10_percent = ( (score+np.random.normal(0,10,n) ) >= np.percentile(score, np.random.normal(80, 2))).astype(int)

# Generate random chef names
first_names = ["James", "Mary", "John", "Patricia", "Robert", "Linda", "Michael", "Barbara", "William", "Elizabeth"]
middle_names = ["Alexander", "Grace", "Benjamin", "Sophie", "Christopher", "Emma", "Daniel", "Olivia", "Edward", "Sophia"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]

names = [
    f"{np.random.choice(first_names)} {np.random.choice(middle_names)} {np.random.choice(last_names)}"
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
df.to_csv("master_chef_cleaned_data.csv", index=False)
