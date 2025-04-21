"""Module for managing references and learning resources."""

# Comprehensive references database
REFERENCES = {
    "Software Development": {
        "books": [
            {"title": "Clean Code", "author": "Robert C. Martin", "year": 2008},
            {"title": "Design Patterns", "author": "Gang of Four", "year": 1994},
            {"title": "Refactoring", "author": "Martin Fowler", "year": 2018},
            {"title": "The Pragmatic Programmer", "author": "Andrew Hunt & David Thomas", "year": 2019}
        ],
        "papers": [
            {"title": "On the Criteria To Be Used in Decomposing Systems into Modules", "author": "D.L. Parnas", "year": 1972},
            {"title": "No Silver Bullet – Essence and Accident in Software Engineering", "author": "Frederick P. Brooks", "year": 1987}
        ],
        "online_resources": [
            {"title": "Martin Fowler's Blog", "url": "https://martinfowler.com"},
            {"title": "Clean Code Handbook", "url": "https://github.com/ryanmcdermott/clean-code-javascript"},
            {"title": "SOLID Principles", "url": "https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design"},
            {"title": "Design Patterns", "url": "https://refactoring.guru/design-patterns"}
        ]
    },
    "Data Science": {
        "books": [
            {"title": "Deep Learning", "author": "Ian Goodfellow et al.", "year": 2016},
            {"title": "The Hundred-Page Machine Learning Book", "author": "Andriy Burkov", "year": 2019},
            {"title": "Python for Data Analysis", "author": "Wes McKinney", "year": 2022},
            {"title": "Introduction to Statistical Learning", "author": "James, Witten, Hastie, Tibshirani", "year": 2021}
        ],
        "papers": [
            {"title": "Attention Is All You Need", "author": "Vaswani et al.", "year": 2017},
            {"title": "Deep Residual Learning for Image Recognition", "author": "He et al.", "year": 2015}
        ],
        "online_resources": [
            {"title": "Papers With Code", "url": "https://paperswithcode.com"},
            {"title": "Distill.pub", "url": "https://distill.pub"},
            {"title": "Towards Data Science", "url": "https://towardsdatascience.com"},
            {"title": "Google AI Blog", "url": "https://ai.googleblog.com"}
        ]
    },
    "Marketing": {
        "books": [
            {"title": "Marketing Management", "author": "Philip Kotler", "year": 2011},
            {"title": "Digital Marketing Strategy", "author": "Simon Kingsnorth", "year": 2019},
            {"title": "Contagious: How to Build Word of Mouth in the Digital Age", "author": "Jonah Berger", "year": 2013}
        ],
        "papers": [
            {"title": "Digital Marketing: A Framework, Review and Research Agenda", "author": "P.K. Kannan", "year": 2017},
            {"title": "Social Media Marketing: A Literature Review and Future Research Directions", "author": "Tuten & Solomon", "year": 2018}
        ],
        "online_resources": [
            {"title": "HubSpot Academy", "url": "https://academy.hubspot.com"},
            {"title": "Google Digital Garage", "url": "https://learndigital.withgoogle.com"},
            {"title": "Moz Blog", "url": "https://moz.com/blog"},
            {"title": "Content Marketing Institute", "url": "https://contentmarketinginstitute.com"}
        ]
    }
}

def get_domain_references(domain: str) -> dict:
    """Get all references for a specific domain."""
    return REFERENCES.get(domain, {})

def get_topic_references(domain: str, topic: str = None) -> dict:
    """Get references filtered by domain and topic."""
    domain_refs = REFERENCES.get(domain, {})
    if not topic:
        return domain_refs
    
    # Convert topic to lowercase for case-insensitive matching
    topic_lower = topic.lower()
    
    # Split topic into individual words for better matching
    topic_words = topic_lower.split()
    
    # Filter references by topic relevance
    filtered_refs = {}
    for category, refs in domain_refs.items():
        filtered_items = []
        for ref in refs:
            # Consider a match if any topic word is in the title
            ref_title_lower = ref['title'].lower()
            if any(word in ref_title_lower for word in topic_words if len(word) > 3):
                filtered_items.append(ref)
        
        # If no matches found, include at least some default references
        if not filtered_items and len(refs) > 0:
            # Just take the first item as a default
            filtered_items.append(refs[0])
        
        filtered_refs[category] = filtered_items
    
    return filtered_refs

def format_reference_for_display(ref: dict) -> str:
    """Format a reference entry for display."""
    if 'url' in ref:
        return f"- [{ref['title']}]({ref['url']})"
    elif 'author' in ref and 'year' in ref:
        return f"- {ref['title']} by {ref['author']} ({ref['year']})"
    else:
        return f"- {ref['title']}"

def get_improvement_suggestions(domain: str, topic: str = None, score: float = None) -> list:
    """Get personalized improvement suggestions based on domain, topic, and score."""
    refs = get_topic_references(domain, topic)
    suggestions = []
    
    # Add score-based suggestions
    if score is not None:
        if score < 5:
            suggestions.append("Consider starting with foundational resources:")
            if refs.get('books'):
                suggestions.append(f"📚 Recommended Book: {refs['books'][0]['title']}")
            if refs.get('online_resources'):
                suggestions.append(f"🌐 Start here: {refs['online_resources'][0]['title']}")
        elif score < 7:
            suggestions.append("To improve your knowledge, explore these intermediate resources:")
            if refs.get('papers'):
                suggestions.append(f"📄 Related Paper: {refs['papers'][0]['title']}")
            if refs.get('online_resources'):
                suggestions.append(f"🌐 Practice here: {refs['online_resources'][-1]['title']}")
        else:
            suggestions.append("To master the topic, dive into these advanced materials:")
            if refs.get('papers'):
                suggestions.append(f"📄 Advanced Reading: {refs['papers'][-1]['title']}")
    
    return suggestions 