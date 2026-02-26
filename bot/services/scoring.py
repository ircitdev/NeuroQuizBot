"""Quiz scoring logic"""
from typing import Dict, Any, List
from collections import Counter
from bot.models import QuizProfile, QuizResult


def calculate_result(user_id: int, answers: Dict[str, Any]) -> QuizResult:
    """
    Calculate quiz result from answers

    Args:
        user_id: Telegram user ID
        answers: Dict with answers in format {
            'q1': {'label': '...', 'score': 1, 'tag': 'stress'},
            'q2': {...}, ...
        }

    Returns:
        QuizResult object
    """
    # Calculate total score (questions 1-6, question 7 has score=0)
    total_score = 0
    tags = []

    for q_num in range(1, 8):  # 7 questions
        q_key = f'q{q_num}'
        if q_key in answers:
            total_score += answers[q_key].get('score', 0)
            tags.append(answers[q_key].get('tag'))

    # Determine profile based on total score
    if total_score <= 12:
        profile = QuizProfile.NEWBIE.value
    elif total_score <= 18:
        profile = QuizProfile.PRACTITIONER.value
    else:
        profile = QuizProfile.MASTER.value

    # Determine main tag (most frequent)
    tag_counter = Counter(tags)
    main_tag = tag_counter.most_common(1)[0][0] if tag_counter else "focus"

    return QuizResult(
        user_id=user_id,
        answers=answers,
        total_score=total_score,
        profile=profile,
        main_tag=main_tag
    )


def get_progress_bar(current: int, total: int, length: int = 14) -> str:
    """Generate progress bar string"""
    filled = int((current / total) * length)
    bar = "▓" * filled + "░" * (length - filled)
    return f"{bar}  {current}/{total}"
