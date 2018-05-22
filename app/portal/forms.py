'''
This file is used to create forms that are used in
the portal app.
'''
from django import forms
from django.contrib.auth.models import User
from portal.models import (
    foss,
    UploadVideo
)
import datetime


class FossCreationForm(forms.Form):
    '''
    Takes in Fields that are required for creating a foss.
    '''
    title = forms.CharField()
    Assigned_to = forms.ModelChoiceField(queryset=User.objects
                                         .filter(is_superuser=False)
                                         .exclude(groups__name='admin'),
                                         required=False)


class TutorialCreationForm(forms.Form):
    '''
    Takes in Fields that are required for creating a new
    Tutorial.
    '''
    title = forms.CharField()
    Deadline = forms.DateTimeField(
        initial=datetime.datetime.now())


class CalendarForm(forms.Form):
    '''
    Takes in information to show payments or
    Submissions for the selected month.
    '''
    month_type_list = (
        ('actual', 'Actual Submission'),
        ('expected', 'Deadline'),
    )
    month_list = (
        ('1', 'January'),
        ('2', 'Feburary'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    )
    month_type = forms.ChoiceField(
        label='Submitted',
        choices=month_type_list)
    month = forms.ChoiceField(choices=month_list)


class VideoForm(forms.ModelForm):
    class Meta:
        model = UploadVideo
        fields = ('tutorial', 'document',)

        labels = {
            "tutorial": ("Tutorial Name"),
            "document": ("Video"),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        file = cleaned_data.get("document")
        file_exts = ('.ogv', '.mov')

        if file is None:
            raise forms.ValidationError('Please select a file!')
        if file.content_type != 'video/ogg' and file.content_type != 'video/quicktime':
            print (file.content_type)
            raise forms.ValidationError(
                'Video accepted only in: %s' % ' '.join(file_exts))
        return cleaned_data
