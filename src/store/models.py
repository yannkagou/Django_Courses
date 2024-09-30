from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from django.contrib import admin

from .validators import validate_file_size

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)

    def __str__(self) -> str:
        return self.title   
    class Meta:
        ordering = ['title']

 
class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self) -> str:
        return self.title   
    
    class Meta:
        ordering = ['title']


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='store/images', validators=[validate_file_size])

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"   
    
    @admin.display(ordering="user__first_name")
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering="user__last_name")
    def last_name(self):
        return self.user.last_name


class Order(models.Model):
    PENDING = 'P'
    COMPLETE = 'C'
    FAILED = 'F'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETE, 'Complete'),
        (FAILED, 'Failed'),
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [['cart', 'product']]

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='addresses')
    

class Review(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")