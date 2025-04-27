from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.template.defaulttags import register
import random
import os
from django.conf import settings

@login_required
def home(request):
    return render(request, 'main/home.html')

@login_required
def sign_practice(request):
    return render(request, 'main/sign_practice.html')

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove all help_texts
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None
        
        # Customize labels
        self.fields['username'].label = 'Username'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

def get_chapter_info(chapter):
    chapters = {
        1: {
            'title': 'Alphabet Signs',
            'description': 'Learn the fundamental alphabet signs for fingerspelling.',
            'lessons': [
                {'number': 1, 'title': 'Alphabet Signs', 'description': 'Discover new vocabulary', 'type': 'vocabulary'},
                {'number': 2, 'title': 'Numbers Signs', 'description': 'Discover new vocabulary', 'type': 'dialogue'},
                {'number': 3, 'title': 'Greetings Signs', 'description': 'Learn iconic signs', 'type': 'signs'},
                {'number': 4, 'title': 'Basic Signs Review', 'description': 'Review new signs', 'type': 'review'}
            ]
        },
        2: {
            'title': 'Numbers Signs',
            'description': 'Master signs for numbers and counting.',
            'lessons': [
                {'number': 1, 'title': 'Common Phrases', 'description': 'Discover new vocabulary', 'type': 'vocabulary'},
                {'number': 2, 'title': 'Family Members', 'description': 'Practice a dialogue', 'type': 'dialogue'},
                {'number': 3, 'title': 'Weather Terms', 'description': 'Learn iconic signs', 'type': 'signs'},
                {'number': 4, 'title': 'Daily Review', 'description': 'Review daily signs', 'type': 'review'}
            ]
        },
        3: {
            'title': 'Common Words',
            'description': 'Learn essential words and phrases for everyday communication.',
            'lessons': [
                {'number': 1, 'title': 'Emotions & Feelings', 'description': 'Discover new vocabulary', 'type': 'vocabulary'},
                {'number': 2, 'title': 'Time & Calendar', 'description': 'Practice a dialogue', 'type': 'dialogue'},
                {'number': 3, 'title': 'Colors & Objects', 'description': 'Learn iconic signs', 'type': 'signs'},
                {'number': 4, 'title': 'Intermediate Review', 'description': 'Review intermediate signs', 'type': 'review'}
            ]
        },
        4: {
            'title': 'Daily Communication',
            'description': 'Practice everyday conversations and interactions.',
            'lessons': [
                {'number': 1, 'title': 'Complex Sentences', 'description': 'Discover new vocabulary', 'type': 'vocabulary'},
                {'number': 2, 'title': 'Questions & Answers', 'description': 'Practice a dialogue', 'type': 'dialogue'},
                {'number': 3, 'title': 'Story Telling', 'description': 'Learn iconic signs', 'type': 'signs'},
                {'number': 4, 'title': 'Advanced Review', 'description': 'Review advanced signs', 'type': 'review'}
            ]
        }
    }
    return chapters.get(chapter, None)

@login_required
def lesson_list(request, chapter):
    chapter_info = get_chapter_info(chapter)
    if chapter_info is None:
        return redirect('home')
        
    context = {
        'chapter': {
            'number': chapter,
            'title': chapter_info['title'],
            'description': chapter_info['description']
        },
        'lessons': chapter_info['lessons']
    }
    return render(request, 'main/lesson_list.html', context)

def get_lesson_title(chapter, lesson):
    chapter_info = get_chapter_info(chapter)
    if chapter_info:
        for lesson_info in chapter_info['lessons']:
            if lesson_info['number'] == lesson:
                return lesson_info['title']
    return "Lesson Not Found"

def lesson_view(request, chapter, lesson):
    lesson_title = get_lesson_title(chapter, lesson)
    return render(request, 'main/lesson.html', {
        'chapter': chapter,
        'lesson': lesson,
        'lesson_title': lesson_title
    })

@login_required
def quiz(request):
    return render(request, 'main/quiz.html')

@login_required
def quiz_start(request, chapter):
    return render(request, 'main/quiz_start.html', {'chapter': chapter})

@login_required
def profile_view(request):
    return render(request, 'main/profile.html')

def alphabet_practice(request):
    # قائمة الأحرف الأبجدية العربية
    letters = ['ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي']
    
    # أسماء الأحرف
    letter_names = {
        'ا': 'Alif',
        'ب': 'Ba',
        'ت': 'Ta',
        'ث': 'Tha',
        'ج': 'Jeem',
        'ح': 'Ha',
        'خ': 'Kha',
        'د': 'Dal',
        'ذ': 'Dhal',
        'ر': 'Ra',
        'ز': 'Za',
        'س': 'Seen',
        'ش': 'Sheen',
        'ص': 'Sad',
        'ض': 'Dad',
        'ط': 'Ta',
        'ظ': 'Za',
        'ع': 'Ayn',
        'غ': 'Ghayn',
        'ف': 'Fa',
        'ق': 'Qaf',
        'ك': 'Kaf',
        'ل': 'Lam',
        'م': 'Meem',
        'ن': 'Noon',
        'ه': 'Ha',
        'و': 'Waw',
        'ي': 'Ya'
    }
    
    context = {
        'letters': letters,
        'letter_names': letter_names
    }
    return render(request, 'main/alphabet_practice.html', context)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def letter_detail(request, letter):
    # أسماء الأحرف
    letter_names = {
        'ا': 'Alif',
        'ب': 'Ba',
        'ت': 'Ta',
        'ث': 'Tha',
        'ج': 'Jeem',
        'ح': 'Ha',
        'خ': 'Kha',
        'د': 'Dal',
        'ذ': 'Dhal',
        'ر': 'Ra',
        'ز': 'Za',
        'س': 'Seen',
        'ش': 'Sheen',
        'ص': 'Sad',
        'ض': 'Dad',
        'ط': 'Ta',
        'ظ': 'Za',
        'ع': 'Ayn',
        'غ': 'Ghayn',
        'ف': 'Fa',
        'ق': 'Qaf',
        'ك': 'Kaf',
        'ل': 'Lam',
        'م': 'Meem',
        'ن': 'Noon',
        'ه': 'Ha',
        'و': 'Waw',
        'ي': 'Ya'
    }
    
    context = {
        'letter': letter,
        'letter_name': letter_names.get(letter, 'Unknown')
    }
    return render(request, 'main/letter_detail.html', context)

def get_arabic_letters():
    return ['أ', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي']

def quiz_question(request, question_number):
    # الحصول على قائمة الفيديوهات
    videos_dir = os.path.join(settings.MEDIA_ROOT, 'dictionary', 'videos')
    video_files = [f for f in os.listdir(videos_dir) if f.endswith('.mp4')]
    video_files.sort()  # ترتيب الملفات أبجدياً
    
    # التأكد من أن رقم السؤال ضمن النطاق
    if question_number > len(video_files):
        return render(request, 'main/quiz_complete.html')
    
    # الحصول على الفيديو الحالي
    current_video = video_files[question_number - 1]
    correct_answer = current_video.replace('.mp4', '')
    
    # الحصول على قائمة الحروف العربية
    all_letters = get_arabic_letters()
    
    # إزالة الإجابة الصحيحة من القائمة إذا كانت موجودة
    if correct_answer in all_letters:
        all_letters.remove(correct_answer)
    
    # اختيار 3 حروف عشوائية
    wrong_answers = random.sample(all_letters, 3)
    
    # دمج الإجابة الصحيحة مع الإجابات الخاطئة
    all_options = wrong_answers + [correct_answer]
    random.shuffle(all_options)  # خلط الخيارات
    
    context = {
        'question_number': question_number,
        'video_path': f'/static/dictionary/videos/videos/{current_video}',
        'options': all_options,
        'correct_answer': correct_answer,
        'total_questions': len(video_files)
    }
    
    return render(request, 'main/quiz_question.html', context)
