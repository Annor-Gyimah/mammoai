from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib import messages
from django.http import JsonResponse
from userauths.models import Profile
from userauths.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import views as auth_view
from django.contrib.auth.views import PasswordChangeView
#from .forms import passwordchangingform
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from userauths.models import Profile, User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Notification





@login_required
def dashboard(request):
    
    notifications = Notification.objects.filter(user=request.user, seen=False)
    total_noti = notifications.count() 
    context = {
        "total_noti":total_noti,
        "notifications":notifications,
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
    total_noti = notifications.count() 
    context = {
        "total_noti":total_noti,
    }

    return render(request, "user_dashboard/records.html", context)


@login_required
def add_patient(request):
    notifications = Notification.objects.filter(user=request.user, seen=False)
    total_noti = notifications.count() 
    context = {
        "total_noti":total_noti,
    }

    return render(request, "user_dashboard/add_patient.html", context)

@login_required
def upload(request):
    notifications = Notification.objects.filter(user=request.user, seen=False)
    total_noti = notifications.count() 
    context = {
        "total_noti":total_noti,
    }

    return render(request, "user_dashboard/upload.html", context)

