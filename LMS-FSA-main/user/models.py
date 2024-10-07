from django.db import models
from role.models import Role
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from training_program.models import TrainingProgram

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Use Django's built-in password hashing
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    training_programs = models.ManyToManyField(TrainingProgram, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'  # This is the unique identifier for authentication
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
