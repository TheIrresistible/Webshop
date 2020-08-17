from decimal import Decimal
from PIL import Image
import mongoengine as me


me.connect('webshop')


class Category(me.Document):
    title = me.StringField(min_length=2, max_length=512, required=True)
    description = me.StringField(min_length=8, max_length=2048)
    subcategories = me.ListField(me.ReferenceField('self'))
    parent = me.ReferenceField('self')

    def get_products(self):
        return Product.objects.filter(category=self)

    @classmethod
    def get_root_categories(cls):
        return cls.objects(parent=None)

    @classmethod
    def get_last_categories(cls):
        id_list = []
        for i in cls.objects(subcategories=[]):
            id_list.append(str(i.id))

        return id_list

    def add_subcategory(self, subcategory: 'Category'):
        subcategory.parent = self
        subcategory.save()

        self.subcategories.append(subcategory)
        self.save()

    def __str__(self):
        return self.title


class Parameter(me.EmbeddedDocument):
    height = me.FloatField()
    width = me.FloatField()
    weight = me.FloatField()
    length = me.FloatField()


class Product(me.Document):
    title = me.StringField(min_length=2, max_length=512, required=True)
    description = me.StringField(min_length=8, max_length=2048)
    in_stock = me.StringField(min_value=0, required=True)
    is_available = me.BooleanField(default=True)
    discount = me.IntField(min_value=0, max_value=100, default=0)
    price = me.DecimalField(min_value=1, force_string=True)
    image = me.ImageField()
    parameter = me.EmbeddedDocumentField(Parameter)
    category = me.ReferenceField(Category)

    @property
    def actual_price(self):
        return (self.price * Decimal((100 - self.discount) / 100)).quantize(Decimal('.01'), 'ROUND_HALF_UP')

    @classmethod
    def get_products_with_discount(cls):
        return cls.objects(discount__ne=0)

    def __str__(self):
        return self.title


class Text(me.Document):

    GREETINGS = 'greetings'
    DISCOUNT = 'discount'
    CATEGORIES = 'categories'
    TITLES_CONSTANTS = (
        (GREETINGS, 'greetings'),
        (DISCOUNT, 'discount'),
        (CATEGORIES, 'categories')
    )
    title = me.StringField(required=True, choices=TITLES_CONSTANTS, unique=True)
    body = me.StringField(min_length=4, max_length=4096)


class User(me.Document):
    user_id = me.IntField(required=True)
    first_name = me.StringField(required=True)
    last_name = me.StringField(required=True)
    username = me.StringField(required=True)
    language_code = me.StringField(required=True)
    phone_number = me.IntField()
    location = me.StringField()


class News(me.Document):
    title = me.StringField(min_length=2, max_length=512, required=True)
    body = me.StringField(min_length=8, max_length=2048, required=True)


if __name__ == '__main__':
    pass
    #News.objects.create(title='Скидки на этой неделе', body='Смотрите вкладку "Товары со скидкой"')
    #for i in Product.objects():
        #image = Image.open('charlie-ellis-planet.jpg')
       # i.image = image
