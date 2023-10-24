from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class MainMenu:
    def __init__(self):
        self.keyboard = InlineKeyboardMarkup()
        show_faq = InlineKeyboardButton("FAQ", callback_data="show_faq")
        # view_original_button = InlineKeyboardButton("Upload CSV file", callback_data="upload_file")
        # download_report_button = InlineKeyboardButton("Download Report", callback_data="download_report")
        self.keyboard.add(show_faq
                          # , view_original_button
        # , download_report_button
        )
