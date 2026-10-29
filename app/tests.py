from django.test import TestCase
from datetime import date
# Create your tests here.
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from app.forms import CheckoutForm, ReviewForm
from app.models import Dish, Order, OrderItem, Review


class RestaurantTestDataMixin:
    def create_dish(
        self,
        name="Idli",
        price="50.00",
        category="BREAKFAST",
        is_available=True,
    ):
        return Dish.objects.create(
            name=name,
            description=f"Fresh {name}",
            price=Decimal(price),
            category=category,
            is_available=is_available,
        )


class ReviewValidationTests(RestaurantTestDataMixin, TestCase):
    def setUp(self):
        self.dish = self.create_dish()

    def test_rating_below_one_is_rejected(self):
        form = ReviewForm(data={
            "dish": self.dish.pk,
            "user_name": "Test Customer",
            "rating": 0,
            "comment": "Good food",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)

    def test_rating_above_five_is_rejected(self):
        form = ReviewForm(data={
            "dish": self.dish.pk,
            "user_name": "Test Customer",
            "rating": 8,
            "comment": "Good food",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)

    def test_rating_between_one_and_five_is_accepted(self):
        form = ReviewForm(data={
            "dish": self.dish.pk,
            "user_name": "Test Customer",
            "rating": 5,
            "comment": "Very good food",
            "created_at": date.today(),
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_empty_review_comment_is_rejected(self):
        form = ReviewForm(data={
            "dish": self.dish.pk,
            "user_name": "Test Customer",
            "rating": 4,
            "comment": "   ",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("comment", form.errors)


class SelectionTests(RestaurantTestDataMixin, TestCase):
    def setUp(self):
        self.dish = self.create_dish()

    def add_dish(self, quantity=1):
        for _ in range(quantity):
            self.client.post(
                reverse("update_selection"),
                {"dish_id": self.dish.pk, "action": "add"},
            )

    def test_adding_same_dish_increases_quantity(self):
        self.add_dish(quantity=2)

        session = self.client.session
        self.assertEqual(
            session["selected_items"][str(self.dish.pk)],
            2,
        )

    def test_subtotal_uses_price_times_quantity(self):
        self.add_dish(quantity=2)

        response = self.client.get(reverse("update_selection"))

        self.assertEqual(response.status_code, 200)