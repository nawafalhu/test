from django.core.management.base import BaseCommand
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Sets up the media directory structure for the application'

    def handle(self, *args, **options):
        # Create main media directory
        media_root = settings.MEDIA_ROOT
        os.makedirs(media_root, exist_ok=True)
        
        # Create chapter1 videos directory
        chapter1_videos = os.path.join(media_root, 'chapter1', 'videos')
        os.makedirs(chapter1_videos, exist_ok=True)
        
        self.stdout.write(self.style.SUCCESS('Successfully created media directory structure'))
        self.stdout.write(f'Media root: {media_root}')
        self.stdout.write(f'Chapter 1 videos: {chapter1_videos}') 