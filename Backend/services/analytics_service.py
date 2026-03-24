from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models import Student, QuizResult, PerformanceHistory


class AnalyticsService:
    @staticmethod
    async def get_struggling_students(db: AsyncSession, threshold: float):
        stmt = (
            select(
                Student.id.label("student_id"),
                Student.name.label("student_name"),
                Student.email.label("email"),
                func.avg(QuizResult.score).label("average_score"),
                func.count(QuizResult.id).label("total_attempts"),
            )
            .join(QuizResult, QuizResult.student_id == Student.id)
            .group_by(Student.id, Student.name, Student.email)
            .having(func.avg(QuizResult.score) < threshold)
            .order_by(func.avg(QuizResult.score).asc())
        )

        result = await db.execute(stmt)
        rows = result.all()
        return [
            {
                "student_id": row.student_id,
                "student_name": row.student_name,
                "email": row.email,
                "average_score": round(float(row.average_score or 0), 2),
                "total_attempts": row.total_attempts,
            }
            for row in rows
        ]

    @staticmethod
    async def get_hardest_topics(db: AsyncSession):
        stmt = (
            select(
                QuizResult.topic.label("topic"),
                func.avg(QuizResult.score).label("average_score"),
                func.count(QuizResult.id).label("total_attempts"),
            )
            .group_by(QuizResult.topic)
            .order_by(func.avg(QuizResult.score).asc())
        )

        result = await db.execute(stmt)
        rows = result.all()
        return [
            {
                "topic": row.topic,
                "average_score": round(float(row.average_score or 0), 2),
                "total_attempts": row.total_attempts,
            }
            for row in rows
        ]

    @staticmethod
    async def get_student_report(db: AsyncSession, student_id: int):
        stmt = (
            select(
                PerformanceHistory.topic,
                PerformanceHistory.average_score,
                PerformanceHistory.average_time_taken,
                PerformanceHistory.total_questions,
                PerformanceHistory.correct_answers,
            )
            .where(PerformanceHistory.student_id == student_id)
            .order_by(PerformanceHistory.topic.asc())
        )
        result = await db.execute(stmt)
        rows = result.all()
        return [
            {
                "topic": row.topic,
                "average_score": round(float(row.average_score or 0), 2),
                "average_time_taken": round(float(row.average_time_taken or 0), 2),
                "total_questions": row.total_questions,
                "correct_answers": row.correct_answers,
            }
            for row in rows
        ]
