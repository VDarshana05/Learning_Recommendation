import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from topic_graph import topic_graph
from skill_assessment import assess_skill_level
from explanations import generate_explanations

# Load datasets
students = pd.read_csv('students.csv')
resources = pd.read_csv('resources.csv')
interactions = pd.read_csv('interactions.csv')

# Convert interests column to list
students['interests'] = students['interests'].apply(lambda x: eval(x) if isinstance(x, str) else x)

# Difficulty and skill level mapping
difficulty_map = {'easy': 1, 'medium': 2, 'hard': 3}
skill_level_map = {'beginner': 1, 'intermediate': 2, 'advanced': 3}

# Check if prerequisites are satisfied
def can_recommend_topic(mastered_topics, topic):
    prereqs = topic_graph.get(topic, [])
    return all(pr in mastered_topics for pr in prereqs)

# Get unified topic list from students and resources
student_topics = set(topic for sublist in students['interests'] for topic in sublist)
resource_topics = set(resources['topic'].unique())
all_topics = sorted(list(student_topics.union(resource_topics)))

# Binarize students' interests with consistent topic columns
mlb_students = MultiLabelBinarizer(classes=all_topics)
student_interest_matrix = mlb_students.fit_transform(students['interests'])

# Binarize resources' topics similarly
resource_topics_list = resources['topic'].apply(lambda x: [x])
mlb_resources = MultiLabelBinarizer(classes=all_topics)
resource_topic_matrix = mlb_resources.fit_transform(resource_topics_list)

# Compute cosine similarity matrix between students and resources
similarity = cosine_similarity(student_interest_matrix, resource_topic_matrix)

def update_student_skill_levels(interactions, students):
    """
    Update skill levels for students based on recent scores in interactions.
    """
    for student_id in students['student_id']:
        student_scores = interactions[interactions['student_id'] == student_id]['score'].tolist()
        new_skill = assess_skill_level(student_scores)
        students.loc[students['student_id'] == student_id, 'skill_level'] = new_skill

def recommend_resources(student_id, top_n=7):
    student = students[students['student_id'] == student_id].iloc[0]
    mastered = []  # optionally deduce from interactions or skill levels

    # Filter resources by difficulty relative to student skill level
    allowed_difficulty = [k for k, v in difficulty_map.items() if v <= skill_level_map[student['skill_level']] + 1]
    career_related_topics = [student['interests'][0]]  # simple assumption

    sim_scores = similarity[students.index[students['student_id'] == student_id][0]]

    filtered_resources = resources[
        (resources['difficulty'].isin(allowed_difficulty)) &
        (resources['topic'].isin(career_related_topics))
    ]

    filtered_resources = filtered_resources[
        filtered_resources['topic'].apply(lambda t: can_recommend_topic(mastered, t))
    ]

    filtered_indices = filtered_resources.index.tolist()
    filtered_sim_scores = sim_scores[filtered_indices]

    recommended_indices = np.argsort(filtered_sim_scores)[::-1][:top_n]
    recommendations = filtered_resources.iloc[recommended_indices]
    return recommendations

if __name__ == "__main__":
    update_student_skill_levels(interactions, students)

    while True:
        try:
            student_id = int(input("Enter the student ID to get recommendations (or -1 to exit): "))
            if student_id == -1:
                print("Exiting...")
                break

            if student_id not in students['student_id'].values:
                print(f"Student ID {student_id} not found. Please try again.")
                continue

            recommendations = recommend_resources(student_id)
            student = students[students['student_id'] == student_id].iloc[0]
            explanations = generate_explanations(student, recommendations)

            print(f"\nRecommended resources for student {student_id}:")
            print(recommendations[['resource_id', 'topic', 'resource_type', 'difficulty', 'url']])
            for res, expl in zip(recommendations.itertuples(), explanations):
                print(f"Resource {res.resource_id}: {expl}")

        except ValueError:
            print("Invalid input. Please enter a valid integer student ID.")

