from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .forms import CreateUserForm, UpdateUserForm


class MyUserAdmin(UserAdmin):
    add_form = CreateUserForm
    form = UpdateUserForm
    model = User
    list_display = ['email', 'username', 'avatar', 'created', 'karma', 'about', 'verified']
    fieldsets = (
        (None, {"fields": ("password",)}),
        ("Personal info", {"fields": ("username", "email", "karma", "about")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "created")}),
    )
    # fieldsets = UserAdmin.fieldsets
    # exclude = ["last_name", "first_name", "date_joined"]
    # fieldsets = [
    #     (None, {"fields": ["email", 'username', 'verified', "password"]}),
    #     ("Personal info", {"fields": ["about"]}),
    #     ("Permissions", {"fields": ['user_permissions']})
    # ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "username", "password1", "password2", 'about', 'verified', 'avatar', 'is_staff'],
            },
        ),
    ]
    search_fields = ["email", 'username']
    ordering = ["created"]
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


admin.site.register(User, MyUserAdmin)
