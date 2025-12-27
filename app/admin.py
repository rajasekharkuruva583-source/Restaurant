from django.contrib import admin

# Register your models here.
from app.models import *

admin.site.register(Dish)
admin.site.register(Review)
