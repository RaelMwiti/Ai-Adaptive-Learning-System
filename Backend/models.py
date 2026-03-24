from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, Text, Boolean, Float, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)

    quiz_results: Mapped[list["QuizResult"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )

    performance_history: Mapped[list["PerformanceHistory"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )


class QuizResult(Base):
    __tablename__ = "quiz_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey(
        "students.id", ondelete="CASCADE"), nullable=False)
    topic: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    student_answer: Mapped[str] = mapped_column(Text, nullable=False)
    correct_answer: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    score: Mapped[float] = mapped_column(Float, default=0.0)
    time_taken_seconds: Mapped[float] = mapped_column(Float, nullable=False)
    ai_feedback: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)

    student: Mapped["Student"] = relationship(back_populates="quiz_results")


class PerformanceHistory(Base):
    __tablename__ = "performance_history"
    __table_args__ = (
        UniqueConstraint("student_id", "topic",
                         name="uq_performance_student_topic"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey(
        "students.id", ondelete="CASCADE"), nullable=False)
    topic: Mapped[str] = mapped_column(String(100), nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, default=0)
    correct_answers: Mapped[int] = mapped_column(Integer, default=0)
    average_score: Mapped[float] = mapped_column(Float, default=0.0)
    average_time_taken: Mapped[float] = mapped_column(Float, default=0.0)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)

    student: Mapped["Student"] = relationship(
        back_populates="performance_history")
