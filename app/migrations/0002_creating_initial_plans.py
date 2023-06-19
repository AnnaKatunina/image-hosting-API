from django.db import migrations

from app.models import Thumbnail, Plan


def create_initial_plans(apps, schema_editor):
    thumbnail_200 = Thumbnail.objects.create(height=200)
    thumbnail_400 = Thumbnail.objects.create(height=400)
    plan_basic = Plan.objects.create(
        name='Basic',
        description="A link to a thumbnail that's 200px in height",
    )
    plan_basic.thumbnails.add(thumbnail_200)
    plan_premium = Plan.objects.create(
        name='Premium',
        description="""A link to a thumbnail that's 200px in height
       A link to a thumbnail that's 400px in height
       A link to the originally uploaded image""",
        is_presence_original_image=True
    )
    plan_premium.thumbnails.add(thumbnail_200)
    plan_premium.thumbnails.add(thumbnail_400)
    plan_enterprise = Plan.objects.create(
        name='Enterprise',
        description="""A link to a thumbnail that's 200px in height
       A link to a thumbnail that's 400px in height
       A link to the originally uploaded image
       Ability to fetch a link for a previously uploaded image that expires after a number of seconds (user can specify any number between 300 and 30000)""",
        is_presence_original_image=True,
        is_expiring_link=True
    )
    plan_enterprise.thumbnails.add(thumbnail_200)
    plan_enterprise.thumbnails.add(thumbnail_400)


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_plans),
    ]
