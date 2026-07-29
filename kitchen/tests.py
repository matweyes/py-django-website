from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from kitchen.forms import (
    CookCreationForm,
    DishForm,
    CookExperienceUpdateForm,
    CookSearchForm,
    DishSearchForm,
    DishTypeSearchForm,
    validate_years_of_experience,
)
from kitchen.models import DishType, Cook, Dish


DISH_TYPE_FORMAT_URL = reverse("kitchen:dish-type-list")
HOME_FORMAT_URL = reverse("kitchen:index")
COOK_FORMAT_URL = reverse("kitchen:cook-list")
DISH_FORMAT_URL = reverse("kitchen:dish-list")


class ModelsTests(TestCase):
    def test_dish_type_str(self):
        dish_type = DishType.objects.create(name="Appetizer")
        self.assertEqual(str(dish_type), dish_type.name)

    def test_cook_str(self):
        cook = Cook.objects.create(
            username="test",
            first_name="John",
            last_name="Doe",
        )
        self.assertEqual(
            str(cook),
            f"{cook.username} "
            f"({cook.first_name} {cook.last_name})"
        )

    def test_dish_str(self):
        dish_type = DishType.objects.create(name="Main Course")
        dish = Dish.objects.create(
            name="Pasta",
            description="Delicious pasta",
            price=12.99,
            dish_type=dish_type,
        )
        self.assertEqual(str(dish), dish.name)


class PublicAccessibilityTest(TestCase):
    def test_login_required(self):
        links = [
            DISH_TYPE_FORMAT_URL,
            HOME_FORMAT_URL,
            COOK_FORMAT_URL,
            DISH_FORMAT_URL,
        ]
        for value in links:
            res = self.client.get(value)
            self.assertNotEqual(res.status_code, 200)


class PrivateAccessibilityTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345",
        )
        self.client.force_login(self.user)

    def test_accessibility_logged_user(self):
        links = [
            DISH_TYPE_FORMAT_URL,
            HOME_FORMAT_URL,
            COOK_FORMAT_URL,
            DISH_FORMAT_URL,
        ]
        for value in links:
            response = self.client.get(value)
            self.assertEqual(response.status_code, 200)

    def test_retrieve_dish_types(self):
        DishType.objects.create(name="Appetizer")
        DishType.objects.create(name="Main Course")
        response = self.client.get(DISH_TYPE_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        dish_types = DishType.objects.all()
        self.assertEqual(
            list(response.context["dish_type_list"]),
            list(dish_types)
        )
        self.assertTemplateUsed(
            response,
            "kitchen/dish_type_list.html"
        )


class DishFormTest(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(
            name="Main Course"
        )
        self.cook1 = get_user_model().objects.create_user(
            username="cook1",
            password="password123",
            years_of_experience=5,
        )
        self.cook2 = get_user_model().objects.create_user(
            username="cook2",
            password="password123",
            years_of_experience=3,
        )

    def test_dish_form_valid(self):
        form_data = {
            "name": "Pasta Carbonara",
            "description": "Classic Italian pasta",
            "price": 15.99,
            "dish_type": self.dish_type.id,
            "cooks": [self.cook1.id, self.cook2.id],
        }
        form = DishForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_dish_form_invalid_no_cooks(self):
        form_data = {
            "name": "Pasta Carbonara",
            "description": "Classic Italian pasta",
            "price": 15.99,
            "dish_type": self.dish_type.id,
        }
        form = DishForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("cooks", form.errors)


class CookCreationFormTest(TestCase):
    def test_cook_creation_form_valid(self):
        form_data = {
            "username": "newcook",
            "password1": "securepassword123",
            "password2": "securepassword123",
            "years_of_experience": 5,
            "first_name": "John",
            "last_name": "Doe",
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_cook_creation_form_invalid_experience(self):
        form_data = {
            "username": "newcook",
            "password1": "securepassword123",
            "password2": "securepassword123",
            "years_of_experience": -1,
            "first_name": "John",
            "last_name": "Doe",
        }
        form = CookCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)


class CookExperienceUpdateFormTest(TestCase):
    def test_experience_update_form_valid(self):
        form_data = {"years_of_experience": 10}
        form = CookExperienceUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_experience_update_form_invalid(self):
        form_data = {"years_of_experience": -5}
        form = CookExperienceUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)


class CookSearchFormTest(TestCase):
    def test_cook_search_form_valid(self):
        form_data = {"username": "testuser"}
        form = CookSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_cook_search_form_empty(self):
        form_data = {"username": ""}
        form = CookSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class DishSearchFormTest(TestCase):
    def test_dish_search_form_valid(self):
        form_data = {"name": "Pasta"}
        form = DishSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_dish_search_form_empty(self):
        form_data = {"name": ""}
        form = DishSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class DishTypeSearchFormTest(TestCase):
    def test_dish_type_search_form_valid(self):
        form_data = {"name": "Appetizer"}
        form = DishTypeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_dish_type_search_form_empty(self):
        form_data = {"name": ""}
        form = DishTypeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class ValidateYearsOfExperienceTest(TestCase):
    def test_valid_years(self):
        self.assertEqual(validate_years_of_experience(5), 5)

    def test_zero_years(self):
        self.assertEqual(validate_years_of_experience(0), 0)

    def test_negative_years(self):
        with self.assertRaises(ValidationError):
            validate_years_of_experience(-1)

    def test_exceeding_years(self):
        with self.assertRaises(ValidationError):
            validate_years_of_experience(81)
