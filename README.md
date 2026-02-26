# NeuroQuizBot - Telegram Quiz Bot

Telegram-бот для мероприятия «Всемогущие Нейроны 3» с квизом по нейрофизиологии, генерацией персонализированных PDF-гайдов и двусторонней перепиской через форум-топики в супергруппе.

## Возможности

- ✅ Квиз из 7 вопросов с inline-кнопками
- ✅ Персонализированная оценка когнитивного профиля
- ✅ Генерация PDF-гайда «5 нейротехник для продуктивности»
- ✅ Автоматическое создание топиков в супергруппе для каждого лида
- ✅ Двусторонняя переписка менеджер ↔ пользователь через топики
- ✅ UTM-трекинг источников трафика
- ✅ Статистика для админов

## Технологии

- Python 3.11+
- aiogram 3.x
- SQLite / PostgreSQL
- ReportLab (генерация PDF)
- Docker

## Установка

### 1. Клонировать репозиторий

```bash
git clone <repo-url>
cd NeuroQuizBot
```

### 2. Настроить .env файл

Файл `.env` уже создан, проверьте настройки:

```env
BOT_TOKEN=8639010263:AAFKebwE7rIUj9kfmlok7jrm4eucfEoZCMQ
SUPERGROUP_CHAT_ID=-1003596687347
DATABASE_URL=sqlite:///data/bot.db
ADMIN_IDS=123456789,987654321
```

**ВАЖНО:** Добавьте свой Telegram ID в `ADMIN_IDS` для доступа к команде `/stats`.

### 3. Запуск с Docker (рекомендуется)

```bash
docker-compose up -d
```

### 4. Запуск без Docker

```bash
# Установить зависимости
pip install -r requirements.txt

# Запустить бота
python -m bot.main
```

## Настройка супергруппы

1. Создайте супергруппу в Telegram
2. Включите топики (Topics): Settings → Topics → Enable Topics
3. Добавьте бота в супергруппу как администратора
4. Дайте боту права:
   - Управление топиками
   - Отправка сообщений
   - Чтение всех сообщений
5. Получите Chat ID супергруппы и укажите в `.env`

### Как получить Chat ID супергруппы:

1. Добавьте [@getmyid_bot](https://t.me/getmyid_bot) в супергруппу
2. Скопируйте Chat ID (будет в формате `-100XXXXXXXXXX`)
3. Удалите @getmyid_bot из группы

## Команды бота

| Команда | Описание |
|---------|----------|
| `/start` | Запуск бота, приветствие |
| `/start lead_site` | Запуск с лендинга (UTM) |
| `/start lead_instagram` | Запуск из Instagram |
| `/quiz` | Запустить квиз |
| `/result` | Показать последний результат |
| `/help` | Справка |
| `/stats` | Статистика (только для админов) |

## Deep Links для интеграции

### На сайте

```html
<a href="https://t.me/NeuroEventsBot?start=lead_site">Получить в Telegram</a>
```

### В Instagram Bio

```
https://t.me/NeuroEventsBot?start=lead_instagram
```

## Структура проекта

```
NeuroQuizBot/
├── bot/
│   ├── __init__.py
│   ├── main.py              # Точка входа
│   ├── config.py             # Настройки
│   ├── db.py                 # База данных
│   ├── models.py             # Модели данных
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── start.py          # /start команда
│   │   ├── quiz.py           # Логика квиза (FSM)
│   │   ├── relay.py          # Пересылка сообщений
│   │   ├── help_handler.py   # /help команда
│   │   └── stats.py          # /stats команда
│   ├── keyboards/
│   │   ├── quiz_kb.py        # Inline-клавиатуры
│   │   └── main_kb.py        # Reply-клавиатуры
│   ├── services/
│   │   ├── quiz_data.py      # Вопросы квиза
│   │   ├── scoring.py        # Подсчёт результата
│   │   ├── pdf_generator.py  # Генерация PDF
│   │   └── topic_manager.py  # Управление топиками
│   └── utils/
│       └── formatting.py     # Форматирование сообщений
├── data/                     # База данных (создаётся автоматически)
├── .env                      # Конфигурация
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Логика работы

### Флоу пользователя:

1. Пользователь нажимает deep link на сайте → `/start lead_site`
2. Бот сохраняет пользователя с UTM-меткой
3. Показывает приветствие с кнопкой «Начать квиз»
4. Пользователь проходит 7 вопросов
5. Бот подсчитывает результат и определяет профиль
6. Отправляет персонализированный PDF-гайд
7. Создаёт топик в супергруппе с данными лида
8. Пользователь может писать боту → сообщения попадают в топик
9. Менеджер отвечает в топике → сообщение уходит пользователю

### Квиз:

- 7 вопросов с inline-кнопками
- Вопросы 1-6: начисляются баллы (1-4)
- Вопрос 7: определяет приоритетный тег (без баллов)
- Итого: 6-24 балла

### Профили:

| Баллы | Профиль | Emoji |
|-------|---------|-------|
| 6-12 | Нейроновичок | 🌱 |
| 13-18 | Нейропрактик | ⚡ |
| 19-24 | Нейромастер | 🏆 |

### Теги:

- `stress` — Стрессоустойчивость
- `focus` — Концентрация и продуктивность
- `memory` — Память и обучаемость
- `decisions` — Принятие решений
- `recovery` — Восстановление и энергия

## Разработка

### Запуск в режиме разработки

```bash
# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Установить зависимости
pip install -r requirements.txt

# Запустить бота
python -m bot.main
```

### Логи

```bash
# Docker
docker-compose logs -f quiz-bot

# Без Docker
python -m bot.main
```

## Деплой на VPS

```bash
# Подключиться к VPS
ssh user@your-vps-ip

# Установить Docker и Docker Compose (если не установлены)
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Клонировать репозиторий
git clone <repo-url>
cd NeuroQuizBot

# Настроить .env
nano .env

# Запустить
docker-compose up -d

# Проверить статус
docker-compose ps
docker-compose logs -f
```

## Поддержка

При возникновении проблем проверьте:

1. Правильность `BOT_TOKEN` в `.env`
2. Права бота в супергруппе
3. Включены ли топики в супергруппе
4. Логи: `docker-compose logs -f quiz-bot`

## Лицензия

MIT

## Автор

Создано для мероприятия «Всемогущие Нейроны 3»
