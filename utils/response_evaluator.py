from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
import numpy as np
from .text_processing import TextProcessor

class ResponseEvaluator:
    def __init__(self):
        self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
        self.sentiment_analyzer = pipeline('sentiment-analysis')
        self.text_processor = TextProcessor()
        
        # Domain-specific keywords and concepts
        self.domain_concepts = {
            "Software Development": [
                "algorithms", "data structures", "design patterns",
                "clean code", "testing", "version control",
                "scalability", "performance", "security"
            ],
            "Data Science": [
                "machine learning", "statistics", "data analysis",
                "visualization", "feature engineering", "model evaluation",
                "big data", "neural networks", "regression"
            ],
            "Marketing": [
                "market research", "brand awareness", "customer segmentation",
                "digital marketing", "ROI", "campaign analysis",
                "social media", "content strategy", "conversion"
            ]
        }

    def calculate_semantic_similarity(self, response, reference):
        """
        Calculate semantic similarity between response and reference using BERT embeddings
        """
        response_embedding = self.sentence_transformer.encode(response, convert_to_tensor=True)
        reference_embedding = self.sentence_transformer.encode(reference, convert_to_tensor=True)
        
        similarity = util.pytorch_cos_sim(response_embedding, reference_embedding)
        return float(similarity[0][0])

    def analyze_domain_relevance(self, response, domain):
        """
        Analyze how well the response aligns with domain-specific concepts
        """
        response_tokens = set(self.text_processor.preprocess_text(response).split())
        domain_keywords = set(self.domain_concepts.get(domain, []))
        
        # Calculate overlap between response and domain concepts
        keyword_overlap = response_tokens.intersection(domain_keywords)
        relevance_score = len(keyword_overlap) / len(domain_keywords)
        
        return relevance_score

    def analyze_technical_depth(self, response):
        """
        Analyze technical depth using NLP features
        """
        # Extract named entities and key phrases
        entities = self.text_processor.extract_entities(response)
        key_phrases = self.text_processor.extract_key_phrases(response)
        
        # Calculate technical depth score based on entities and key phrases
        technical_score = (len(entities) + len(key_phrases)) / 10  # Normalized score
        return min(1.0, technical_score)

    def analyze_clarity(self, response):
        """
        Analyze response clarity using sentiment and syntax
        """
        # Get sentiment analysis
        sentiment = self.sentiment_analyzer(response)[0]
        
        # Analyze syntax
        syntax = self.text_processor.analyze_syntax(response)
        
        # Calculate clarity score based on sentiment confidence and syntactic complexity
        sentiment_score = sentiment['score']
        syntax_score = min(1.0, len(syntax) / 20)  # Normalize based on complexity
        
        clarity_score = (sentiment_score + syntax_score) / 2
        return clarity_score

def evaluate_response(response, question, domain):
    """
    Main function to evaluate user responses
    """
    evaluator = ResponseEvaluator()
    
    # Calculate various scores
    relevance_score = evaluator.analyze_domain_relevance(response, domain) * 3  # Weight: 30%
    technical_score = evaluator.analyze_technical_depth(response) * 4    # Weight: 40%
    clarity_score = evaluator.analyze_clarity(response) * 3             # Weight: 30%
    
    # Calculate total score (out of 10)
    total_score = relevance_score + technical_score + clarity_score
    
    # Generate feedback
    feedback = []
    feedback.append("Response Evaluation:")
    feedback.append(f"- Domain Relevance: {relevance_score:.1f}/3.0")
    feedback.append(f"- Technical Depth: {technical_score:.1f}/4.0")
    feedback.append(f"- Clarity and Structure: {clarity_score:.1f}/3.0")
    
    # Add specific feedback based on scores
    if relevance_score < 1.5:
        feedback.append("\nTip: Try to incorporate more domain-specific concepts and terminology.")
    if technical_score < 2:
        feedback.append("\nTip: Consider adding more technical details and specific examples.")
    if clarity_score < 1.5:
        feedback.append("\nTip: Work on making your response more clear and well-structured.")
    
    return total_score, "\n".join(feedback) 