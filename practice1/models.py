from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from django.http.response import HttpResponse, HttpResponseBadRequest
from rest_framework.response import Response
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    address = models.TextField()
    landmark = models.TextField(default=None, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    times_rated = models.IntegerField(default=0)
    lat = models.DecimalField(default=None, null=True, max_digits=15, decimal_places=13)
    lng = models.DecimalField(default=0.0, null=True, max_digits=15, decimal_places=13)

    def __str__(self):
        return self.name

class Food_Item(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    price = models.IntegerField()

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, default="default@default.com")
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    raw_address = models.TextField(null=False)
    lat = models.DecimalField(null=False, max_digits=15, decimal_places=13)
    lng = models.DecimalField(null=False, max_digits=15, decimal_places=13)

    def __str__(self):
        return str(self.user.name)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=CASCADE)
    food_item = models.ForeignKey(Food_Item, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.user.name) + " " + str(self.food_item.name)

    def save(self, *args, **kwargs):
        if self.restaurant.id == self.food_item.restaurant.id:
            super().save(*args, **kwargs)
        else:
            return HttpResponseBadRequest("You should select food item of the same restaurant")

    class Meta:
        db_table = 'practice1_cart'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'food_item'],
                 name='unique user fooditem'
            )
        ]
        
# class Cart_Data(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     food_item = models.ForeignKey(Food_Item, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     name = models.CharField(max_length=30)
#     price = models.IntegerField()
    
#     class Meta:
#         db_table = 'practice1_cart_data'
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['cart', 'food_item'],
#                  name='unique appversion'
#             )
#         ]
    
#     def __str__(self):
#         return self.name

class Payment(models.Model):
    PAYMENT_CHOICES = (
        ('1', 'COD'),
        ('2', 'Debit/Credit'),
        ('3', 'UPI')
    )
    transaction_id = models.CharField(max_length=10, unique=True)
    payment_mode = models.CharField(max_length=1, choices=PAYMENT_CHOICES)
    payment_status = models.BooleanField(default=False)
    order_id = models.CharField(max_length=20, unique=True, null=True)
    user = models.ForeignKey(User, null=True, on_delete=PROTECT)
    restaurant = models.ForeignKey(Restaurant, null=True, on_delete=PROTECT)

    def __str__(self):
        return self.transaction_id

class Order(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    restaurant = models.ForeignKey(Restaurant, null=True, on_delete=PROTECT)
    city = models.ForeignKey(City, null=True, on_delete=PROTECT)
    payment = models.ForeignKey(Payment, null=True, on_delete=PROTECT)
    total_price = models.IntegerField()
    order_status = models.BooleanField(default=False)
    address = models.TextField(default="Just Deliver it")
    lat = models.DecimalField(default=0.0, max_digits=15, decimal_places=13)
    lng = models.DecimalField(default=0.0, max_digits=15, decimal_places=13)

    def __str__(self):
        return str(self.user.name)

class Order_Data(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return str(self.order)

class RatingsAndReview(models.Model):
    RATING_CHOICES = (
        (1, 'Worst'),
        (2, 'Poor'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent')
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    delivery_rating = models.IntegerField(choices=RATING_CHOICES)
    food_rating = models.IntegerField(choices=RATING_CHOICES)
    delivery_review = models.TextField(default="Not provided")
    food_review = models.TextField(default="Not provided")

    def __str__(self):
        return str(self.user.name) + " " + str(self.restaurant.name)