import streamlit as st
import numpy as np
import spacy
import nltk
from pathlib import Path
import os
import sys
import random

# Add the src directory to Python path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Import utility modules
from utils.text_processing import preprocess_text
from utils.response_evaluator import evaluate_response
from utils.question_generator import generate_question
from utils.chat_agents import create_interview_agents, get_rule_based_chat_response
from utils.references import get_domain_references, get_topic_references, format_reference_for_display, get_improvement_suggestions

# Initialize NLP components
@st.cache_resource
def load_nlp_models():
    # Download necessary NLTK data
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('averaged_perceptron_tagger')
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet')

    # Load spaCy model
    try:
        nlp = spacy.load('en_core_web_sm')
    except OSError:
        spacy.cli.download('en_core_web_sm')
        nlp = spacy.load('en_core_web_sm')
    
    return nlp

# Define domains
DOMAINS = {
    "Software Development": ["Programming", "System Design", "Software Architecture"],
    "Data Science": ["Machine Learning", "Statistics", "Data Analysis"],
    "Marketing": ["Digital Marketing", "Brand Management", "Market Research"]
}

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'question_history' not in st.session_state:
        st.session_state.question_history = []
    if 'scores' not in st.session_state:
        st.session_state.scores = []
    if 'agents' not in st.session_state:
        st.session_state.agents = None
    if 'interview_started' not in st.session_state:
        st.session_state.interview_started = False
    if 'current_question_messages' not in st.session_state:
        st.session_state.current_question_messages = 0
    if 'evaluation_done' not in st.session_state:
        st.session_state.evaluation_done = False
    if 'chat_mode' not in st.session_state:
        st.session_state.chat_mode = False
    if 'models' not in st.session_state:
        st.session_state.models = None
    if 'chat_count' not in st.session_state:
        st.session_state.chat_count = 0
    if 'current_topic' not in st.session_state:
        st.session_state.current_topic = None

def display_chat_message(role: str, content: str, score: float = None):
    """Display a chat message with appropriate styling"""
    if role == "assistant":
        st.markdown(f"🤖 **Interviewer:** {content}")
    elif role == "user":
        st.markdown(f"👤 **You:** {content}")
    elif role == "system":
        if score is not None:
            color = "green" if score >= 7 else "orange" if score >= 5 else "red"
            st.markdown(f"📊 **Evaluation:** Score: <span style='color:{color}'>{score:.1f}/10</span>", unsafe_allow_html=True)
        st.markdown(f"💡 **Feedback:** {content}")
    elif role == "improvement":
        st.markdown(f"🔍 **Improvement Tips:** {content}")
    elif role == "references":
        st.markdown(f"📚 **Learning Resources:** {content}")
    elif role == "chat":
        st.markdown(f"🤖 **Assistant:** {content}")

def display_references(domain: str, topic: str = None, score: float = None):
    """Display relevant references and learning resources."""
    # Get references
    refs = get_topic_references(domain, topic)
    
    # Get improvement suggestions
    suggestions = get_improvement_suggestions(domain, topic, score)
    
    # Display improvement suggestions
    if suggestions:
        display_chat_message("improvement", "\n".join(suggestions))
    
    # Format and display references
    reference_text = ""
    for category, items in refs.items():
        if items:  # Only show categories with items
            reference_text += f"**{category.replace('_', ' ').title()}**\n"
            for item in items[:2]:  # Limit to 2 items per category
                reference_text += format_reference_for_display(item) + "\n"
    
    if reference_text:
        display_chat_message("references", reference_text)

def extract_topic_from_question(question):
    """Extract the main topic from a question for better reference matching"""
    # Simple extraction based on keywords
    question_lower = question.lower()
    
    # Common topics by domain
    topics = {
        "Software Development": ["microservices", "design patterns", "architecture", "testing", 
                              "refactoring", "clean code", "agile", "version control", 
                              "api", "database", "interface", "debugging", "solid", "object-oriented",
                              "framework", "library", "dependency", "exception", "distributed system"],
        "Data Science": ["machine learning", "algorithm", "data", "features", "model", 
                      "classification", "regression", "clustering", "neural", "statistics",
                      "visualization", "prediction", "training", "supervised", "unsupervised",
                      "overfitting", "normalization", "exploratory", "missing data", "bias-variance",
                      "deep learning", "random forest", "sentiment analysis"],
        "Marketing": ["campaign", "audience", "segmentation", "brand", "digital", 
                   "content", "strategy", "social media", "analytics", "conversion",
                   "inbound", "outbound", "marketing funnel", "swot", "roi", 
                   "a/b testing", "retention", "competitive analysis", "b2b", "b2c",
                   "omnichannel"]
    }
    
    # Search for multi-word topics first (more specific)
    found_topics = []
    for domain, domain_topics in topics.items():
        for topic in domain_topics:
            if " " in topic:  # Multi-word topic
                if topic in question_lower:
                    found_topics.append(topic)
    
    # If no multi-word topics found, try single words
    if not found_topics:
        for domain, domain_topics in topics.items():
            for topic in domain_topics:
                if " " not in topic and topic in question_lower:
                    found_topics.append(topic)
    
    # If still no topics found, extract key nouns based on common patterns in questions
    if not found_topics:
        # Extract topic after "concept of", "principles of", etc.
        patterns = ["concept of ", "purpose of ", "principles of ", "difference between ", "explain ", "describe "]
        for pattern in patterns:
            if pattern in question_lower:
                # Get the words following the pattern
                after_pattern = question_lower.split(pattern)[1].split()
                # Take first 2-3 words as potential topic
                potential_topic = " ".join(after_pattern[:3])
                found_topics.append(potential_topic)
                break
    
    # If all else fails, use longest words in the question as they're often domain-specific terms
    if not found_topics:
        words = question_lower.split()
        # Filter out short words and get the longest ones
        long_words = [word for word in words if len(word) > 5]
        if long_words:
            # Sort by length (descending) and take the top 2
            long_words.sort(key=len, reverse=True)
            found_topics = long_words[:2]
    
    return " ".join(found_topics) if found_topics else None

def format_references_as_text(domain, topic=None, score=None):
    """Format references as text to be included directly in feedback"""
    # Get references
    refs = get_topic_references(domain, topic)
    
    # Get improvement suggestions
    suggestions = get_improvement_suggestions(domain, topic, score)
    
    # Format the text
    result = ""
    
    # Add improvement suggestions
    if suggestions:
        result += "\n\n🔍 **Improvement Tips:**\n" + "\n".join(suggestions)
    
    # Add references
    result += "\n\n📚 **Learning Resources:**"
    
    # Check if there are any references to display
    has_references = False
    
    for category, items in refs.items():
        if items:  # Only show categories with items
            has_references = True
            result += f"\n**{category.replace('_', ' ').title()}**:\n"
            for item in items[:2]:  # Limit to 2 items per category
                result += format_reference_for_display(item) + "\n"
    
    # If no specific references found, include some general domain references
    if not has_references:
        # Add default references based on domain
        result += "\n**Recommended Resources**:\n"
        if domain == "Software Development":
            result += "- [Clean Code by Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)\n"
            result += "- [Design Patterns: Elements of Reusable Object-Oriented Software](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)\n"
        elif domain == "Data Science":
            result += "- [Python for Data Analysis by Wes McKinney](https://www.amazon.com/Python-Data-Analysis-Wrangling-IPython/dp/1491957662)\n"
            result += "- [Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow](https://www.amazon.com/Hands-Machine-Learning-Scikit-Learn-TensorFlow/dp/1492032646)\n"
        elif domain == "Marketing":
            result += "- [Marketing Management by Philip Kotler](https://www.amazon.com/Marketing-Management-15th-Philip-Kotler/dp/0133856461)\n"
            result += "- [Digital Marketing Strategy by Simon Kingsnorth](https://www.amazon.com/Digital-Marketing-Strategy-Integrated-Approach/dp/0749484225)\n"
    
    return result

def main():
    st.title("Rule-based Technical Interview Assistant")
    
    # Initialize session state
    initialize_session_state()
    
    # Load NLP models
    nlp = load_nlp_models()
    st.session_state.models = {"nlp": nlp}
    
    # Create interview agents if not already created
    if not st.session_state.agents:
        st.session_state.agents = create_interview_agents()
    
    # Sidebar for domain selection and controls
    st.sidebar.title("Interview Settings")
    
    domain = st.sidebar.selectbox(
        "Select Domain",
        ["Software Development", "Data Science", "Marketing"]
    )
    
    difficulty = st.sidebar.select_slider(
        "Select Difficulty",
        options=["Beginner", "Intermediate", "Advanced"]
    )
    
    # Display interview progress in sidebar if interview started
    if st.session_state.scores:
        st.sidebar.write("### Progress")
        avg_score = np.mean(st.session_state.scores)
        st.sidebar.progress(min(avg_score/10, 1.0), f"Average Score: {avg_score:.1f}/10")
        st.sidebar.write(f"Questions Answered: {len(st.session_state.scores)}")
        if st.session_state.chat_mode:
            st.sidebar.write(f"Chat Exchanges: {st.session_state.chat_count}/8")
    
    # Start interview button
    if not st.session_state.interview_started and st.sidebar.button("Start Interview"):
        st.session_state.interview_started = True
        st.session_state.current_question = generate_question(
            domain,
            difficulty,
            st.session_state.question_history
        )
        st.session_state.question_history.append(st.session_state.current_question)
        st.session_state.current_topic = extract_topic_from_question(st.session_state.current_question)
        
        # Add welcome message
        welcome_msg = (
            f"Welcome to your {domain} interview! "
            f"I'll be asking you questions about {domain}. "
            "Let's begin with your first question:"
        )
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
        st.session_state.messages.append({"role": "assistant", "content": st.session_state.current_question})
        st.rerun()
    
    # Reset interview button
    if st.session_state.interview_started and st.sidebar.button("Reset Interview"):
        st.session_state.messages = []
        st.session_state.current_question = None
        st.session_state.question_history = []
        st.session_state.scores = []
        st.session_state.interview_started = False
        st.session_state.evaluation_done = False
        st.session_state.chat_mode = False
        st.session_state.chat_count = 0
        st.session_state.current_topic = None
        st.rerun()
    
    # Main chat interface
    chat_container = st.container()
    with chat_container:
        # Display all messages
        for message in st.session_state.messages:
            role = message.get("role", "assistant")
            content = message.get("content", "")
            score = message.get("score", None)
            display_chat_message(role, content, score)
    
    # Input area at the bottom
    st.markdown("---")
    if st.session_state.interview_started:
        # Create a container for input at the bottom
        with st.container():
            # Show different prompts based on mode
            if st.session_state.chat_mode:
                prompt = "Ask a question about this topic:"
                button_text = "Ask"
                
                # Add suggested questions to help the user
                st.write("Suggested questions you could ask:")
                question_cols = st.columns(2)
                
                suggested_questions = [
                    "Can you explain this concept in simpler terms?",
                    "What are the key best practices?",
                    "Can you provide a concrete example?",
                    "What are common challenges or pitfalls?"
                ]
                
                for i, question in enumerate(suggested_questions):
                    with question_cols[i % 2]:
                        if st.button(question, key=f"suggest_{i}"):
                            user_response = question
                            st.session_state.messages.append({"role": "user", "content": user_response})
                            
                            # Get chat response
                            chat_response = get_rule_based_chat_response(
                                user_response,
                                st.session_state.current_question,
                                domain
                            )
                            
                            # Add response to messages
                            st.session_state.messages.append({"role": "chat", "content": chat_response})
                            
                            # Increment chat count
                            st.session_state.chat_count += 1
                            
                            st.rerun()
            else:
                prompt = "Your Answer:"
                button_text = "Submit"
            
            user_response = st.text_area(prompt, key="user_input", height=100)
            
            if st.button(button_text, use_container_width=True):
                if user_response:
                    if st.session_state.chat_mode:
                        # Check if we've reached the chat limit
                        if st.session_state.chat_count >= 8:
                            st.error("You've reached the maximum number of chat exchanges (8). Submit your final answer or move to the next question.")
                            st.rerun()
                        
                        # Handle chat mode - follow-up questions
                        st.session_state.messages.append({"role": "user", "content": user_response})
                        
                        # Get chat response
                        chat_response = get_rule_based_chat_response(
                            user_response,
                            st.session_state.current_question,
                            domain
                        )
                        
                        # Add response to messages
                        st.session_state.messages.append({"role": "chat", "content": chat_response})
                        
                        # Increment chat count
                        st.session_state.chat_count += 1
                        
                        # Check if we've reached the maximum chat exchanges
                        if st.session_state.chat_count >= 8:
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": "You've reached the maximum number of chat exchanges. Please submit your final answer or move to the next question."
                            })
                        
                        st.rerun()
                    else:
                        # Handle answer submission mode
                        st.session_state.messages.append({"role": "user", "content": user_response})
                        
                        # Evaluate the response
                        score, feedback = evaluate_response(
                            st.session_state.current_question,
                            user_response,
                            domain,
                            nlp
                        )
                        
                        # Store results
                        st.session_state.scores.append(score)
                        st.session_state.evaluation_done = True
                        
                        # Combine feedback with references
                        references_text = format_references_as_text(domain, st.session_state.current_topic, score)
                        combined_feedback = feedback + references_text
                        
                        # Add evaluation and feedback
                        st.session_state.messages.append({
                            "role": "system",
                            "content": combined_feedback,
                            "score": score
                        })
                        
                        # Add option to ask questions
                        st.session_state.chat_mode = True
                        st.session_state.chat_count = 0
                        st.session_state.messages.append({
                            "role": "chat",
                            "content": "You can now ask up to 8 follow-up questions about this topic to better understand it."
                        })
                        
                        st.rerun()
            
            # Show next question button when in chat mode
            if st.session_state.chat_mode and st.button("Next Question", use_container_width=True):
                # Reset chat mode and generate new question
                st.session_state.chat_mode = False
                st.session_state.chat_count = 0
                st.session_state.evaluation_done = False
                
                # Generate new question
                st.session_state.current_question = generate_question(
                    domain,
                    difficulty,
                    st.session_state.question_history
                )
                st.session_state.question_history.append(st.session_state.current_question)
                
                # Extract topic from new question
                st.session_state.current_topic = extract_topic_from_question(st.session_state.current_question)
                
                # Add to messages
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Moving on to the next question:"
                })
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": st.session_state.current_question
                })
                
                st.rerun()

if __name__ == "__main__":
    main() 