from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from .models import Restaurant, Dish

RATING_CHOICES = [(x, str(x) if x > 0 else "N/A") for x in range(0, 6)]


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Usernames must be at least 3 characters long
        self.fields["username"].validators += [MinLengthValidator(3)]

    email = forms.EmailField(help_text="Enter a valid email address.")

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

    def clean_email(self):

        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                _("An existing user with the specified email address already exists")
            )
        return email


class RestaurantCreationForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        exclude = ("slug",)
        widgets = {"rating": forms.Select(choices=RATING_CHOICES)}


class DishCreationForm(forms.ModelForm):
    class Meta:
        model = Dish
        exclude = ("restaurant",)
        widgets = {"rating": forms.Select(choices=RATING_CHOICES)}
