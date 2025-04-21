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

def create_interview_agents(domain: str = None) -> Dict[str, InterviewAgent]:
    """Create a set of interview agents for different roles"""
    domains = ["Software Development", "Data Science", "Marketing"]
    domain = domain if domain in domains else domains[0]
    
    return {
        "technical": InterviewAgent("technical_expert", domain),
        "improvement": InterviewAgent("improvement_coach", domain),
        "clarification": InterviewAgent("clarification_seeker", domain)
    }

def get_rule_based_chat_response(user_input: str, current_question: str, domain: str) -> str:
    """Generate a context-aware chat response to user follow-up questions"""
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
    if "explain" in user_input_lower or "detail" in user_input_lower or "what is" in user_input_lower:
        if relevant_topic and relevant_topic in domain_knowledge[domain]:
            return "\n".join(domain_knowledge[domain][relevant_topic])
        return f"The concept in this question relates to core principles in {domain}. The key point to understand is how this applies in real-world scenarios and what best practices are recommended by industry experts."
    
    elif "example" in user_input_lower or "instance" in user_input_lower or "sample" in user_input_lower:
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
        
        if domain == "Software Development":
            return "A good example would be how clean code principles apply in a large-scale project. Consider how naming conventions, modularity, and testing impact maintainability and collaboration."
        elif domain == "Data Science":
            return "For instance, when building a machine learning model, you need to consider data preprocessing, feature selection, model choice, and evaluation metrics appropriate for your specific problem."
        else:
            return "For example, in a marketing campaign, you would analyze your target audience, set measurable goals, select appropriate channels, create compelling content, and track your results."
    
    elif "difficult" in user_input_lower or "challenge" in user_input_lower or "hard" in user_input_lower:
        return f"The challenging part of this topic is balancing theoretical knowledge with practical implementation. In {domain}, you often need to adapt best practices to specific contexts while considering constraints like time, resources, and team expertise."
    
    elif "best practice" in user_input_lower or "tip" in user_input_lower or "advice" in user_input_lower:
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
        
        if domain == "Software Development":
            return "Some best practices include: writing self-documenting code, following SOLID principles, implementing continuous integration, conducting code reviews, and writing comprehensive tests."
        elif domain == "Data Science":
            return "Key best practices include: thoroughly understanding your data before modeling, validating properly to avoid leakage, starting with simple models, and documenting your assumptions and process."
        else:
            return "Important best practices include: defining clear objectives, understanding your audience, testing different approaches, measuring results, and continuously improving based on feedback."
    
    else:
        # Default response
        return f"That's an interesting aspect of the question. To answer well, consider both theoretical foundations and practical applications in {domain}. Industry experience suggests focusing on real-world implications and current best practices." 