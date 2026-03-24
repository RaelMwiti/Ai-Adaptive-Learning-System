import json
from groq import Groq
from config import settings

client = Groq(api_key=settings.groq_api_key)


class GroqService:
    @staticmethod
    def build_feedback_prompt(
        topic: str,
        question: str,
        student_answer: str,
        correct_answer: str,
        is_correct: bool,
    ) -> str:
        if is_correct:
            return f"""
You are a supportive AI tutor.

The student answered a question correctly.

Topic: {topic}
Question: {question}
Student Answer: {student_answer}
Correct Answer: {correct_answer}

Write a concise response with:
1. A short congratulatory remark
2. A simple reason why the answer is correct
3. One extension tip or challenge question

Keep the tone encouraging and beginner-friendly.
""".strip()

        return f"""
You are a patient AI tutor.

The student answered a question incorrectly.

Topic: {topic}
Question: {question}
Student Answer: {student_answer}
Correct Answer: {correct_answer}

Write a helpful teaching response with:
1. A gentle correction
2. A clear explanation of the correct answer
3. One simple example
4. One follow-up practice question

Keep it beginner-friendly and do not shame the student.
""".strip()

    @staticmethod
    def get_feedback(
        topic: str,
        question: str,
        student_answer: str,
        correct_answer: str,
        is_correct: bool,
    ) -> str:
        prompt = GroqService.build_feedback_prompt(
            topic=topic,
            question=question,
            student_answer=student_answer,
            correct_answer=correct_answer,
            is_correct=is_correct,
        )

        try:
            response = client.chat.completions.create(
                model=settings.groq_model,
                messages=[
                    {"role": "system",
                        "content": "You are an expert adaptive learning tutor."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
                max_tokens=400,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            if is_correct:
                return (
                    "Great job. Your answer is correct. "
                    "You understood the main concept well. "
                    "Try explaining the idea in your own words as a next challenge."
                )
            return (
                f"That answer is not correct. The correct answer is: {correct_answer}. "
                "Review the concept step by step, then try a similar question again."
            )

    @staticmethod
    def generate_question(topic: str, difficulty: str) -> dict:
        prompt = f"""
Generate exactly one quiz item.

Topic: {topic}
Difficulty: {difficulty}

Return valid JSON only using this structure:
{{
  "question": "...",
  "answer": "...",
  "explanation": "..."
}}

The question must be appropriate for a learner and have one clear answer.
""".strip()

        try:
            response = client.chat.completions.create(
                model=settings.groq_model,
                messages=[
                    {"role": "system",
                        "content": "You generate educational quiz items in strict JSON."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.5,
                max_tokens=300,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content.strip()
            parsed = json.loads(content)
            return {
                "question": parsed.get("question", ""),
                "answer": parsed.get("answer", ""),
                "explanation": parsed.get("explanation", ""),
            }
        except Exception:
            return {
                "question": f"What is one important concept in {topic}?",
                "answer": f"A correct response should name and explain one important concept in {topic}.",
                "explanation": "This is a fallback question generated because the AI service was unavailable.",
            }
