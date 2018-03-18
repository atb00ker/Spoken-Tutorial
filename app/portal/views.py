# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
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
            return render(request, 'portal/admin_panel.html')


def edit_foss(request):
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='admin').exists()
        if is_admin:
            return render(request, 'portal/admin_panel.html')
    return render(request, 'portal/admin_panel.html')
