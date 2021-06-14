import datetime
from django.core.exceptions import ValidationError

def validate_birth_date(value):
    if value >= datetime.datetime.now().date():
        raise ValidationError('Дата не может быть позже тем текущая!')