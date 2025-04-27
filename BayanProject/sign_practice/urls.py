from django.urls import path
from sign_practice import views

app_name = 'sign_practice'

urlpatterns = [
    path('', views.practice_home, name='home'),
]