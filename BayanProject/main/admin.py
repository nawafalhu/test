from django.contrib import admin

# Register your models here.
# userName: mohamad
# PassWord: 123123
from .models import Video, QuizScore, dictionary

admin.site.register(Video)
admin.site.register(QuizScore)
admin.site.register(dictionary)