from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ChatType, InputFile, ChatActions

from app.core.keyboards import reply
from app.core.messages.private_chat import base as msgs
from app.core.middlewares.throttling import throttle
from app.core.navigations.command import Commands
from app.exceptions.load_api import LoadError
from app.models.dto import get_user_from_message
from app.services.api.base import Audio
from app.services.api.youtube import YouTubeLoader
from app.services.database.dao.user import UserDAO


@throttle(limit=2)
async def cmd_start(m: types.Message, state: FSMContext):
    """/start command handling. Adds new user to database, finish states"""

    await state.finish()

    user = get_user_from_message(message=m)
    session = UserDAO(session=m.bot.get("db"))
    await session.add_user(user)

    await m.answer(msgs.welcome(user_firstname=user.firstname), reply_markup=None)


@throttle(limit=4)
async def load_content(m: types.Message):

    yt_loader = YouTubeLoader(url=m.text)
    await m.reply(msgs.loading_started)
    await m.answer_chat_action(ChatActions.RECORD_AUDIO)

    try:

        audio: Audio = yt_loader.load(user_id=m.from_user.id)

        await m.answer_audio(InputFile(audio.file_path), caption="@RadiamBot", title=audio.file_name)
        yt_loader.clear_cache(user_id=m.from_user.id)

    except LoadError:
        await m.reply(msgs.load_error)


def register_handlers(dp: Dispatcher) -> None:
    """Register base handlers: /start and handling events from default menu"""

    dp.register_message_handler(cmd_start, commands=str(Commands.start),
                                chat_type=ChatType.PRIVATE, state="*")
    dp.register_message_handler(load_content, chat_type=ChatType.PRIVATE)
