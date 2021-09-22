from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, firstname, password, **other_fields):

        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, firstname, password, **other_fields)

    def create_user(self, email, username, firstname, password, **other_fields):

        if not email:
            raise ValueError(('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          firstname=firstname, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(('email address'), unique=True)
    firstname = models.CharField(max_length=150, blank=True, null=True)
    Joined_date = models.DateTimeField(auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(('is a superuser'), default=False)
    Mail_opt_in = models.BooleanField(
        ('News Email subscription'), default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'firstname']
    objects = CustomAccountManager()

    # def get_absolute_url(self):
    #     return reverse("users:detail", kwargs={"username": self.username})

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)



