import os

from celery import shared_task

from app.models import Image, ImageVersion, ExpiringLink
from app.utils import make_thumbnail


@shared_task
def create_image_versions(image_id):
    image = Image.objects.get(id=image_id)
    image_link = image.image
    thumbnails = image.account.plan.thumbnails.all()
    for thumbnail in thumbnails:
        if not ImageVersion.objects.filter(image=image, thumbnail=thumbnail).exists():
            link = make_thumbnail(image_link, thumbnail.height)
            ImageVersion.objects.create(
                image=image,
                thumbnail=thumbnail,
                thumbnail_link=link
            )


@shared_task
def delete_expired_link(expiring_link_id):
    try:
        expired_link = ExpiringLink.objects.get(id=expiring_link_id)
        os.remove(expired_link.link.path)
        expired_link.delete()
    except ExpiringLink.DoesNotExist:
        pass
