# Инструкция по развёртыванию и управлению

## 🚀 Бот успешно развёрнут!

- **GitHub:** https://github.com/ircitdev/NeuroQuizBot
- **Сервер:** root@31.44.7.144
- **Путь:** `/root/NeuroQuizBot`
- **Telegram:** [@NeuroEvents_bot](https://t.me/NeuroEvents_bot)

---

## 📊 Проверка статуса

```bash
# Подключение к серверу
ssh root@31.44.7.144

# Проверить запущен ли контейнер
docker ps | grep neuroquiz

# Посмотреть логи
docker logs neuroquiz-bot

# Посмотреть последние 50 строк логов
docker logs neuroquiz-bot --tail 50

# Следить за логами в реальном времени
docker logs -f neuroquiz-bot
```

---

## 🔄 Обновление бота

### Через GitHub (рекомендуется)

```bash
# 1. Внести изменения локально
cd d:/DevTools/Database/NeuroQuizBot
git add .
git commit -m "Update: описание изменений"
git push

# 2. Обновить на сервере
ssh root@31.44.7.144
cd /root/NeuroQuizBot
git pull
docker compose down
docker compose up -d --build
```

### Прямое редактирование на сервере

```bash
ssh root@31.44.7.144
cd /root/NeuroQuizBot

# Редактировать файлы
nano bot/handlers/quiz.py

# Перезапустить бота
docker compose restart
```

---

## 🛠 Управление контейнером

```bash
# Остановить бота
docker compose down

# Запустить бота
docker compose up -d

# Перезапустить бота
docker compose restart

# Пересобрать и запустить (после изменений кода)
docker compose up -d --build

# Посмотреть статус
docker compose ps

# Посмотреть использование ресурсов
docker stats neuroquiz-bot
```

---

## 🗄 База данных

```bash
# Подключиться к контейнеру
docker exec -it neuroquiz-bot bash

# Внутри контейнера посмотреть БД
cd /app/data
sqlite3 bot.db

# Примеры запросов
SELECT COUNT(*) FROM users;
SELECT * FROM quiz_results ORDER BY completed_at DESC LIMIT 10;
.exit

# Выйти из контейнера
exit
```

### Бэкап базы данных

```bash
# Скопировать БД с сервера
scp root@31.44.7.144:/root/NeuroQuizBot/data/bot.db ./backup_$(date +%Y%m%d).db

# Восстановить БД на сервер
scp ./backup_20260226.db root@31.44.7.144:/root/NeuroQuizBot/data/bot.db
docker compose restart
```

---

## 📝 Изменение настроек

### Редактировать .env файл

```bash
ssh root@31.44.7.144
cd /root/NeuroQuizBot
nano .env
```

Содержимое `.env`:
```env
BOT_TOKEN=8639010263:AAFKebwE7rIUj9kfmlok7jrm4eucfEoZCMQ
SUPERGROUP_CHAT_ID=-1003596687347
DATABASE_URL=sqlite:///data/bot.db
ADMIN_IDS=123456789,987654321
```

После изменений:
```bash
docker compose restart
```

---

## 🔍 Диагностика проблем

### Бот не отвечает

```bash
# 1. Проверить запущен ли контейнер
docker ps | grep neuroquiz

# 2. Посмотреть логи на наличие ошибок
docker logs neuroquiz-bot --tail 100

# 3. Перезапустить
docker compose restart
```

### Ошибки в логах

```bash
# Посмотреть полные логи
docker logs neuroquiz-bot > bot_logs.txt
cat bot_logs.txt | grep ERROR

# Посмотреть последние ошибки
docker logs neuroquiz-bot 2>&1 | grep -i error
```

### Проблемы с памятью/CPU

```bash
# Посмотреть использование ресурсов
docker stats neuroquiz-bot --no-stream

# Увеличить лимиты в docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 512M
```

---

## 📊 Статистика бота

### Через команду /stats

1. Добавьте свой Telegram ID в `ADMIN_IDS` в `.env`
2. Перезапустите бота: `docker compose restart`
3. Отправьте `/stats` боту в Telegram

### Через базу данных

```bash
docker exec -it neuroquiz-bot sqlite3 /app/data/bot.db "
SELECT
  COUNT(*) as total_users,
  COUNT(CASE WHEN thread_id IS NOT NULL THEN 1 END) as completed_quiz
FROM users;
"
```

---

## 🔒 Безопасность

### Не забудьте:

1. **Изменить ADMIN_IDS** в `.env` на свой Telegram ID
2. **Не коммитить .env** в Git (уже в .gitignore)
3. **Настроить firewall** на сервере (только SSH)
4. **Регулярные бэкапы** базы данных

### Получить свой Telegram ID

Отправьте `/start` боту [@userinfobot](https://t.me/userinfobot)

---

## 🆘 Быстрые команды

```bash
# Подключиться и перезапустить
ssh root@31.44.7.144 "cd /root/NeuroQuizBot && docker compose restart"

# Посмотреть логи удалённо
ssh root@31.44.7.144 "docker logs neuroquiz-bot --tail 50"

# Обновить бота
ssh root@31.44.7.144 "cd /root/NeuroQuizBot && git pull && docker compose up -d --build"

# Остановить бота
ssh root@31.44.7.144 "cd /root/NeuroQuizBot && docker compose down"
```

---

## 📱 Настройка BotFather

См. файл [BOTFATHER_SETUP.md](./BOTFATHER_SETUP.md) для настройки описания и команд бота.

---

## 🐛 Известные проблемы и решения

### Проблема: Бот не создаёт топики

**Решение:**
1. Проверьте, что супергруппа имеет включённые топики (Settings → Topics)
2. Проверьте права бота в супергруппе (администратор + управление топиками)
3. Проверьте правильность `SUPERGROUP_CHAT_ID` в `.env`

### Проблема: PDF не отправляется

**Решение:**
1. Проверьте наличие файла: `docker exec neuroquiz-bot ls -la /app/assets/`
2. Проверьте права: `docker exec neuroquiz-bot chmod 644 /app/assets/5-neurotechnics.pdf`

### Проблема: База данных заблокирована

**Решение:**
```bash
docker compose down
docker compose up -d
```

---

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи: `docker logs neuroquiz-bot`
2. Проверьте статус: `docker ps`
3. Проверьте GitHub Issues: https://github.com/ircitdev/NeuroQuizBot/issues

---

## ✅ Чек-лист после развёртывания

- [x] Бот запущен и отвечает на `/start`
- [x] База данных создана
- [x] Docker контейнер работает
- [ ] Настроен BotFather (описание, команды)
- [ ] Изменён ADMIN_IDS на свой ID
- [ ] Проверена работа квиза
- [ ] Проверена отправка PDF
- [ ] Настроена супергруппа с топиками
- [ ] Проверена система relay (пересылка сообщений)
- [ ] Настроен автозапуск при перезагрузке сервера
