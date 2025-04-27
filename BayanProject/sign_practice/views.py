from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def practice_home(request):
    return render(request, 'sign_practice/home.html')