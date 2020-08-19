from typing import List
from telebot import TeleBot
from telebot import types
from .db.models import Category, Product
from .lookups import CATEGORY_LOOKUP, SEPARATOR, PRODUCT_LOOKUP
from .keyboards import ADD_TO_CART


class WebShopBot(TeleBot):

    @staticmethod
    def generate_categories_kb(categories: List[Category], **kwargs):
        kb = types.InlineKeyboardMarkup(**kwargs)
        buttons = [types.InlineKeyboardButton(
            text=c.title,
            callback_data=f'{CATEGORY_LOOKUP}{SEPARATOR}{c.id}'
        ) for c in categories]
        kb.add(*buttons)

        return kb

    def generate_and_send_categories_kb(self, text: str, chat_id: int, categories: List[Category], **kwargs):
        self.send_message(chat_id, text, reply_markup=self.generate_categories_kb(categories, **kwargs))

    def generate_and_edit_categories_kb(self, text: str, chat_id: int, message_id: int, categories: List[Category],
                                        **kwargs):
        self.edit_message_text(chat_id, text, message_id, reply_markup=self.generate_categories_kb(categories,
                                                                                                   **kwargs))

    @staticmethod
    def generate_products_kb(pid, **kwargs):
        kb = types.InlineKeyboardMarkup(**kwargs)
        button = types.InlineKeyboardButton(text=f'{ADD_TO_CART}',
                                            callback_data=f'{PRODUCT_LOOKUP}{SEPARATOR}{pid}')
        kb.add(button)

        return kb

    def generate_and_send_products_kb(self, chat_id: int, photo, products: List[Product], **kwargs):
        for p in products:
            self.send_photo(chat_id, photo, f'{p.title}\nЦена: {p.actual_price}',
                            reply_markup=self.generate_products_kb(p.id, **kwargs))
