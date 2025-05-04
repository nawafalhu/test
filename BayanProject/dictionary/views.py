from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.utils.text import slugify
from .models import DictionaryVideo
import os

# Dictionary data structure (you can move this to a database later)
DICTIONARY_DATA = {
    'alphabet': {
        'title': 'Alphabet Signs',
        'description': 'Learn the basic alphabet in sign language',
        'chapter': 1,
        'category': 'Alphabet Signs',
        'content': 'Content for Alphabet Signs lesson will go here.'
    },
    'numbers': {
        'title': 'Numbers Signs',
        'description': 'Master numbers from 0 to 100',
        'chapter': 2,
        'category': 'Numbers Signs',
        'content': 'Content for Numbers Signs lesson will go here.'
    },
    'common_words': {
        'title': 'Common Words Signs',
        'description': 'Essential everyday words and phrases',
        'chapter': 3,
        'category': 'Common Words Signs',
        'content': 'Content for Common Words Signs lesson will go here.'
    }
}

# Chapter 2 lessons structure
CHAPTER2_LESSONS = {
    'lesson1': {
        'title': 'Basic Numbers',
        'description': 'Learn numbers from 0 to 9',
        'videos': [
            {'title': 'Number 0', 'path': 'chapter2/0.mp4'},
            {'title': 'Number 1', 'path': 'chapter2/1.mp4'},
            {'title': 'Number 2', 'path': 'chapter2/2.mp4'},
            {'title': 'Number 3', 'path': 'chapter2/3.mp4'},
            {'title': 'Number 4', 'path': 'chapter2/4.mp4'},
        ]
    },
    'lesson2': {
        'title': 'Tens Numbers',
        'description': 'Learn numbers from 10 to 90',
        'videos': [
            {'title': 'Number 10', 'path': 'chapter2/10.mp4'},
            {'title': 'Number 20', 'path': 'chapter2/20.mp4'},
            {'title': 'Number 30', 'path': 'chapter2/30.mp4'},
            {'title': 'Number 40', 'path': 'chapter2/40.mp4'},
            {'title': 'Number 50', 'path': 'chapter2/50.mp4'},
        ]
    },
    'lesson3': {
        'title': 'Advanced Numbers',
        'description': 'Learn numbers from 100 to 1000',
        'videos': [
            {'title': 'Number 100', 'path': 'chapter2/100.mp4'},
            {'title': 'Number 200', 'path': 'chapter2/200.mp4'},
            {'title': 'Number 500', 'path': 'chapter2/500.mp4'},
            {'title': 'Number 1000', 'path': 'chapter2/1000.mp4'},
            {'title': 'Number 2000', 'path': 'chapter2/2000.mp4'},
        ]
    }
}

@login_required
def dictionary_home(request):
    search_query = request.GET.get('q', '').lower()
    
    # Arabic alphabet letters and their English names
    letters = [
        {'letter': 'ا', 'name': 'Alif'},
        {'letter': 'ب', 'name': 'Ba'},
        {'letter': 'ت', 'name': 'Ta'},
        {'letter': 'ث', 'name': 'Tha'},
        {'letter': 'ج', 'name': 'Jeem'},
        {'letter': 'ح', 'name': 'Ha'},
        {'letter': 'خ', 'name': 'Kha'},
        {'letter': 'د', 'name': 'Dal'},
        {'letter': 'ذ', 'name': 'Dhal'},
        {'letter': 'ر', 'name': 'Ra'},
        {'letter': 'ز', 'name': 'Za'},
        {'letter': 'س', 'name': 'Seen'},
        {'letter': 'ش', 'name': 'Sheen'},
        {'letter': 'ص', 'name': 'Sad'},
        {'letter': 'ض', 'name': 'Dad'},
        {'letter': 'ط', 'name': 'Ta'},
        {'letter': 'ظ', 'name': 'Za'},
        {'letter': 'ع', 'name': 'Ayn'},
        {'letter': 'غ', 'name': 'Ghayn'},
        {'letter': 'ف', 'name': 'Fa'},
        {'letter': 'ق', 'name': 'Qaf'},
        {'letter': 'ك', 'name': 'Kaf'},
        {'letter': 'ل', 'name': 'Lam'},
        {'letter': 'م', 'name': 'Meem'},
        {'letter': 'ن', 'name': 'Noon'},
        {'letter': 'ه', 'name': 'Ha'},
        {'letter': 'و', 'name': 'Waw'},
        {'letter': 'ي', 'name': 'Ya'}
    ]

    # Numbers data (1-15)
    numbers = [
        {'number': '1', 'name': 'One'},
        {'number': '2', 'name': 'Two'},
        {'number': '3', 'name': 'Three'},
        {'number': '4', 'name': 'Four'},
        {'number': '5', 'name': 'Five'},
        {'number': '6', 'name': 'Six'},
        {'number': '7', 'name': 'Seven'},
        {'number': '8', 'name': 'Eight'},
        {'number': '9', 'name': 'Nine'},
        {'number': '10', 'name': 'Ten'},
        {'number': '11', 'name': 'Eleven'},
        {'number': '12', 'name': 'Twelve'},
        {'number': '13', 'name': 'Thirteen'},
        {'number': '14', 'name': 'Fourteen'},
        {'number': '15', 'name': 'Fifteen'}
    ]

    # Add video paths to each letter
    for letter_info in letters:
        video_file = f"{letter_info['letter']}.mp4"
        letter_info['video_path'] = f'videos/videos/{video_file}'

    # Add video paths to each number
    for number_info in numbers:
        video_file = f"{number_info['number']}.mp4"
        number_info['video_path'] = f'videos/chapter2/{video_file}'

    # Common phrases for Chapter 3
    common_phrases = [
        {'phrase': 'السلام عليكم', 'translation': 'Peace be upon you'},
        {'phrase': 'وعليكم السلام', 'translation': 'And peace be upon you'},
        {'phrase': 'صباح الخير', 'translation': 'Good morning'},
        {'phrase': 'صباح النور', 'translation': 'Good morning (response)'},
        {'phrase': 'كيف هي أمورك ؟', 'translation': '? How are things'},
        {'phrase': 'كيف صحتك ؟', 'translation': '? How is your health'},
        {'phrase': 'كيف حالك ؟', 'translation': '? How are you'},
        {'phrase': 'كيف حال أولادك ؟', 'translation': '? How are your children'},
        {'phrase': 'أتوصي بشيء ؟', 'translation': '? Do you need anything'},
        {'phrase': 'اعتن بنفسك', 'translation': 'Take care of yourself'},
        {'phrase': 'أراك قريبا', 'translation': 'See you soon'},
        {'phrase': 'مع السلامة', 'translation': 'Goodbye'},
    ]

    if search_query:
        # Filter letters and numbers based on search query
        filtered_letters = [
            letter for letter in letters
            if search_query in letter['letter'].lower() or 
            search_query in letter['name'].lower()
        ]
        letters = filtered_letters

        filtered_numbers = [
            number for number in numbers
            if search_query in number['number'].lower() or 
            search_query in number['name'].lower()
        ]
        numbers = filtered_numbers

    return render(request, 'dictionary/home.html', {
        'letters': letters,
        'numbers': numbers,
        'search_query': search_query,
        'common_phrases': common_phrases
    })

@login_required
def lesson_detail(request, lesson_key):
    lesson = DICTIONARY_DATA.get(lesson_key, {})
    if not lesson:
        return redirect('dictionary:home')
    
    # Get videos for this chapter
    videos = DictionaryVideo.objects.filter(chapter=lesson['chapter'])
        
    return render(request, 'dictionary/lesson_detail.html', {
        'lesson': lesson,
        'videos': videos
    })

@login_required
def search(request):
    search_query = request.GET.get('q', '').strip()
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if search_query:
        # Normalize the search query
        normalized_query = search_query.lower()
        
        # Search in both title and description
        videos = DictionaryVideo.objects.filter(
            Q(title__icontains=normalized_query) |
            Q(description__icontains=normalized_query)
        ).select_related('chapter')

        context = {
            'videos': videos,
            'search_query': search_query,
            'is_search': True
        }
    else:
        # Return all videos grouped by chapter
        videos = DictionaryVideo.objects.all().select_related('chapter')
        videos_by_chapter = {}
        
        for video in videos:
            if video.chapter not in videos_by_chapter:
                videos_by_chapter[video.chapter] = {
                    'title': f"Chapter {video.chapter}",
                    'videos': []
                }
            videos_by_chapter[video.chapter]['videos'].append(video)

        context = {
            'chapters': videos_by_chapter,
            'search_query': search_query,
            'is_search': False
        }

    template = 'dictionary/search_results.html' if is_ajax else 'dictionary/home.html'
    return render(request, template, context)

@login_required
def chapter_detail(request, chapter_num):
    # Get all videos for this chapter
    videos = DictionaryVideo.objects.filter(chapter=chapter_num)
    
    # Get chapter title
    chapter_title = dict(DictionaryVideo.CHAPTER_CHOICES).get(int(chapter_num), f'Chapter {chapter_num}')
    
    return render(request, 'dictionary/chapter_detail.html', {
        'videos': videos,
        'chapter_title': chapter_title,
        'chapter_num': chapter_num
    })

@login_required
def video_detail(request, video_id):
    video = get_object_or_404(DictionaryVideo, id=video_id)
    return render(request, 'dictionary/video_detail.html', {
        'video': video
    })

@login_required
def letter_detail(request, letter):
    # Names for letters
    letter_names = [
        {'letter': 'ا', 'name': 'Alif'},
        {'letter': 'ب', 'name': 'Ba'},
        {'letter': 'ت', 'name': 'Ta'},
        {'letter': 'ث', 'name': 'Tha'},
        {'letter': 'ج', 'name': 'Jeem'},
        {'letter': 'ح', 'name': 'Ha'},
        {'letter': 'خ', 'name': 'Kha'},
        {'letter': 'د', 'name': 'Dal'},
        {'letter': 'ذ', 'name': 'Dhal'},
        {'letter': 'ر', 'name': 'Ra'},
        {'letter': 'ز', 'name': 'Za'},
        {'letter': 'س', 'name': 'Seen'},
        {'letter': 'ش', 'name': 'Sheen'},
        {'letter': 'ص', 'name': 'Sad'},
        {'letter': 'ض', 'name': 'Dad'},
        {'letter': 'ط', 'name': 'Ta'},
        {'letter': 'ظ', 'name': 'Za'},
        {'letter': 'ع', 'name': 'Ayn'},
        {'letter': 'غ', 'name': 'Ghayn'},
        {'letter': 'ف', 'name': 'Fa'},
        {'letter': 'ق', 'name': 'Qaf'},
        {'letter': 'ك', 'name': 'Kaf'},
        {'letter': 'ل', 'name': 'Lam'},
        {'letter': 'م', 'name': 'Meem'},
        {'letter': 'ن', 'name': 'Noon'},
        {'letter': 'ه', 'name': 'Ha'},
        {'letter': 'و', 'name': 'Waw'},
        {'letter': 'ي', 'name': 'Ya'}
    ]
    # Numbers data
    numbers = [
        {'letter': '1', 'name': 'One'},
        {'letter': '2', 'name': 'Two'},
        {'letter': '3', 'name': 'Three'},
        {'letter': '4', 'name': 'Four'},
        {'letter': '5', 'name': 'Five'},
        {'letter': '6', 'name': 'Six'},
        {'letter': '7', 'name': 'Seven'},
        {'letter': '8', 'name': 'Eight'},
        {'letter': '9', 'name': 'Nine'},
        {'letter': '10', 'name': 'Ten'},
        {'letter': '11', 'name': 'Eleven'},
        {'letter': '12', 'name': 'Twelve'},
        {'letter': '13', 'name': 'Thirteen'},
        {'letter': '14', 'name': 'Fourteen'},
        {'letter': '15', 'name': 'Fifteen'}
    ]
    # Common phrases for Chapter 3
    common_phrases = [
        {'phrase': 'السلام عليكم', 'translation': 'Peace be upon you'},
        {'phrase': 'وعليكم السلام', 'translation': 'And peace be upon you'},
        {'phrase': 'صباح الخير', 'translation': 'Good morning'},
        {'phrase': 'صباح النور', 'translation': 'Good morning (response)'},
        {'phrase': 'كيف هي أمورك ؟', 'translation': 'How are things?'},
        {'phrase': 'كيف صحتك ؟', 'translation': 'How is your health?'},
        {'phrase': 'كيف حالك ؟', 'translation': 'How are you?'},
        {'phrase': 'كيف حال أولادك ؟', 'translation': 'How are your children?'},
        {'phrase': 'أتوصي بشيء ؟', 'translation': 'Do you need anything?'},
        {'phrase': 'اعتن بنفسك', 'translation': 'Take care of yourself'},
        {'phrase': 'أراك قريبا', 'translation': 'See you soon'},
        {'phrase': 'مع السلامة', 'translation': 'Goodbye'},
    ]
    # Check if it's a letter
    letter_info = next((l for l in letter_names if l['letter'] == letter), None)
    if letter_info:
        video_path = f'videos/videos/{letter}.mp4'
        template = 'dictionary/letter_detail.html'
        context = {
            'letter': letter,
            'letter_name': letter_info['name'],
            'video_path': video_path
        }
        return render(request, template, context)
    # Check if it's a number
    number_info = next((n for n in numbers if n['letter'] == letter), None)
    if number_info:
        video_path = f'videos/chapter2/{letter}.mp4'
        template = 'dictionary/number_detail.html'
        context = {
            'letter': letter,
            'letter_name': number_info['name'],
            'video_path': video_path
        }
        return render(request, template, context)
    # Check if it's a phrase
    phrase_info = next((p for p in common_phrases if p['phrase'] == letter), None)
    if phrase_info:
        video_path = f'chapter3/{letter}.mp4'
        template = 'dictionary/phrase_detail.html'
        context = {
            'phrase': letter,
            'translation': phrase_info['translation'],
            'video_path': video_path
        }
        return render(request, template, context)
    return redirect('dictionary:home') 