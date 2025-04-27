from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.quiz_home, name='home'),
    path('<int:chapter>/', views.quiz_start, name='start'),
    # Add more quiz-specific URLs here
] 