from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from kitchen.models import Dish, Cook


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Dish
        fields = "__all__"


def validate_years_of_experience(years_of_experience):
    if not isinstance(years_of_experience, int):
        raise ValidationError(
            "Years of experience should be an integer"
        )
    if years_of_experience < 0:
        raise ValidationError(
            "Years of experience cannot be negative"
        )
    if years_of_experience > 80:
        raise ValidationError(
            "Years of experience cannot exceed 80"
        )
    return years_of_experience


class YearsOfExperienceValidationMixin:
    def clean_years_of_experience(self):
        return validate_years_of_experience(
            self.cleaned_data["years_of_experience"]
        )


class CookCreationForm(YearsOfExperienceValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name",
        )


class CookExperienceUpdateForm(YearsOfExperienceValidationMixin, forms.ModelForm):
    class Meta:
        model = Cook
        fields = ["years_of_experience"]


def _build_search_form(field_name, placeholder):
    return type(
        f"{field_name.capitalize()}SearchForm",
        (forms.Form,),
        {
            field_name: forms.CharField(
                max_length=255,
                required=False,
                label="",
                widget=forms.TextInput(
                    attrs={"placeholder": placeholder}
                ),
            )
        },
    )


CookSearchForm = _build_search_form("username", "Search by username")
DishSearchForm = _build_search_form("name", "Search by name")
DishTypeSearchForm = _build_search_form("name", "Search by name")
