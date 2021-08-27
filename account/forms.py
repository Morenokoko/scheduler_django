from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import NumberInput

from .models import *
import datetime as dt

HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']

class DateInput(forms.DateInput):
    input_type = 'date'

class ShiftForm(ModelForm):
	class Meta:
		model = Availability
		fields = ['date', 'shift', 'rank']
		widgets = {
            'date': DateInput(attrs={'min': dt.date.today}),
			'shift': forms.Select(choices=HOUR_CHOICES),
			'rank': NumberInput(attrs={'min':1, 'max':24})
        }

class DateForm(forms.Form):
	date = forms.DateField(label='Date', widget=DateInput(attrs={'min': dt.date.today}))

