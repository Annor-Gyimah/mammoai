from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient
from django.forms import FileInput
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from django.contrib.auth import get_user_model



class PatientForm(forms.ModelForm):
    GENDER = [
        ("Male", "Male"),
        ("Female","Female"),
    ]
    firstname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "First name", 'type': 'text','name':'fname', 'id': 'fname', 'required': 'required'}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Last name", 'type': 'text', 'name':'lname', 'id': 'lname', 'required': 'required'}))
    age = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': "Age", 'type': 'number', 'name':'age', 'id': 'age', 'required': 'required'}))
    gender = forms.ChoiceField(choices=GENDER,widget=forms.RadioSelect(attrs={'type':'radio','name':'gender', 'id': 'gender'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Address", 'type': 'text', 'name':'address', 'id': 'address'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Phone", 'type': 'tel', 'name':'mobile', 'id': 'mobile'}))
    occupation = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Occupation", 'type': 'text', 'name':'occu', 'id': 'occu'}))
    breast_health = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Breast Health History", 'type': 'text', 'name':'bhh', 'id': 'bhh'}))
    medical_history = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Medical History", 'type': 'text', 'name':'hh', 'id': 'hh'}))
    notes = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Notes", 'type': 'text', 'name':'notes', 'id': 'notes'}))
    # facebook = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Facebook", 'type': 'text', 'class': 'form--control', 'id': 'zip'}))

    # twitter = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Twitter", 'type': 'text', 'class': 'form--control', 'id': 'zip'}))
    class Meta:
        
        model = Patient
        fields = ['firstname', 'lastname', 'phone', 'age', 'gender', 'address', 'occupation', 'notes', 'breast_health', 'medical_history', 'mammogram_image', 'risk_assessment_form', 'pid']

        widgets = {
            "mammogram_image": FileInput(attrs={"onchange": "loadImg(event)", "class": "upload_img"}),
            "risk_assessment_form": FileInput(attrs={"onchange": "loadFile(event)", "class": "upload_file"})
        }
        

