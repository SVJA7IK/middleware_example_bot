import asyncio
import logging
from aiogram.fsm.state import StatesGroup
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers.other import other_router
from handlers.user import user_router
from middlewares.inner import (
    FirstInnerMiddleware,
    SecondInnerMiddleware,
    ThirdInnerMiddleware,
)
from middlewares.outer import (
    FirstOuterMiddleware,
    SecondOuterMiddleware,
    ThirdOuterMiddleware,
)
from lexicon.lexicon_en import LEXICON_EN
from lexicon.lexicon_ru import LEXICON_RU
from middlewares.i18n import TranslatorMiddleware


# Настраиваем базовую конфигурацию логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s'
)

# Инициализируем логгер модуля
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main() -> None:
    translations = {
        'default': 'ru',
        'en': LEXICON_EN,
        'ru': LEXICON_RU,
    }

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    # Регистрируем роутеры в диспетчере
    dp.include_router(user_router)
    dp.include_router(other_router)

    # Здесь будем регистрировать миддлвари
    dp.update.middleware(TranslatorMiddleware())
    dp.update.outer_middleware(FirstOuterMiddleware())
    user_router.callback_query.outer_middleware(SecondOuterMiddleware())
    other_router.message.outer_middleware(ThirdOuterMiddleware())

    user_router.message.middleware(FirstInnerMiddleware())
    user_router.message.middleware(SecondInnerMiddleware())
    other_router.message.middleware(ThirdInnerMiddleware())

    # Запускаем polling
    await dp.start_polling(bot, _translations=translations)


asyncio.run(main())
