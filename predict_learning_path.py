from train_recommender import recommend_resources
import pandas as pd

def generate_learning_path(student_id, path_length=5):
    recommendations = recommend_resources(student_id, top_n=path_length)
    difficulty_order = {'easy': 1, 'medium': 2, 'hard': 3}
    recommendations['difficulty_rank'] = recommendations['difficulty'].map(difficulty_order)
    learning_path = recommendations.sort_values('difficulty_rank')
    return learning_path[['resource_id', 'topic', 'resource_type', 'difficulty', 'url']]

if __name__ == "__main__":
    student_id = 0
    path = generate_learning_path(student_id)
    print(f"Learning path for student {student_id}:")
    print(path)
