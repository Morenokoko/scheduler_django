from django.forms.widgets import Select
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db import IntegrityError
from django.forms import inlineformset_factory
from django import forms

# Create your views here.
from .models import *
from .forms import * 
from .filters import *
import datetime as dt

HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

        context = {'form':form}
        return render(request, 'account/register.html', context)


def loginPage(request): # named as 'loginPage' to avoid conflict with the Django method login
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username OR Password is incorrect')

        context = {}
        return render(request, 'account/login.html', context)


@login_required(login_url='login')
def index(request):
    schedule = Schedule.objects.order_by('-date','-shift')
    schedule_date_list = []

    for i in schedule:
        if i.date not in schedule_date_list:
            if i.date == date.today():
                schedule_date_list.append(i.date)

    print('SCHEDULE DATE LIST',schedule_date_list)
    context = {'schedule':schedule, 'schedule_date_list':schedule_date_list}
    return render(request, 'account/home.html', context)


@login_required(login_url='login')
def viewSchedules(request):
    schedule = Schedule.objects.order_by('-date','-shift')
    myFilter = ScheduleFilter(request.GET, queryset=schedule)
    schedule = myFilter.qs 
    schedule_date_list = []

    for i in schedule:
        if i.date not in schedule_date_list:
            schedule_date_list.append(i.date)

    context = {'schedule':schedule, 'schedule_date_list':schedule_date_list, 'myFilter': myFilter}
    return render(request, 'account/viewSchedule.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
def myavailability(request):
    user = request.user
    availability_list = Availability.objects.filter(user = request.user).order_by('-date','-shift')
    availability_date_list = []

    myFilter = AvailabilityFilter(request.GET, queryset=availability_list)
    availability_list = myFilter.qs 

    for i in availability_list:
        if i.date not in availability_date_list:
            availability_date_list.append(i.date)

    context = {'availability_list': availability_list, 
        'availability_date_list': availability_date_list,  'myFilter': myFilter, 'user':user}
    return render(request, 'account/myavailability.html', context)


@login_required(login_url='login')
def shiftavailability(request):
    shift_list =[]
    rank_list = []
    AvailabilityFormSet = inlineformset_factory(User, Availability, 
                                                fields=('shift', 'rank'), can_delete_extra=False,
                                                widgets={'shift': forms.Select(choices=HOUR_CHOICES),
                                                        'rank': NumberInput(attrs={'min':0, 'max':24})
                                                }, extra=24)
    dateform = DateForm()
    user = request.user
    formset = AvailabilityFormSet(queryset=Availability.objects.none(),instance=user)
    if request.method == 'POST':
        formset = AvailabilityFormSet(request.POST, instance=user)
        dateform = DateForm(request.POST)
        if formset.is_valid() and dateform.is_valid():
            # check that no duplicates of shifts and ranks in formset
            date_chosen = dateform.cleaned_data
            for f in formset:
                cd = f.cleaned_data
                shift = cd.get('shift')
                rank = cd.get('rank')
                if shift != None:
                    shift_list.append(shift)
                rank = cd.get('rank')
                if rank != 0 and rank != None:
                    rank_list.append(rank)
            contains_shift_duplicates = any(shift_list.count(shift) > 1 for shift in shift_list)
            contains_rank_duplicates = any(rank_list.count(rank) > 1 for rank in rank_list)
            print(contains_shift_duplicates, shift_list)
            print(contains_rank_duplicates, rank_list)
            if contains_shift_duplicates == False and contains_rank_duplicates == False:
                print('no duplicates within formset')
                for f in formset:
                    cd = f.cleaned_data
                    shift = cd.get('shift')
                    rank = cd.get('rank')
                    if shift != None and rank != 0 and rank != None:
                        try:
                            print('a shift exists where rank exists and is not equal to 0')
                            availability = Availability(user = user, date = date_chosen.get('date'), shift = shift, rank = rank)
                            availability.save()
                            print('availability saved')
                            createSchedule(availability)
                        except IntegrityError as e:
                            messages.error(request, 'Shift at time ' + str(shift.strftime('%H:%M')) +
                                        ' was not saved as you already have an existing shift with similar timing OR rank of ' +
                                         str(rank))
                return redirect('myavailability')
            else:
                messages.error(request, 'You can only rank a shift once and there cannot be repeated ranks')
                return redirect('shiftavailability')
        else:
            print('formset not valid')
    context = {'form':formset, 'dateform':dateform}
    return render(request, 'account/shift.html', context)


def createSchedule(availability): 
    print('running create schedule')
    schedule_list = []
    schedule = Schedule
    for s in Schedule.objects.all():
        schedule_list.append((s.shift, s.date))
    if schedule_list:
        try:
            schedule = Schedule.objects.get(date=availability.date, shift=availability.shift)
            print(schedule)
            if schedule:
                if availability.user == schedule.employee: # if user is same, override schedule
                    updateSchedule(availability)
                    return
                elif availability.rank < schedule.rank: # if the availability rank is higher than the rank in existing availability data
                    print('updating schedule to user with higher rank')
                    updateSchedule(availability)
                    return
        except schedule.DoesNotExist:
            print('schedule does not exist')
            saveSchedule(availability)
            return  
    else:
        print('no schedule_list exists, saving new schedule')
        saveSchedule(availability)


def saveSchedule(availability):
    print('running save schedule')
    print('adding user to specific shift in schedule')
    schedule = Schedule()
    schedule.date = availability.date
    schedule.shift = availability.shift
    schedule.employee = availability.user
    schedule.rank = availability.rank
    schedule.save()
    print('schedule created')


def updateSchedule(availability):
    print('running update schedule')
    #retrieve the schedule with the same date and shift as availability
    schedule = Schedule.objects.get(date=availability.date, shift=availability.shift)
    schedule.employee = availability.user
    schedule.rank = availability.rank
    schedule.save()
    print('schedule updated')


@login_required(login_url='login')
def updateAvailability(request, pk):
    availability = Availability.objects.get(id=pk)
    form = ShiftForm(instance=availability)

    if request.method == 'POST':
        try:
            form = ShiftForm(request.POST, instance=availability)
            if form.is_valid():
                form.save()
                new_availability = Availability.objects.get(id=pk)
                messages.success(request, 'Availability updated')
                createSchedule(new_availability)
                return redirect('myavailability')
        except IntegrityError as e:
            messages.error(request, 'Shift already added on that date OR another shift has already been ranked the same')
            return redirect('shiftavailability')
    context = {'form': form}
    return render(request, 'account/shift.html', context)


@login_required(login_url='login')
def deleteAvailability(request, pk):
    availability = Availability.objects.get(id=pk)
    schedule = Schedule
    if request.method == "POST":
        try:
            schedule = Schedule.objects.get(employee=availability.user, date=availability.date, shift=availability.shift)
            schedule.delete()
            availability.delete()
            return redirect('myavailability')
        except schedule.DoesNotExist:
            availability.delete()
            return redirect('myavailability')
    context = {'item':availability}
    return render(request, 'account/delete.html', context)