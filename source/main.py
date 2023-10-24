import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
import plotly.express as px
import pandas as pd
import io
import os
import time


from libs.file_wrapper import FileWrapper
from libs.report_builder import ReportBuilder
from libs.settings import settings
from handlers.keyboard import MainMenu

from customs.text import WELCOME_TEXT

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Define states
PROCESSING_STATE = 'processing'

# Dictionary to store uploaded CSV data
uploaded_csv_data = {}

reportBuilder = ReportBuilder()

# Directory for storing uploaded CSV files
UPLOADS_DIRECTORY = 'downloads'

# Create the directory if it doesn't exist
if not os.path.exists(UPLOADS_DIRECTORY):
    os.makedirs(UPLOADS_DIRECTORY)

main_menu = MainMenu()


@dp.message_handler(commands=['start', 'help', 'menu'])

async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(WELCOME_TEXT
                        , reply_markup=main_menu.keyboard
                        , parse_mode=ParseMode.MARKDOWN)

# @dp_bot.message_handler(commands=['graph'])
# async def send_welcome(message: types.Message):
#     """
#     This handler will be called when user sends `/start` or `/help` command
#     """
#     # Replace 'path/to/your/file.txt' with the actual path to your file
#
#     file_path = ReportBuilder.draw_graph(data)
#     # file_path = "path/to/your/file.txt"
#
#     # Open and send the file to the user
#     with open(file_path, "rb") as file:
#         await message.reply_document(file)

# @dp_bot.message_handler(content_types=types.ContentType.DOCUMENT)
# async def handle_document(message: types.Message):
#     document = message.document
#     file_id = document.file_id
#     file_name = document.file_name
#
#     # Download the file
#     file_bytes = await bot.download_file_by_id(file_id)
#
#     csv_data = io.StringIO(file_bytes.decode("utf-8"))
#
#     FileWrapper(csv_data)
#
#     # Get the file using the file_id and send a response
#     await bot.send_message(message.chat.id, f"Received document: {file_name} (File ID: {file_id})")

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def upload_file(message: types.Message):
    if message.document.mime_type == 'text/csv':
        try:
            # Get the uploaded document
            document = message.document

            file_info = await bot.get_file(document.file_id)
            # file_path = file_info.file_path
            # csv_file = await bot.download_file(file_path)

            file_path = os.path.join('downloads', document.file_name)

            file = await bot.download_file(file_info.file_path, file_path)

            with open(file_path, 'rb') as file:
                # Read the CSV file using pandas
                df = pd.read_csv(file, index_col=['Unnamed: 0'])
                reportBuilder.data = df

                # Store the CSV data in the dictionary with the user's chat ID as the key
                user_id = message.from_user.id
                uploaded_csv_data[user_id] = df

            # Send a response message
            await message.answer("CSV file uploaded and processed.")

            if not os.path.exists(f'reports/{user_id}'):
                os.makedirs(f'reports/{user_id}')

            report_path = os.path.join(f'reports/{user_id}',f"{message.from_user.id}_{int(time.time())}.html")

            file_name, report_html = reportBuilder.draw_graph(report_path)

            await bot.send_document(user_id, types.InputFile(report_path))

        except Exception as e:
            await message.answer(f"An error occurred: {str(e)}")


@dp.callback_query_handler(lambda query: query.data in ["show_faq", "download_report"])
async def handle_inline_buttons(callback_query: types.CallbackQuery):
    if callback_query.data == "show_faq":
        await callback_query.message.reply(WELCOME_TEXT, reply_markup=main_menu.keyboard)
    elif callback_query.data == "download_report":
        file_name = f"{callback_query.from_user.id}.html"
        await bot.send_document(callback_query.from_user.id, types.InputFile(f"/Users/nadyakott/PycharmProjects/analyzeWise_tg/source/{file_name}"))

if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)