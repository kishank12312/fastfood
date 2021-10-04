from django.db.models import fields
from django.contrib.gis.forms import ModelForm, widgets
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.gis import forms
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm

class DateInput(forms.DateInput):
    input_type = 'date'


class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Your password can’t be too similar to your other personal information. Your password must contain at least 8 characters. Your password can’t be a commonly used password. Your password can’t be entirely numeric.'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control text-light'
            visible.field.widget.attrs['autocomplete'] = 'off'
            visible.field.widget.attrs['placeholder'] = 'Placeholder'
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'password1': 'My password1 help_text',
        }
    
class CustomerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control text-light'
    class Meta:
        model = Customer
        fields = ['CustomerName', 'DateOfBirth']
        labels = {
            'CustomerName': 'Please enter your First Name and Last Name separated by a space*:',
            'DateOfBirth': 'Your Date of Birth*:',
        }
        widgets = {
            'DateOfBirth': DateInput(),
        }


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        self.fields['password1'].help_text = 'Your password can’t be too similar to your other personal information. Your password must contain at least 8 characters. Your password can’t be a commonly used password. Your password can’t be entirely numeric.'
        self.fields['password2'].help_text = 'Enter the same password as before, for verification.'

        self.fields['email'] = forms.EmailField(label='Email')
        self.fields['email'].help_text = 'Required. This email will be verified.'

        self.fields['username'].widget = forms.TextInput(attrs={'type': 'text', 'class': 'form-control text-light', 'placeholder':'Placeholder'})
        self.fields['email'].widget = forms.EmailInput(attrs={'type': 'email', 'class': 'form-control text-light', 'placeholder':'Placeholder'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control text-light', 'placeholder':'Placeholder'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control text-light', 'placeholder':'Placeholder'})