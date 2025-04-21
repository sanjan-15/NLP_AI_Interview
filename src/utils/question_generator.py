import random
from typing import List, Optional

class QuestionGenerator:
    def __init__(self):
        # Initialize question templates organized by difficulty and domain
        self.question_templates = {
            "Software Development": {
                "Beginner": [
                    "What is the purpose of {concept} in software development?",
                    "Explain the concept of {concept} and its basic applications.",
                    "How would you describe {concept} to a junior developer?",
                    "What are the key benefits of using {concept}?",
                    "What is the difference between {concept} and {related_concept}?"
                ],
                "Intermediate": [
                    "How would you implement {concept} in a real-world project? Provide specific examples.",
                    "What are the best practices for {concept} in modern software development?",
                    "Explain how {concept} contributes to code quality and maintainability.",
                    "What challenges might you face when implementing {concept} and how would you address them?",
                    "How has {concept} evolved in recent years, and what are current trends?"
                ],
                "Advanced": [
                    "Design a system that leverages {concept} for a high-scale application.",
                    "Compare and contrast different approaches to implementing {concept} in enterprise systems.",
                    "How would you optimize {concept} for performance in a resource-constrained environment?",
                    "Discuss the trade-offs between {concept} and {related_concept} in complex systems.",
                    "How would you approach refactoring a legacy system to incorporate {concept}?"
                ]
            },
            "Data Science": {
                "Beginner": [
                    "What is the purpose of {concept} in data science?",
                    "Explain the concept of {concept} and its basic applications in data analysis.",
                    "What kind of problems can {concept} help solve?",
                    "What are the key benefits of using {concept} for data processing?",
                    "What is the difference between {concept} and {related_concept}?"
                ],
                "Intermediate": [
                    "How would you apply {concept} to solve a real-world data science problem?",
                    "Explain the mathematical foundations of {concept} and its applications in data analysis.",
                    "What are the advantages and limitations of using {concept} in machine learning?",
                    "How does {concept} compare to {related_concept} in terms of performance and use cases?",
                    "Describe the process of implementing {concept} in a data science project."
                ],
                "Advanced": [
                    "Design a pipeline that uses {concept} for a large-scale machine learning application.",
                    "How would you handle edge cases and limitations when implementing {concept}?",
                    "Discuss the computational complexity of {concept} and approaches to optimization.",
                    "How would you tune the parameters of {concept} for optimal performance?",
                    "Describe a novel approach to extend the capabilities of {concept} for an unusual problem."
                ]
            },
            "Marketing": {
                "Beginner": [
                    "What is {concept} in marketing?",
                    "How does {concept} help in reaching target audiences?",
                    "Explain the basic principles of {concept} in a marketing context.",
                    "What are the key benefits of including {concept} in a marketing strategy?",
                    "What is the difference between {concept} and {related_concept}?"
                ],
                "Intermediate": [
                    "How would you leverage {concept} to improve marketing campaign performance?",
                    "Explain the role of {concept} in modern digital marketing strategies.",
                    "What metrics would you use to measure the success of {concept} in marketing?",
                    "Compare the effectiveness of {concept} versus {related_concept} in marketing.",
                    "How would you implement {concept} in a marketing strategy for a new product launch?"
                ],
                "Advanced": [
                    "Design a comprehensive marketing strategy centered around {concept} for a competitive market.",
                    "How would you integrate {concept} with other marketing approaches for maximum impact?",
                    "Discuss the ROI considerations when investing in {concept} for different types of businesses.",
                    "How would you adapt {concept} for international markets with cultural differences?",
                    "Analyze how {concept} might evolve in the next 5 years and how marketers should prepare."
                ]
            }
        }

        self.domain_concepts = {
            "Software Development": {
                "concepts": [
                    "microservices architecture",
                    "containerization",
                    "continuous integration",
                    "design patterns",
                    "test-driven development",
                    "RESTful APIs",
                    "dependency injection",
                    "clean code principles",
                    "version control",
                    "agile methodologies",
                    "functional programming",
                    "object-oriented design",
                    "reactive programming",
                    "serverless architecture",
                    "DevOps practices"
                ],
                "related_pairs": [
                    ("microservices", "monolithic architecture"),
                    ("unit testing", "integration testing"),
                    ("REST", "GraphQL"),
                    ("Docker", "Kubernetes"),
                    ("Git", "SVN"),
                    ("agile", "waterfall"),
                    ("frontend", "backend"),
                    ("compiled languages", "interpreted languages"),
                    ("statically typed", "dynamically typed"),
                    ("SQL", "NoSQL")
                ]
            },
            "Data Science": {
                "concepts": [
                    "feature engineering",
                    "model validation",
                    "deep learning",
                    "dimensionality reduction",
                    "ensemble methods",
                    "cross-validation",
                    "regularization",
                    "clustering algorithms",
                    "time series analysis",
                    "natural language processing",
                    "data preprocessing",
                    "hypothesis testing",
                    "reinforcement learning",
                    "transfer learning",
                    "explainable AI"
                ],
                "related_pairs": [
                    ("supervised learning", "unsupervised learning"),
                    ("classification", "regression"),
                    ("neural networks", "traditional ML"),
                    ("PCA", "t-SNE"),
                    ("random forests", "gradient boosting"),
                    ("bias", "variance"),
                    ("precision", "recall"),
                    ("online learning", "batch learning"),
                    ("parametric models", "non-parametric models"),
                    ("frequentist", "Bayesian")
                ]
            },
            "Marketing": {
                "concepts": [
                    "content marketing",
                    "SEO optimization",
                    "social media strategy",
                    "marketing automation",
                    "customer segmentation",
                    "brand positioning",
                    "lead generation",
                    "conversion optimization",
                    "email marketing",
                    "influencer marketing",
                    "market research",
                    "customer journey mapping",
                    "A/B testing",
                    "personalization",
                    "marketing analytics"
                ],
                "related_pairs": [
                    ("organic marketing", "paid advertising"),
                    ("B2B marketing", "B2C marketing"),
                    ("social media", "traditional media"),
                    ("content marketing", "direct marketing"),
                    ("inbound marketing", "outbound marketing"),
                    ("branding", "performance marketing"),
                    ("customer acquisition", "customer retention"),
                    ("market segmentation", "mass marketing"),
                    ("digital marketing", "print marketing"),
                    ("qualitative research", "quantitative research")
                ]
            }
        }

    def generate_question(self, domain: str, difficulty: str, previous_questions: Optional[List[str]] = None) -> str:
        """
        Generate a domain-specific question using templates and concepts
        """
        if previous_questions is None:
            previous_questions = []
            
        # Validate inputs
        if domain not in self.question_templates:
            domain = list(self.question_templates.keys())[0]
            
        if difficulty not in self.question_templates[domain]:
            difficulty = "Intermediate"

        # Select template
        domain_templates = self.question_templates[domain][difficulty]
        template = random.choice(domain_templates)

        # Select concepts
        domain_data = self.domain_concepts[domain]
        
        # Generate question
        attempts = 0
        max_attempts = 10
        
        while attempts < max_attempts:
            if "{related_concept}" in template:
                # Select a pair of related concepts
                concept_pair = random.choice(domain_data["related_pairs"])
                question = template.format(concept=concept_pair[0], related_concept=concept_pair[1])
            else:
                # Select a single concept
                concept = random.choice(domain_data["concepts"])
                question = template.format(concept=concept)

            # Check if this question is unique
            if question not in previous_questions:
                return question
                
            attempts += 1
        
        # If we couldn't generate a unique question after max attempts,
        # modify a question slightly to make it different
        if "{related_concept}" in template:
            concept_pair = random.choice(domain_data["related_pairs"])
            return template.format(concept=concept_pair[0], related_concept=concept_pair[1]) + " (Please provide more specific details in your answer.)"
        else:
            concept = random.choice(domain_data["concepts"])
            return template.format(concept=concept) + " (Include specific examples in your answer.)"

def generate_question(domain: str, difficulty: str, previous_questions: Optional[List[str]] = None) -> str:
    """
    Wrapper function for question generation
    """
    generator = QuestionGenerator()
    return generator.generate_question(domain, difficulty, previous_questions) 