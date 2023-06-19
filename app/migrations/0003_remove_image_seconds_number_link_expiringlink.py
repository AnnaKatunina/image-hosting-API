# Generated by Django 4.2.2 on 2023-06-18 21:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_creating_initial_plans'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='seconds_number_link',
        ),
        migrations.CreateModel(
            name='ExpiringLink',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('number_of_seconds', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(300), django.core.validators.MaxValueValidator(30000)], verbose_name='Number of seconds')),
                ('link', models.ImageField(upload_to='expiring_links', verbose_name='Link')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expiring_links', to='app.image', verbose_name='Image')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
