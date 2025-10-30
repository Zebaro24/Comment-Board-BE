import os
import uuid

from PIL import Image
from django.core.files.base import ContentFile
import io

def resize_image_if_needed(file_obj):
    image = Image.open(file_obj)
    max_w, max_h = 320, 240
    if image.width > max_w or image.height > max_h:
        image.thumbnail((max_w, max_h))
        buf = io.BytesIO()
        image.save(buf, format=image.format)
        return ContentFile(buf.getvalue(), name=file_obj.name)
    return file_obj

def get_file_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    return os.path.join('uploads', unique_name)