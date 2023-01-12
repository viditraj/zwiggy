import os
from django.core.exceptions import ValidationError


def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1]
    valid_extentions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extentions:
        raise ValidationError('Unsupported file extension. Allowed extensions: '+ str(valid_extentions))
        
