from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db import IntegrityError

# Create your views here.
from .models import *
from .forms import * 
from .filters import *

# date_today = timezone.datetime.today()

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

    print('SCHEDULE DATE LISTTTTTT',schedule_date_list)
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
    availability_list = Availability.objects.filter(user = request.user).order_by('-date','-shift')
    availability_date_list = []

    myFilter = AvailabilityFilter(request.GET, queryset=availability_list)
    availability_list = myFilter.qs 

    for i in availability_list:
        if i.date not in availability_date_list:
            availability_date_list.append(i.date)

    context = {'availability_list': availability_list, 'availability_date_list': availability_date_list,  'myFilter': myFilter}
    return render(request, 'account/myavailability.html', context)

@login_required(login_url='login')
def shiftavailability(request):
    user=request.user
    form = ShiftForm()
    if request.method == 'POST':
        try:
            form = ShiftForm(request.POST)
            if form.is_valid():
                availability = form.save(commit=False)
                availability.user = user
                availability.save()
                print(availability.date, availability.shift, availability.rank)
                createSchedule(availability)
                messages.success(request, 'Availability updated')
                return redirect('myavailability')
            else:
                print(form.errors)
        except IntegrityError as e:
            messages.error(request, 'Shift already added on that date OR another shift has already been ranked the same')
            return redirect('shiftavailability')
    context = {'form':form}
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