from django import forms
from django.contrib.auth.models import User

from app.models import Dish, Review


class UserMF(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()

        if not name:
            raise forms.ValidationError(
                'Please enter a dish name.'
            )

        return name

    def clean_description(self):
        description = self.cleaned_data.get(
            'description', ''
        ).strip()

        if not description:
            raise forms.ValidationError(
                'Please enter a dish description.'
            )

        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is None or price <= 0:
            raise forms.ValidationError(
                'The dish price must be greater than zero.'
            )

        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')

        # Allow an empty image if the model permits it.
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                'The image must be smaller than 5 MB.'
            )

        return image


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'step': 1,
                'required': True,
            }),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')

        if rating is None or rating < 1 or rating > 5:
            raise forms.ValidationError(
                'Rating must be between 1 and 5.'
            )

        return rating

    def clean_comment(self):
        comment = self.cleaned_data.get('comment', '').strip()

        if not comment:
            raise forms.ValidationError(
                'Please enter your review before submitting.'
            )

        return comment


class CheckoutForm(forms.Form):
    ORDER_TYPE_CHOICES = [
        ('DINE_IN', 'Dine in'),
        ('TAKEAWAY', 'Takeaway'),
        ('DELIVERY', 'Delivery'),
    ]

    customer_name = forms.CharField(
        max_length=100,
        label='Full name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name',
            'autocomplete': 'name',
        }),
        error_messages={
            'required': 'Please enter your name.',
            'max_length': 'Your name cannot exceed 100 characters.',
        },
    )

    phone = forms.RegexField(
        regex=r'^[6-9]\d{9}$',
        max_length=10,
        min_length=10,
        label='10-digit phone number',
        error_messages={
            'required': 'Please enter your phone number.',
            'invalid': (
                'Enter a valid 10-digit Indian mobile number '
                'starting with 6, 7, 8, or 9.'
            ),
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'inputmode': 'numeric',
            'autocomplete': 'tel',
            'maxlength': '10',
            'placeholder': 'Enter your 10-digit mobile number',
        }),
    )

    order_type = forms.ChoiceField(
        choices=ORDER_TYPE_CHOICES,
        label='Order type',
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        error_messages={
            'required': 'Please select an order type.',
            'invalid_choice': 'Please select a valid order type.',
        },
    )

    delivery_address = forms.CharField(
        required=False,
        max_length=500,
        label='Delivery address',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'maxlength': '500',
            'placeholder': 'Enter your complete delivery address',
        }),
    )

    def clean_customer_name(self):
        name = self.cleaned_data.get(
            'customer_name', ''
        ).strip()

        if not name:
            raise forms.ValidationError(
                'Your name cannot contain only spaces.'
            )

        return name

    def clean_delivery_address(self):
        address = self.cleaned_data.get(
            'delivery_address', ''
        ).strip()

        return address

    def clean(self):
        cleaned_data = super().clean()

        order_type = cleaned_data.get('order_type')
        address = cleaned_data.get('delivery_address', '')

        if order_type == 'DELIVERY' and not address:
            self.add_error(
                'delivery_address',
                'A delivery address is required for delivery orders.'
            )

        return cleaned_data
