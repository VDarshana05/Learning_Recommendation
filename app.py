import streamlit as st
import pandas as pd
import plotly.express as px

# Load datasets
students = pd.read_csv('students.csv')
resources = pd.read_csv('resources.csv')
interactions = pd.read_csv('interactions.csv')

st.set_page_config('Learning Recommendation Dashboard', layout='wide')
st.title("📚 Learning Recommendation Dashboard")

# --- Dataset-wide Analytics ---
st.header("Dataset-wide Insights")
col1, col2, col3 = st.columns(3)

# Skill Level Distribution
with col1:
    fig1 = px.histogram(students, x='skill_level', color='skill_level', title="Skill Level Distribution")
    st.plotly_chart(fig1, use_container_width=True)

# Topic Popularity
with col2:
    merged = interactions.merge(resources[['resource_id', 'topic']], on='resource_id')
    topic_counts = merged['topic'].value_counts().reset_index()
    topic_counts.columns = ['topic', 'count']
    fig2 = px.bar(topic_counts, x='topic', y='count', color='topic', title='Topic Popularity (by Interaction Count)')
    st.plotly_chart(fig2, use_container_width=True)

# Resource Type Pie
with col3:
    fig3 = px.pie(resources, names='resource_type', title='Resource Type Distribution')
    st.plotly_chart(fig3, use_container_width=True)

# --- User Input Section ---
st.header("Personalized Recommendation")

# Get student ID input
student_input = st.text_input("Enter your Student ID:")

if student_input:
    try:
        student_id = int(student_input)
        if student_id in students['student_id'].values:
            st.success(f"Student ID {student_id} found! Fetching recommendations...")

            # Display student details
            student = students[students['student_id'] == student_id].iloc[0]
            st.write(f"**Name:** {student.get('name', 'N/A')}")
            st.write(f"**Skill Level:** {student['skill_level']}")
            st.write(f"**Learning Pace:** {student['learning_pace']}")
            st.write(f"**Interests:** {student['interests']}")

            # Simple recommendations based on interests and skill level
            try:
                interests = eval(student['interests']) if isinstance(student['interests'], str) else student['interests']
            except:
                interests = [student['interests']] if isinstance(student['interests'], str) else []

            allowed_difficulty = ['easy', 'medium'] if student['skill_level'] == 'beginner' else ['medium', 'hard']
            recommended = resources[
                (resources['topic'].isin(interests)) &
                (resources['difficulty'].isin(allowed_difficulty))
            ]

            st.subheader("Recommended Resources")
            if recommended.empty:
                st.info("No recommendations found based on the current data.")
            else:
                st.dataframe(recommended[['resource_id', 'topic', 'resource_type', 'difficulty', 'url']])

        else:
            st.error(f"Student ID {student_id} not found. Please enter a valid ID.")
    except ValueError:
        st.error("Please enter a valid integer Student ID.")
else:
    st.info("Please enter a Student ID above to see recommendations.")



st.markdown("---")

