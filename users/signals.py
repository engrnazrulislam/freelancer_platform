from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()
# from users.models import User

@receiver(post_save, sender=User)
def assign_group(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'Seller':
            try:
                group = Group.objects.get(name='Seller')
                instance.groups.add(group)
            except Group.DoesNotExist:
                raise ValueError("Seller Group Does Not Exist")
        elif instance.role == 'Buyer':
            try:
                group = Group.objects.get(name='Buyer')
                instance.groups.add(group)
            except Group.DoesNotExist:
                raise ValueError("Buyer Group Does Not Exist")