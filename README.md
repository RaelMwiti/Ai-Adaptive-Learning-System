# 🚀 Adaptive Learning System (AI-Powered)

An **AI-driven adaptive learning backend** that personalizes student learning using real-time performance tracking, analytics, and intelligent feedback generation.

Built with **FastAPI, PostgreSQL, SQLAlchemy, and Groq AI**, this system dynamically adjusts learning experiences based on student responses — simulating real-world EdTech platforms.

---

## 🌟 Key Highlights

- 🎯 Personalized learning through AI-generated feedback
- 📊 Performance analytics by student and topic
- 🧠 Adaptive question generation using LLMs (Groq)
- ⚡ High-performance async backend (FastAPI + asyncpg)
- 🗄️ Scalable PostgreSQL database design
- 📚 Clean architecture (routers, services, models)

---

## 🧱 Architecture Overview

```
Client (Swagger / Frontend)
        ↓
FastAPI Backend (Routes)
        ↓
Service Layer (AI + Analytics)
        ↓
Database Layer (SQLAlchemy ORM)
        ↓
PostgreSQL (Aiven / Local)
```

---

## 🛠️ Tech Stack

| Layer        | Technology |
|-------------|-----------|
| Backend     | FastAPI |
| Server      | Uvicorn |
| Database    | PostgreSQL |
| ORM         | SQLAlchemy (Async) |
| AI Engine   | Groq API (LLMs) |
| Validation  | Pydantic |
| Environment | python-dotenv |

---

## 📂 Project Structure

```
Backend/
│
├── main.py
├── config.py
├── database.py
├── models.py
├── schemas.py
├── init_db.py
│
├── routers/
│   ├── students.py
│   ├── quiz.py
│   ├── analytics.py
│   └── ai.py
│
├── services/
│   ├── groq_service.py
│   └── analytics_service.py
│
├── utils/
│   └── helpers.py
│
├── requirements.txt
└── .env
```

---

## ⚙️ Setup Instructions

### 1. Clone / Create Project

```bash
git clone <your-repo-link>
cd Adaptive-Learning-System/Backend
```

---

### 2. Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\activate
```

---

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create `.env`:

```env
APP_NAME=Adaptive Learning System
DEBUG=True

DATABASE_URL=postgresql+asyncpg://username:password@host:port/database_name

GROQ_API_KEY=your_api_key
GROQ_MODEL=llama-3.1-8b-instant
```

---

### 5. Initialize Database

```powershell
python init_db.py
```

---

### 6. Run Application

```powershell
uvicorn main:app --reload
```

---

### 7. Access API Docs

👉 http://127.0.0.1:8000/docs

---

## 🔌 API Endpoints

### 👤 Students
- `POST /students` → Create student
- `GET /students/{id}` → Get student

### 📝 Quiz
- `POST /quiz/submit-answer` → Submit answer + AI feedback
- `GET /quiz/student-progress/{id}` → Track performance

### 📊 Analytics
- `GET /analytics/struggling-students`
- `GET /analytics/hardest-topics`
- `GET /analytics/student-report/{id}`

### 🤖 AI
- `POST /ai/generate-question`

```json
{
  "topic": "Python",
  "difficulty": "easy"
}
```

---

## 🔄 System Workflow

1. Student registers
2. Student answers quiz question
3. System evaluates correctness
4. AI generates feedback
5. Results stored in database
6. Performance metrics updated
7. Analytics generated for insights

---

## 📊 Example Use Case

- Identify weak topics per student
- Automatically generate practice questions
- Provide instant AI tutoring feedback
- Track learning progress over time


## 🚀 Future Improvements

- 🔐 Authentication (JWT)
- 🌐 Frontend (React / Next.js)
- 📈 Advanced AI grading (semantic similarity)
- 🐳 Dockerization
- ☁️ Cloud deployment (AWS / Render)
- 🎯 Recommendation engine

---

## 👩‍💻 Author

**Rael Mwiti**  
Data Analyst → AI & Data Science  

Passionate about building intelligent systems that combine **data, AI, and real-world impact**.

---

## 📌 Project Value

This project demonstrates:

- Backend engineering skills (FastAPI)
- Database design (PostgreSQL + ORM)
- AI integration (LLMs in production workflows)
- Real-world system design (adaptive learning)
- Clean and scalable architecture