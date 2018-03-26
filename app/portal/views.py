# -*- coding: utf-8 -*-
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponse
from django.conf import settings
from django.http.request import QueryDict
from django.db.models import F
import logging
import datetime
from django.shortcuts import (
    render,
    redirect
)
from django.contrib.auth import (
    login,
    authenticate
)
from .forms import (
    FossCreationForm,
    CalendarForm,
    TutorialCreationForm
)
from portal.models import (
    foss,
    payment,
    tutorial_detail
)

# Logger for the file, settings for this logger
# in spoken_tutorial/settings.py
logger = logging.getLogger("PaymentPortalErrors")


def dashboard(request):
    '''
    This function will render Dashboard if logged in else render landing page
    '''
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='admin').exists()
        return render(request, 'portal/dashboard.html', {'is_admin': is_admin})
    else:
        return render(request, 'index.html')


def admin_panel(request):
    '''
    This function will render administrator panel if admin else redirect to login
    '''
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='admin').exists()
        if is_admin:
            return render(request,
                          'portal/admin_panel.html',
                          {'is_admin': is_admin})
        else:
            return redirect('login')
    else:
        return redirect('login')


def viewFossTable(request):
    '''
    View all foss in a table
    '''
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='admin').exists()
        if is_admin:
            table = foss.objects.all()
            return render(request, 'portal/viewFossTable.html', {
                'table': table,
                'is_admin': is_admin})
        else:
            return redirect('login')
    else:
        return redirect('login')


def viewFossDetails(request, foss):
    '''
    View details about the selected foss
    '''
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='admin').exists()
        if is_admin:
            table = tutorial_detail.objects.filter(foss=foss)
            return render(request, 'portal/viewFossDetails.html', {
                'foss': foss,
                'table': table,
                'is_admin': is_admin})
        else:
            return redirect('login')
    else:
        return redirect('login')


def submitted(request):
    '''
    If the administrator decides to mark a tutorial as submitted
    the request is transfered to this function.
    '''
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='admin').exists()
        if is_admin:
            tutorial_detail.objects.filter(pk=request.POST['tut_id']
                                           ).update(actual_submission_date=datetime.datetime.now())
            table = tutorial_detail.objects.filter(foss=request.POST['foss'])
            return render(request,
                          'portal/partials/tables/_tutorials.html',
                          {'foss': request.POST['foss'],
                           'table': table,
                           'is_admin': is_admin})
        else:
            return redirect('login')
    else:
        return redirect('login')


class AddFossTutorial(View):
    '''
    This class handles the form used to create new tutorial in a FOSS.
    '''

    def get(self, request, foss_id):
        if request.user.is_authenticated:
            is_admin = request.user.groups.filter(name='admin').exists()
            if is_admin:
                form = TutorialCreationForm()
                return render(request,
                              'portal/forms.html',
                              {'form': form,
                               "form_page_name": 'Create Tutorial',
                               'submit_btn_name': "Create Tutorial",
                               'is_admin': is_admin})
            else:
                return redirect('login')
        else:
            return redirect('login')

    def post(self, request, foss_id):
        if request.user.is_authenticated:
            is_admin = request.user.groups.filter(name='admin').exists()
            if is_admin:
                form = TutorialCreationForm(request.POST)
                if form.is_valid():
                    data = tutorial_detail(
                        title=form.cleaned_data['title'],
                        assigned_by=request.user,
                        foss=foss.objects.get(pk=foss_id),
                        expected_submission_date=form.cleaned_data['Deadline'])
                    data.save()
                    return redirect('viewFossDetails', foss_id)
                else:
                    return render(request,
                                  'portal/forms.html',
                                  {'form': form,
                                   "form_page_name": 'Create Tutorial',
                                   'submit_btn_name': "Create Tutorial",
                                   'is_admin': is_admin})
            else:
                return redirect('login')
        else:
            return redirect('login')


class CreateFOSS(View):
    '''
    This class handles the form used to create new FOSS.
    '''

    def get(self, request):
        if request.user.is_authenticated:
            is_admin = request.user.groups.filter(name='admin').exists()
            if is_admin:
                form = FossCreationForm()
                return render(request,
                              'portal/forms.html',
                              {'form': form,
                               "form_page_name": 'Create Foss',
                               'submit_btn_name': "Create Foss",
                               'is_admin': is_admin})
            else:
                return redirect('login')
        else:
            return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            is_admin = request.user.groups.filter(name='admin').exists()
            if is_admin:
                form = FossCreationForm(request.POST)
                if form.is_valid():
                    data = foss(
                        title=form.cleaned_data['title'],
                        user=form.cleaned_data['Assigned_to'])
                    data.save()
                    return redirect('viewFossTable')
                else:
                    return render(request,
                                  'portal/forms.html',
                                  {'form': form,
                                   "form_page_name": 'Create Foss',
                                   'submit_btn_name': "Create Foss",
                                   'is_admin': is_admin})
            else:
                return redirect('login')
        else:
            return redirect('login')


class UserSubmissions(View):
    '''
    UserSubmissions class used for the Submission page. The post function takes in the month of data that needs to be displayed and displays it.
    You can publish tutorial from this page.
    '''

    def get(self, request):
        if request.user.is_authenticated:
            is_admin = request.user.groups.filter(name='admin').exists()
            if is_admin:
                form = CalendarForm()
                return render(request,
                              'portal/forms.html',
                              {"form_page_name": 'Submissions',
                               'submit_btn_name': "Show List",
                               'is_admin': is_admin,
                               "form": form})
            else:
                return redirect('login')
        else:
            return redirect('login')

    def post(self, request):
        form = CalendarForm(request.POST)
        is_admin = request.user.groups.filter(name='admin').exists()
        if form.is_valid():
            table = self.generateTable(request, form)
            return render(request, 'portal/submissions.html',
                          {'is_admin': is_admin,
                           "table": table,
                           "month": form.cleaned_data['month'],
                           "month_type": form.cleaned_data['month_type']})
        else:
            if is_admin:
                return render(request,
                              'portal/forms.html',
                              {"form_page_name": 'Payment',
                               'submit_btn_name': "Show List",
                               'is_admin': is_admin,
                               "form": form})
            else:
                return redirect('login')

    def generateTable(self, request, form):
        if form.cleaned_data['month_type'] == 'Actual':
            queryResponse = tutorial_detail.objects.filter(
                actual_submission_date__month=form.cleaned_data['month']).values()
        else:
            queryResponse = tutorial_detail.objects.filter(
                expected_submission_date__month=form.cleaned_data['month']).values()
        return queryResponse


def publish(request):
    '''
    If the administrator decides to publish a tutorial,
    the request is send to this function.
    '''
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='admin').exists()
        if is_admin:
            tut_id = request.POST['tut_id']
            foss_id = request.POST['foss_id']
            month = request.POST['month']
            month_type = request.POST['month_type']
            tut_id = (tutorial_detail.objects.get(pk=tut_id))
            if tut_id.is_published:
                return render(
                    request,
                    'portal/messages.html',
                    {"msg_page_name": 'Failed',
                     'message': 'Looks like the tutorial is already published, if this is a mistake, contact site administrator.',
                     'is_admin': is_admin})
            else:
                tut_id.is_published = True
                tut_id.save()
                request.POST = QueryDict(
                    'month='+month+'&month_type='+month_type)
                form = CalendarForm(request.POST)
                form.is_valid()
                table = UserSubmissions().generateTable(request, form)
                return render(request, 'portal/partials/tables/_submissions.html',
                                        {'is_admin': is_admin,
                                         "table": table,
                                         "month": form.cleaned_data['month'],
                                         "month_type": form.cleaned_data['month_type']})
        else:
            return render(
                request,
                'portal/messages.html',
                {"msg_page_name": 'Failed',
                 'message': 'You do not have the access to make the transaction, please login from an administrator account.',
                 'is_admin': is_admin})
    else:
        return redirect('login')


class UserPayment(View):
    '''
    UserPayment class used for the payment page. The post function takes in the month of data that needs to be displayed and displays it.
    You can play contributor from this page.
    '''

    def get(self, request):
        if request.user.is_authenticated:
            is_admin = request.user.groups.filter(name='admin').exists()
            if is_admin:
                form = CalendarForm()
                return render(request,
                              'portal/forms.html',
                              {"form_page_name": 'Payment',
                               'submit_btn_name': "Show List",
                               'is_admin': is_admin,
                               "form": form})
            else:
                return redirect('login')
        else:
            return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            is_admin = request.user.groups.filter(name='admin').exists()
            if is_admin:
                form = CalendarForm(request.POST)
                if form.is_valid():
                    processedResponse = self.generateTable(request, form)
                    return render(request,
                                  'portal/payment.html',
                                  {'is_admin': is_admin,
                                   "table": processedResponse,
                                   "month": form.cleaned_data['month'],
                                   "month_type": form.cleaned_data['month_type']})
                else:
                    return render(request,
                                  'portal/forms.html',
                                  {"form_page_name": 'Payment',
                                   'submit_btn_name': "Show List",
                                   'is_admin': is_admin,
                                   "form": form})
            else:
                return redirect('login')
        else:
            return redirect('login')

    def generateTable(self, request, form):
        if form.cleaned_data['month_type'] == 'actual':
            queryResponse = tutorial_detail.objects.filter(
                actual_submission_date__month=form.cleaned_data['month']).values(
                username=F('foss__user_id__username')).annotate(
                    multiplier=Count('foss'))
        else:
            queryResponse = tutorial_detail.objects.filter(
                expected_submission_date__month=form.cleaned_data['month']).values(
                username=F('foss__user_id__username')).annotate(
                multiplier=Count('foss'))
        for processQuery in queryResponse:
            is_paid = payment.objects.filter(
                date__month=form.cleaned_data['month'], payment_for__username=processQuery['username'])
            if is_paid:
                processQuery['is_paid'] = True
            else:
                processQuery['is_paid'] = False
        return queryResponse


def pay(request):
    '''
    If the administrator decides to pay a contributor for
    a month the request is transfered to this page.
    '''
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='admin').exists()
        if is_admin:
            username = request.POST['username']
            month = request.POST['month']
            month_type = request.POST['month_type']
            multiplier = request.POST['multiplier']
            user_id = (User.objects.get(username=username)).pk
            is_paid = payment.objects.filter(
                date__month=month, payment_for=user_id)
            if is_paid:
                return render(
                    request,
                    'portal/messages.html',
                    {"msg_page_name": 'Failed',
                     'message': 'Looks like the transaction is not allowed, since the payment has already been made, if you think this is a mistake, please contact the administrator.',
                     'is_admin': is_admin})
            else:
                try:
                    data = payment(
                        payment_for=(User.objects.get(username=username)),
                        amount=(int(multiplier) * 1000),
                        date=datetime.datetime.now(tz=timezone.utc),
                        approved_by=request.user
                    )
                    data.save()
                    request.POST = QueryDict(
                        'month='+month+'&month_type='+month_type)
                    form = CalendarForm(request.POST)
                    form.is_valid()
                    processedResponse = UserPayment().generateTable(request, form)
                    return render(request,
                                  'portal/partials/tables/_payment.html',
                                  {"table": processedResponse,
                                   "month": form.cleaned_data['month'],
                                   "month_type": form.cleaned_data['month_type']})
                except Exception as Error:
                    logger.error(str(Error))
                    return render(
                        request,
                        'portal/messages.html',
                        {"msg_page_name": 'Failed',
                         'message': 'Something went wrong during the transaction, please try again.',
                         'is_admin': is_admin})
        else:
            return render(
                request,
                'portal/messages.html',
                {"msg_page_name": 'Failed',
                 'message': 'You do not have the access to make the transaction, please login from an administrator account.',
                 'is_admin': is_admin})
    else:
        return redirect('login')
