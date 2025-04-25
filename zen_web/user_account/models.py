"""
Custom User Authentication Model.
Customising the User model in Django to use email as the primary identifier.
User Authentication in Django docs
https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
"""
from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now


class UserManager(BaseUserManager):
    def create_user(self, *, email: str, username: str, password: str = None, **kwargs):
        user = self.model(email=self.normalize_email(email), username=username, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *, email: str, username: str, password: str = None):
        self.create_user(email=email, username=username, password=password, verified=True,
                         is_superuser=True, is_staff=True)


# AbstractBaseUser is a class that provides the core implementation of a User model.
# PermissionsMixin is a class that provides the core implementation of permissions in Django.
# Simpler customizations can be made by Subclassing AbstractUser Instead
# But for more complex customizations, Subclassing AbstractBaseUser and PermissionsMixin is recommended
# PermissionsMixin adds is_superuser, groups, and user_permissions fields
# AbstractBaseUser adds last_login and password fields, is_active is a property not a field
# is_staff needed to work with Django's authentication system and admin, it is defined in AbstractUser
# is_active is also defined in AbstractUser and works with the authentication and admin system
class User(AbstractBaseUser, PermissionsMixin):
    # email not suitable for primary key when using allauth
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True, primary_key=True)
    avatar = models.URLField(default="https://www.gravatar.com/avatar/", blank=True)
    created = models.DateTimeField(default=now)
    karma = models.IntegerField(default=0, blank=True)
    about = models.TextField(default="", blank=True)
    verified = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True, default=now)
    profile_picture = models.ImageField(upload_to="images/", blank=True, null=True) # pip install pillow
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ('username', )

    objects = UserManager()

    def __str__(self):
        return str(self.username)

    class Meta(AbstractBaseUser.Meta):
        unique_together = ('email', 'username')
        db_table = 'user'
