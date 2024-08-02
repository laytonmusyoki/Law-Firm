from django import forms
from .models import Clients
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from typing import Any

class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['first_name', 'sir_name', 'phone_number', 'email', 'county', 'country','status',
                  'matter_number', 'matter_name', 'document_upload', 'description', 'pleading_status',
                  'statement', 'dispute', 'criminal_sub_option', 'civil_sub_option', 'other_services_sub_option']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sir_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'county': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'matter_number': forms.TextInput(attrs={'class': 'form-control'}),
            'matter_name': forms.TextInput(attrs={'class': 'form-control'}),
            'document_upload': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'pleading_status': forms.Select(attrs={'class': 'form-control'}),
            'statement': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 150px;'}),
            'dispute': forms.Select(attrs={'class': 'form-control'}),
            'criminal_sub_option': forms.Select(attrs={'class': 'form-control'}),
            'civil_sub_option': forms.Select(attrs={'class': 'form-control'}),
            'other_services_sub_option': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        dispute = cleaned_data.get("dispute")
        criminal_sub_option = cleaned_data.get("criminal_sub_option")
        civil_sub_option = cleaned_data.get("civil_sub_option")
        other_services_sub_option = cleaned_data.get("other_services_sub_option")

        if dispute == 'criminal' and not criminal_sub_option:
            self.add_error('criminal_sub_option', 'This field is required for criminal disputes.')
        elif dispute == 'civil' and not civil_sub_option:
            self.add_error('civil_sub_option', 'This field is required for civil disputes.')
        elif dispute == 'other' and not other_services_sub_option:
            self.add_error('other_services_sub_option', 'This field is required for other services.')

        return cleaned_data

class UserRegistration(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter your password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'
