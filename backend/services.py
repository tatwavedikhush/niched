import asyncio
from models import ResearchJob, ResearchAnalysis
from database import SessionLocal
from pytrends.request import TrendReq
import feedparser
import os
from urllib.parse import quote_plus

# from google import genai
# from google.genai import types
import ollama

# client = genai.Client()


# def analyze_research(research):
#     prompt = f"""
# You are a digital product market researcher.

# Analyze the following research data and identify promising digital product opportunities.

# Research data:
# {research}

# Focus on:
# - real pain points
# - target audiences
# - recurring problems
# - product opportunities
# - realistic demand
# - assign a demand score from 0 to 100
# - reasonable pricing

# Return your analysis using the provided JSON schema.
# """

#     response = client.models.generate_content(
#         model="gemini-3.7-flash",
#         contents=prompt,
#         config=types.GenerateContentConfig(
#             response_mime_type="application/json",
#             response_schema=ResearchAnalysis,
#         ),
#     )

#     return ResearchAnalysis.model_validate_json(response.text)


def analyze_research(research):
    prompt = f"""
    You are a digital product market researcher.

    Analyze the following research data and identify promising digital product opportunities.

    Research data:
    {research}

    Focus on:
    - real pain points
    - target audiences
    - recurring problems
    - product opportunities
    - realistic demand
    - reasonable pricing
    - assign a demand score from 0 to 100

    Return ONLY valid JSON matching this structure:

    {{
      "pain_points": ["string"],
      "opportunities": [
        {{
          "title": "string",
          "target_audience": "string",
          "problem": "string",
          "solution": "string",
          "demand_score": 0,
          "suggested_price": "string",
          "reasoning": "string"
        }}
      ]
    }}
    """
    ollama_client = ollama.Client(
        host=os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
    )

    response = ollama_client.chat(
        model="llama3.1:8b",
        messages=[{"role": "user", "content": prompt}],
        format=ResearchAnalysis.model_json_schema(),
    )

    content = response["message"]["content"]

    return ResearchAnalysis.model_validate_json(content)


async def research_seed(seed: str):
    reddit, trends = await asyncio.gather(fetch_reddit(seed), fetch_trends(seed))

    return {"reddit": reddit, "trends": trends}


async def run_research(job_id, seed):
    try:
        research = await research_seed(seed)

        analysis = await asyncio.to_thread(analyze_research, research)

        result = {**research, "analysis": analysis.model_dump()}

        db = SessionLocal()

        try:
            job = db.query(ResearchJob).filter(ResearchJob.id == job_id).first()

            if not job:
                raise ValueError(f"Research job {job_id} not found")

            job.status = "completed"
            job.result = result

            db.commit()

        finally:
            db.close()

    except Exception as e:
        db = SessionLocal()

        try:
            job = db.query(ResearchJob).filter(ResearchJob.id == job_id).first()

            if job:
                job.status = "failed"
                job.error = str(e)
                db.commit()

        finally:
            db.close()

    except Exception as e:
        db = SessionLocal()
        job = db.query(ResearchJob).filter(ResearchJob.id == job_id).first()
        job.status = "failed"
        job.error = str(e)
        db.commit()
        db.close()


def get_trends(seed):
    pytrends = TrendReq()

    pytrends.build_payload([seed], timeframe="today 12-m", geo="")

    data = pytrends.interest_over_time()

    if data.empty:
        return []

    return {str(date.date()): int(value) for date, value in data[seed].tail(12).items()}


def get_reddit(seed):
    url = (
        f"https://www.reddit.com/search.rss?q={quote_plus(seed)}&sort=relevance&t=month"
    )

    feed = feedparser.parse(url)

    posts = []

    for entry in feed.entries[:10]:
        posts.append(
            {
                "title": entry.get("title", ""),
                "url": entry.get("link", ""),
                "published": entry.get("published", ""),
            }
        )

    return posts


async def fetch_reddit(seed):
    print(f"Researching Reddit for: {seed}")

    posts = await asyncio.to_thread(get_reddit, seed)

    return {"source": "reddit", "query": seed, "posts": posts}


async def fetch_trends(seed):
    print(f"Researching Google Trends for: {seed}")

    result = await asyncio.to_thread(get_trends, seed)

    return {"source": "google_trends", "query": seed, "data": result}


async def fetch_gumroad(seed):
    print("Gumroad started")
    await asyncio.sleep(4)
    return "Gumroad research completed"
