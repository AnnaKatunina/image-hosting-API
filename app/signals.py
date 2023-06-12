from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from app.models import Account, Plan, Image
from app.tasks import create_image_versions


@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        basic_plan = Plan.objects.get(name='Basic')
        Account.objects.create(user=instance, plan=basic_plan)


@receiver(post_save, sender=Image)
def create_images_thumbnails(sender, instance, created, **kwargs):
    if created:
        create_image_versions.delay(instance.id)
