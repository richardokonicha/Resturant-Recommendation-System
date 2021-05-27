from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Usernames must be at least 3 characters long
        self.fields["username"].validators += [MinLengthValidator(3)]

    email = forms.EmailField(help_text="Enter a valid email address.")

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
