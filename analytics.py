import streamlit as st
from SRC.search_tracker import get_top_questions, get_top_users
 
def show_analytics():
 
    st.title("📊 Chatbot Analytics Dashboard")
 
    # TOP QUESTIONS
    st.subheader("🔥 Most Asked Questions")
 
    questions = get_top_questions()
 
    for q in questions:
        st.write(f"{q[0]} → {q[1]} times")
 
 
    # TOP USERS
    st.subheader("👤 Most Active Users")
 
    users = get_top_users()
 
    for user in users:
        st.write(f"{user[0]} → {user[1]} searches")