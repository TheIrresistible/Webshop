from flask import Flask
from flask_restful import Api
from .resources import UserResource, CategoryResource, ProductResource, OrderResource

app = Flask(__name__)
api = Api(app)

api.add_resource(UserResource, '/users', '/users/<user_id>')
api.add_resource(CategoryResource, '/categories', '/categories/<category_id>')
api.add_resource(ProductResource, '/products', '/products/<product_id>')
api.add_resource(OrderResource, '/orders', '/orders/<order_id>')