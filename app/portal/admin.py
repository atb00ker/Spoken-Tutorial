'''
This file is used for
1. Registering the portal models in auth.admin
2. Creating a group called 'admin' an allowing it the
permissions to all the portal modals.
3. Giving administrator panel access to
all the superusers by entering them in the 'admin' group.
'''

from django.contrib import admin as administrator
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from .models import (
    foss,
    tutorial_detail,
    payment
)
from django.contrib.auth.models import (
    Group,
    Permission
)

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

superUserslist = User.objects.filter(is_superuser=1)

for superuser in superUserslist:
    admin.user_set.add(superuser)
