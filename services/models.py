from django.db import models
from uuid import uuid4
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from services.validators import validate_file_size
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
User = get_user_model()
# Create your models here

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    
class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_services")
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_services', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivery_time = models.PositiveIntegerField(help_text='Delivery Times in Days')
    is_active = models.BooleanField(default=True) 

    class Meta:
            ordering = ['-id',]

    def __str__(self):
        return self.title
    
# Model for Product Image
class ServiceImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')
    # image = models.ImageField(upload_to="products/images/",validators=[validate_file_size])
    image = CloudinaryField('image')

class ServiceReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_reviews')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer} -> {self.service} ({self.rating})"