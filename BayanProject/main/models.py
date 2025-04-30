from django.db import models
from django.contrib.auth.models import User

class dictionary(models.Model):
    pass

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.title

class QuizScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.IntegerField()
    score = models.IntegerField()
    total_questions = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'chapter')

    def __str__(self):
        return f"{self.user.username} - Chapter {self.chapter} - {self.score}/{self.total_questions}"
