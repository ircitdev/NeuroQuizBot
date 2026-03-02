"""Quiz handler with FSM"""
import os
from pathlib import Path
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.db import db
from bot.keyboards.quiz_kb import get_quiz_keyboard, get_event_keyboard
from bot.services.quiz_data import get_question, get_total_questions
from bot.services.scoring import calculate_result, get_progress_bar
from bot.services.topic_manager import create_lead_topic
from bot.services.pdf_handler import send_pdfs
from bot.utils.formatting import format_question_message, format_result_message

# Path to quiz images
QUIZ_IMAGES_DIR = Path(__file__).parent.parent.parent / "assets" / "quiz"

router = Router()


class QuizStates(StatesGroup):
    """Quiz FSM states"""
    waiting_start = State()
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    question_7 = State()
    completed = State()


@router.callback_query(F.data == "start_quiz")
@router.message(Command("quiz"))
@router.message(F.text == "📊 Пройти квиз")
async def start_quiz(event: Message | CallbackQuery, state: FSMContext):
    """Start quiz"""
    # Clear previous state
    await state.clear()

    # Send first question
    question = get_question(1)
    total = get_total_questions()
    progress = get_progress_bar(1, total)

    text = format_question_message(1, total, question.text)
    text += f"\n\n{progress}"

    # Check if image exists for this question
    image_path = QUIZ_IMAGES_DIR / "q1.jpg"

    if isinstance(event, CallbackQuery):
        # For callback query, delete old message and send new one with photo
        if image_path.exists():
            chat_id = event.message.chat.id
            await event.message.delete()
            await event.bot.send_photo(
                chat_id=chat_id,
                photo=FSInputFile(image_path),
                caption=text,
                reply_markup=get_quiz_keyboard(question)
            )
        else:
            await event.message.edit_text(
                text,
                reply_markup=get_quiz_keyboard(question)
            )
        await event.answer()
    else:
        if image_path.exists():
            await event.answer_photo(
                photo=FSInputFile(image_path),
                caption=text,
                reply_markup=get_quiz_keyboard(question)
            )
        else:
            await event.answer(
                text,
                reply_markup=get_quiz_keyboard(question)
            )

    await state.set_state(QuizStates.question_1)


@router.callback_query(F.data.startswith("quiz:"))
async def process_answer(callback: CallbackQuery, state: FSMContext):
    """Process quiz answer"""
    # Parse callback data: quiz:question_id:option_index
    parts = callback.data.split(":")
    question_id = int(parts[1])
    option_index = int(parts[2])

    # Get question and selected option
    question = get_question(question_id)
    selected_option = question.options[option_index]

    # Save answer to state
    data = await state.get_data()
    answers = data.get('answers', {})
    answers[f'q{question_id}'] = {
        'label': selected_option.label,
        'score': selected_option.score,
        'tag': selected_option.tag
    }
    await state.update_data(answers=answers)

    # Check if quiz is completed
    total_questions = get_total_questions()
    if question_id >= total_questions:
        # Quiz completed
        await complete_quiz(callback, state)
        return

    # Move to next question
    next_question_id = question_id + 1
    next_question = get_question(next_question_id)
    progress = get_progress_bar(next_question_id, total_questions)

    text = format_question_message(next_question_id, total_questions, next_question.text)
    text += f"\n\n{progress}"

    # Check if image exists for this question
    image_path = QUIZ_IMAGES_DIR / f"q{next_question_id}.jpg"

    if image_path.exists():
        # Delete old message and send new one with photo
        chat_id = callback.message.chat.id
        await callback.message.delete()
        await callback.bot.send_photo(
            chat_id=chat_id,
            photo=FSInputFile(image_path),
            caption=text,
            reply_markup=get_quiz_keyboard(next_question)
        )
    else:
        # Just edit text if no image
        await callback.message.edit_text(
            text,
            reply_markup=get_quiz_keyboard(next_question)
        )

    # Update state
    state_name = f"question_{next_question_id}"
    await state.set_state(getattr(QuizStates, state_name))

    await callback.answer()


async def complete_quiz(callback: CallbackQuery, state: FSMContext):
    """Complete quiz and show results"""
    data = await state.get_data()
    answers = data.get('answers', {})

    # Calculate result
    user_id = callback.from_user.id
    quiz_result = calculate_result(user_id, answers)

    # Save to database
    await db.save_quiz_result(
        user_id=user_id,
        answers=answers,
        total_score=quiz_result.total_score,
        profile=quiz_result.profile,
        main_tag=quiz_result.main_tag
    )

    # Delete question message and send result
    result_text = format_result_message({
        'total_score': quiz_result.total_score,
        'profile': quiz_result.profile,
        'main_tag': quiz_result.main_tag
    })

    # Delete old message (might be a photo)
    try:
        await callback.message.delete()
    except Exception:
        pass  # Ignore if deletion fails

    # Send result as new message
    await callback.message.answer(
        result_text,
        parse_mode="HTML"
    )

    # Send PDFs (personalized + general presentation)
    user_data = await db.get_user(user_id)
    await send_pdfs(
        callback.message,
        user_data,
        {
            'total_score': quiz_result.total_score,
            'profile': quiz_result.profile,
            'main_tag': quiz_result.main_tag
        }
    )

    # Create topic in supergroup (or get existing)
    try:
        thread_id = await create_lead_topic(
            callback.bot,
            user_data,
            {
                'total_score': quiz_result.total_score,
                'profile': quiz_result.profile,
                'main_tag': quiz_result.main_tag,
                'answers': answers
            }
        )

        # Save thread_id to database if it's new
        if not user_data.get('thread_id'):
            await db.update_user_thread(user_id, thread_id)

        # Notify user
        await callback.message.answer(
            "✅ Спасибо за прохождение квиза!\n\n"
            "💬 Теперь вы можете писать сообщения прямо сюда — "
            "наши менеджеры получат их и ответят вам."
        )
    except Exception as e:
        print(f"Error creating topic: {e}")
        # Don't fail the whole flow if topic creation fails
        await callback.message.answer(
            "✅ Спасибо за прохождение квиза!"
        )

    # Clear FSM state so user can send messages to topic
    await state.clear()
    await callback.answer()


@router.message(Command("result"))
@router.message(F.text == "📈 Мой результат")
async def show_result(message: Message):
    """Show last quiz result"""
    user_id = message.from_user.id
    result = await db.get_last_quiz_result(user_id)

    if not result:
        await message.answer(
            "У вас пока нет результатов квиза.\n"
            "Пройдите квиз: /quiz"
        )
        return

    result_text = format_result_message({
        'total_score': result['total_score'],
        'profile': result['profile'],
        'main_tag': result['main_tag']
    })

    await message.answer(
        result_text,
        parse_mode="HTML",
        reply_markup=get_event_keyboard()
    )
