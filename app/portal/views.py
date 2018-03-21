# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import login, authenticate
from .forms import FossCreationForm, CalendarForm, FossSubmissionForm
from portal.models import foss, payment, tutorial_detail
from .listGenerator import listGenerator
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.models import User
from django.views import View
import datetime


def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin')
        else:
            is_admin = request.user.groups.filter(name='admin').exists()
            return render(request, 'portal/dashboard.html', {'is_admin': is_admin})
    else:
        return render(request, 'index.html')


def admin_panel(request):
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='admin').exists()
        if is_admin:
            return render(request, 'portal/admin_panel.html', {'is_admin': is_admin})
        else:
            return redirect('/login')
    else:
        return redirect('/login')


def edit_foss(request):
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='admin').exists()
        if is_admin:
            form = FossCreationForm()
            return render(request, 'portal/forms.html', {'form': form,
                                                         "form_page_name": 'Create Foss', 'submit_btn_name': "Create Foss", 'is_admin': is_admin})
        else:
            return redirect('/login')
    else:
        return redirect('/login')


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
                return render(request, 'portal/forms.html', {"form_page_name": 'Submissions',
                                                             'submit_btn_name': "Show List",
                                                             'is_admin': is_admin,
                                                             "form": form})
            else:
                return redirect('/login')
        else:
            return redirect('/login')

    def post(self, request):
        form = CalendarForm(request.POST)
        is_admin = request.user.groups.filter(name='admin').exists()
        if form.is_valid():
            if form.cleaned_data['month_type'] == 'Actual':
                queryResponse = tutorial_detail.objects.filter(
                    actual_submission_date__month=form.cleaned_data['month']).values()
            else:
                queryResponse = tutorial_detail.objects.filter(
                    expected_submission_date__month=form.cleaned_data['month']).values()
            return render(request, 'portal/submissions.html', {'is_admin': is_admin, "table": queryResponse})
        else:
            if is_admin:
                return render(request, 'portal/forms.html', {"form_page_name": 'Payment',
                                                             'submit_btn_name': "Show List",
                                                             'is_admin': is_admin,
                                                             "form": form})
            else:
                return redirect('/login')


def publish(request, foss_id, tut_id):
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='admin').exists()
        if is_admin:
            tut_id = (tutorial_detail.objects.get(pk=tut_id))
            if tut_id.is_published:
                return render(request, 'portal/messages.html', {
                    "msg_page_name": 'Failed', 'message': 'Looks like the tutorial is already published, if this is a mistake, contact site administrator.', 'is_admin': is_admin})
            else:
                try:
                    tut_id.is_published = True
                    tut_id.save()
                    return render(request, 'portal/messages.html', {
                        "msg_page_name": 'Success', 'message': 'The tutorial has been published', 'is_admin': is_admin})
                except:
                    return render(request, 'portal/messages.html', {
                        "msg_page_name": 'Failed', 'message': 'Something went wrong during the transaction, please try again.', 'is_admin': is_admin})
        else:
            return render(request, 'portal/messages.html', {
                "msg_page_name": 'Failed', 'message': 'You do not have the access to make the transaction, please login from an administrator account.', 'is_admin': is_admin})
    else:
        return redirect('/login')


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
                return render(request, 'portal/forms.html', {"form_page_name": 'Payment',
                                                             'submit_btn_name': "Show List",
                                                             'is_admin': is_admin,
                                                             "form": form})
            else:
                return redirect('/login')
        else:
            return redirect('/login')

    def post(self, request):
        form = CalendarForm(request.POST)
        is_admin = request.user.groups.filter(name='admin').exists()
        if form.is_valid():
            if form.cleaned_data['month_type'] == 'actual':
                queryResponse = tutorial_detail.objects.filter(
                    actual_submission_date__month=form.cleaned_data['month']).values('foss').annotate(multiplier=Count('foss'))
            else:
                queryResponse = tutorial_detail.objects.filter(
                    expected_submission_date__month=form.cleaned_data['month']).values('foss').annotate(multiplier=Count('foss'))
            for processQuery in queryResponse:
                processQuery['foss'] = (foss.objects.get(
                    pk=processQuery['foss'])).user.username
            processedResponse = listGenerator(list(queryResponse))
            for processQuery in processedResponse:
                user_id = (User.objects.get(username=processQuery['foss'])).pk
                is_paid = payment.objects.filter(
                    date__month=form.cleaned_data['month'], payment_for=user_id)
                if is_paid:
                    processQuery['is_paid'] = True
                else:
                    processQuery['is_paid'] = False
            return render(request, 'portal/payment.html', {'is_admin': is_admin,
                                                           "table": processedResponse,
                                                           "month": form.cleaned_data['month']
                                                           })
        else:
            if is_admin:
                return render(request, 'portal/forms.html', {"form_page_name": 'Payment',
                                                             'submit_btn_name': "Show List",
                                                             'is_admin': is_admin,
                                                             "form": form})
            else:
                return redirect('/login')


def pay(request, username, multiplier, month):
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='admin').exists()
        if is_admin:
            user_id = (User.objects.get(username=username)).pk
            is_paid = payment.objects.filter(
                date__month=month, payment_for=user_id)
            if is_paid:
                return render(request, 'portal/messages.html', {
                    "msg_page_name": 'Failed', 'message': 'Looks like the transaction is not allowed, since the payment has already been made, if you think this is a mistake, please contact the administrator.', 'is_admin': is_admin})
            else:
                try:
                    data = payment(payment_for=(User.objects.get(username=username)), amount=(int(multiplier)*1000),
                                   date=datetime.datetime.now(tz=timezone.utc), approved_by=request.user)
                    data.save()
                    return render(request, 'portal/messages.html', {
                        "msg_page_name": 'Success', 'message': 'Payment has been successfully made for the user.', 'is_admin': is_admin})
                except Exception as Error:
                    print(Error)
                    return render(request, 'portal/messages.html', {
                        "msg_page_name": 'Failed', 'message': 'Something went wrong during the transaction, please try again.', 'is_admin': is_admin})
        else:
            return render(request, 'portal/messages.html', {
                "msg_page_name": 'Failed', 'message': 'You do not have the access to make the transaction, please login from an administrator account.', 'is_admin': is_admin})
    else:
        return redirect('/login')
