
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from .constant import TIMEZONES, USER_TYPES, DAY_OF_WEEK, REPEAT_MODE
from django.db import models
from multiselectfield import MultiSelectField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=50, blank=True)
    time_zone = models.CharField(max_length=100, blank=True, null=True, choices=TIMEZONES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_type = models.CharField(max_length=100, blank=True, null=True, choices=USER_TYPES)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email


class Calendar(models.Model):
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)

    repeat_mode = models.CharField(max_length=10, choices=REPEAT_MODE, blank=True,default='Daily')

    start_time = models.DateTimeField(blank=True)
    end_time = models.DateTimeField(blank=True)

    #days_of_week = MultiSelectField(choices=DAY_OF_WEEK,max_length=100,blank=True)

    def __str__(self):
        return f"{self.title} - {self.start_time}"
