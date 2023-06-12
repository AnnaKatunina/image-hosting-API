import uuid

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from app.tasks import create_image_versions


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Thumbnail(TimeStampedMixin, UUIDMixin):
    height = models.PositiveIntegerField()

    def __str__(self):
        return f'Thumbnail size {self.height}'


class Plan(TimeStampedMixin, UUIDMixin):
    name = models.CharField('Name', max_length=32)
    description = models.TextField('Description', null=True, blank=True)
    is_original_size = models.BooleanField('Presence of the link to the original image', default=False)
    is_expiring_link = models.BooleanField('Ability to generate expiring links', default=False)
    thumbnails = models.ManyToManyField(Thumbnail, verbose_name='Thumbnails', related_name='plans')

    def __str__(self):
        return self.name


class Account(TimeStampedMixin, UUIDMixin):
    user = models.OneToOneField(User, verbose_name='User', on_delete=models.CASCADE, related_name='account')
    plan = models.ForeignKey(Plan, verbose_name='Plan', on_delete=models.CASCADE, related_name='accounts')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        images = self.images.all()
        for image in images:
            create_image_versions.delay(image.id)

    def __str__(self):
        return self.user.username


class Image(TimeStampedMixin, UUIDMixin):
    account = models.ForeignKey(Account, verbose_name='Account', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Image', upload_to='images')
    seconds_number_link = models.PositiveIntegerField('Number of seconds',
                                                      validators=[MinValueValidator(300), MaxValueValidator(30000)],
                                                      null=True, blank=True)


class ImageVersion(TimeStampedMixin, UUIDMixin):
    image = models.ForeignKey(Image, verbose_name='Image', on_delete=models.CASCADE, related_name='versions')
    thumbnail_name = models.CharField('Name', max_length=32)
    thumbnail_link = models.ImageField('Image version', upload_to='images')

    def __str__(self):
        return self.thumbnail_name
