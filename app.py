import streamlit as st
import pandas as pd
import plotly.express as px

# Load datasets
students = pd.read_csv('students.csv')
resources = pd.read_csv('resources.csv')
interactions = pd.read_csv('interactions.csv')

st.set_page_config('Learning Recommendation Dashboard', layout='wide')
st.title("📚 Learning Recommendation Dashboard")

# --- Sidebar: Student selection
st.sidebar.header("Choose Options")
student_ids = students['student_id'].tolist()
selected_student_id = st.sidebar.selectbox("Select Student ID", student_ids)

# --- Dataset-wide Analytics ---
st.header("Dataset-wide Insights")
col1, col2, col3 = st.columns(3)

# Skill Level Distribution
with col1:
    fig1 = px.histogram(students, x='skill_level', color='skill_level',
                        title="Skill Level Distribution")
    st.plotly_chart(fig1, use_container_width=True)

# Topic Popularity
with col2:
    topic_counts = interactions.merge(resources[['resource_id', 'topic']], on='resource_id')['topic'].value_counts().reset_index()
    topic_counts.columns = ['topic', 'count']
    fig2 = px.bar(topic_counts, x='topic', y='count', color='topic',
                  title='Topic Popularity (by Interaction Count)')
    st.plotly_chart(fig2, use_container_width=True)

# Resource Type Pie
with col3:
    fig3 = px.pie(resources, names='resource_type', title='Resource Type Distribution')
    st.plotly_chart(fig3, use_container_width=True)

# --- Per Student Recommendation ---
st.header('Personalized Recommendations')
student = students[students['student_id'] == selected_student_id].iloc[0]
st.subheader(f"Student Details: {getattr(student, 'name', 'N/A')}")
st.write(f"- **Skill Level:** {student['skill_level']}")
st.write(f"- **Learning Pace:** {student['learning_pace']}")
st.write(f"- **Interests:** {student['interests']}")

# Simple recommendation: all resources matching the student's interests and skill
try:
    interests = eval(student['interests']) if isinstance(student['interests'], str) else student['interests']
except:
    interests = [student['interests']] if isinstance(student['interests'], str) else []

allowed_difficulty = ['easy', 'medium'] if student['skill_level'] == 'beginner' else ['medium', 'hard']
recs = resources[
    (resources['topic'].isin(interests)) &
    (resources['difficulty'].isin(allowed_difficulty))
]

st.subheader("Recommended Resources")
if recs.empty:
    st.info("No recommended resources found for this student.")
else:
    st.dataframe(recs[['resource_id', 'topic', 'resource_type', 'difficulty', 'url']])


if 'avg_score' in students.columns:
    st.markdown("### Student Progress (Avg Scores by Skill Level)")
    fig4 = px.box(students, x='skill_level', y='avg_score', points='all')
    st.plotly_chart(fig4, use_container_width=True)


