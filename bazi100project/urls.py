

from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


app_name = 'myapp'

urlpatterns = [

    path("", views.index, name='index'),



]
