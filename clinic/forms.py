from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from . import opening_hours
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Let the browser grey out past dates before the form is even submitted.
        self.fields['preferred_date'].widget.attrs['min'] = timezone.localdate().isoformat()

    def clean(self):
        cleaned_data = super().clean()
        errors = opening_hours.slot_errors(
            cleaned_data.get('preferred_date'), cleaned_data.get('preferred_time')
        )
        for field, message in errors.items():
            self.add_error(field, message)
        return cleaned_data


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
