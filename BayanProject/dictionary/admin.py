from django.contrib import admin
from .models import DictionaryVideo

@admin.register(DictionaryVideo)
class DictionaryVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'created_at', 'updated_at')
    list_filter = ('chapter', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('chapter', 'created_at')
