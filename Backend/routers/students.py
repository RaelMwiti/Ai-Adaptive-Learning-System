from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Student
from schemas import StudentCreate, StudentResponse

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(payload: StudentCreate, db: AsyncSession = Depends(get_db)):
    existing_stmt = select(Student).where(Student.email == payload.email)
    existing_result = await db.execute(existing_stmt)
    existing_student = existing_result.scalar_one_or_none()

    if existing_student:
        raise HTTPException(
            status_code=400, detail="A student with this email already exists.")

    student = Student(name=payload.name, email=payload.email)
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return student


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    return student
