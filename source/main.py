import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
import datapane as dp
import plotly.express as px
import pandas as pd
import io

from libs.file_wrapper import CSVWorker
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Create inline keyboard
def create_inline_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    view_original_button = InlineKeyboardButton("View Original CSV", callback_data="view_original")
    download_report_button = InlineKeyboardButton("Download Report", callback_data="download_report")
    keyboard.add(view_original_button, download_report_button)
    return keyboard

def draw_graph():
    df_page1 = pd.DataFrame({
        'col1': [1, 2, 3, 4, 5],
        'col2': [6, 7, 8, 9, 10]
    })

    plot_page1 = px.bar(x=range(5), y=range(5), title='Example Bar Plot')

    datapane_app = dp.App(
        dp.Page(
            dp.Text('# Page 1'),
            dp.Text('In this page I will demonstrate combination of data frames, plots, and Markdown'),
            dp.Text('### Table Example'),
            dp.DataTable(df_page1),
            dp.Text('This is example table. Here I can add comments of any length'),
            dp.Text('### Plot Example'),
            dp.Plot(plot_page1),
            title='Page1'
        ),
        dp.Page(
            dp.Text('In this page I will focus on KPIs and aligning multiple elements in one row'),
            dp.Group(
                dp.BigNumber(
                    heading="Percentage points",
                    value="84%",
                    change="2%",
                    is_upward_change=False,
                ),
                dp.BigNumber(
                    heading="Points",
                    value="1234",
                    change="200",
                    is_upward_change=True,
                ),
                columns=2
            ),
            dp.Group(
                dp.Text('My simple text 1'),
                dp.Text('My simple text 2'),
                dp.Text('My simple text 3'),
                columns=3
            ),
            title='Page2',
        )
    )
    datapane_app.save('final_example.html')

    return 'final_example.html'


# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token='6488657739:AAGOkHPkasMy1l5vO6lB_bfpbmnbyjDHTw8')
dp_bot = Dispatcher(bot)
dp_bot.middleware.setup(LoggingMiddleware())

@dp_bot.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

@dp_bot.message_handler(commands=['graph'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    # Replace 'path/to/your/file.txt' with the actual path to your file

    file_path = draw_graph()
    # file_path = "path/to/your/file.txt"

    # Open and send the file to the user
    with open(file_path, "rb") as file:
        await message.reply_document(file)

@dp_bot.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_document(message: types.Message):
    document = message.document
    file_id = document.file_id
    file_name = document.file_name

    # Download the file
    file_bytes = await bot.download_file_by_id(file_id)

    csv_data = io.StringIO(file_bytes.decode("utf-8"))

    CSVWorker(csv_data)

    # Get the file using the file_id and send a response
    await bot.send_message(message.chat.id, f"Received document: {file_name} (File ID: {file_id})")

@dp_bot.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)



# Callback query handler for inline buttons
@dp_bot.callback_query_handler(lambda query: query.data in ["view_original", "download_report"])
async def handle_inline_buttons(callback_query: types.CallbackQuery):
    if callback_query.data == "view_original":
        await bot.send_message(callback_query.from_user.id, "Viewing original CSV...")
    elif callback_query.data == "download_report":
        await bot.send_document(callback_query.from_user.id, types.InputFile("/Users/nadyakott/PycharmProjects/analyzeWise_tg/source/final_example.html"))

if __name__ == '__main__':
  executor.start_polling(dp_bot, skip_updates=True)