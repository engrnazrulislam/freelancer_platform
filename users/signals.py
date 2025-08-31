from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()
# from users.models import User

@receiver(post_save, sender=User)
def assign_group(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'seller':
            group, _ = Group.objects.get_or_create(name='Seller')
            instance.groups.add(group)
        elif instance.role == 'buyer':
            group, _ = Group.objects.get_or_create(name='Buyer')
            instance.groups.add(group)