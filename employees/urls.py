from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('add/', views.addEmployee, name="add_employee"),
    path('signin/', views.signin, name="signin"), 
    path('signout/',views.signout, name="signout"),
]