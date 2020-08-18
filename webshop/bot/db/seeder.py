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
    Category.objects.create(title='Смартфоны')
    sub = Category.objects.get(title='Наушники')
    for c in Category.objects(title='Смартфоны'):
        c.add_subcategory(sub)
