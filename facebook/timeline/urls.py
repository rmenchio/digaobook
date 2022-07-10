from django.urls import path

from . import views

app_name = 'timeline'

urlpatterns = [
    path('', views.Timeline.as_view(), name='index'),
]