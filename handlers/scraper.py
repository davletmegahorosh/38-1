import sqlite3

from aiogram import types, Dispatcher
from scrap.async_scrap import AsyncScraper
# from aiogram.utils.deep_linking import _create_link

from config import bot
from database import bot_db
# from keyboards import start_inline_buttons
# import const


# from scraping.news_scraper import NewsScraper


async def start_button(message: types.Message):
    db = bot_db.Database()
    scraper = AsyncScraper()
    films = await scraper.get_pages()
    films_list = []
    for i in films:
        films_list.extend(i)
    if not db.sql_select_films():
        for i in films_list[:5]:
            db.sql_insert_film(i["link"], i["image"], i["title"], i["desc"])

    for i in films_list[-5:]:
        text = (f'{i["link"]}\n'
                f'{i["title"]}\n'
                f'{i["desc"]}')
        await message.answer(text)



# async def latest_news_call(call: types.CallbackQuery):
#     scraper = NewsScraper()
#     data = scraper.scrape_data()
#     print()
#     db.insert_news()
#     for i in data[:4]:
#         await bot.send_message(
#             chat_id=call.from_user.id,
#             text=scraper.PLUS_URL + i
#         )


def register_scraper_handlers(dp: Dispatcher):
    dp.register_message_handler(
        start_button,
        commands=['scraper']
    )
    # dp.register_callback_query_handler(
    #     latest_news_call,
    #     lambda call: call.data == "latest_news"
    # )
