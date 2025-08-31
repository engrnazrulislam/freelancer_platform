from django.db import models
from django.contrib.auth.models import AbstractUser 
from users.managers import CustomUserManager
import uuid
# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    SELLER = 'Seller'
    BUYER = 'Buyer'
    ADMIN = 'Admin'
    ROLE_CHOICES = (
        (SELLER, 'Seller'),
        (BUYER, 'Buyer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email