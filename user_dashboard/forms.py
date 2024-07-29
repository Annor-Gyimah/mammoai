from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient
from django.forms import FileInput
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from django.contrib.auth import get_user_model



# class PatientForm(forms.ModelForm):
#     GENDER = [
#         ("Male", "Male"),
#         ("Female","Female"),
#     ]
#     firstname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "First name", 'type': 'text','name':'fname', 'id': 'fname', 'required': 'required'}))
#     lastname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Last name", 'type': 'text', 'name':'lname', 'id': 'lname', 'required': 'required'}))
#     age = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': "Age", 'type': 'number', 'name':'age', 'id': 'age', 'required': 'required'}))
#     gender = forms.ChoiceField(choices=GENDER,widget=forms.RadioSelect(attrs={'type':'radio','name':'gender', 'id': 'gender'}))
#     address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Address", 'type': 'text', 'name':'address', 'id': 'address'}))
#     phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Phone", 'type': 'tel', 'name':'mobile', 'id': 'mobile'}))
#     occupation = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Occupation", 'type': 'text', 'name':'occu', 'id': 'occu'}))
#     class Meta:
        
#         model = Patient
#         fields = ['firstname', 'lastname', 'phone', 'age', 'gender', 'address', 'occupation', 'notes', 'breast_health', 'medical_history', 'mammogram_image', 'risk_assessment_form', 'pid']

#         widgets = {
#             "mammogram_image": FileInput(attrs={"onchange": "loadImg(event)","name":"filePath", "class": "upload_img"}),
            
#         }
        


class PatientForm(forms.ModelForm):
    GENDER = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

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

    firstname = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "First name", 'type': 'text', 'name': 'fname', 'id': 'fname', 'required': 'required'})
    )
    lastname = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Last name", 'type': 'text', 'name': 'lname', 'id': 'lname', 'required': 'required'})
    )
    age = forms.IntegerField(
        widget=forms.TextInput(attrs={'placeholder': "Age", 'type': 'number', 'name': 'age', 'id': 'age', 'required': 'required'})
    )
    gender = forms.ChoiceField(
        choices=GENDER,
        widget=forms.Select(attrs={'type': 'radio', 'name': 'gender', 'id': 'gender'})
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Address", 'type': 'text', 'name': 'address', 'id': 'address'})
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Phone", 'type': 'tel', 'name': 'mobile', 'id': 'mobile'})
    )
    occupation = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Occupation", 'type': 'text', 'name': 'occu', 'id': 'occu'})
    )
    age_group_5_years = forms.ChoiceField(
        choices=AGE_GROUP_CHOICES,
        widget=forms.Select(attrs={'name': 'age_group', 'id': 'age_group'})
    )
    menopaus = forms.ChoiceField(
        choices=MENOPAUSAL_STATUS_CHOICES,
        widget=forms.Select(attrs={'name': 'menopaus', 'id': 'menopaus'})
    )
    bmi_group = forms.ChoiceField(
        choices=BMI_GROUP_CHOICES,
        widget=forms.Select(attrs={'name': 'bmi_group', 'id': 'bmi_group'})
    )
    biophx = forms.ChoiceField(
        choices=BIOPHX_CHOICES,
        widget=forms.Select(attrs={'name': 'biophx', 'id': 'biophx'})
    )
    first_degree_hx = forms.ChoiceField(
        choices=FIRST_DEGREE_HX_CHOICES,
        widget=forms.Select(attrs={'name': 'first_degree_hx', 'id': 'first_degree_hx'})
    )
    age_menarche = forms.ChoiceField(
        choices=AGE_MENARCHE_CHOICES,
        widget=forms.Select(attrs={'name': 'age_menarche', 'id': 'age_menarche'})
    )
    age_first_birth = forms.ChoiceField(
        choices=AGE_FIRST_BIRTH_CHOICES,
        widget=forms.Select(attrs={'name': 'age_first_birth', 'id': 'age_first_birth'})
    )
    birads_breast_density = forms.ChoiceField(
        choices=BIRADS_DENSITY_CHOICES,
        widget=forms.Select(attrs={'name': 'birads_breast_density', 'id': 'birads_breast_density'})
    )
    breast_cancer_history = forms.ChoiceField(
        choices=BREAST_CANCER_HISTORY_CHOICES,
        widget=forms.Select(attrs={'name': 'breast_cancer_history', 'id': 'breast_cancer_history'})
    )
    current_hrt = forms.ChoiceField(
        choices=CURRENT_HRT_CHOICES,
        widget=forms.Select(attrs={'name': 'current_hrt', 'id': 'current_hrt'})
    )

    class Meta:
        model = Patient
        fields = [
            'firstname', 'lastname', 'phone', 'age', 'gender', 'address', 'occupation', 
            'age_group_5_years', 'first_degree_hx', 'age_menarche', 'age_first_birth', 
            'birads_breast_density', 'breast_cancer_history', 'current_hrt', 'menopaus', 'bmi_group', 'biophx',
            'mammogram_image', 'pid'
        ]

        widgets = {
            "mammogram_image": forms.FileInput(attrs={"onchange": "loadImg(event)", "name": "filePath", "class": "upload_img"}),
        }
