from django.urls import path
from sign_practice import views

app_name = 'sign_practice'

urlpatterns = [
    path('', views.practice_home, name='home'),
    path('common-phrases/', views.common_phrases_practice, name='common_phrases_practice'),
    path('phrase/<str:phrase>/', views.phrase_detail, name='phrase_detail'),
]