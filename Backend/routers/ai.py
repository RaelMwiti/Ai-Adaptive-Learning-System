from fastapi import APIRouter
from schemas import QuestionGenerationRequest, QuestionGenerationResponse
from services.groq_service import GroqService

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/generate-question", response_model=QuestionGenerationResponse)
async def generate_question(payload: QuestionGenerationRequest):
    generated = GroqService.generate_question(
        payload.topic, payload.difficulty)
    return {
        "topic": payload.topic,
        "difficulty": payload.difficulty,
        "question": generated["question"],
        "answer": generated["answer"],
        "explanation": generated["explanation"],
    }
