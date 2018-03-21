from django import forms
from django.contrib.auth.models import User


class FossCreationForm(forms.Form):
    '''
    Takes in Fields that are required for creating a foss.
    '''
    title = forms.CharField()
    assigned_to = forms.CharField()
    assigned_by = forms.CharField()
    expected_submission_date = forms.CharField()


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
        choices=month_type_list, required=False)
    month = forms.ChoiceField(
        choices=month_list, required=False)


class FossSubmissionForm(forms.Form):
    '''
    Takes in information to show payments.
    '''
    expected_submission_month = forms.CharField()
    actual_submission_month = forms.CharField()
