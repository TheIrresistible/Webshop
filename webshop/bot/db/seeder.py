from .models import Text, News, Category, Product


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
    Category.objects.create(title='Компьютеры')
    Category.objects.create(title='Смартфоны')
    sub = Category.objects.get(title='Аксесуары')
    sub2 = Category.objects.get(title='Наушники')
    for c in Category.objects(title='Смартфоны'):
        c.add_subcategory(sub)
        c.add_subcategory(sub2)


def seed_products():

    '''
    product1 = {
        'title': 'IPhone',
        'in_stock': 'yes',
        'is_available': True,
        'price': 2000,
    }

    product2 = {
        'title': 'Lenovo',
        'in_stock': 'yes',
        'is_available': True,
        'price': 1500,
    }

    product3 = {
        'title': 'Galaxy Buds',
        'in_stock': 'yes',
        'is_available': True,
        'price': 1000,
    }

    Product.objects.create(**product1)
    Product.objects.create(**product2)
    Product.objects.create(**product3)
    '''

    for c in Category.objects(title='Аксесуары'):
        for p in Product.objects(title='IPhone'):
            p.category = c
            p.discount = 10
            p.save()

    for c in Category.objects(title='Компьютеры'):
        for p in Product.objects(title='Lenovo'):
            p.category = c
            p.discount = 10
            p.save()

    for c in Category.objects(title='Наушники'):
        for p in Product.objects(title='Galaxy Buds'):
            p.category = c
            p.discount = 10
            p.save()

