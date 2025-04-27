from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class dictionary(models.Model):
    pass

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.title
