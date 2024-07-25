from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile
from django.forms import FileInput
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from django.contrib.auth import get_user_model
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth.forms import PasswordChangeForm

GENDER = [
    ("Other", "Other"),
    ("Male", "Male"),
    ("Female","Female"),
]

# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': "Email Address",  'id': 'email', 'required': 'required'}))
#     full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Full name", 'id': 'full-name', 'required': 'required'}))
#     username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Username",  'id': 'username', 'required': 'required'}))
#     phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Mobile number", 'id': 'mobile', 'type': 'number', 'required': 'required'}))
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Password", 'id': 'password', 'required': 'required'}),label='Password')
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Confirm Password", 'id': 'confirm-password', 'required': 'required'}),label='Confirm Password')
#     #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
#     class Meta:
#         model = User
#         fields = [ 'email', 'full_name', 'username', 'phone', 'password1', 'password2']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': "Email Address", 'class': 'form-control', 'id': 'email', 'required': 'required'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Full name", 'class': 'form-control', 'id': 'full-name', 'required': 'required'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Username", 'class': 'form-control', 'id': 'username', 'required': 'required'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Mobile number", 'class': 'form-control left-padding', 'id': 'mobile', 'type': 'number', 'required': 'required'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Password", 'class': 'form-control', 'id': 'your-password', 'required': 'required'}),label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Confirm Password", 'class': 'form-control', 'id': 'confirm-password', 'required': 'required'}),label='Confirm Password')
    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    class Meta:
        model = User
        fields = [ 'email', 'full_name', 'username', 'phone', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Username",  'id': 'username', 'name':'username'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': "Email Address", 'type': 'text', 'id': 'email', 'name':'email'}))
    # phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Mobile number", 'class': 'form--control checkUser left-padding', 'id': 'mobile', 'type': 'number', 'required': 'required'}))
    # gender = forms.ChoiceField(choices=GENDER,widget=forms.Select(attrs={'class': 'form--control form-select','id': 'gender'}))
    class Meta:
        model = User
        
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Full Name",  'id': 'full name', 'name':'full name'}))
    # country = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Country", 'type': 'text', 'class': 'form--control', 'id': 'country'}))
    # gender = forms.ChoiceField(choices=GENDER,widget=forms.Select(attrs={'class': 'form--control form-select','id': 'gender'}))
    # state = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "State", 'type': 'text', 'class': 'form--control', 'id': 'state'}))
    # city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "City", 'type': 'text', 'class': 'form--control', 'id': 'city'}))
    # address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Address", 'type': 'text', 'class': 'form--control', 'id': 'address'}))
    # facebook = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Facebook", 'type': 'text', 'class': 'form--control', 'id': 'zip'}))

    # twitter = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Twitter", 'type': 'text', 'class': 'form--control', 'id': 'zip'}))
    class Meta:
        
        model = Profile
        fields = [
            "image",
            "full_name",
            # "phone",
            # "gender",
            # "country",
            # "city",
            # "state",
            # "address",
        ]
        widgets = {
            "image": FileInput(attrs={"type":"file", "onchange": "loadFile(event)", "class": "upload"})
        }

class passwordchangingform(PasswordChangeForm):
    old_password = forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={"type":"password", "name":"pswd_old", "id":"pswd_old"}))
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={"type":"password", "name":"pswd_new", "id":"pswd_new"}))
    new_password2 = forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={"type":"password", "name":"pswd_new", "id":"pswd_new"}))

    class Meta:
        model = User
        fields = ['old_password' 'new_password1', 'new_password2']

class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Password", 'class': 'form-control', 'id': 'your-password', 'required': 'required'}),label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Confirm Password", 'class': 'form-control', 'id': 'confirm-password', 'required': 'required'}),label='Confirm New Password')

    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': "Email Address", 'type': 'text', 'class': 'form-control', 'id': 'email'}))
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    class Meta:
        model = User
        
        fields = ['email']
    

