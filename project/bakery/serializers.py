from rest_framework import serializers
from .models import User, Ingredient, BakeryItem, BakeryItemIngredient, Order, OrderItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'is_admin', 'is_customer']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class BakeryItemIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = BakeryItemIngredient
        fields = '__all__'

class BakeryItemSerializer(serializers.ModelSerializer):
    ingredients = BakeryItemIngredientSerializer(many=True)

    class Meta:
        model = BakeryItem
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
