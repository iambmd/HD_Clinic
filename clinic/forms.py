from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Appointment, ContactMessage


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['full_name', 'phone', 'email', 'preferred_date', 'preferred_time', 'branch']
        widgets = {
            'full_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': _('Your full name')}
            ),
            'phone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '+84 ...'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'you@example.com'}
            ),
            'preferred_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'
            ),
            'preferred_time': forms.TimeInput(
                attrs={'class': 'form-control', 'type': 'time'}, format='%H:%M'
            ),
            'branch': forms.Select(attrs={'class': 'form-select'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'email', 'message']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': _('Your name')}
            ),
            'phone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '+84 ...'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'you@example.com'}
            ),
            'message': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 5, 'placeholder': _('How can we help?')}
            ),
        }
