# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import login, authenticate
from .forms import FossCreationForm, PaymentForm, FossSubmissionForm
from portal.models import foss, payment, tutorial_detail
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


class UserPayment(View):
    '''
    UserPayment class used for the payment page.
    takes in the form username and returns the and/or month to spit the appropriate data.
    '''

    def get(self, request):
        if request.user.is_authenticated:
            is_admin = request.user.groups.filter(name='admin').exists()
            if is_admin:
                form = PaymentForm()
                return render(request, 'portal/forms.html', {"form_page_name": 'Payment',
                                                             'submit_btn_name': "Show List",
                                                             'is_admin': is_admin,
                                                             "form": form})
            else:
                return redirect('/login')
        else:
            return redirect('/login')

    def post(self, request):
        form = PaymentForm(request.POST)
        is_admin = request.user.groups.filter(name='admin').exists()
        if form.is_valid():
            if form.cleaned_data['month_type'] == 'Actual':
                queryResponse = tutorial_detail.objects.filter(
                    actual_submission_date__month=form.cleaned_data['month']).values()
                return render(request, 'portal/payment.html', {'is_admin': is_admin, "table": queryResponse})
            else:
                queryResponse = tutorial_detail.objects.filter(
                    expected_submission_date__month=form.cleaned_data['month']).values()
                return render(request, 'portal/payment.html', {'is_admin': is_admin, "table": queryResponse})
        else:
            if is_admin:
                return render(request, 'portal/forms.html', {"form_page_name": 'Payment',
                                                             'submit_btn_name': "Show List",
                                                             'is_admin': is_admin,
                                                             "form": form})
            else:
                redirect('/login')


def pay(request, foss_id, tut_id):
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='admin').exists()
        if is_admin:
            tut_id = (tutorial_detail.objects.get(pk=tut_id))
            if tut_id.is_paid:
                return render(request, 'portal/messages.html', {
                    "msg_page_name": 'Failed', 'message': 'Looks like the transaction is not allowed, since the payment has already been made, if you think this is a mistake, please contact the administrator.', 'is_admin': is_admin})
            else:
                try:
                    username = (foss.objects.get(pk=foss_id)).user
                    data = payment(payment_for=username, amount=1000,
                                   date=datetime.datetime.now(), approved_by=request.user)
                    tut_id.is_paid = True
                    data.save()
                    tut_id.save()
                    return render(request, 'portal/messages.html', {
                        "msg_page_name": 'Success', 'message': 'Payment has been successfully made for the user.', 'is_admin': is_admin})
                except:
                    return render(request, 'portal/messages.html', {
                        "msg_page_name": 'Failed', 'message': 'Something went wrong during the transaction, please try again.', 'is_admin': is_admin})
        else:
            return render(request, 'portal/messages.html', {
                "msg_page_name": 'Failed', 'message': 'You do not have the access to make the transaction, please login from a administrator account.', 'is_admin': is_admin})
    else:
        redirect('/login')
