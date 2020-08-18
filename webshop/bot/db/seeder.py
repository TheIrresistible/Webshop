from .models import Text, News, Category


def seed_texts():

    greetings = {
        'title': 'greetings',
        'body': 'Здраствуй, дорогой пользователь. Рад тебя приветствовать в нашем машазине'
    }

    discount = {
        'title': 'discount',
        'body': 'Спеши! Эти товары со скидкой до конца недели.'
    }

    categories = {
        'title': 'categories',
        'body': 'Выберите категорию:'
    }

    Text.objects.create(**greetings)
    Text.objects.create(**discount)
    Text.objects.create(**categories)


def seed_news():
    News.objects.create(title='Скоро открытие', body='Открываеться новый магазин...')
    News.objects.create(title='Скидки на этой неделе', body='Смотрите вкладку "Товары со скидкой"')
    News.objects.create(title='Осторожно', body='В сети появились мошенники...')


def seed_categories():
    Category.objects.create(title='Ноутбуки')
    Category.objects.create(title='Видеокарты')
    Category.objects.create(title='Моноблоки')
    Category.objects.create(title='Смартфоны')
    Category.objects.create(title='Аксесуары')
    Category.objects.create(title='Наушники')
    for i in Category.objects(title='Компьютеры'):
        i.add_subcategory(Category.objects(title='Ноутбуки'))
        i.add_subcategory(Category.objects(title='Видеокарты'))
        i.add_subcategory(Category.objects(title='Моноблоки'))
    for i in Category.objects(title='Смартфоны'):
        i.add_subcategory(Category.objects(title='Смартфоны'))
        i.add_subcategory(Category.objects(title='Аксесуары'))
        i.add_subcategory(Category.objects(title='Наушники'))
