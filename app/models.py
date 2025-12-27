from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.utils import timezone


class Dish(models.Model):
    CATEGORY_CHOICES = [
        ('BREAKFAST','Breakfast'),
        ('VEG', 'Vegetarian'),
        ('NON_VEG', 'Non-Vegetarian'),
        ('STARTERS','Starters'), 
        ('ICE_CREAM','Ice_cream')
    ]

    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='VEG')
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return self.name



class Review(models.Model):
    #customer = models.ForeignKey(User, on_delete=models.CASCADE)
    dish=models.ForeignKey(Dish, on_delete=models.CASCADE,related_name='reviews')
    user_name=models.CharField(max_length=100,null=True,blank=True)
    rating= models.PositiveIntegerField(default=5)
    comment=models.TextField()
    created_at = models.DateField(default=timezone.now)

   
    
    def __str__(self):
        return f"{self.user_name} - {self.dish.name} ({self.rating}/5)"




    # def __str__(self):
    #     return f"{self.customer.username} - {self.dish.name} ({self.rating})"


