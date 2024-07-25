from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter Name", 'type':'text', 'class': 'form-control', 'id': 'name', 'required': 'required'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': "Email Address", "type":"email",'class': 'form-control checkUser', 'id': 'email', 'required': 'required'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter Subject", "type": "text", 'class': 'form-control', 'id': 'subject', 'required': 'required'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Enter Message", 'type': 'text', 'class': 'form-control', 'id': 'message','required':'required'}))

    class Meta:
        fields = ['name','email','subject','message']
    