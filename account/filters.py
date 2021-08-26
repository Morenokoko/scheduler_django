from django.forms import fields, widgets
import django_filters
from django_filters import DateFilter
from django import forms

from .models import *
import datetime as dt

HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]
choice_time = dt.time(hour=23)

class AvailabilityFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date", lookup_expr='gte', label='From',
        widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name="date", lookup_expr='lte', label='To',
        widget=forms.DateInput(attrs={'type': 'date'}))
    shift_start = django_filters.TimeFilter(field_name='shift', lookup_expr 
    ='gte', label='Starting shift', widget=forms.Select(choices=HOUR_CHOICES))
    shift_end = django_filters.TimeFilter(field_name='shift', lookup_expr 
    ='lte', label='Ending shift', widget=forms.Select(choices=HOUR_CHOICES))
    rank = django_filters.NumberFilter(field_name='rank', label='Rank', widget=forms.NumberInput(attrs={'min':1, 'max':24}))

    # class Meta:
    #     model = Availability
    #     fields = []
        # widgets ={
        #     'date': forms.DateInput()
        # }

class ScheduleFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date", lookup_expr='gte', label='From',
        widget=forms.DateInput(attrs={'type': 'date',}))
    end_date = DateFilter(field_name="date", lookup_expr='lte', label='To',
        widget=forms.DateInput(attrs={'type': 'date',}))
    shift_start = django_filters.TimeFilter(field_name='shift', lookup_expr 
    ='gte', label='Starting shift', widget=forms.Select(choices=HOUR_CHOICES))
    shift_end = django_filters.TimeFilter(field_name='shift', lookup_expr 
    ='lte', label='Ending shift', widget=forms.Select(choices=HOUR_CHOICES))

    class Meta:
        model = Schedule
        fields = ['employee']
        # fields = ['shift', 'employee']
        # widgets = {
		# 	'shift': forms.Select(choices= HOUR_CHOICES)
        # }