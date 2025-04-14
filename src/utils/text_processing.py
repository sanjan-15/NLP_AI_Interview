import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

class TextProcessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text):
        """
        Comprehensive text preprocessing using various NLP techniques
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenization
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]
        
        return ' '.join(tokens)

    def extract_entities(self, text):
        """
        Extract named entities using spaCy
        """
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities

    def get_pos_tags(self, text):
        """
        Get Part of Speech tags
        """
        doc = nlp(text)
        pos_tags = [(token.text, token.pos_) for token in doc]
        return pos_tags

    def extract_key_phrases(self, text):
        """
        Extract key phrases using noun chunks
        """
        doc = nlp(text)
        key_phrases = [chunk.text for chunk in doc.noun_chunks]
        return key_phrases

    def analyze_syntax(self, text):
        """
        Analyze syntactic dependencies
        """
        doc = nlp(text)
        dependencies = [(token.text, token.dep_, token.head.text) for token in doc]
        return dependencies

def preprocess_text(text):
    """
    Wrapper function for text preprocessing
    """
    processor = TextProcessor()
    return processor.preprocess_text(text) 