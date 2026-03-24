from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import Student, QuizResult, PerformanceHistory
from schemas import QuizSubmission, QuizSubmissionResponse, StudentProgressResponse, TopicProgress
from services.groq_service import GroqService
from utils.helpers import check_answer, score_answer

router = APIRouter(prefix="/quiz", tags=["Quiz"])


@router.post("/submit-answer", response_model=QuizSubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_answer(payload: QuizSubmission, db: AsyncSession = Depends(get_db)):
    student_result = await db.execute(select(Student).where(Student.id == payload.student_id))
    student = student_result.scalar_one_or_none()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    is_correct = check_answer(payload.student_answer, payload.correct_answer)
    score = score_answer(is_correct)

    ai_feedback = GroqService.get_feedback(
        topic=payload.topic,
        question=payload.question,
        student_answer=payload.student_answer,
        correct_answer=payload.correct_answer,
        is_correct=is_correct,
    )

    quiz_result = QuizResult(
        student_id=payload.student_id,
        topic=payload.topic,
        question=payload.question,
        student_answer=payload.student_answer,
        correct_answer=payload.correct_answer,
        is_correct=is_correct,
        score=score,
        time_taken_seconds=payload.time_taken_seconds,
        ai_feedback=ai_feedback,
    )
    db.add(quiz_result)
    await db.flush()

    perf_stmt = select(PerformanceHistory).where(
        PerformanceHistory.student_id == payload.student_id,
        PerformanceHistory.topic == payload.topic,
    )
    perf_result = await db.execute(perf_stmt)
    perf = perf_result.scalar_one_or_none()

    if perf is None:
        perf = PerformanceHistory(
            student_id=payload.student_id,
            topic=payload.topic,
            total_questions=1,
            correct_answers=1 if is_correct else 0,
            average_score=score,
            average_time_taken=payload.time_taken_seconds,
            last_updated=datetime.utcnow(),
        )
        db.add(perf)
    else:
        new_total = perf.total_questions + 1
        new_correct = perf.correct_answers + (1 if is_correct else 0)
        new_avg_score = ((perf.average_score * perf.total_questions) + score) / new_total
        new_avg_time = ((perf.average_time_taken * perf.total_questions) + payload.time_taken_seconds) / new_total
        
        perf.total_questions = new_total
        perf.correct_answers = new_correct
        perf.average_score = new_avg_score
        perf.average_time_taken = new_avg_time
        perf.last_updated = datetime.utcnow()

    await db.commit()
    await db.refresh(quiz_result)

    return {
        "message": "Answer submitted successfully.",
        "student_id": payload.student_id,
        "topic": payload.topic,
        "is_correct": is_correct,
        "score": score,
        "ai_feedback": ai_feedback,
        "submitted_at": quiz_result.created_at,
    }

@router.get("/student-progress/{student_id}", response_model=StudentProgressResponse)
async def get_student_progress(student_id: int, db: AsyncSession = Depends(get_db)):
    student_result = await db.execute(select(Student).where(Student.id == student_id))
    student = student_result.scalar_one_or_none()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    perf_stmt = select(PerformanceHistory).where(PerformanceHistory.student_id == student_id)
    perf_result = await db.execute(perf_stmt)
    records = perf_result.scalars().all()

    progress = [
        TopicProgress(
            topic=item.topic,
            total_questions=item.total_questions,
            correct_answers=item.correct_answers,
            average_score=round(float(item.average_score), 2),
            average_time_taken=round(float(item.average_time_taken), 2),
        )
        for item in records
    ]


    return {
        "student_id": student.id,
        "student_name": student.name,
        "progress_by_topic": progress,
    }


