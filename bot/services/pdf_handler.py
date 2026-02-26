"""PDF handler - sends both personalized PDF and general presentation"""
import os
from typing import Dict, Any
from io import BytesIO
from aiogram.types import Message, FSInputFile, BufferedInputFile
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from bot.keyboards.quiz_kb import get_event_keyboard
from bot.services.quiz_data import TAG_LABELS, TAG_TECHNIQUES

# Color palette matching the website
NEON_BLUE = colors.HexColor('#00B4FF')
NEON_PURPLE = colors.HexColor('#8B5CF6')
ACCENT_GREEN = colors.HexColor('#10B981')
TEXT_DARK = colors.HexColor('#1F2937')
TEXT_GRAY = colors.HexColor('#6B7280')
BACKGROUND_LIGHT = colors.HexColor('#F5F7FA')


# Path to general presentation
PRESENTATION_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'assets',
    '5-neurotechnics.pdf'
)


def generate_personalized_pdf(user_data: Dict[str, Any], quiz_result: Dict[str, Any]) -> BytesIO:
    """
    Generate personalized PDF guide

    Args:
        user_data: User information
        quiz_result: Quiz results

    Returns:
        BytesIO object with PDF content
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           rightMargin=2*cm, leftMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm)

    story = []
    styles = getSampleStyleSheet()

    # Modern styles matching website design
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=32,
        textColor=TEXT_DARK,
        spaceAfter=20,
        alignment=TA_CENTER,
        leading=38,
        fontName='Helvetica-Bold'
    )

    title_accent_style = ParagraphStyle(
        'TitleAccent',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=NEON_BLUE,
        spaceAfter=30,
        alignment=TA_CENTER,
        leading=34,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=NEON_PURPLE,
        spaceAfter=12,
        spaceBefore=20,
        leading=22,
        fontName='Helvetica-Bold'
    )

    subheading_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=TEXT_DARK,
        spaceAfter=10,
        spaceBefore=10,
        leading=18,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=TEXT_DARK,
        spaceAfter=12,
        leading=16,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )

    body_gray_style = ParagraphStyle(
        'BodyGray',
        parent=styles['BodyText'],
        fontSize=10,
        textColor=TEXT_GRAY,
        spaceAfter=10,
        leading=14,
        alignment=TA_LEFT,
        fontName='Helvetica'
    )

    highlight_style = ParagraphStyle(
        'Highlight',
        parent=styles['BodyText'],
        fontSize=12,
        textColor=NEON_BLUE,
        spaceAfter=8,
        leading=16,
        fontName='Helvetica-Bold'
    )

    # Extract data
    first_name = user_data.get('first_name', 'Участник')
    profile = quiz_result.get('profile', '')
    total_score = quiz_result.get('total_score', 0)
    main_tag = quiz_result.get('main_tag', 'focus')

    # Cover page with modern design
    story.append(Spacer(1, 1.5*cm))

    # Title with gradient effect (using color)
    story.append(Paragraph("🧠 ВСЕМОГУЩИЕ НЕЙРОНЫ", title_accent_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("ВАШИ РЕЗУЛЬТАТЫ НЕЙРОТЕСТА", title_style))
    story.append(Spacer(1, 1.5*cm))

    # User info card (table for styling)
    user_data_content = [
        ['', ''],
        [Paragraph(f'<font size="14"><b>{first_name}</b></font>', body_style), ''],
        ['', ''],
    ]

    results_table_data = [
        [Paragraph('<font color="#8B5CF6"><b>Профиль</b></font>', body_style),
         Paragraph(f'<b>{profile}</b>', body_style)],
        [Paragraph('<font color="#8B5CF6"><b>Балл</b></font>', body_style),
         Paragraph(f'<b>{total_score}/24</b>', body_style)],
        [Paragraph('<font color="#8B5CF6"><b>Приоритет</b></font>', body_style),
         Paragraph(TAG_LABELS.get(main_tag, ''), body_style)],
    ]

    results_table = Table(results_table_data, colWidths=[7*cm, 9*cm])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BACKGROUND_LIGHT),
        ('TEXTCOLOR', (0, 0), (-1, -1), TEXT_DARK),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
    ]))

    story.append(results_table)
    story.append(Spacer(1, 1*cm))

    story.append(PageBreak())

    # Results analysis with modern styling
    story.append(Paragraph("📊 Анализ ваших результатов", heading_style))
    story.append(Spacer(1, 0.5*cm))

    # Profile description with styled boxes
    if profile == "Нейроновичок":
        profile_emoji = "🌱"
        profile_color = ACCENT_GREEN
        description = """
        Ваши результаты показывают, что вашему мозгу нужна перезагрузка.
        Не переживайте — это отличная точка старта! Многие успешные люди начинали
        именно с этого уровня. Мероприятие «Всемогущие Нейроны 3» даст вам конкретные
        инструменты для быстрого улучшения когнитивных функций.
        """
    elif profile == "Нейропрактик":
        profile_emoji = "⚡"
        profile_color = NEON_BLUE
        description = """
        У вас хорошая база когнитивных навыков, но есть точки роста.
        Вы уже используете некоторые техники для повышения продуктивности,
        но действуете интуитивно. На мероприятии вы получите продвинутые техники
        и научитесь системно применять нейронауку в повседневной жизни.
        """
    else:  # Нейромастер
        profile_emoji = "🏆"
        profile_color = NEON_PURPLE
        description = """
        Впечатляющий результат! Вы уже находитесь на высоком уровне когнитивной
        эффективности. Мероприятие «Всемогущие Нейроны 3» поможет вам выйти
        на экспертный уровень, освоить передовые техники и получить доступ
        к сообществу единомышленников.
        """

    # Profile badge with colored background
    profile_title = ParagraphStyle(
        'ProfileTitle',
        parent=heading_style,
        textColor=profile_color,
        fontSize=20,
        alignment=TA_CENTER
    )

    story.append(Paragraph(f"{profile_emoji} {profile}", profile_title))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(description, body_style))
    story.append(Spacer(1, 1*cm))

    # Priority technique with highlight box
    story.append(Paragraph("🎯 Ваша приоритетная техника", heading_style))
    story.append(Spacer(1, 0.3*cm))

    # Create highlighted box for priority
    priority_data = [
        [Paragraph(f'<b>{TAG_LABELS.get(main_tag, "")}</b>', highlight_style)],
        [Paragraph(TAG_TECHNIQUES.get(main_tag, ''), body_style)],
    ]

    priority_table = Table(priority_data, colWidths=[16*cm])
    priority_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BACKGROUND_LIGHT),
        ('TEXTCOLOR', (0, 0), (-1, -1), TEXT_DARK),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('BOX', (0, 0), (-1, -1), 2, NEON_BLUE),
    ]))

    story.append(priority_table)
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "💡 Именно на этой области вам стоит сфокусироваться в первую очередь. "
        "В приложенной презентации вы найдёте все 5 нейротехник подробно.",
        body_gray_style
    ))

    story.append(PageBreak())

    # Recommendations with styled bullets
    story.append(Paragraph("💡 Персональные рекомендации", heading_style))
    story.append(Spacer(1, 0.5*cm))

    recommendations = {
        "stress": [
            "Практикуйте дыхательные упражнения 2-3 раза в день",
            "Изучите технику «Стресс-рефрейм» из презентации",
            "Ведите журнал стрессовых ситуаций и своих реакций",
            "Начните с 5-минутной медитации каждое утро"
        ],
        "focus": [
            "Используйте технику Pomodoro (25 минут работы / 5 минут отдыха)",
            "Уберите все отвлекающие факторы во время работы",
            "Практикуйте монозадачность — одна задача за раз",
            "Изучите технику «Фокус-блок» из презентации"
        ],
        "memory": [
            "Записывайте важную информацию от руки, а не в гаджет",
            "Используйте mind maps для структуризации знаний",
            "Повторяйте информацию через 1 час, 1 день, 1 неделю",
            "Изучите технику «Нейрозапись» из презентации"
        ],
        "decisions": [
            "Записывайте важные решения на бумаге",
            "Прислушивайтесь к интуиции, но проверяйте логикой",
            "Создавайте список «за» и «против» для сложных решений",
            "Изучите технику «Дерево решений» из презентации"
        ],
        "recovery": [
            "Оптимизируйте утренний ритуал: свет → вода → движение",
            "Соблюдайте режим сна (7-9 часов)",
            "Практикуйте активное восстановление в течение дня",
            "Изучите технику «Нейростарт» из презентации"
        ]
    }

    # Create styled list with colored bullets
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=20,
        bulletIndent=10,
        spaceAfter=8
    )

    for idx, rec in enumerate(recommendations.get(main_tag, []), 1):
        bullet_text = f'<font color="#00B4FF">★</font> {rec}'
        story.append(Paragraph(bullet_text, bullet_style))

    story.append(Spacer(1, 1*cm))

    # Call to action with styled box
    story.append(PageBreak())
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("🚀 Что дальше?", heading_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "Эти рекомендации — только начало вашего пути. Чтобы получить полную систему "
        "управления своим мозгом и энергией, приходите на живое мероприятие:",
        body_style
    ))
    story.append(Spacer(1, 1*cm))

    # Event info in styled box
    event_data = [
        [Paragraph('<font size="16" color="#8B5CF6"><b>ВСЕМОГУЩИЕ НЕЙРОНЫ 3</b></font>', body_style)],
        [Paragraph('<font size="12" color="#00B4FF"><b>20 марта 2026 • Крокус-Экспо</b></font>', body_style)],
        [Spacer(1, 0.3*cm)],
        [Paragraph('<b>🎯 Вы получите:</b>', body_style)],
        [Paragraph('⚡ Практические мастер-классы от ведущих нейрофизиологов', body_style)],
        [Paragraph('⚡ Индивидуальную диагностику когнитивного профиля', body_style)],
        [Paragraph('⚡ Персональную программу нейроразвития', body_style)],
        [Paragraph('⚡ Доступ к закрытому комьюнити', body_style)],
    ]

    event_table = Table(event_data, colWidths=[16*cm])
    event_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BACKGROUND_LIGHT),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, 0), 20),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -2), 5),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 20),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
        ('BOX', (0, 0), (-1, -1), 2, NEON_PURPLE),
    ]))

    story.append(event_table)
    story.append(Spacer(1, 1*cm))

    # Footer
    story.append(Paragraph(
        '<font color="#6B7280" size="9">📱 Вернитесь в бота, чтобы связаться с нашей командой и узнать больше!</font>',
        body_gray_style
    ))

    # Build PDF
    doc.build(story)
    buffer.seek(0)

    return buffer


async def send_pdfs(message: Message, user_data: Dict[str, Any], quiz_result: Dict[str, Any]) -> None:
    """
    Send both personalized PDF and general presentation

    Args:
        message: Message object to reply to
        user_data: User information
        quiz_result: Quiz results
    """
    # Generate and send personalized PDF
    try:
        pdf_buffer = generate_personalized_pdf(user_data, quiz_result)
        first_name = user_data.get('first_name', 'Guide')
        safe_name = "".join(c for c in first_name if c.isalnum() or c in (' ', '-', '_'))
        filename = f"Neiro_Results_{safe_name}.pdf"

        pdf_file = BufferedInputFile(pdf_buffer.read(), filename=filename)

        await message.answer_document(
            pdf_file,
            caption="📊 <b>Ваши персональные результаты</b>\n\n"
                    "Сохраните этот документ — в нём ваш профиль и индивидуальные рекомендации.",
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Error generating personalized PDF: {e}")

    # Send general presentation
    try:
        if os.path.exists(PRESENTATION_PATH):
            presentation_file = FSInputFile(PRESENTATION_PATH, filename="5_Neurotechnics.pdf")

            await message.answer_document(
                presentation_file,
                caption="📚 <b>5 нейротехник для продуктивности</b>\n\n"
                        "Полная презентация со всеми техниками, которые помогут вам "
                        "улучшить концентрацию, память и стрессоустойчивость.",
                parse_mode="HTML",
                reply_markup=get_event_keyboard()
            )
        else:
            print(f"Presentation file not found: {PRESENTATION_PATH}")
    except Exception as e:
        print(f"Error sending presentation: {e}")
