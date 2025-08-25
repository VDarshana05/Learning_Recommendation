import pandas as pd
import numpy as np
import random

def generate_students(num_students=100):
    interests = ['Data Structures', 'Algorithms', 'Operating Systems', 'Computer Networks', 'Databases', 'Machine Learning', 'Cybersecurity', 'Software Engineering']
    skill_levels = ['beginner', 'intermediate', 'advanced']
    career_goals = ['Software Developer', 'Data Scientist', 'Network Engineer', 'Security Analyst', 'Researcher']

    students = []
    for i in range(num_students):
        student = {
            'student_id': i,
            'age': np.random.randint(18, 25),
            'grade_level': np.random.randint(1, 5),  # Undergraduate year
            'learning_pace': random.choice(['slow', 'medium', 'fast']),
            'interests': random.sample(interests, 3),
            'avg_score': np.random.uniform(50, 100),
            'skill_level': random.choice(skill_levels),
            'career_goal': random.choice(career_goals)
        }
        students.append(student)
    return pd.DataFrame(students)

def generate_resources(num_resources=60):
    topics = ['Data Structures', 'Algorithms', 'Operating Systems', 'Computer Networks', 'Databases', 'Machine Learning', 'Cybersecurity', 'Software Engineering']
    resource_types = ['video', 'quiz', 'reading', 'coding_challenge', 'podcast']
    difficulties = ['easy', 'medium', 'hard']

    resources = []
    for i in range(num_resources):
        resource = {
            'resource_id': i,
            'topic': random.choice(topics),
            'resource_type': random.choice(resource_types),
            'difficulty': random.choice(difficulties),
            'url': f"https://example.com/resource/{i}"
        }
        resources.append(resource)
    return pd.DataFrame(resources)

def generate_interactions(students, resources, num_interactions=500):
    interactions = []
    for _ in range(num_interactions):
        student_id = random.choice(students['student_id'])
        # Pick resource from a topic the student is interested in
        interest_topics = students.loc[students['student_id'] == student_id, 'interests'].values[0]
        if isinstance(interest_topics, str):
            interest_topics = eval(interest_topics)  # Handle string representation if loaded from CSV

        eligible_resources = resources[resources['topic'].isin(interest_topics)]
        # Inside generate_interactions function

        if eligible_resources.empty:
            resource_id = random.choice(resources['resource_id'].values)
        else:
            resource_id = random.choice(eligible_resources['resource_id'].values)


        interactions.append({
            'student_id': student_id,
            'resource_id': resource_id,
            'completed': random.choice([0,1]),
            'score': np.random.uniform(50, 100)
        })
    return pd.DataFrame(interactions)

if __name__ == "__main__":
    students = generate_students()
    students.to_csv('students.csv', index=False)
    resources = generate_resources()
    resources.to_csv('resources.csv', index=False)
    interactions = generate_interactions(students, resources)
    interactions.to_csv('interactions.csv', index=False)
