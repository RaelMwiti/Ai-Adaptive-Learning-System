from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StudentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    created_at: datetime

class QuizSubmission(BaseModel):
    student_id: int
    topic: str = Field(..., min_length=2, max_length=100)
    question: str = Field(..., min_length=5)
    student_answer: str = Field(..., min_length=1)
    correct_answer: str = Field(..., min_length=1)
    time_taken_seconds: float = Field(..., gt=0)


class QuizSubmissionResponse(BaseModel):
    message: str
    student_id: int
    topic: str
    is_correct: bool
    score: float
    ai_feedback: str
    submitted_at: datetime

class TopicProgress(BaseModel):
    topic: str
    total_questions: int
    correct_answers: int
    average_score: float
    average_time_taken: float


class StudentProgressResponse(BaseModel):
    student_id: int
    student_name: str
    progress_by_topic: list[TopicProgress]


class StrugglingStudentItem(BaseModel):
    student_id: int
    student_name: str
    email: EmailStr
    average_score: float
    total_attempts: int

class HardestTopicItem(BaseModel):
    topic: str
    average_score: float
    total_attempts: int


class StudentTopicReportItem(BaseModel):
    topic: str
    average_score: float
    average_time_taken: float
    total_questions: int
    correct_answers: int


class QuestionGenerationRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=100)
    difficulty: str = Field(..., pattern="^(easy|medium|hard)$")

class QuestionGenerationResponse(BaseModel):
    topic: str
    difficulty: str
    question: str
    answer: str
    explanation: str


    

