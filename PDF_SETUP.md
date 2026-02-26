# Настройка PDF генерации

## 🔤 Кириллица в PDF

### Проблема
По умолчанию ReportLab использует шрифты, не поддерживающие кириллицу (Helvetica, Times).

### Решение
Подключен шрифт **Montserrat** с полной поддержкой кириллицы.

---

## 📁 Файлы шрифтов

### Расположение
```
NeuroQuizBot/
├── Montserrat-Regular.ttf  # Основной текст (240 KB)
├── Montserrat-Black.ttf     # Жирные заголовки (252 KB)
└── logo.jpg                 # Логотип (93 KB)
```

### Регистрация шрифтов

В [bot/services/pdf_handler.py](bot/services/pdf_handler.py):

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Пути к шрифтам
FONT_PATH = BASE_DIR / "Montserrat-Regular.ttf"
FONT_BOLD_PATH = BASE_DIR / "Montserrat-Black.ttf"

# Регистрация
pdfmetrics.registerFont(TTFont('Montserrat', str(FONT_PATH)))
pdfmetrics.registerFont(TTFont('Montserrat-Bold', str(FONT_BOLD_PATH)))
```

### Использование в стилях

```python
# Определяем шрифты с fallback
font_regular = 'Montserrat' if FONT_PATH.exists() else 'Helvetica'
font_bold = 'Montserrat-Bold' if FONT_BOLD_PATH.exists() else 'Helvetica-Bold'

# Применяем в стилях
body_style = ParagraphStyle(
    'CustomBody',
    fontName=font_regular,  # Montserrat вместо Helvetica
    fontSize=11,
    textColor=TEXT_DARK,
)
```

---

## 🖼️ Логотип в PDF

### Файл
- **Путь**: `logo.jpg` в корне проекта
- **Размер**: 93 KB
- **Формат**: JPEG

### Добавление в PDF

```python
from reportlab.platypus import Image

# Путь к логотипу
LOGO_PATH = BASE_DIR / "logo.jpg"

# Добавление в конец документа
if LOGO_PATH.exists():
    logo = Image(str(LOGO_PATH), width=8*cm, height=None, kind='proportional')
    logo.hAlign = 'CENTER'
    story.append(logo)
```

### Параметры
- **Ширина**: 8 см
- **Высота**: Пропорциональная
- **Выравнивание**: По центру

---

## ✅ Что исправлено

### Кодировка
- ✅ Все русские символы корректно отображаются
- ✅ Заголовки, текст, таблицы используют Montserrat
- ✅ Fallback на Helvetica если шрифт недоступен

### Логотип
- ✅ Добавлен в конец каждого PDF
- ✅ Центрируется и масштабируется
- ✅ Не ломает генерацию если файл отсутствует

---

## 🔧 Развёртывание на сервере

### Структура файлов на сервере

```bash
/root/NeuroQuizBot/
├── Montserrat-Regular.ttf
├── Montserrat-Black.ttf
├── logo.jpg
└── bot/
    └── services/
        └── pdf_handler.py
```

### Загрузка файлов

```bash
# Загрузить шрифты и логотип
scp Montserrat-Regular.ttf root@31.44.7.144:/root/NeuroQuizBot/
scp Montserrat-Black.ttf root@31.44.7.144:/root/NeuroQuizBot/
scp logo.jpg root@31.44.7.144:/root/NeuroQuizBot/

# Загрузить обновленный обработчик
scp bot/services/pdf_handler.py root@31.44.7.144:/root/NeuroQuizBot/bot/services/

# Перезапустить бота
ssh root@31.44.7.144 "cd /root/NeuroQuizBot && docker compose restart"
```

---

## 🐛 Решение проблем

### Проблема: Кракозябры вместо русских букв

**Причина**: Шрифт не поддерживает кириллицу

**Решение**:
1. Проверьте наличие файлов шрифтов:
   ```bash
   ls -lh Montserrat*.ttf
   ```
2. Убедитесь, что шрифты зарегистрированы в коде
3. Проверьте логи бота на ошибки регистрации шрифтов

### Проблема: Логотип не отображается

**Причина**: Файл `logo.jpg` отсутствует или путь неверный

**Решение**:
1. Проверьте наличие файла:
   ```bash
   ls -lh logo.jpg
   ```
2. Убедитесь, что путь `LOGO_PATH` корректен
3. Проверьте формат файла (должен быть JPEG)

### Проблема: PDF не генерируется

**Причина**: Ошибка в импорте или регистрации шрифтов

**Решение**:
1. Проверьте логи бота:
   ```bash
   docker logs neuroquiz-bot --tail 50
   ```
2. Убедитесь, что ReportLab установлен:
   ```bash
   docker exec neuroquiz-bot pip list | grep reportlab
   ```
3. Проверьте права доступа к файлам шрифтов:
   ```bash
   chmod 644 Montserrat*.ttf logo.jpg
   ```

---

## 📊 Цветовая палитра PDF

```python
NEON_BLUE = colors.HexColor('#00B4FF')      # Акценты
NEON_PURPLE = colors.HexColor('#8B5CF6')    # Заголовки
ACCENT_GREEN = colors.HexColor('#10B981')   # Новички
TEXT_DARK = colors.HexColor('#1F2937')      # Основной текст
TEXT_GRAY = colors.HexColor('#6B7280')      # Вторичный текст
BACKGROUND_LIGHT = colors.HexColor('#F5F7FA') # Фон таблиц
```

---

## 🎨 Пример структуры PDF

1. **Обложка**
   - Заголовок: "ВСЕМОГУЩИЕ НЕЙРОНЫ" (Montserrat-Bold, голубой)
   - Подзаголовок: "ВАШИ РЕЗУЛЬТАТЫ НЕЙРОТЕСТА" (Montserrat-Bold, черный)
   - Таблица с результатами (Montserrat-Regular)

2. **Анализ результатов**
   - Профиль с эмодзи (Montserrat-Bold, цветной)
   - Описание профиля (Montserrat-Regular)

3. **Рекомендации**
   - Приоритетная техника в рамке
   - Список рекомендаций с цветными звездочками

4. **Призыв к действию**
   - Информация о мероприятии
   - Контактная информация
   - **Логотип** (центрирован, 8см ширина)

---

Готово! PDF теперь корректно отображает кириллицу и содержит логотип. 🎨
