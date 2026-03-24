from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import Student
from schemas import StrugglingStudentItem, HardestTopicItem, StudentTopicReportItem
from services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/struggling-students", response_model=list[StrugglingStudentItem])
async def struggling_students(
    threshold: float = Query(0.6, ge=0, le=1),
    db: AsyncSession = Depends(get_db),
):
    return await AnalyticsService.get_struggling_students(db, threshold)


@router.get("/hardest-topics", response_model=list[HardestTopicItem])
async def hardest_topics(db: AsyncSession = Depends(get_db)):
    return await AnalyticsService.get_hardest_topics(db)

@router.get("/student-report/{student_id}", response_model=list[StudentTopicReportItem])
async def student_report(student_id: int, db: AsyncSession = Depends(get_db)):
    student_result = await db.execute(select(Student).where(Student.id == student_id))
    student = student_result.scalar_one_or_none()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    return await AnalyticsService.get_student_report(db, student_id)