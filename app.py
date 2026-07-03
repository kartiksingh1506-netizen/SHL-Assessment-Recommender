from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from recommender import search_assessments

app = FastAPI(
    title="SHL Assessment Recommender",
    version="1.0.0"
)


# -----------------------------
# Request Models
# -----------------------------

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# -----------------------------
# Health Endpoint
# -----------------------------

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# -----------------------------
# Chat Endpoint
# -----------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    # Get the latest user message
    latest_message = ""

    for message in reversed(request.messages):
        if message.role == "user":
            latest_message = message.content
            break

        # Clarify vague requests
    vague_queries = [
        "assessment",
        "test",
        "recommend",
        "hire",
        "hiring",
        "candidate",
        "job"
    ]

    if (
        len(latest_message.split()) < 4
        or latest_message.lower().strip() in vague_queries
    ):
        return {
            "reply": (
                "Could you tell me more about the role? "
                "Please include the job title, required skills, experience level, "
                "or paste the job description so I can recommend the most suitable SHL assessments."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # Semantic search
    results = search_assessments(latest_message, top_k=10)

    recommendations = []

    for assessment in results:

        recommendations.append({
            "name": assessment.get("name"),
            "url": assessment.get("link"),
            "test_type": ", ".join(assessment.get("keys", []))
        })

    return {
        "reply": f"I found {len(recommendations)} SHL assessments that match your requirements.",
        "recommendations": recommendations,
        "end_of_conversation": True
    }