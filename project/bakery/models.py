from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User Model
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

# Ingredient Model
class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    quantity_in_stock = models.FloatField()  # Quantity in kilograms or liters
    cost_price_per_unit = models.FloatField()

    def __str__(self):
        return self.name

# Bakery Item Model
class BakeryItem(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ingredients = models.ManyToManyField(Ingredient, through='BakeryItemIngredient')
    cost_price = models.FloatField()
    selling_price = models.FloatField()

    def __str__(self):
        return self.name

class BakeryItemIngredient(models.Model):
    bakery_item = models.ForeignKey(BakeryItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    percentage_quantity = models.FloatField()  # Percentage of total quantity

# Order Model
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_customer': True})
    bakery_items = models.ManyToManyField(BakeryItem, through='OrderItem')
    total_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    bakery_item = models.ForeignKey(BakeryItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
