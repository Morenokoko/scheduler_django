from django.urls import path
from datetime import datetime
from . import views



urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
	path('myavailability/', views.myavailability, name="myavailability"),
	path('shift/', views.shiftavailability, name="shiftavailability"),
	path('view_schedules/', views.viewSchedules, name="view_schedules"),
	path('update_availability/<str:pk>/', views.updateAvailability, name="update_availability"),
	path('delete_availability/<str:pk>/', views.deleteAvailability, name="delete_availability"),

    path('', views.index, name="index"),

]