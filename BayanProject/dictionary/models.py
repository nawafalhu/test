from django.db import models
from django.core.validators import FileExtensionValidator

class DictionaryVideo(models.Model):
    CHAPTER_CHOICES = [
        (1, 'Alphabet Signs'),
        (2, 'Numbers Signs'),
        (3, 'Common Words Signs'),
    ]

    chapter = models.IntegerField(choices=CHAPTER_CHOICES, help_text="Select the chapter this video belongs to")
    title = models.CharField(max_length=200, help_text="Title of the video")
    description = models.TextField(help_text="Description of the video content")
    video_file = models.FileField(
        upload_to='dictionary/videos/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'ogg'])],
        help_text="Upload video file (mp4, webm, or ogg)"
    )
    thumbnail = models.ImageField(
        upload_to='dictionary/thumbnails/',
        null=True,
        blank=True,
        help_text="Optional thumbnail image for the video"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['chapter', 'created_at']

    def __str__(self):
        return f"{self.get_chapter_display()} - {self.title}"
