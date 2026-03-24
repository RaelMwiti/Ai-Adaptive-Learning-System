from fastapi import FastAPI
from config import settings
from routers.students import router as students_router
from routers.quiz import router as quiz_router
from routers.analytics import router as analytics_router
from routers.ai import router as ai_router

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="AI-powered adaptive learning backend using FastAPI, Groq, and PostgreSQL.",
)


@app.get("/")
async def root():
    return {
        "message": "Adaptive Learning System API is running.",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(students_router)
app.include_router(quiz_router)
app.include_router(analytics_router)
app.include_router(ai_router)
