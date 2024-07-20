from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib import messages
from django.http import JsonResponse
from userauths.models import Profile
from userauths.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import views as auth_view
from django.contrib.auth.views import PasswordChangeView
from .forms import PatientForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from userauths.models import Profile, User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Notification, Patient





@login_required
def dashboard(request):
    
    notifications = Notification.objects.filter(user=request.user, seen=False)
    patients = Patient.objects.filter(user=request.user)
    total_noti = notifications.count()
    total_pat = patients.count()
    date = timezone.now().date() 
    context = {
        "total_noti":total_noti,
        "notifications":notifications,
        "total_pat":total_pat,
        "date":date,
    }
    
    return render(request, "user_dashboard/dashboard.html", context)

def notification_mark_as_seen(request, id):
    noti = Notification.objects.get(id=id)
    noti.seen = True
    noti.save()
    noti.delete()
    messages.success(request, "Notification Deleted")

    return redirect("user_dashboard:dashboard")


@login_required
def records(request):
    notifications = Notification.objects.filter(user=request.user, seen=False)
    patients = Patient.objects.filter(user=request.user)
    total_noti = notifications.count() 
    context = {
        "total_noti":total_noti,
        "patients":patients,
    }

    return render(request, "user_dashboard/records.html", context)



@login_required
def add_patient(request):
    notifications = Notification.objects.filter(user=request.user, seen=False)
    total_noti = notifications.count()
    
    if request.method == "POST":
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user
            patient.save()
            messages.success(request, "Patient form filled successfully.")
            return redirect("user_dashboard:records")
    else:
        form = PatientForm()

    context = {
        "total_noti": total_noti,
        "form": form,
    }

    return render(request, "user_dashboard/add_patient.html", context)

def edit_records(request, pk):
    record = Patient.objects.get(id=pk)
    form = PatientForm(instance=record) 
    notifications = Notification.objects.filter(user=request.user, seen=False)
    total_noti = notifications.count() 
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient details was updated')
            return redirect('user_dashboard:records')
        
    context = {
        "total_noti":total_noti,
        "form":form,
        "record":record,
    }

    return render(request, 'user_dashboard/add_patient.html', context=context)

def delete_records(request, pk):
    record = Patient.objects.get(id=pk)

    record.delete()
    messages.success(request, 'Patient details was deleted')

    return redirect("user_dashboard:records")



@login_required
def upload(request):
    notifications = Notification.objects.filter(user=request.user, seen=False)
    total_noti = notifications.count() 
    context = {
        "total_noti":total_noti,
    }

    return render(request, "user_dashboard/upload.html", context)

