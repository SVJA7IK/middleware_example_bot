import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from filters.filters import MyFalseFilter, MyTrueFilter


# Инициализируем логгер модуля
logger = logging.getLogger(__name__)

# Инициализируем роутер уровня модуля
user_router = Router()


# Этот хэндлер срабатывает на команду /start
@user_router.message(CommandStart(), MyTrueFilter())
async def process_start_command(message: Message, i18n: dict[str, str]):
    logger.debug('Вошли в хэндлер, обрабатывающий команду /start')
    # Создаем объект инлайн-кнопки
    button = InlineKeyboardButton(
        text=i18n.get('button'),
        callback_data='button_pressed'
    )
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    # Отправляем сообщение пользователю
    await message.answer(text=i18n.get('/start'), reply_markup=markup)
    logger.debug('Выходим из хэндлера, обрабатывающего команду /start')


# Этот хэндлер срабатывает на нажатие инлайн-кнопки
@user_router.callback_query(F.data, MyTrueFilter())
async def process_button_click(callback: CallbackQuery, i18n: dict[str, str]):
    logger.debug('Вошли в хэндлер, обрабатывающий нажатие на инлайн-кнопку')
    await callback.answer(text=i18n.get('button_pressed'))
    logger.debug('Выходим из хэндлера, обрабатывающего нажатие на инлайн-кнопку')


# Это хэндлер, который мог бы обрабатывать любой текст, но `MyFalseFilter` его не пропустит
@user_router.message(F.text, MyFalseFilter())
async def process_text(message: Message):
    logger.debug('Вошли в хэндлер, обрабатывающий текст')
    logger.debug('Выходим из хэндлера, обрабатывающего текст')
