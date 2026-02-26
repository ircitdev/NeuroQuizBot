# Исправление: Бот не реагирует на нажатие кнопок

## Дата
27 февраля 2026

## Проблема
Бот не реагировал на нажатие кнопок в викторине. Callback-запросы не обрабатывались.

## Причина
В файле `bot/handlers/quiz.py` была ошибка в обработке callback-запросов при отправке фото с вопросами:

```python
# ОШИБОЧНЫЙ КОД:
if image_path.exists():
    await callback.message.delete()
    await callback.message.answer_photo(  # ❌ ОШИБКА!
        photo=FSInputFile(image_path),
        caption=text,
        reply_markup=get_quiz_keyboard(question)
    )
```

**Проблема:** После вызова `message.delete()` объект сообщения удаляется из чата, и последующий вызов `message.answer_photo()` пытается отправить сообщение от несуществующего объекта, что вызывает ошибку.

## Решение

Изменено на использование `bot.send_photo()` с явным указанием `chat_id`:

```python
# ИСПРАВЛЕННЫЙ КОД:
if image_path.exists():
    chat_id = callback.message.chat.id  # Сохраняем chat_id
    await callback.message.delete()
    await callback.bot.send_photo(  # ✅ ПРАВИЛЬНО!
        chat_id=chat_id,
        photo=FSInputFile(image_path),
        caption=text,
        reply_markup=get_quiz_keyboard(question)
    )
```

## Затронутые места

Исправлено в двух функциях в `bot/handlers/quiz.py`:

1. **Функция `start_quiz()`** (строки ~56-64)
   - Обрабатывает начало викторины по нажатию кнопки "Начать квиз"

2. **Функция `process_answer()`** (строки ~129-137)
   - Обрабатывает ответы на вопросы викторины

## Коммит

Commit: `c6574d0`
Сообщение: "Исправлена отправка фото в callback-запросах"

## Как применить исправление

### На локальной машине
```bash
cd /path/to/NeuroQuizBot
git pull origin master
```

### На сервере
```bash
cd /root/NeuroQuizBot
git pull
docker compose restart
```

## Проверка

После применения исправления:
1. Отправьте боту команду `/start`
2. Нажмите кнопку "📊 Пройти квиз"
3. Бот должен показать первый вопрос с картинкой
4. Нажмите на любой вариант ответа
5. Бот должен показать следующий вопрос

## Связанные файлы
- `bot/handlers/quiz.py` - основной файл с исправлением
- `BUGFIX_RELAY.md` - предыдущее исправление relay-системы
