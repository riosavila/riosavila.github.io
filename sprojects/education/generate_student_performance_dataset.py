import numpy as np
import pandas as pd
import faker
from scipy import stats

# Set random seed for reproducibility
np.random.seed(42)

# Initialize Faker for generating names
fake = faker.Faker()

# Number of students to generate
n_students = 1500

# Define majors with probabilities
majors = ['Computer Science', 'Business', 'Engineering', 'Psychology', 
          'Biology', 'Economics', 'Mathematics', 'Social Sciences']
major_probs = [0.15, 0.2, 0.15, 0.1, 0.1, 0.1, 0.1, 0.1]

# Learning styles
learning_styles = ['Visual', 'Auditory', 'Kinesthetic', 'Reading/Writing']

# Parent education levels with weighted probabilities
parent_edu_levels = ['High School', 'Associate Degree', "Bachelor's Degree", "Master's Degree", 'Doctorate']
parent_edu_probs = [0.35, 0.25, 0.25, 0.12, 0.03]

def generate_student_performance_dataset():
    # Generate basic demographics
    data = {
        'student_id': range(1, n_students + 1),
        'name': [fake.name() for _ in range(n_students)],
        'age': np.random.choice(range(18, 26), n_students, p=[0.35, 0.25, 0.2, 0.1, 0.04, 0.03, 0.02, 0.01]),
        'gender': np.random.choice(['Male', 'Female', 'Non-Binary'], n_students, p=[0.48, 0.48, 0.04]),
        'major': np.random.choice(majors, n_students, p=major_probs),
        'learning_style': np.random.choice(learning_styles, n_students),
        'parents_education_level': np.random.choice(parent_edu_levels, n_students, p=parent_edu_probs)
    }
    df = pd.DataFrame(data)
    
    # Generate sleep quality (hours per night)
    df['avg_sleep_hours'] = np.clip(np.random.normal(7, 1.5, n_students), 4, 10)
    
    # Parent education level influence (higher education = better academic support)
    parent_edu_score = pd.Categorical(df['parents_education_level'], 
                                    categories=parent_edu_levels, 
                                    ordered=True).codes
    parent_edu_influence = (parent_edu_score / (len(parent_edu_levels) - 1))  # Scale to 0-1 range
    
    # Generate high school GPA influenced by parent education
    base_hs_gpa = np.random.normal(3.0, 0.5, n_students)
    df['high_school_gpa'] = np.round(np.clip(base_hs_gpa + parent_edu_influence * 0.5, 2.0, 4.0), 2)
    
    # Study hours influenced by parent education and high school performance
    study_base = np.random.gamma(shape=2, scale=6, size=n_students)
    study_influence = 0.4 * parent_edu_influence + 0.3 * (df['high_school_gpa'] - 2) / 2
    df['study_hours_per_week'] = np.clip(study_base + study_influence * 25, 0, 40).astype(int)
    
    # Family income correlated with parent education
    income_base = np.exp(np.random.normal(11, 0.7, n_students))
    income_edu_boost = parent_edu_score * 15000  # Higher education = higher income
    df['family_income'] = np.round(income_base + income_edu_boost, -3)
    
    # Generate base academic ability (influenced by high school GPA and parent education)
    academic_ability = (
        0.4 * ((df['high_school_gpa'] - 2) / 2) +  # High school performance component
        0.2 * parent_edu_influence +                # Parent education component
        0.2 * (df['study_hours_per_week'] / 40) +  # Study hours component
        0.1 * ((df['avg_sleep_hours'] - 4) / 6) +  # Sleep quality component
        0.1 * np.random.normal(0, 0.2, n_students) # Random variation
    )
    
    # Generate proficiency scores with correlations
    def generate_proficiency(base_score, subject_bonus=0, sleep_factor=True):
        sleep_influence = 0.15 * ((df['avg_sleep_hours'] - 4) / 6) if sleep_factor else 0
        study_influence = 0.3 * (df['study_hours_per_week'] / 40)
        
        score = (
            65 +                                # Base score
            base_score * 25 +                  # Academic ability influence
            subject_bonus +                    # Subject-specific bonus
            sleep_influence * 10 +             # Sleep quality impact
            study_influence * 15 +             # Study hours impact
            np.random.normal(0, 5, n_students) # Random variation
        )
        return np.clip(score, 40, 100).astype(int)
    
    # Generate correlated subject proficiencies
    base_scores = academic_ability + np.random.normal(0, 0.1, n_students)
    
    # English proficiency
    english_bonus = np.where(df['learning_style'] == 'Reading/Writing', 8, 
                   np.where(df['learning_style'] == 'Auditory', 5, 0))
    english_bonus += np.where(df['major'].isin(['Psychology', 'Social Sciences']), 5, 0)
    df['english_proficiency'] = generate_proficiency(base_scores, english_bonus)
    
    # Math proficiency with correlated bonus
    math_bonus = np.where(df['major'].isin(['Computer Science', 'Engineering', 'Mathematics']), 10, 
                np.where(df['major'].isin(['Economics', 'Physics']), 7, 0))
    math_bonus += np.where(df['learning_style'] == 'Visual', 5, 0)
    math_bonus += (df['english_proficiency'] - 70) * 0.15  # Moderate correlation with English
    df['math_proficiency'] = generate_proficiency(base_scores, math_bonus)
    
    # Science proficiency correlated with math
    science_bonus = np.where(df['major'].isin(['Biology', 'Engineering']), 10,
                   np.where(df['major'].isin(['Computer Science', 'Psychology']), 5, 0))
    science_bonus += np.where(df['learning_style'] == 'Kinesthetic', 5, 0)
    science_bonus += (df['math_proficiency'] - 70) * 0.25  # Strong correlation with math
    df['science_proficiency'] = generate_proficiency(base_scores, science_bonus)
    
    # Calculate GPA with realistic correlations
    gpa_components = {
        'high_school': 0.2 * (df['high_school_gpa'] / 4.0),
        'study_hours': 0.2 * (df['study_hours_per_week'] / 40),
        'sleep_quality': 0.1 * ((df['avg_sleep_hours'] - 4) / 6),
        'proficiencies': 0.4 * ((df['english_proficiency'] + df['math_proficiency'] + df['science_proficiency']) / 300),
        'parent_edu': 0.1 * parent_edu_influence
    }
    
    gpa_base = sum(gpa_components.values())
    gpa_with_noise = gpa_base + np.random.normal(0, 0.1, n_students)
    df['final_gpa'] = np.round(np.clip(gpa_with_noise * 4, 1.5, 4.0) * 4) / 4
    
    # Calculate graduation probability with enhanced correlations
    grad_factors = (
        (df['final_gpa'] - 2.0) * 1.5 +           # GPA impact
        (df['study_hours_per_week'] / 40) * 0.8 +  # Study hours impact
        ((df['avg_sleep_hours'] - 4) / 6) * 0.4 +  # Sleep quality impact
        parent_edu_influence * 0.8 +               # Family education impact
        np.where(df['family_income'] > df['family_income'].median(), 0.3, 0) +  # Family income impact
        np.random.normal(0, 0.3, n_students)       # Random factors
    )
    
    grad_prob = 1 / (1 + np.exp(-grad_factors))  # Logistic function
    df['graduation_within_4_years'] = (grad_prob > np.random.random(n_students)).astype(int)
    
    # Generate performance descriptions based on multiple factors
    def get_performance_description(row):
        gpa = row['final_gpa']
        study = row['study_hours_per_week']
        sleep = row['avg_sleep_hours']
        avg_prof = (row['english_proficiency'] + row['math_proficiency'] + row['science_proficiency']) / 3
        
        if gpa >= 3.7:
            if study >= 25:
                return "Outstanding achievement through dedicated effort and consistent study"
            else:
                return "Exceptional academic performance with natural ability"
        elif gpa >= 3.3:
            if sleep >= 7:
                return "Strong performance supported by good sleep habits"
            else:
                return "High achievement despite suboptimal rest"
        elif gpa >= 3.0:
            if study >= 20:
                return "Good academic standing maintained through consistent effort"
            else:
                return "Solid performance with room for increased study time"
        elif gpa >= 2.5:
            if sleep < 6:
                return "Average performance, possibly impacted by insufficient rest"
            else:
                return "Average performance, requires more focused study approach"
        else:
            if study < 10:
                return "Below average performance, needs significant increase in study effort"
            else:
                return "Struggling despite effort, may benefit from academic support services"
    
    df['academic_performance_description'] = df.apply(get_performance_description, axis=1)
    
    return df

# Generate and save the dataset
student_data = generate_student_performance_dataset()
student_data.to_csv('student_performance_dataset.csv', index=False)
print("Dataset generated successfully!")
print("\nDetailed Dataset Summary:")
print("\nNumerical Variables Summary:")
numerical_cols = ['high_school_gpa', 'study_hours_per_week', 'avg_sleep_hours', 
                 'english_proficiency', 'math_proficiency', 'science_proficiency', 'final_gpa']
print(student_data[numerical_cols].describe())

print("\nCorrelation Matrix:")
print(student_data[numerical_cols].corr().round(3))

# Print distribution of GPAs
print("\nGPA Distribution:")
print(student_data['final_gpa'].value_counts().sort_index())
