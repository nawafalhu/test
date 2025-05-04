from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Home page
    path('signup/', views.signup, name='signup'),
    path('sign-practice/', views.sign_practice, name='sign_practice'),
    path('lesson/<int:chapter>/', views.lesson_list, name='lesson_list'),
    path('lesson/<int:chapter>/<int:lesson>/', views.lesson_view, name='lesson_view'),
    path('mark-lesson-complete/', views.mark_lesson_complete, name='mark_lesson_complete'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz/start/<int:chapter>/', views.quiz_start, name='quiz_start'),
    path('quiz/question/<int:question_number>/', views.quiz_question, name='quiz_question'),
    path('profile/', views.profile_view, name='profile'),
    path('alphabet-practice/', views.alphabet_practice, name='alphabet_practice'),
    path('letter/<str:letter>/', views.letter_detail, name='letter_detail'),
    path('number/<int:number>/', views.number_detail, name='number_detail'),
    path('accounts/', include('django.contrib.auth.urls')),
]

