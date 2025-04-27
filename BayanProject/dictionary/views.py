from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.utils.text import slugify
from .models import DictionaryVideo

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

@login_required
def dictionary_home(request):
    search_query = request.GET.get('q', '').lower()
    
    # Get all videos grouped by chapter
    videos_by_chapter = {}
    for video in DictionaryVideo.objects.all():
        if video.chapter not in videos_by_chapter:
            videos_by_chapter[video.chapter] = []
        videos_by_chapter[video.chapter].append(video)
    
    if search_query:
        # Filter dictionary items based on search query
        search_results = {
            key: value for key, value in DICTIONARY_DATA.items()
            if search_query in key.lower() or 
               search_query in value['title'].lower() or 
               search_query in value['description'].lower() or 
               search_query in value['category'].lower()
        }
        
        # Organize results by chapter
        organized_results = {}
        for key, value in search_results.items():
            chapter = value['chapter']
            if chapter not in organized_results:
                organized_results[chapter] = {
                    'title': f"Chapter {chapter}: {value['category']}",
                    'items': [],
                    'videos': videos_by_chapter.get(chapter, [])
                }
            organized_results[chapter]['items'].append({
                'key': key,
                'title': value['title'],
                'description': value['description']
            })
    else:
        # Show all items organized by chapter
        organized_results = {
            1: {
                'title': 'Chapter 1: Alphabet Signs',
                'items': [{'key': 'alphabet', **DICTIONARY_DATA['alphabet']}],
                'videos': videos_by_chapter.get(1, [])
            },
            2: {
                'title': 'Chapter 2: Numbers Signs',
                'items': [{'key': 'numbers', **DICTIONARY_DATA['numbers']}],
                'videos': videos_by_chapter.get(2, [])
            },
            3: {
                'title': 'Chapter 3: Common Words Signs',
                'items': [{'key': 'common_words', **DICTIONARY_DATA['common_words']}],
                'videos': videos_by_chapter.get(3, [])
            }
        }

    return render(request, 'dictionary/home.html', {
        'chapters': organized_results,
        'search_query': search_query
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