from django import forms
from django.contrib.auth.models import User
from portal.models import foss
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
    Takes in Fields that are required for creating a foss.
    '''
    title = forms.CharField()
    Deadline = forms.DateTimeField(
        initial=datetime.datetime.now())


class CalendarForm(forms.Form):
    '''
    Takes in information to show payments.
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
