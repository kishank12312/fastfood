from django.db.models import fields
from django.forms import ModelForm, widgets
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User


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
        fields = ['CustomerName', 'Address', 'DateOfBirth']
        labels = {
            'CustomerName': 'Please enter your First Name and Last Name separated by a space*:',
            'DateOfBirth': 'Your Date of Birth*:',
        }
        widgets = {
            'DateOfBirth': DateInput(),
        }
