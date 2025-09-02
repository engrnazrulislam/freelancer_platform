from django.db import models
from uuid import uuid4
from services.models import Service
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer_orders")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="service_orders")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller_orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Order {self.id} - {self.service.title} ({self.status})"


