from django.contrib import admin

# Register your models here.
# userName: mohamad
# PassWord: 123123
from .models import User , dictionary , Video

admin.site.register(User)
admin.site.register(dictionary)
admin.site.register(Video)