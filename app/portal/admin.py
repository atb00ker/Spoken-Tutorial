from django.contrib import admin as administrator
from .models import (
    foss,
    tutorial_detail,
    payment
)
from django.contrib.auth.models import (
    Group,
    Permission
)
from django.contrib.contenttypes.models import ContentType

# Register your models here.

administrator.site.register(foss)
administrator.site.register(tutorial_detail)
administrator.site.register(payment)


# Registration of Groups

admin, created = Group.objects.get_or_create(name='admin')
# Code to add permission to group
fossModel = ContentType.objects.get(model='foss').pk
TutorialModel = ContentType.objects.get(model='tutorial_detail').pk
PaymentModel = ContentType.objects.get(model='payment').pk
allPermissions = Permission.objects.filter(content_type_id__in=[
    fossModel, TutorialModel, PaymentModel])
for permission in allPermissions:
    admin.permissions.add(permission)
