from io import BytesIO
from django.core.files import File
from PIL import Image


def make_thumbnail(image, height):
    with Image.open(image) as im:
        im.convert('RGB')
        size = (height, height)
        im.thumbnail(size)
        thumb_io = BytesIO()
        im.save(thumb_io, im.format, quality=85)
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail
