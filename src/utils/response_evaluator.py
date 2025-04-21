from sentence_transformers import SentenceTransformer, util
import numpy as np
import random
from typing import Tuple, List, Dict
import nltk
from collections import Counter

class ResponseEvaluator:
    def __init__(self, nlp):
        # Initialize the sentence transformer model for semantic similarity
        self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
        self.nlp = nlp
        
        # Domain-specific keywords and concepts
        self.domain_concepts = {
            "Software Development": [
                "algorithms", "data structures", "design patterns",
                "clean code", "testing", "version control",
                "scalability", "performance", "security",
                "architecture", "framework", "api", "database",
                "deployment", "debugging", "code review", "documentation",
                "agile", "devops", "continuous integration"
            ],
            "Data Science": [
                "machine learning", "statistics", "data analysis",
                "visualization", "feature engineering", "model evaluation",
                "big data", "neural networks", "regression", "classification",
                "clustering", "data cleaning", "hypothesis testing", "correlation",
                "predictive modeling", "overfitting", "validation", "training data",
                "algorithm", "deep learning"
            ],
            "Marketing": [
                "market research", "brand awareness", "customer segmentation",
                "digital marketing", "ROI", "campaign analysis",
                "social media", "content strategy", "conversion", "lead generation",
                "customer journey", "target audience", "SEO", "PPC", "analytics",
                "email marketing", "A/B testing", "engagement", "brand positioning",
                "marketing funnel"
            ]
        }
        
        # Feedback templates based on different score ranges
        self.feedback_templates = {
            "high": [
                "Excellent answer that covers the key aspects of the topic. You demonstrated good understanding of {concepts}.",
                "Strong response that effectively addresses the question. Your explanation of {concepts} was particularly good.",
                "Comprehensive answer that shows in-depth knowledge. The way you connected {concepts} was impressive.",
                "Very good response with clear explanations. Your understanding of {concepts} is evident."
            ],
            "medium": [
                "Good answer that covers some important aspects. Consider exploring {concepts} in more depth.",
                "Solid response with some good points. To improve, you could elaborate more on {concepts}.",
                "Decent answer that shows understanding. Adding more specifics about {concepts} would strengthen it.",
                "Your answer demonstrates basic knowledge. Try to provide more concrete examples of {concepts} in practice."
            ],
            "low": [
                "Your answer touches on the topic but lacks depth. Focus on strengthening your understanding of {concepts}.",
                "There are some gaps in your explanation. Study more about {concepts} to improve your knowledge.",
                "Your response is too general. Work on developing specific knowledge about {concepts}.",
                "The answer needs more specific details and technical accuracy. Review the fundamentals of {concepts}."
            ]
        }

    def calculate_semantic_similarity(self, response: str, question: str) -> float:
        """
        Calculate semantic similarity between response and question
        """
        response_embedding = self.sentence_transformer.encode(response, convert_to_tensor=True)
        question_embedding = self.sentence_transformer.encode(question, convert_to_tensor=True)
        
        similarity = util.pytorch_cos_sim(response_embedding, question_embedding)
        return float(similarity[0][0])

    def analyze_domain_relevance(self, response: str, domain: str) -> Tuple[float, List[str]]:
        """
        Analyze how well the response aligns with domain-specific concepts
        """
        response_lower = response.lower()
        domain_keywords = self.domain_concepts.get(domain, [])
        
        # Calculate keyword presence
        found_keywords = []
        for keyword in domain_keywords:
            if keyword.lower() in response_lower:
                found_keywords.append(keyword)
        
        # Calculate relevance score
        relevance_score = min(1.0, len(found_keywords) / 5)  # Normalize, max at 5 keywords
        
        return relevance_score, found_keywords

    def analyze_response_quality(self, response: str) -> float:
        """
        Analyze response quality based on length, structure, and complexity
        """
        # Simple metrics for response quality
        words = response.split()
        word_count = len(words)
        
        # Sentence count
        sentences = nltk.sent_tokenize(response)
        sentence_count = len(sentences)
        
        # Calculate word diversity (unique words ratio)
        unique_words = len(set(w.lower() for w in words))
        word_diversity = unique_words / max(1, word_count)
        
        # Calculate quality score
        length_score = min(1.0, word_count / 200)  # Max at 200 words
        complexity_score = min(1.0, sentence_count / 10)  # Max at 10 sentences
        diversity_score = word_diversity
        
        quality_score = (length_score * 0.4) + (complexity_score * 0.3) + (diversity_score * 0.3)
        return quality_score

    def get_feedback(self, score: float, found_concepts: List[str], domain: str) -> str:
        """
        Generate constructive feedback based on evaluation scores
        """
        # Determine feedback category based on score
        if score >= 7.5:
            templates = self.feedback_templates["high"]
        elif score >= 5.0:
            templates = self.feedback_templates["medium"]
        else:
            templates = self.feedback_templates["low"]
        
        # Get random concepts if none found
        if not found_concepts:
            domain_concepts = self.domain_concepts.get(domain, [])
            found_concepts = random.sample(domain_concepts, min(3, len(domain_concepts)))
        
        # Ensure we have at most 3 concepts for readability
        if len(found_concepts) > 3:
            found_concepts = random.sample(found_concepts, 3)
        
        # Format concepts for readability
        concepts_text = ", ".join(found_concepts)
        
        # Generate feedback
        feedback = random.choice(templates).format(concepts=concepts_text)
        
        # Add improvement suggestions
        if score < 7.5:
            suggestions = [
                f"Try to provide more specific examples related to {random.choice(found_concepts)}.",
                f"Consider discussing practical applications of the concepts you mentioned.",
                f"Structure your answer with clear sections covering different aspects of the topic.",
                f"Include relevant industry best practices in your response.",
                f"Compare and contrast different approaches to demonstrate deeper understanding."
            ]
            feedback += "\n\n" + random.choice(suggestions)
        
        return feedback

def evaluate_response(question: str, response: str, domain: str, nlp) -> Tuple[float, str]:
    """
    Main function to evaluate user responses
    """
    evaluator = ResponseEvaluator(nlp)
    
    # Calculate various scores
    semantic_similarity = evaluator.calculate_semantic_similarity(response, question)
    relevance_score, found_concepts = evaluator.analyze_domain_relevance(response, domain)
    quality_score = evaluator.analyze_response_quality(response)
    
    # Calculate total score (out of 10)
    semantic_weight = 0.5
    relevance_weight = 0.3
    quality_weight = 0.2
    
    total_score = (
        semantic_similarity * semantic_weight * 10 +
        relevance_score * relevance_weight * 10 +
        quality_score * quality_weight * 10
    )
    
    # Generate feedback
    feedback = evaluator.get_feedback(total_score, found_concepts, domain)
    
    return total_score, feedback 