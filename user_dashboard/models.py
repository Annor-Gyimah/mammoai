from django.db import models
from userauths.models import User
import os
from shortuuid.django_fields import ShortUUIDField
from django.core.validators import MinValueValidator, MaxValueValidator


NOTIFICATION_TYPE = (
    ("User Registered", "User Registered"),
    
)

GENDER = (
    
    ("Male", "Male"),
    ("Female","Female"),
    ("Other", "Other"),
)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    type = models.CharField(max_length=180, choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username}" 


def user_patient_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/patient_<pid>/<filename>
    return f'user_{instance.user.id}/patient_{instance.firstname}/{filename}'


class Patient(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    
    id =  models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20)
    age = models.CharField(max_length=3)
    gender = models.CharField(max_length=10, null=True, choices=GENDER)
    address = models.CharField(max_length=200, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(blank=True)
    breast_health = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    mammogram_image = models.ImageField(upload_to=user_patient_directory_path, null=True, blank=True)
    risk_assessment_form = models.FileField(upload_to=user_patient_directory_path, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    pid = ShortUUIDField(length=10, max_length=20, alphabet='0123456789', null=True, blank=True)

    

    def save(self, *args, **kwargs):
        if not self.pk and 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Patient {self.firstname} {self.lastname}"
     