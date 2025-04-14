import random
from transformers import pipeline
import json

class QuestionGenerator:
    def __init__(self):
        # Initialize question templates and domain-specific knowledge base
        self.question_templates = {
            "Software Development": [
                "Explain the concept of {concept} and its practical applications in software development.",
                "How would you implement {concept} in a real-world project? Provide specific examples.",
                "What are the best practices for {concept} in modern software development?",
                "Compare and contrast {concept} with {related_concept} in terms of their use cases.",
                "Describe a situation where {concept} would be the optimal solution and explain why."
            ],
            "Data Science": [
                "How would you apply {concept} to solve a real-world data science problem?",
                "Explain the mathematical foundations of {concept} and its applications in data analysis.",
                "What are the advantages and limitations of using {concept} in machine learning?",
                "How does {concept} compare to {related_concept} in terms of performance and use cases?",
                "Describe the process of implementing {concept} in a data science project."
            ],
            "Marketing": [
                "How would you leverage {concept} to improve marketing campaign performance?",
                "Explain the role of {concept} in modern digital marketing strategies.",
                "What metrics would you use to measure the success of {concept} in marketing?",
                "Compare the effectiveness of {concept} versus {related_concept} in marketing.",
                "How would you implement {concept} in a marketing strategy for a new product launch?"
            ]
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
                    "agile methodologies"
                ],
                "related_pairs": [
                    ("microservices", "monolithic architecture"),
                    ("unit testing", "integration testing"),
                    ("REST", "GraphQL"),
                    ("Docker", "Kubernetes"),
                    ("Git", "SVN")
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
                    "natural language processing"
                ],
                "related_pairs": [
                    ("supervised learning", "unsupervised learning"),
                    ("classification", "regression"),
                    ("neural networks", "traditional ML"),
                    ("PCA", "t-SNE"),
                    ("random forests", "gradient boosting")
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
                    "influencer marketing"
                ],
                "related_pairs": [
                    ("organic marketing", "paid advertising"),
                    ("B2B marketing", "B2C marketing"),
                    ("social media", "traditional media"),
                    ("content marketing", "direct marketing"),
                    ("inbound marketing", "outbound marketing")
                ]
            }
        }

    def generate_question(self, domain, subdomain, previous_questions=None):
        """
        Generate a domain-specific question using templates and concepts
        """
        if previous_questions is None:
            previous_questions = []

        # Select template
        template = random.choice(self.question_templates[domain])

        # Select concepts
        domain_data = self.domain_concepts[domain]
        
        if "{related_concept}" in template:
            # Select a pair of related concepts
            concept_pair = random.choice(domain_data["related_pairs"])
            question = template.format(concept=concept_pair[0], related_concept=concept_pair[1])
        else:
            # Select a single concept
            concept = random.choice(domain_data["concepts"])
            question = template.format(concept=concept)

        # Ensure we don't repeat questions
        if question in previous_questions and len(previous_questions) < len(self.question_templates[domain]) * len(domain_data["concepts"]):
            return self.generate_question(domain, subdomain, previous_questions)

        return question

def generate_question(domain, subdomain, previous_questions=None):
    """
    Wrapper function for question generation
    """
    generator = QuestionGenerator()
    return generator.generate_question(domain, subdomain, previous_questions) 