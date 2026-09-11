from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Text, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ResearchRequest(BaseModel):
    seed: str


class ProductOpportunity(BaseModel):
    title: str
    target_audience: str
    problem: str
    solution: str
    demand_score: int = Field(ge=0, le=100)
    suggested_price: str
    reasoning: str


class ResearchAnalysis(BaseModel):
    pain_points: list[str]
    opportunities: list[ProductOpportunity]


class ResearchJob(Base):
    __tablename__ = "research_jobs"

    id = Column(String, primary_key=True)
    seed = Column(String, nullable=False)
    status = Column(String, nullable=False, default="running")
    result = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
