from telebot import types
from datetime import datetime
from .config import TOKEN, DEFAULT
from .lookups import SEPARATOR, PRODUCT_LOOKUP, CATEGORY_LOOKUP, FINISH_LOOKUP, DELETE_LOOKUP
from .keyboards import START_KB, FINISH, DELETE
from .db.models import Category, Product, Text, News, Cart, User, Order
from .service import WebShopBot

API_TOKEN = TOKEN

bot_instance = WebShopBot(API_TOKEN)


@bot_instance.callback_query_handler(func=lambda query: query.data.startswith(CATEGORY_LOOKUP))
def get_products_or_subcategory(query):
    id_ = query.data.split(SEPARATOR)[1]
    category = Category.objects(id=id_)
    txt = Text.objects.get(title=Text.CATEGORIES).body
    for c in category:
        if c.subcategories:
            bot_instance.generate_and_edit_categories_kb(query.message.chat.id,
                                                         txt,
                                                         query.message.message_id,
                                                         c.subcategories)

        else:
            bot_instance.generate_and_send_products_kb(query.message.chat.id, DEFAULT, Product.objects(category=id_))


@bot_instance.callback_query_handler(func=lambda query: query.data.startswith(PRODUCT_LOOKUP))
def add_product_to_cart(query):
    product_id = query.data.split(SEPARATOR)[1]
    id_list = []
    for u in User.objects():
        id_list.append(u.user_id)

    if query.from_user.id not in id_list:

        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        button_phone = types.KeyboardButton(text='Поделитесь вашим контактом', request_contact=True)
        keyboard.add(button_phone)
        bot_instance.send_message(query.message.chat.id, 'Для продолжения покупок поделитесь вашим контактом',
                                  reply_markup=keyboard)
        User.objects.create(user_id=query.from_user.id,
                            first_name=query.from_user.first_name,
                            username=query.from_user.username,
                            language_code=query.from_user.language_code,
                            phone_number=query.message.contact)

    cart_list = []

    for u in User.objects(user_id=query.from_user.id):
        for c in Cart.objects(customer=u):
            cart_list.append(c.customer)
        if u not in cart_list:
            Cart.objects.create(customer=u)

        for c in Cart.objects(customer=u):
            for p in Product.objects(id=product_id):
                c.add_to_cart(p)

    txt = Text.objects.get(title=Text.ADD).body
    bot_instance.send_message(query.message.chat.id, txt)


@bot_instance.callback_query_handler(func=lambda query: query.data.startswith(DELETE_LOOKUP))
def clear_cart(query):
    txt = Text.objects.get(title=Text.CLEAR).body
    for user in User.objects(user_id=query.from_user.id):
        for cart in Cart.objects(customer=user):
            cart.delete()
            bot_instance.send_message(query.message.chat.id, txt)


@bot_instance.callback_query_handler(func=lambda query: query.data.startswith(FINISH_LOOKUP))
def finish_work(query):
    txt = Text.objects.get(title=Text.FINISH).body
    for user in User.objects(user_id=query.from_user.id):
        for cart in Cart.objects(customer=user):
            Order.objects.create(customer=cart.customer, products=cart.products, date=datetime.today())
            cart.delete()

    bot_instance.send_message(query.message.chat.id, txt)


@bot_instance.message_handler(commands=['help', 'start'])
def send_welcome(message):
    chat_id = message.chat.id
    txt = Text.objects.get(title=Text.GREETINGS).body
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(button) for button in START_KB.values()]
    keyboard.add(*buttons)
    bot_instance.send_message(chat_id, txt, reply_markup=keyboard)


@bot_instance.message_handler(content_types=['text'], func=lambda m: m.text == START_KB['categories'])
def show_root_categories(message):
    txt = Text.objects.get(title=Text.CATEGORIES).body
    categories = Category.get_root_categories()
    bot_instance.generate_and_send_categories_kb(txt, message.chat.id, categories)


@bot_instance.message_handler(content_types=['text'], func=lambda m: m.text == START_KB['discount'])
def get_discount_products(message):
    chat_id = message.chat.id
    txt = Text.objects.get(title=Text.DISCOUNT).body
    bot_instance.generate_and_send_products_kb(chat_id, DEFAULT, Product.get_products_with_discount())
    bot_instance.send_message(chat_id, txt)


@bot_instance.message_handler(content_types=['text'], func=lambda m: m.text == START_KB['news'])
def show_latest_news(message):
    list_of_obj = []
    for position in News.objects:
        list_of_obj.append((position.title, position.body))

    bot_instance.send_message(message.chat.id, f'{list_of_obj[-1][0]}\n{list_of_obj[-1][1]}')
    bot_instance.send_message(message.chat.id, f'{list_of_obj[-2][0]}\n{list_of_obj[-2][1]}')
    bot_instance.send_message(message.chat.id, f'{list_of_obj[-3][0]}\n{list_of_obj[-3][1]}')


@bot_instance.message_handler(content_types=['text'], func=lambda m: m.text == START_KB['cart'])
def show_cart(message):
    list_of_products = []
    summa = 0
    kb = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text=f'{FINISH}',
                                         callback_data=f'{FINISH_LOOKUP}{SEPARATOR}{message.from_user.id}')

    button2 = types.InlineKeyboardButton(text=f'{DELETE}',
                                         callback_data=f'{DELETE_LOOKUP}{SEPARATOR}{message.from_user.id}')
    kb.add(button2)
    kb.add(button1)

    for u in User.objects(user_id=message.from_user.id):
        for c in Cart.objects(customer=u):
            for product in c.products:
                list_of_products.append(product.id)

    for product in list_of_products:
        for p in Product.objects(id=product):
            bot_instance.send_message(message.chat.id, f'{p.title}: {p.actual_price}')
            summa = summa + p.actual_price

    bot_instance.send_message(message.chat.id, f'Общая сумма: {summa}', reply_markup=kb)


@bot_instance.message_handler(content_types=['text'], func=lambda m: m.text == START_KB['history'])
def history_of_orders(message):
    list_of_products = []
    summa = 0
    for u in User.objects(user_id=message.from_user.id):
        for order in Order.objects(customer=u):
            for product in order.products:
                list_of_products.append(product.id)

            for product in list_of_products:
                for p in Product.objects(id=product):
                    summa = summa + p.actual_price

            bot_instance.send_message(message.chat.id, f'Заказ {order.id}\n'
                                                       f'Время: {order.date}\n'
                                                       f'Общая сумма: {summa}')


