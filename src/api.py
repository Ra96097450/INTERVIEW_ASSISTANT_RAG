from fastapi import FastAPI
from pydantic import BaseModel

from .rag import generate_answer


app = FastAPI(
    title="InterviewIQ RAG API",
    description="AI Engineer knowledge assistant using RAG",
    version="1.0"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "InterviewIQ RAG API is running"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    answer, results = generate_answer(
        request.question
    )

    sources = list(
        dict.fromkeys(
            metadata["source"]
            for metadata in results["metadatas"][0]
        )
    )

    return {
        "question": request.question,
        "answer": answer,
        "sources": sources
    }