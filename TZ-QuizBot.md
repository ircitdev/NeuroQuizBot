# ТЗ: Telegram Quiz-бот «Всемогущие Нейроны 3»

## 1. Общие сведения

| Параметр | Значение |
|---|---|
| Имя бота | `@NeuroEventsBot` |
| API Token | `8639010263:AAFKebwE7rIUj9kfmlok7jrm4eucfEoZCMQ` |
| Суперпуппа (CRM) | `https://t.me/c/3596687347` (chat_id: `-1003596687347`) |
| Стек | Python 3.11+ / aiogram 3.x |
| База данных | SQLite (или PostgreSQL для прода) |
| Деплой | VPS / Docker |

## 2. Цели бота

1. Квалифицировать лидов через 3-минутный квиз по нейрофизиологии
2. Выдавать персональный PDF-гайд «5 нейротехник для продуктивности»
3. Создавать **отдельный топик** в суперуппе для каждого лида
4. Обеспечить **двустороннюю переписку** менеджер ↔ пользователь через топик

---

## 3. Флоу пользователя

```
Пользователь нажимает «Получить в Telegram» на сайте
         ↓
   /start lead_site  (deep link с UTM)
         ↓
   Приветственное сообщение + кнопка «Начать квиз»
         ↓
   Вопрос 1 → Ответ (inline-кнопки)
   Вопрос 2 → Ответ
   ...
   Вопрос N → Ответ
         ↓
   Подсчёт результата → Персональная рекомендация
         ↓
   Отправка PDF-гайда + предложение записаться
         ↓
   В суперуппе создаётся топик с данными лида
         ↓
   Менеджер может писать в топик — сообщение уходит пользователю
   Пользователь отвечает — сообщение появляется в топике
```

---

## 4. Команды бота

| Команда | Описание |
|---|---|
| `/start` | Запуск бота, приветствие |
| `/start lead_site` | Запуск с лендинга (UTM-трекинг) |
| `/start lead_instagram` | Запуск из Instagram |
| `/quiz` | Запустить / перезапустить квиз |
| `/result` | Показать последний результат |
| `/help` | Справка |

---

## 5. Квиз: вопросы и логика

### 5.1 Структура вопроса

```json
{
  "id": 1,
  "text": "Как часто вы чувствуете умственную усталость к середине рабочего дня?",
  "options": [
    {"label": "Почти каждый день", "score": 1, "tag": "stress"},
    {"label": "2–3 раза в неделю", "score": 2, "tag": "stress"},
    {"label": "Редко", "score": 3, "tag": "focus"},
    {"label": "Никогда", "score": 4, "tag": "focus"}
  ]
}
```

### 5.2 Вопросы (7 штук)

**Вопрос 1** — Умственная усталость
> Как часто вы чувствуете умственную усталость к середине рабочего дня?
- Почти каждый день → 1 балл, тег: `stress`
- 2–3 раза в неделю → 2 балла, тег: `stress`
- Редко → 3 балла, тег: `focus`
- Никогда → 4 балла, тег: `focus`

**Вопрос 2** — Принятие решений
> Как вы оцениваете качество своих решений в стрессовых ситуациях?
- Часто ошибаюсь → 1, тег: `decisions`
- Иногда сомневаюсь → 2, тег: `decisions`
- Обычно принимаю верные → 3, тег: `decisions`
- Всегда уверен в решениях → 4, тег: `decisions`

**Вопрос 3** — Память
> Бывает ли, что вы забываете важную информацию в течение дня?
- Постоянно → 1, тег: `memory`
- Иногда → 2, тег: `memory`
- Редко → 3, тег: `memory`
- У меня отличная память → 4, тег: `memory`

**Вопрос 4** — Концентрация
> Сколько минут вы можете работать с полной концентрацией без отвлечений?
- Менее 15 минут → 1, тег: `focus`
- 15–30 минут → 2, тег: `focus`
- 30–60 минут → 3, тег: `focus`
- Более часа → 4, тег: `focus`

**Вопрос 5** — Сон и восстановление
> Чувствуете ли вы себя отдохнувшим после сна?
- Почти никогда → 1, тег: `recovery`
- Иногда → 2, тег: `recovery`
- Обычно да → 3, тег: `recovery`
- Всегда → 4, тег: `recovery`

**Вопрос 6** — Многозадачность
> Как вы справляетесь с несколькими задачами одновременно?
- Теряюсь и путаюсь → 1, тег: `stress`
- С трудом переключаюсь → 2, тег: `focus`
- Справляюсь нормально → 3, тег: `focus`
- Легко жонглирую задачами → 4, тег: `focus`

**Вопрос 7** — Интерес к развитию
> Что бы вы хотели улучшить в первую очередь?
- Стрессоустойчивость → тег: `stress`
- Память и обучаемость → тег: `memory`
- Скорость принятия решений → тег: `decisions`
- Концентрацию и энергию → тег: `focus`

### 5.3 Подсчёт результата

**Суммарный балл** (вопросы 1–6, от 6 до 24):

| Баллы | Профиль | Рекомендация |
|---|---|---|
| 6–12 | «Нейроновичок» | Вашему мозгу срочно нужна перезагрузка. Мероприятие даст вам конкретные инструменты. |
| 13–18 | «Нейропрактик» | У вас хорошая база, но есть точки роста. Вы получите продвинутые техники. |
| 19–24 | «Нейромастер» | Впечатляющий результат! Мероприятие поможет выйти на новый уровень. |

**Основной тег** (наиболее частый среди ответов) определяет, какой раздел PDF-гайда выделить как приоритетный.

---

## 6. Топики в суперуппе (CRM)

### 6.1 Создание топика

При завершении квиза бот вызывает `createForumTopic` в суперуппе:

```
POST /bot{TOKEN}/createForumTopic
{
  "chat_id": "-1003596687347",
  "name": "🧠 Имя Фамилия (@username)",
  "icon_custom_emoji_id": <опционально>
}
```

Ответ содержит `message_thread_id` — сохраняется в БД.

### 6.2 Первое сообщение в топике (карточка лида)

```
📋 НОВЫЙ ЛИД

👤 Имя: {first_name} {last_name}
📱 Username: @{username}
🆔 User ID: {user_id}
📊 Источник: {utm_source}

━━━ РЕЗУЛЬТАТЫ КВИЗА ━━━
📈 Балл: {total_score}/24
🏷 Профиль: {profile_name}
🎯 Приоритет: {main_tag}

━━━ ОТВЕТЫ ━━━
1. Умственная усталость → {answer_1}
2. Принятие решений → {answer_2}
3. Память → {answer_3}
4. Концентрация → {answer_4}
5. Сон → {answer_5}
6. Многозадачность → {answer_6}
7. Интерес → {answer_7}

📅 {datetime}
🔗 Чтобы ответить — просто напишите в этот топик
```

### 6.3 Двусторонняя переписка

#### Менеджер → Пользователь
- Менеджер пишет сообщение в топик лида
- Бот получает `message` с `message_thread_id`
- Бот определяет по `message_thread_id` → `user_id` (из БД)
- Бот пересылает/отправляет сообщение пользователю в личный чат
- Поддерживаемые типы: текст, фото, документы, голосовые

#### Пользователь → Менеджер
- Пользователь пишет боту в личные сообщения
- Бот определяет по `user_id` → `message_thread_id` (из БД)
- Бот пересылает сообщение в соответствующий топик суперуппы
- Поддерживаемые типы: текст, фото, документы, голосовые, видео

---

## 7. PDF-гайд

### 7.1 Генерация

Один базовый PDF «5 нейротехник для продуктивности» с персонализированной обложкой:
- Имя пользователя
- Его профиль (Нейроновичок / Нейропрактик / Нейромастер)
- Выделенная приоритетная техника на основе `main_tag`

### 7.2 Контент (заглушки — заполняет заказчик)

1. **Техника «Нейростарт»** — утренняя активация мозга (тег: `recovery`)
2. **Техника «Фокус-блок»** — глубокая концентрация 25/5 (тег: `focus`)
3. **Техника «Стресс-рефрейм»** — превращение стресса в ресурс (тег: `stress`)
4. **Техника «Нейрозапись»** — усиление памяти через структуризацию (тег: `memory`)
5. **Техника «Дерево решений»** — нейрофизиология принятия решений (тег: `decisions`)

---

## 8. База данных

### 8.1 Таблица `users`

| Поле | Тип | Описание |
|---|---|---|
| `id` | INTEGER PK | Внутренний ID |
| `tg_user_id` | BIGINT UNIQUE | Telegram user ID |
| `username` | TEXT | @username |
| `first_name` | TEXT | Имя |
| `last_name` | TEXT | Фамилия |
| `phone` | TEXT | Телефон (если поделится) |
| `utm_source` | TEXT | Источник (lead_site, lead_instagram и т.д.) |
| `thread_id` | INTEGER | ID топика в суперуппе |
| `created_at` | DATETIME | Дата первого /start |

### 8.2 Таблица `quiz_results`

| Поле | Тип | Описание |
|---|---|---|
| `id` | INTEGER PK | |
| `user_id` | BIGINT FK | → users.tg_user_id |
| `answers` | JSON | `{"q1": "option_label", "q1_score": 2, ...}` |
| `total_score` | INTEGER | Суммарный балл |
| `profile` | TEXT | Нейроновичок / Нейропрактик / Нейромастер |
| `main_tag` | TEXT | Приоритетный тег |
| `completed_at` | DATETIME | |

### 8.3 Таблица `messages`

| Поле | Тип | Описание |
|---|---|---|
| `id` | INTEGER PK | |
| `user_id` | BIGINT | Telegram user ID |
| `direction` | TEXT | `in` (от пользователя) / `out` (от менеджера) |
| `text` | TEXT | Текст сообщения |
| `tg_message_id` | INTEGER | ID сообщения в Telegram |
| `created_at` | DATETIME | |

---

## 9. Структура проекта

```
quiz-bot/
├── bot/
│   ├── __init__.py
│   ├── main.py              # Точка входа, запуск polling
│   ├── config.py             # Настройки (TOKEN, CHAT_ID и т.д.)
│   ├── db.py                 # Подключение и миграции БД
│   ├── models.py             # Pydantic-модели / dataclasses
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── start.py          # /start, deep links, приветствие
│   │   ├── quiz.py           # Логика квиза (FSM)
│   │   ├── result.py         # Подсчёт, отправка PDF, создание топика
│   │   ├── relay.py          # Пересылка сообщений (менеджер ↔ юзер)
│   │   └── help.py           # /help
│   ├── keyboards/
│   │   ├── __init__.py
│   │   ├── quiz_kb.py        # Inline-кнопки для вопросов квиза
│   │   └── main_kb.py        # Reply-клавиатуры
│   ├── services/
│   │   ├── __init__.py
│   │   ├── quiz_data.py      # Вопросы, варианты, баллы
│   │   ├── scoring.py        # Подсчёт результата
│   │   ├── pdf_generator.py  # Генерация персонального PDF
│   │   └── topic_manager.py  # Создание топиков, маппинг thread ↔ user
│   └── utils/
│       ├── __init__.py
│       └── formatting.py     # Форматирование сообщений
├── assets/
│   └── guide_template.pdf    # Шаблон PDF-гайда
├── .env                      # BOT_TOKEN, SUPERGROUP_ID
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## 10. Конфигурация (.env)

```env
BOT_TOKEN=8639010263:AAFKebwE7rIUj9kfmlok7jrm4eucfEoZCMQ
SUPERGROUP_CHAT_ID=-1003596687347
DATABASE_URL=sqlite:///data/bot.db
ADMIN_IDS=123456789,987654321
```

---

## 11. Ключевые технические моменты

### 11.1 FSM (Finite State Machine) для квиза

```python
class QuizStates(StatesGroup):
    waiting_start = State()    # Ожидание нажатия «Начать квиз»
    question_1 = State()       # Вопрос 1
    question_2 = State()       # Вопрос 2
    question_3 = State()       # ...
    question_4 = State()
    question_5 = State()
    question_6 = State()
    question_7 = State()
    completed = State()        # Квиз завершён
```

### 11.2 Relay-система (пересылка сообщений)

```python
# relay.py — псевдокод

@router.message(F.chat.id == SUPERGROUP_CHAT_ID)
async def manager_to_user(message: Message):
    """Менеджер написал в топик → переслать пользователю"""
    if message.from_user.is_bot:
        return  # Игнорируем сообщения от самого бота

    thread_id = message.message_thread_id
    user = await db.get_user_by_thread(thread_id)
    if not user:
        return

    await bot.copy_message(
        chat_id=user.tg_user_id,
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )

@router.message(F.chat.type == "private")
async def user_to_manager(message: Message, state: FSMContext):
    """Пользователь написал боту → переслать в топик"""
    current_state = await state.get_state()
    if current_state and current_state.startswith("QuizStates"):
        return  # Не пересылать во время квиза

    user = await db.get_user(message.from_user.id)
    if not user or not user.thread_id:
        return

    await bot.copy_message(
        chat_id=SUPERGROUP_CHAT_ID,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
        message_thread_id=user.thread_id
    )
```

### 11.3 Создание топика

```python
# topic_manager.py

async def create_lead_topic(bot: Bot, user_data: dict, quiz_result: dict) -> int:
    """Создаёт топик в суперуппе и возвращает thread_id"""

    name = user_data.get("first_name", "Аноним")
    username = user_data.get("username", "")
    topic_name = f"🧠 {name}"
    if username:
        topic_name += f" (@{username})"

    # Обрезаем до 128 символов (лимит Telegram)
    topic_name = topic_name[:128]

    result = await bot.create_forum_topic(
        chat_id=SUPERGROUP_CHAT_ID,
        name=topic_name
    )

    thread_id = result.message_thread_id

    # Отправляем карточку лида в топик
    card = format_lead_card(user_data, quiz_result)
    await bot.send_message(
        chat_id=SUPERGROUP_CHAT_ID,
        message_thread_id=thread_id,
        text=card,
        parse_mode="HTML"
    )

    return thread_id
```

---

## 12. Inline-кнопки квиза

Каждый вопрос — отдельное сообщение с inline-клавиатурой:

```
┌─────────────────────────────────────┐
│  ❓ Вопрос 2 из 7                   │
│                                     │
│  Как вы оцениваете качество своих   │
│  решений в стрессовых ситуациях?    │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Часто ошибаюсь               │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ Иногда сомневаюсь            │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ Обычно принимаю верные       │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ Всегда уверен в решениях     │  │
│  └───────────────────────────────┘  │
│                                     │
│  ▓▓▓▓▓▓░░░░░░░░  2/7              │
└─────────────────────────────────────┘
```

Callback data формат: `quiz:{question_id}:{option_index}`

---

## 13. Сообщения бота

### Приветствие (`/start`)

```
🧠 Добро пожаловать в «Всемогущие Нейроны»!

Пройдите 3-минутный квиз и узнайте, на сколько процентов
работает ваш мозг — и получите персональный гайд
«5 нейротехник для продуктивности».

📊 7 вопросов • ⏱ 3 минуты • 📄 PDF-гайд в подарок

[🚀 Начать квиз]
```

### Результат квиза

```
📊 Ваш результат: {score}/24

🏷 Профиль: {profile_emoji} {profile_name}

{profile_description}

🎯 Ваш приоритет: {main_tag_label}
{tag_recommendation}

━━━━━━━━━━━━━━━━━━━━━

📄 Ваш персональный гайд готов! Сейчас отправлю...

💡 Хотите узнать больше? 20 марта 2026 в Крокус-Экспо
пройдёт мероприятие «Всемогущие Нейроны 3» — живые
мастер-классы от нейрофизиологов.

[🎟 Забронировать место]  [🌐 Подробнее]
```

---

## 14. Аналитика

Бот собирает и отправляет по команде `/stats` (только для ADMIN_IDS):

- Всего пользователей
- Прошли квиз / не прошли
- Средний балл
- Распределение по профилям
- Источники трафика (UTM)
- Конверсия в заявку на мероприятие

---

## 15. Деплой

```yaml
# docker-compose.yml
version: "3.8"
services:
  quiz-bot:
    build: .
    restart: unless-stopped
    env_file: .env
    volumes:
      - ./data:/app/data
```

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "bot.main"]
```

---

## 16. Requirements

```
aiogram>=3.4.0
aiosqlite>=0.19.0
reportlab>=4.1.0
pydantic>=2.5.0
python-dotenv>=1.0.0
```
