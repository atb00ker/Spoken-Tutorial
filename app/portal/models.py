'''
This file is used to create all the
database tables that are required for the
portal app.
'''
from django.db import models
from django.contrib.auth.models import User


class foss(models.Model):
    '''
    Please find models' description on http://bit.do/STModels
    in tabular form.
    '''
    foss_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "foss"

    def __str__(self):
        return self.title


class tutorial_detail(models.Model):
    '''
    Please find models' description on http://bit.do/STModels
    in tabular form.
    '''
    tut_id = models.AutoField(primary_key=True)
    actual_submission_date = models.DateTimeField(null=True, blank=True)
    expected_submission_date = models.DateTimeField()
    is_published = models.BooleanField(default=False)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE)
    foss = models.ForeignKey(
        foss, on_delete=models.CASCADE, related_name='user_details')
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class payment(models.Model):
    '''
    Please find models' description on http://bit.do/STModels
    in tabular form.
    '''
    payment_for = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    amount = models.IntegerField(default=0)
    date = models.DateTimeField()
    approved_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='admin')

    def __str__(self):
        return str(self.payment_for)


def user_directory_path(self, filename):
    folderName = 'videos/%s/%s' % (self.tutorial, filename)
    return folderName


class UploadVideo(models.Model):
    tutorial = models.CharField(max_length=255)
    # document = models.FileField(upload_to='videos')
    document = models.FileField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tutorial
