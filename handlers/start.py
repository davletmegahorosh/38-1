from aiogram import types, Dispatcher
from config import bot


async def start_button(message: types.Message):
    print(message)

    await bot.send_message(
        chat_id=message.from_user.id,
        text=f'Hello {message.from_user.last_name}'
    )


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(
        start_button,
        commands=['start']
    )
