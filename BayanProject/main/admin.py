from django.contrib import admin

# Register your models here.
# userName: mohamad
# PassWord: 123123
from .models import Video, QuizScore, dictionary, UserProgress, ContactMessage

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'chapter', 'lesson', 'completed_at')
    list_filter = ('chapter', 'lesson')
    search_fields = ('user__username',)

@admin.register(QuizScore)
class QuizScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'chapter', 'score', 'total_questions', 'date_taken')
    list_filter = ('chapter',)
    search_fields = ('user__username',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'subject', 'message')
    readonly_fields = ('user', 'subject', 'message', 'created_at')
    list_editable = ('is_read',)

admin.site.register(Video)
admin.site.register(dictionary)