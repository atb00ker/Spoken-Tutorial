from django.db import models
from django.contrib.auth.models import User


class foss(models.Model):
    foss_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class tutorial_detail(models.Model):
    actual_submission_date = models.DateTimeField()
    expected_submission_date = models.DateTimeField()
    published = models.BooleanField(default=True)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE)
    foss = models.ForeignKey(foss, on_delete=models.CASCADE)


class payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    amount = models.IntegerField(default=0)
    date = models.DateTimeField()
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin')
