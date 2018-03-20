# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import login, authenticate
from .forms import FossCreationForm, PaymentForm, FossSubmissionForm
from portal.models import foss, payment, tutorial_detail
from django.views import View


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
