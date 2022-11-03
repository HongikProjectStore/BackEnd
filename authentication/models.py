from email.policy import default
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager

GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=128, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    gender = models.CharField(max_length=1, blank=True, choices=GENDER)
    birth = models.DateField(max_length=128, blank=True)
    image = models.ImageField(upload_to='profile/', default='default_user.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email