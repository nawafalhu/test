from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def quiz_home(request):
    return render(request, 'quiz/home.html')

@login_required
def quiz_start(request, chapter):
    return render(request, 'quiz/start.html', {'chapter': chapter}) 