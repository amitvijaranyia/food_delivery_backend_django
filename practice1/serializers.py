from django.db import models
from django.db.models import fields
from rest_framework import serializers
from practice1.models import *

class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'

class RestaurantByCitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    # food_item = FoodItemSerializer()
    class Meta:
        model = Restaurant
        fields = '__all__'

class FoodItemSerializer(serializers.ModelSerializer):
    # restaurant = RestaurantSerializer()
    class Meta:
        model = Food_Item
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # restaurant = RestaurantSerializer()
    # food_item = FoodItemSerializer()
    class Meta:
        model = Cart
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Data
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__al__'

class RatingsAndReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingsAndReview
        fields = '__all__'