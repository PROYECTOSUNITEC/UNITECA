from django.urls import path
from .views import *

from . import views

urlpatterns = [
    path("hello/", views.hello_world, name="hello-world"),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]