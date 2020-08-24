from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from .schema import CategorySchema, ProductSchema, UserSchema, OrderSchema
from ..db.models import Category, Product, User, Order


class CategoryResource(Resource):

    def get(self, category_id=None):
        if category_id:
            obj = Product.objects.get(category=category_id)
            return ProductSchema().dump(obj)
        else:
            result = Category.objects
            return CategorySchema().dump(result, many=True)

    def post(self):
        try:
            res = CategorySchema().load(request.get_json())
            obj = Category.objects.create(**res)
            return CategorySchema().dump(obj)
        except ValidationError as err:
            return {'error': err.messages}

    def put(self, category_id):
        try:
            res = CategorySchema().load(request.get_json())
            obj = Category.objects.get(id=category_id)
            obj.update(**res)
            return CategorySchema().dump(obj.reload())
        except ValidationError as err:
            return {'error': err.messages}

    def delete(self, category_id):
        Category.objects(id=category_id).delete()
        return {'status': 'deleted'}


class UserResource(Resource):

    def get(self, user_id=None):
        if user_id:
            obj = Order.objects.get(customer=user_id)
            return OrderSchema().dump(obj)
        else:
            result = User.objects
            return UserSchema().dump(result, many=True)

    def post(self):
        try:
            res = UserSchema().load(request.get_json())
            obj = User.objects.create(**res)
            return UserSchema().dump(obj)
        except ValidationError as err:
            return {'error': err.messages}

    def put(self, user_id):
        try:
            res = UserSchema().load(request.get_json())
            obj = User.objects.get(id=user_id)
            obj.update(**res)
            return UserSchema().dump(obj.reload())
        except ValidationError as err:
            return {'error': err.messages}

    def delete(self, user_id):
        User.objects(id=user_id).delete()
        return {'status': 'deleted'}


class ProductResource(Resource):

    def get(self, product_id):
        if product_id:
            obj = Product.objects.get(id=product_id)
            return ProductSchema().dump(obj)
        else:
            result = Product.objects
            return ProductSchema().dump(result, many=True)

    def post(self):
        try:
            res = ProductSchema().load(request.get_json())
            obj = Product.objects.create(**res)
            return ProductSchema().dump(obj)
        except ValidationError as err:
            return {'error': err.messages}

    def put(self, product_id):
        try:
            res = ProductSchema().load(request.get_json())
            obj = Product.objects.get(id=product_id)
            obj.update(**res)
            return ProductSchema().dump(obj.reload())
        except ValidationError as err:
            return {'error': err.messages}

    def delete(self, product_id):
        Product.objects(id=product_id).delete()
        return {'status': 'deleted'}


class OrderResource(Resource):

    def get(self, order_id):
        if order_id:
            obj = Order.objects.get(id=order_id)
            return OrderSchema().dump(obj)
        else:
            result = Order.objects
            return OrderSchema().dump(result, many=True)

    def post(self):
        try:
            res = OrderSchema().load(request.get_json())
            obj = Order.objects.create(**res)
            return OrderSchema().dump(obj)
        except ValidationError as err:
            return {'error': err.messages}

    def put(self, order_id):
        try:
            res = OrderSchema().load(request.get_json())
            obj = Order.objects.get(id=order_id)
            obj.update(**res)
            return OrderSchema().dump(obj.reload())
        except ValidationError as err:
            return {'error': err.messages}

    def delete(self, order_id):
        Order.objects(id=order_id).delete()
        return {'status': 'deleted'}