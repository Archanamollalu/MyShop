from rest_framework import serializers
from .models import *

class User_detailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
class Orders_detailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders_detail
        fields = '__all__'
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'