from django import forms

from app.models import *

class UserMF(forms.ModelForm):
    class Meta:
        model=User
        #fields="__all__"
        fields=['username']

class DishForm(forms.ModelForm):
    class Meta:
        model=Dish
        fields='__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields='__all__'
    