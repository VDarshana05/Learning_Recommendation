import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def visualize_dataset_insights(students, interactions, resources, save_path=None):
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))
    
    # Skill Level Distribution
    sns.countplot(x='skill_level', data=students, ax=axs[0, 0], palette='pastel')
    axs[0, 0].set_title('Skill Level Distribution Across Students')
    axs[0, 0].set_xlabel('Skill Level')
    axs[0, 0].set_ylabel('Number of Students')
    
    # Topic Popularity in Interactions
    merged = interactions.merge(resources[['resource_id', 'topic']], on='resource_id')
    topic_counts = merged['topic'].value_counts()
    topic_counts.plot(kind='bar', ax=axs[0, 1], color='skyblue')
    axs[0, 1].set_title('Popularity of Topics (by Interaction Count)')
    axs[0, 1].set_xlabel('Topic')
    axs[0, 1].set_ylabel('Number of Interactions')
    
    # Resource Type Distribution
    resource_type_counts = resources['resource_type'].value_counts()
    resource_type_counts.plot(kind='pie', autopct='%1.1f%%', ax=axs[1, 0], startangle=90)
    axs[1, 0].set_title('Resource Type Distribution')
    axs[1, 0].set_ylabel('')
    
    # Learning Pace vs Average Score Scatterplot
    pace_order = {'slow': 1, 'medium': 2, 'fast': 3}
    students['pace_num'] = students['learning_pace'].map(pace_order)
    sns.scatterplot(x='pace_num', y='avg_score', hue='skill_level', data=students, palette='Set2', ax=axs[1, 1])
    axs[1, 1].set_title('Learning Pace vs Average Score')
    axs[1, 1].set_xlabel('Learning Pace (slow=1, fast=3)')
    axs[1, 1].set_ylabel('Average Score')
    axs[1, 1].legend(title='Skill Level')
    
    plt.suptitle('Dataset-Wide Personalized Learning Insights', fontsize=16, fontweight='bold')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    if save_path:
        os.makedirs(save_path, exist_ok=True)
        file_path = os.path.join(save_path, 'dataset_insights_dashboard.png')
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        print(f"Visualization saved at: {file_path}")
    
    plt.show()

if __name__ == "__main__":
    # Load datasets
    students = pd.read_csv('students.csv')
    resources = pd.read_csv('resources.csv')
    interactions = pd.read_csv('interactions.csv')
    
    # Call visualization and save the image in "visualizations" folder
    visualize_dataset_insights(students, interactions, resources, save_path="visualizations")
