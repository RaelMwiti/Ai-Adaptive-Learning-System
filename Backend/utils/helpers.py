import re


def normalize_text(text: str) -> str:
    cleaned = re.sub(r"\s+", " ", text.strip().lower())
    return cleaned


def check_answer(student_answer: str, correct_answer: str) -> bool:
    return normalize_text(student_answer) == normalize_text(correct_answer)


def score_answer(is_correct: bool) -> float:
    return 1.0 if is_correct else 0.0