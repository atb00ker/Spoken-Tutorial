'''
This file is used for registering the portal models in site admin panel.
'''

from django.contrib import admin as administrator
from django.contrib.contenttypes.models import ContentType
from .models import (
    foss,
    tutorial_detail,
    payment
)

# Register your models here.

administrator.site.register(foss)
administrator.site.register(tutorial_detail)
administrator.site.register(payment)
