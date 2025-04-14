from typing import List, Dict, Optional
import random

class InterviewAgent:
    def __init__(self, role: str, domain: str):
        self.role = role
        self.domain = domain
        self.chat_count = 0
        self.MAX_CHATS = 5
        
        # Define agent personalities and their focus areas
        self.agent_types = {
            "technical_expert": {
                "focus": "technical depth",
                "questions": [
                    "Could you elaborate more on {concept}?",
                    "How would you implement {concept} in practice?",
                    "What are the potential challenges in implementing {concept}?",
                    "Can you explain the technical details of {concept}?",
                    "What are the best practices when working with {concept}?"
                ]
            },
            "improvement_coach": {
                "focus": "improvement suggestions",
                "questions": [
                    "Have you considered learning more about {concept}?",
                    "What resources would you use to improve your knowledge of {concept}?",
                    "How would you approach learning {concept} in more depth?",
                    "What practical projects could help you better understand {concept}?",
                    "How do you plan to stay updated with {concept}?"
                ]
            },
            "clarification_seeker": {
                "focus": "clarity and understanding",
                "questions": [
                    "Could you clarify your approach to {concept}?",
                    "What do you mean specifically when you mention {concept}?",
                    "Can you provide an example of {concept} in action?",
                    "How would you explain {concept} to a beginner?",
                    "What are the key components of {concept}?"
                ]
            }
        }

    def generate_follow_up(self, response: str, score: float, feedback: str) -> Optional[str]:
        """Generate a follow-up question based on the response and score"""
        self.chat_count += 1
        if self.chat_count >= self.MAX_CHATS:
            return None

        # Extract concepts from the response
        concepts = self._extract_key_concepts(response)
        
        if score < 7.0:
            # Focus on improvement for lower scores
            agent_type = "improvement_coach"
            if score < 5.0:
                # Add clarification questions for very low scores
                agent_type = "clarification_seeker"
        else:
            # Ask more technical questions for high scores
            agent_type = "technical_expert"

        # Select a random question template and fill it with a concept
        question_template = random.choice(self.agent_types[agent_type]["questions"])
        concept = random.choice(concepts) if concepts else "this topic"
        
        return question_template.format(concept=concept)

    def _extract_key_concepts(self, response: str) -> List[str]:
        """Extract key concepts from the response"""
        # Simple keyword extraction
        keywords = response.lower().split()
        domain_specific_concepts = {
            "Software Development": [
                "architecture", "design", "testing", "deployment", "scalability",
                "algorithm", "database", "security", "performance", "framework",
                "api", "code", "development", "programming", "software"
            ],
            "Data Science": [
                "model", "algorithm", "data", "analysis", "prediction",
                "feature", "training", "validation", "accuracy", "dataset",
                "machine learning", "statistics", "visualization", "preprocessing", "clustering"
            ],
            "Marketing": [
                "strategy", "campaign", "audience", "conversion", "engagement",
                "brand", "market", "customer", "social", "content",
                "advertising", "marketing", "sales", "digital", "analytics"
            ]
        }
        
        # Get concepts for the current domain
        domain_concepts = domain_specific_concepts.get(self.domain, [])
        
        # Find matching concepts in the response
        found_concepts = []
        for concept in domain_concepts:
            if concept in response.lower():
                found_concepts.append(concept)
        
        return found_concepts if found_concepts else ["this topic"]

    def _generate_scenario(self) -> str:
        """Generate a domain-specific scenario"""
        scenarios = {
            "Software Development": [
                "a high-traffic web application",
                "a distributed system",
                "a legacy code migration"
            ],
            "Data Science": [
                "a large dataset with missing values",
                "a real-time prediction system",
                "an imbalanced classification problem"
            ],
            "Marketing": [
                "a product launch campaign",
                "a brand repositioning strategy",
                "a digital marketing conversion optimization"
            ]
        }
        return random.choice(scenarios.get(self.domain, ["this situation"]))

    def get_improvement_suggestions(self, score: float, response: str) -> List[str]:
        """Generate specific improvement suggestions based on the score and response"""
        suggestions = []
        
        if score < 7.0:
            suggestions.extend([
                f"Consider studying more about core {self.domain} concepts",
                "Try to provide more specific examples in your answers",
                "Focus on practical applications of theoretical concepts",
                f"Look into real-world applications of {self.domain}",
                "Practice explaining complex concepts clearly"
            ])
        
        if score < 5.0:
            suggestions.extend([
                "Review fundamental concepts in this area",
                "Practice explaining technical concepts more clearly",
                "Work on structured response formats",
                "Consider taking some online courses in this domain",
                "Try to build practical projects to reinforce your knowledge"
            ])
            
        return suggestions[:3]  # Return top 3 suggestions

def create_interview_agents(domain: str) -> Dict[str, InterviewAgent]:
    """Create a set of interview agents for different roles"""
    return {
        "technical": InterviewAgent("technical_expert", domain),
        "improvement": InterviewAgent("improvement_coach", domain),
        "clarification": InterviewAgent("clarification_seeker", domain)
    } 