from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import uuid


class Dish(models.Model):
    CATEGORY_CHOICES = [
        ('BREAKFAST', 'Breakfast'),
        ('VEG', 'Vegetarian'),
        ('NON_VEG', 'Non-Vegetarian'),
        ('STARTERS', 'Starters'),
        ('ICE_CREAM', 'Ice_cream'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    category = models.CharField(
        max_length=10, choices=CATEGORY_CHOICES, default='VEG'
    )
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE, related_name='reviews'
    )
    user_name = models.CharField(max_length=100, null=True, blank=True)
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user_name} - {self.dish.name} ({self.rating}/5)"


class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('DINE_IN', 'Dine in'),
        ('TAKEAWAY', 'Takeaway'),
        ('DELIVERY', 'Delivery'),
    ]
    STATUS_CHOICES = [
        ('PLACED', 'Placed'),
        ('PREPARING', 'Preparing'),
        ('READY', 'Ready'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    order_number = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False
    )
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES)
    delivery_address = models.TextField(blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default='PLACED'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items'
    )
    # Keep a reference when possible, but preserve the purchased item details
    # even if the original dish is later deleted or renamed.
    dish = models.ForeignKey(
        Dish, on_delete=models.SET_NULL, null=True, blank=True
    )
    dish_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.dish_name} x {self.quantity}"
