from django.urls import path
from dictionary import views

app_name = 'dictionary'

urlpatterns = [
    path('', views.dictionary_home, name='home'),
    path('lesson/<str:lesson_key>/', views.lesson_detail, name='lesson_detail'),
    path('search/', views.search, name='search'),
    path('chapter/<int:chapter_num>/', views.chapter_detail, name='chapter_detail'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    path('letter/<str:letter>/', views.letter_detail, name='letter_detail'),
    # Add more dictionary-specific URLs here
] 