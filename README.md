# Rule-Based Technical Interview Assistant

This is a streamlined technical interview assistant that uses rule-based approaches for response evaluation, feedback generation, and follow-up question handling.

## Key Features

1. **Smart Question Generation**: Uses domain-specific templates with automatic question selection
2. **Semantic Response Evaluation**: Employs Sentence Transformers for basic response similarity
3. **Rule-Based Feedback**: Generates constructive feedback based on keyword analysis
4. **Learning Resources**: Provides curated references for improvement in each domain
5. **Multi-Chat Support**: Allows up to 8 follow-up questions after each answer submission

## Models Used

- Response Evaluation: `all-MiniLM-L6-v2` (Sentence Transformers)
- NLP Processing: `en_core_web_sm` (spaCy)
- NLTK for text analysis

## Setup Instructions

1. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run src/app.py
   ```

## User Experience Flow

1. **Initial Setup**: Select domain and difficulty level and start the interview
2. **Answer Submission**: Respond to the interview question
3. **Evaluation**: Receive score and detailed feedback on your answer
4. **Multi-Chat Phase**: Ask up to 8 follow-up questions to clarify concepts
5. **Next Question**: After completing the chat phase, proceed to a new question

## Advantages of Rule-Based Approach

1. **Lightweight**: Minimal dependencies and lightweight models
2. **Fast Loading**: Quick startup with no large model loading
3. **Predictable Responses**: Rule-based feedback ensures consistent quality
4. **Offline Operation**: Works entirely offline without requiring internet
5. **Resource Efficient**: Minimal CPU/RAM requirements

## Modules

1. **Question Generator**: Creates domain-specific interview questions
2. **Response Evaluator**: Scores responses based on semantic similarity and keywords
3. **Chat Agents**: Provides follow-up responses to user questions
4. **References**: Curates domain-specific learning resources
5. **Text Processing**: Handles basic NLP tasks

## Troubleshooting

If you encounter dependency issues:

1. Ensure you have the latest pip and setuptools:

   ```bash
   pip install --upgrade pip setuptools wheel
   ```

2. Install packages individually if needed:
   ```bash
   pip install numpy==1.26.0
   pip install streamlit==1.25.0
   pip install sentence-transformers==2.4.0
   pip install spacy==3.6.0
   pip install nltk==3.8.1
   # ... then download required models
   python -m spacy download en_core_web_sm
   python -m nltk.downloader punkt wordnet
   ```

## Future Improvements

1. Add more sophisticated rule-based evaluation metrics
2. Expand the reference database
3. Add support for code evaluation and execution
4. Enhance the chat responses with more context-awareness
5. Add adaptive difficulty based on user performance

## License

MIT License
