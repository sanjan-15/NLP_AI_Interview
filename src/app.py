import streamlit as st
import numpy as np
import pandas as pd
import spacy
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import nltk
import sys
from pathlib import Path

# Add the project root directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from utils.text_processing import preprocess_text
from utils.response_evaluator import evaluate_response
from utils.question_generator import generate_question

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# Load spaCy model
try:
    nlp = spacy.load('en_core_web_sm')
except:
    spacy.cli.download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

# Initialize Sentence Transformer
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define domains
DOMAINS = {
    "Software Development": ["Programming", "System Design", "Software Architecture"],
    "Data Science": ["Machine Learning", "Statistics", "Data Analysis"],
    "Marketing": ["Digital Marketing", "Brand Management", "Market Research"]
}

def main():
    st.title("AI-Powered Domain Interview System")
    st.write("An intelligent interview system using advanced NLP techniques")

    # Sidebar for domain selection
    st.sidebar.title("Interview Settings")
    selected_domain = st.sidebar.selectbox(
        "Choose Domain",
        list(DOMAINS.keys())
    )
    
    selected_subdomain = st.sidebar.selectbox(
        "Choose Specialization",
        DOMAINS[selected_domain]
    )

    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
        st.session_state.question_history = []
        st.session_state.response_history = []
        st.session_state.scores = []

    # Start Interview button
    if st.sidebar.button("Start New Interview"):
        st.session_state.current_question = generate_question(selected_domain, selected_subdomain)
        st.session_state.question_history = []
        st.session_state.response_history = []
        st.session_state.scores = []

    # Display current question and get response
    if st.session_state.current_question:
        st.write("### Current Question:")
        st.write(st.session_state.current_question)
        
        user_response = st.text_area("Your Answer:", height=150)
        
        if st.button("Submit Answer"):
            if user_response:
                # Preprocess response
                processed_response = preprocess_text(user_response)
                
                # Evaluate response
                score, feedback = evaluate_response(
                    processed_response,
                    st.session_state.current_question,
                    selected_domain
                )
                
                # Store response and score
                st.session_state.question_history.append(st.session_state.current_question)
                st.session_state.response_history.append(user_response)
                st.session_state.scores.append(score)
                
                # Display feedback
                st.write("### Feedback:")
                st.write(feedback)
                st.write(f"Score: {score}/10")
                
                # Generate next question
                st.session_state.current_question = generate_question(
                    selected_domain,
                    selected_subdomain,
                    st.session_state.question_history
                )

    # Display interview progress
    if st.session_state.scores:
        st.sidebar.write("### Interview Progress")
        st.sidebar.write(f"Questions Answered: {len(st.session_state.scores)}")
        st.sidebar.write(f"Average Score: {np.mean(st.session_state.scores):.2f}/10")

if __name__ == "__main__":
    main() 