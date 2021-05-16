from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index),
    path('send_sms/', views.send_sms),
    path('get_cowin_response/', views.get_cowin_response)
]