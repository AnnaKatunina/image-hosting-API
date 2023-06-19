from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from app.models import Account, Image, ExpiringLink
from app.tasks import create_image_versions, delete_expired_link


@receiver(post_save, sender=Image)
def create_images_thumbnails(sender, instance, created, **kwargs):
    if created:
        create_image_versions.delay(instance.id)


@receiver(pre_save, sender=Account)
def create_images_thumbnails_change_plan(sender, instance, **kwargs):
    try:
        previous_plan = Account.objects.get(pk=instance.pk).plan
        new_plan = instance.plan
        if previous_plan != new_plan:
            images = instance.images.all()
            for image in images:
                create_image_versions.delay(image.id)
    except Account.DoesNotExist:
        pass


@receiver(post_save, sender=ExpiringLink)
def delete_expired_image_link(sender, instance, created, **kwargs):
    if created:
        delete_expired_link.apply_async(args=(instance.id,), countdown=instance.number_of_seconds)
