from django.dispatch import receiver
from django.db.models.signals import post_save
from api.models import User
from django.contrib.auth.models import Group


@receiver(post_save, sender=User)
def add_to_accounting_group(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        accounting_group, created = Group.objects.get_or_create(name='new_group')
        instance.groups.add(accounting_group)
