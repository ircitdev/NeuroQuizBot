"""Quiz questions and data"""
from bot.models import QuizQuestion, QuizOption

# Quiz questions
QUIZ_QUESTIONS = [
    QuizQuestion(
        id=1,
        text="Как часто вы чувствуете умственную усталость к середине рабочего дня?",
        options=[
            QuizOption(label="Почти каждый день", score=1, tag="stress"),
            QuizOption(label="2–3 раза в неделю", score=2, tag="stress"),
            QuizOption(label="Редко", score=3, tag="focus"),
            QuizOption(label="Никогда", score=4, tag="focus"),
        ]
    ),
    QuizQuestion(
        id=2,
        text="Как вы оцениваете качество своих решений в стрессовых ситуациях?",
        options=[
            QuizOption(label="Часто ошибаюсь", score=1, tag="decisions"),
            QuizOption(label="Иногда сомневаюсь", score=2, tag="decisions"),
            QuizOption(label="Обычно принимаю верные", score=3, tag="decisions"),
            QuizOption(label="Всегда уверен в решениях", score=4, tag="decisions"),
        ]
    ),
    QuizQuestion(
        id=3,
        text="Бывает ли, что вы забываете важную информацию в течение дня?",
        options=[
            QuizOption(label="Постоянно", score=1, tag="memory"),
            QuizOption(label="Иногда", score=2, tag="memory"),
            QuizOption(label="Редко", score=3, tag="memory"),
            QuizOption(label="У меня отличная память", score=4, tag="memory"),
        ]
    ),
    QuizQuestion(
        id=4,
        text="Сколько минут вы можете работать с полной концентрацией без отвлечений?",
        options=[
            QuizOption(label="Менее 15 минут", score=1, tag="focus"),
            QuizOption(label="15–30 минут", score=2, tag="focus"),
            QuizOption(label="30–60 минут", score=3, tag="focus"),
            QuizOption(label="Более часа", score=4, tag="focus"),
        ]
    ),
    QuizQuestion(
        id=5,
        text="Чувствуете ли вы себя отдохнувшим после сна?",
        options=[
            QuizOption(label="Почти никогда", score=1, tag="recovery"),
            QuizOption(label="Иногда", score=2, tag="recovery"),
            QuizOption(label="Обычно да", score=3, tag="recovery"),
            QuizOption(label="Всегда", score=4, tag="recovery"),
        ]
    ),
    QuizQuestion(
        id=6,
        text="Как вы справляетесь с несколькими задачами одновременно?",
        options=[
            QuizOption(label="Теряюсь и путаюсь", score=1, tag="stress"),
            QuizOption(label="С трудом переключаюсь", score=2, tag="focus"),
            QuizOption(label="Справляюсь нормально", score=3, tag="focus"),
            QuizOption(label="Легко жонглирую задачами", score=4, tag="focus"),
        ]
    ),
    QuizQuestion(
        id=7,
        text="Что бы вы хотели улучшить в первую очередь?",
        options=[
            QuizOption(label="Стрессоустойчивость", score=0, tag="stress"),
            QuizOption(label="Память и обучаемость", score=0, tag="memory"),
            QuizOption(label="Скорость принятия решений", score=0, tag="decisions"),
            QuizOption(label="Концентрацию и энергию", score=0, tag="focus"),
        ]
    ),
]


def get_question(question_id: int) -> QuizQuestion:
    """Get question by ID"""
    for q in QUIZ_QUESTIONS:
        if q.id == question_id:
            return q
    raise ValueError(f"Question {question_id} not found")


def get_total_questions() -> int:
    """Get total number of questions"""
    return len(QUIZ_QUESTIONS)


TAG_LABELS = {
    "stress": "Стрессоустойчивость",
    "focus": "Концентрация и продуктивность",
    "memory": "Память и обучаемость",
    "decisions": "Принятие решений",
    "recovery": "Восстановление и энергия",
}


TAG_TECHNIQUES = {
    "stress": "Техника «Стресс-рефрейм» — превращение стресса в ресурс",
    "focus": "Техника «Фокус-блок» — глубокая концентрация 25/5",
    "memory": "Техника «Нейрозапись» — усиление памяти через структуризацию",
    "decisions": "Техника «Дерево решений» — нейрофизиология принятия решений",
    "recovery": "Техника «Нейростарт» — утренняя активация мозга",
}


TAG_IMAGES = {
    "stress": "https://storage.googleapis.com/uspeshnyy-projects/smit/smit34.ru/priority/stress.jpg",
    "focus": "https://storage.googleapis.com/uspeshnyy-projects/smit/smit34.ru/priority/focus.jpg",
    "memory": "https://storage.googleapis.com/uspeshnyy-projects/smit/smit34.ru/priority/memory.jpg",
    "decisions": "https://storage.googleapis.com/uspeshnyy-projects/smit/smit34.ru/priority/decisions.jpg",
    "recovery": "https://storage.googleapis.com/uspeshnyy-projects/smit/smit34.ru/priority/recovery.jpg",
}
