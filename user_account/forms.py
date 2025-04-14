from django.contrib.auth.forms import UserCreationForm, UserChangeForm, BaseUserCreationForm

from .models import User


class CreateUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "username", "password1", "password2")


class UpdateUserForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ("username", "about", "avatar", "profile_picture")
        exclude = ["last_name", "first_name", "date_joined"]
