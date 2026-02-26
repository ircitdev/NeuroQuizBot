"""Data models for the bot"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum


class QuizProfile(Enum):
    """Quiz result profiles"""
    NEWBIE = "Нейроновичок"
    PRACTITIONER = "Нейропрактик"
    MASTER = "Нейромастер"


class QuizTag(Enum):
    """Quiz answer tags"""
    STRESS = "stress"
    FOCUS = "focus"
    MEMORY = "memory"
    DECISIONS = "decisions"
    RECOVERY = "recovery"


@dataclass
class QuizOption:
    """Quiz question option"""
    label: str
    score: int
    tag: str


@dataclass
class QuizQuestion:
    """Quiz question"""
    id: int
    text: str
    options: List[QuizOption]


@dataclass
class QuizResult:
    """Quiz result data"""
    user_id: int
    answers: Dict[str, Any]
    total_score: int
    profile: str
    main_tag: str

    @property
    def profile_emoji(self) -> str:
        """Get emoji for profile"""
        if self.profile == QuizProfile.NEWBIE.value:
            return "🌱"
        elif self.profile == QuizProfile.PRACTITIONER.value:
            return "⚡"
        elif self.profile == QuizProfile.MASTER.value:
            return "🏆"
        return "🧠"

    @property
    def profile_description(self) -> str:
        """Get description for profile"""
        if self.profile == QuizProfile.NEWBIE.value:
            return "Вашему мозгу срочно нужна перезагрузка. Мероприятие даст вам конкретные инструменты."
        elif self.profile == QuizProfile.PRACTITIONER.value:
            return "У вас хорошая база, но есть точки роста. Вы получите продвинутые техники."
        elif self.profile == QuizProfile.MASTER.value:
            return "Впечатляющий результат! Мероприятие поможет выйти на новый уровень."
        return ""


@dataclass
class UserData:
    """User data for lead card"""
    tg_user_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    utm_source: Optional[str]
