from services import analyze_research

research = {
    "reddit": {
        "source": "reddit",
        "query": "Indian Gaming Industry",
        "posts": [
            {
                "title": "I am tired of the Indian Gaming Scene and it's community",
                "url": "https://www.reddit.com/example1",
                "published": "2026-08-11"
            },
            {
                "title": "Where do Indian iGaming professionals actually network?",
                "url": "https://www.reddit.com/example2",
                "published": "2026-08-24"
            },
            {
                "title": "India's gaming industry finally crossed $1 billion. The bigger story is how little players spend",
                "url": "https://www.reddit.com/example3",
                "published": "2026-08-17"
            }
        ]
    },
    "trends": {
        "source": "google_trends",
        "query": "Indian Gaming Industry",
        "data": {
            "2026-08-02": 12,
            "2026-08-09": 19,
            "2026-08-16": 29,
            "2026-08-23": 2,
            "2026-08-30": 6,
            "2026-09-06": 6
        }
    }
}

analysis = analyze_research(research)

print(analysis.model_dump_json(indent=2))