from django import forms
from .models import login

class Contact(forms.Form):
    name = forms.CharField(label="Namee",max_length=100,required=True)
    email = forms.EmailField(label="Email",required=True)
    message = forms.CharField(label="Message",required=True)

class Login_form(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)

class CodeForm(forms.Form):
    re_enter_code = forms.CharField(max_length=100)

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = login
        fields = ['username', 'password','email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data

class CodeVerificationForm(forms.Form):
    re_enter_code = forms.CharField(max_length=100, label="Enter Verification Code")