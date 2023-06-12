from celery import shared_task

from django.apps import apps

from app.utils import make_thumbnail


@shared_task
def create_image_versions(image_id):
    image = apps.get_model('app', 'Image').objects.get(id=image_id)
    image_link = image.image
    thumbnails = image.account.plan.thumbnails.all()
    for thumbnail in thumbnails:
        if not apps.get_model('app', 'ImageVersion').objects.filter(image=image,
                                                                    thumbnail_name=str(thumbnail.height)).exists():
            link = make_thumbnail(image_link, thumbnail.height)
            apps.get_model('app', 'ImageVersion').objects.create(
                image=image,
                thumbnail_name=str(thumbnail.height),
                thumbnail_link=link
            )
