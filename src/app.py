import streamlit as st
import numpy as np
import spacy
import nltk
from pathlib import Path
import os
import sys

# Add the src directory to Python path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Import utility modules
from utils.text_processing import preprocess_text
from utils.response_evaluator import evaluate_response
from utils.question_generator import generate_question
from utils.chat_agents import create_interview_agents

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
        st.markdown(f"📚 **Improvement Tips:**\n{content}")
    elif role == "chat":
        st.markdown(f"🤖 **Assistant:** {content}")

def get_chatbot_response(user_input: str, domain: str, current_question: str) -> str:
    """Generate a context-aware chat response"""
    # Extract the main topic from the current question
    topic = current_question.lower()
    
    # Domain-specific knowledge bases
    domain_knowledge = {
        "Software Development": {
            "clean code": [
                "Clean code implementation involves several key principles:",
                "1. **Meaningful Names**: Use clear, intention-revealing names for variables, functions, and classes",
                "2. **Single Responsibility**: Each function or class should do one thing and do it well",
                "3. **DRY (Don't Repeat Yourself)**: Avoid code duplication through proper abstraction",
                "4. **SOLID Principles**: Follow Object-Oriented Design principles",
                "5. **Comments and Documentation**: Write self-documenting code with necessary comments",
                "6. **Error Handling**: Implement proper exception handling and validation",
                "7. **Unit Testing**: Write comprehensive tests for your code"
            ],
            "architecture": [
                "Software architecture best practices include:",
                "1. **Layered Architecture**: Separate concerns into presentation, business, and data layers",
                "2. **Microservices**: Break down complex applications into manageable services",
                "3. **API Design**: Create clear, consistent, and well-documented APIs",
                "4. **Scalability**: Design for horizontal and vertical scaling",
                "5. **Security**: Implement security at every layer"
            ],
            "testing": [
                "Effective testing strategies include:",
                "1. **Unit Testing**: Test individual components in isolation",
                "2. **Integration Testing**: Test component interactions",
                "3. **End-to-End Testing**: Test complete user workflows",
                "4. **Test-Driven Development (TDD)**: Write tests before implementation",
                "5. **Continuous Integration**: Automate testing in your pipeline"
            ]
        },
        "Data Science": {
            "machine learning": [
                "Key machine learning concepts:",
                "1. **Feature Engineering**: Create relevant features from raw data",
                "2. **Model Selection**: Choose appropriate algorithms for your problem",
                "3. **Cross-Validation**: Ensure model generalization",
                "4. **Hyperparameter Tuning**: Optimize model parameters",
                "5. **Model Evaluation**: Use appropriate metrics for assessment"
            ],
            "data analysis": [
                "Data analysis best practices:",
                "1. **Data Cleaning**: Handle missing values and outliers",
                "2. **Exploratory Analysis**: Understand data distributions and relationships",
                "3. **Statistical Testing**: Apply appropriate statistical methods",
                "4. **Visualization**: Create informative plots and charts",
                "5. **Reporting**: Communicate findings effectively"
            ]
        },
        "Marketing": {
            "digital marketing": [
                "Digital marketing strategies include:",
                "1. **SEO Optimization**: Improve search engine rankings",
                "2. **Content Marketing**: Create valuable, relevant content",
                "3. **Social Media**: Engage with audiences effectively",
                "4. **Email Marketing**: Build and nurture customer relationships",
                "5. **Analytics**: Track and measure campaign performance"
            ],
            "brand management": [
                "Brand management principles:",
                "1. **Brand Identity**: Develop consistent brand elements",
                "2. **Positioning**: Create unique market positioning",
                "3. **Customer Experience**: Ensure consistent brand experience",
                "4. **Brand Monitoring**: Track brand perception and mentions",
                "5. **Crisis Management**: Handle brand-related issues"
            ]
        }
    }

    # Identify the relevant topic from the question
    relevant_topic = None
    for topic in domain_knowledge[domain].keys():
        if topic in current_question.lower():
            relevant_topic = topic
            break

    user_input_lower = user_input.lower()
    
    # Handle different types of questions
    if "explain" in user_input_lower or "detail" in user_input_lower:
        if relevant_topic and relevant_topic in domain_knowledge[domain]:
            return "\n".join(domain_knowledge[domain][relevant_topic])
        return f"Let me explain the key concepts in {domain}:\n" + "\n".join(domain_knowledge[domain][list(domain_knowledge[domain].keys())[0]])
    
    elif "example" in user_input_lower:
        examples = {
            "clean code": """Here's a practical example of clean code:

```python
# Bad code
def p(x, y):
    return x + y

# Clean code
def add_numbers(first_number: float, second_number: float) -> float:
    "Add two numbers and return their sum."
    return first_number + second_number
```""",
            "machine learning": """Here's a practical example of machine learning pipeline:

```python
# Data preprocessing
X_train = preprocess_data(raw_data)
# Feature engineering
features = create_features(X_train)
# Model training
model = RandomForestClassifier()
model.fit(features, y_train)
```""",
            "digital marketing": """Example digital marketing campaign structure:
1. Goal: Increase website traffic by 50%
2. Strategy: Content marketing + SEO
3. Tactics:
   - Weekly blog posts
   - Social media sharing
   - Email newsletter
4. Metrics: Traffic, engagement, conversions"""
        }
        if relevant_topic in examples:
            return examples[relevant_topic]
        return f"Here's a general example for {domain}:\n" + examples[list(examples.keys())[0]]
    
    elif "how" in user_input_lower:
        implementations = {
            "clean code": """To implement clean code:
1. Use version control (git)
2. Set up code linting and formatting
3. Implement code review process
4. Write comprehensive tests
5. Use meaningful variable/function names
6. Keep functions small and focused
7. Document your code properly""",
            "machine learning": """Steps to implement ML:
1. Data collection and cleaning
2. Feature engineering
3. Model selection and training
4. Validation and testing
5. Deployment and monitoring
6. Regular model updates""",
            "digital marketing": """Digital marketing implementation:
1. Set clear goals and KPIs
2. Create content calendar
3. Set up analytics tracking
4. Implement SEO best practices
5. Monitor and adjust strategies"""
        }
        if relevant_topic in implementations:
            return implementations[relevant_topic]
        return f"Here's how to approach this in {domain}:\n" + implementations[list(implementations.keys())[0]]
    
    elif "best practice" in user_input_lower or "tip" in user_input_lower:
        practices = {
            "clean code": """Clean Code Best Practices:
1. Write self-documenting code
2. Follow SOLID principles
3. Keep functions small and focused
4. Use meaningful names
5. Write tests first (TDD)
6. Regular code reviews
7. Continuous refactoring""",
            "machine learning": """ML Best Practices:
1. Start simple, then iterate
2. Cross-validate everything
3. Handle data leakage
4. Version control your data
5. Document assumptions
6. Monitor model performance""",
            "digital marketing": """Digital Marketing Best Practices:
1. Know your audience
2. Test and measure everything
3. Focus on mobile-first
4. Create valuable content
5. Optimize for conversion"""
        }
        if relevant_topic in practices:
            return practices[relevant_topic]
        return f"Best practices in {domain}:\n" + practices[list(practices.keys())[0]]
    
    else:
        return f"I can help you understand {relevant_topic if relevant_topic else 'this topic'} better. Would you like to know about:\n" + \
               "1. Detailed explanation\n" + \
               "2. Practical examples\n" + \
               "3. Implementation steps\n" + \
               "4. Best practices\n" + \
               "Just ask about any of these aspects!"

def main():
    st.title("🎯 AI Interview Assistant")
    
    # Load NLP models
    nlp = load_nlp_models()

    # Sidebar for domain selection and controls
    st.sidebar.title("Interview Settings")
    selected_domain = st.sidebar.selectbox(
        "Choose Domain",
        list(DOMAINS.keys())
    )
    
    selected_subdomain = st.sidebar.selectbox(
        "Choose Specialization",
        DOMAINS[selected_domain]
    )

    # Initialize session state
    initialize_session_state()

    # Create interview agents if not already created
    if st.session_state.agents is None:
        st.session_state.agents = create_interview_agents(selected_domain)

    # Start/Reset Interview button
    if st.sidebar.button("Start New Interview"):
        st.session_state.messages = []
        st.session_state.current_question = generate_question(selected_domain, selected_subdomain)
        st.session_state.question_history = []
        st.session_state.scores = []
        st.session_state.interview_started = True
        st.session_state.current_question_messages = 0
        st.session_state.evaluation_done = False
        st.session_state.chat_mode = False
        # Add initial greeting
        welcome_msg = (
            f"Welcome to your {selected_domain} interview! "
            f"I'll be asking you questions about {selected_subdomain}. "
            "Let's begin with your first question:"
        )
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
        st.session_state.messages.append({"role": "assistant", "content": st.session_state.current_question})

    # Display interview progress in sidebar
    if st.session_state.scores:
        st.sidebar.write("### Progress")
        avg_score = np.mean(st.session_state.scores)
        st.sidebar.progress(min(avg_score/10, 1.0), f"Average Score: {avg_score:.1f}/10")
        st.sidebar.write(f"Questions Answered: {len(st.session_state.scores)}")
        if st.session_state.current_question_messages > 0:
            st.sidebar.write(f"Chat Messages: {st.session_state.current_question_messages}/8")

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
            else:
                prompt = "Your Answer:"
            
            user_response = st.text_area(prompt, key="user_input", height=100)
            
            # Show different button text based on mode
            button_text = "Ask" if st.session_state.chat_mode else "Submit"
            
            if st.button(button_text, use_container_width=True):
                if user_response and st.session_state.current_question_messages < 8:
                    st.session_state.current_question_messages += 1
                    
                    if st.session_state.chat_mode:
                        # Handle chat mode
                        st.session_state.messages.append({"role": "user", "content": user_response})
                        chat_response = get_chatbot_response(user_response, selected_domain, st.session_state.current_question)
                        st.session_state.messages.append({"role": "chat", "content": chat_response})
                        
                        # Check if we should move to next question
                        if st.session_state.current_question_messages >= 8:
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": "We've reached the maximum number of interactions for this question. Let's move to the next one:"
                            })
                            st.session_state.current_question = generate_question(
                                selected_domain,
                                selected_subdomain,
                                st.session_state.question_history
                            )
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": st.session_state.current_question
                            })
                            st.session_state.current_question_messages = 0
                            st.session_state.chat_mode = False
                    else:
                        # Handle answer evaluation mode
                        st.session_state.messages.append({"role": "user", "content": user_response})
                        
                        # Process and evaluate response
                        processed_response = preprocess_text(user_response)
                        score, feedback = evaluate_response(
                            processed_response,
                            st.session_state.current_question,
                            selected_domain
                        )
                        
                        # Store score
                        st.session_state.scores.append(score)
                        
                        # Add evaluation and feedback
                        st.session_state.messages.append({
                            "role": "system",
                            "content": feedback,
                            "score": score
                        })
                        
                        # Get improvement suggestions if needed
                        if score < 8.0:
                            improvement_agent = st.session_state.agents["improvement"]
                            suggestions = improvement_agent.get_improvement_suggestions(score, user_response)
                            if suggestions:
                                suggestion_text = "\n".join(f"• {s}" for s in suggestions)
                                st.session_state.messages.append({
                                    "role": "improvement",
                                    "content": suggestion_text
                                })
                        
                        # Switch to chat mode after evaluation
                        st.session_state.chat_mode = True
                        st.session_state.messages.append({
                            "role": "chat",
                            "content": "You can now ask questions about this topic to better understand it. You have 8 messages per question."
                        })
                    
                    # Clear the input area
                    st.rerun()
                elif st.session_state.current_question_messages >= 8:
                    st.error("You've reached the maximum number of messages for this question. Moving to the next question.")
                    st.session_state.current_question = generate_question(
                        selected_domain,
                        selected_subdomain,
                        st.session_state.question_history
                    )
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "Let's move on to the next question:"
                    })
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": st.session_state.current_question
                    })
                    st.session_state.current_question_messages = 0
                    st.session_state.chat_mode = False
                    st.rerun()

if __name__ == "__main__":
    main() 