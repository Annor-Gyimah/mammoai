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
STATUS = (
    ("Completed","Completed"),
    ("Pending", "Pending"),
    ("Process","Process"),
)
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    type = models.CharField(max_length=180, choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username}" 
    
class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    type = models.CharField(max_length=180, choices=STATUS)
    status_date = models.DateField(null=True, blank=True)
    firstname = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self) -> str:
        return f"{self.user.username}" 



def user_patient_directory_path(instance, filename):
    if instance.user is None:
        raise ValueError("User must be set before saving the file.")
    return f'user_{instance.user.id}/patient_{instance.firstname}/{filename}'




class Patient(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    FIRST_DEGREE_HX_CHOICES = (
        (0, 'No'),
        (1, 'Yes'),
        (9, 'Unknown'),
    )

    AGE_MENARCHE_CHOICES = (
        (0, '>14 years'),
        (1, '12-13 years'),
        (2, '<12 years'),
        (9, 'Unknown'),
    )

    AGE_FIRST_BIRTH_CHOICES = (
        (0, '<20 years'),
        (1, '20-24 years'),
        (2, '25-29 years'),
        (3, '>= 30 years'),
        (4, 'Nulliparous'),
        (9, 'Unknown'),
    )

    BIRADS_DENSITY_CHOICES = (
        (1, 'Almost entirely fatty'),
        (2, 'Scattered areas of fibroglandular density'),
        (3, 'Heterogeneously dense'),
        (4, 'Extremely dense'),
        (9, 'Unknown'),
    )

    BREAST_CANCER_HISTORY_CHOICES = (
        (0, 'No history'),
        (1, 'Yes, history of breast cancer'),
        (9, 'Unknown'),
    )

    CURRENT_HRT_CHOICES = (
        (0, 'No current HRT'),
        (1, 'Yes, current HRT'),
        (9, 'Unknown'),
    )
    
    AGE_GROUP_CHOICES = (
        (1, 'Age 18-29'),
        (2, 'Age 30-34'),
        (3, 'Age 35-39'),
        (4, 'Age 40-44'),
        (5, 'Age 45-49'),
        (6, 'Age 50-54'),
        (7, 'Age 55-59'),
        (8, 'Age 60-64'),
        (9, 'Age 65-69'),
        (10, 'Age 70-74'),
        (11, 'Age 75-79'),
        (12, 'Age 80-84'),
        (13, 'Age >85'),
    )

    MENOPAUSAL_STATUS_CHOICES = (
        (1, 'Pre- or peri-menopausal'),
        (2, 'Post-menopausal'),
        (3, 'Surgical menopause'),
        (9, 'Unknown'),
    )

    BMI_GROUP_CHOICES = (
        (1, '10-24.99'),
        (2, '25-29.99'),
        (3, '30-34.99'),
        (4, '35 or more'),
        (9, 'Unknown'),
    )

    BIOPHX_CHOICES = (
        (0, 'No'),
        (1, 'Yes'),
        (9, 'Unknown'),
    )

    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20)
    age = models.CharField(max_length=3)
    gender = models.CharField(max_length=10, null=True, choices=GENDER)
    address = models.CharField(max_length=200, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    first_degree_hx = models.PositiveIntegerField(choices=FIRST_DEGREE_HX_CHOICES, null=True, blank=True)
    age_menarche = models.PositiveIntegerField(choices=AGE_MENARCHE_CHOICES, null=True, blank=True)
    age_first_birth = models.PositiveIntegerField(choices=AGE_FIRST_BIRTH_CHOICES, null=True, blank=True)
    birads_breast_density = models.PositiveIntegerField(choices=BIRADS_DENSITY_CHOICES, null=True, blank=True)
    breast_cancer_history = models.PositiveIntegerField(choices=BREAST_CANCER_HISTORY_CHOICES, null=True, blank=True)
    current_hrt = models.PositiveIntegerField(choices=CURRENT_HRT_CHOICES, null=True, blank=True)
    age_group_5_years = models.PositiveIntegerField(choices=AGE_GROUP_CHOICES, null=True, blank=True)
    menopaus = models.PositiveIntegerField(choices=MENOPAUSAL_STATUS_CHOICES, null=True, blank=True)
    bmi_group = models.PositiveIntegerField(choices=BMI_GROUP_CHOICES, null=True, blank=True)
    biophx = models.PositiveIntegerField(choices=BIOPHX_CHOICES, null=True, blank=True)
    mammogram_image = models.ImageField(upload_to=user_patient_directory_path, null=True, blank=True)
    heatmap_image = models.ImageField(upload_to='heatmaps/', null=True, blank=True)
    predicted_class = models.CharField(max_length=100, null=True, blank=True)
    prediction_value = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    pid = ShortUUIDField(length=10, max_length=20, alphabet='0123456789', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Patient {self.firstname} {self.lastname}"


class Results(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    age = models.CharField(max_length=3, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, choices=GENDER)
    address = models.CharField(max_length=200, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    first_degree_hx = models.PositiveIntegerField(null=True, blank=True)
    age_menarche = models.PositiveIntegerField(null=True, blank=True)
    age_first_birth = models.PositiveIntegerField(null=True, blank=True)
    birads_breast_density = models.PositiveIntegerField(null=True, blank=True)
    breast_cancer_history = models.PositiveIntegerField(null=True, blank=True)
    current_hrt = models.PositiveIntegerField(null=True, blank=True)
    age_group_5_years = models.PositiveIntegerField(null=True, blank=True)
    menopaus = models.PositiveIntegerField(null=True, blank=True)
    bmi_group = models.PositiveIntegerField(null=True, blank=True)
    biophx = models.PositiveIntegerField(null=True, blank=True)
    mammogram_image = models.ImageField(upload_to=user_patient_directory_path, null=True, blank=True)
    heatmap_image = models.ImageField(upload_to='heatmaps/', null=True, blank=True)
    entry_count = models.PositiveIntegerField(default=0)  # New field to track the count
    date = models.DateTimeField(auto_now_add=True)
    predicted_class = models.CharField(max_length=100, null=True, blank=True)
    value = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f"Patient"

