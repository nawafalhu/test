from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.template.defaulttags import register
import random
import os
from django.conf import settings
from .models import QuizScore, UserProgress
from django.http import JsonResponse
from django.db.models import Max
from django.templatetags.static import static

@register.filter
def multiply(value, arg):
    """Multiply the arg by the value."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return ''

@login_required
def home(request):
    # Get completed lessons count for chapter 1
    chapter1_completed_count = UserProgress.objects.filter(
        user=request.user,
        chapter=1
    ).count()
    # Get completed lessons count for chapter 2
    chapter2_completed_count = UserProgress.objects.filter(
        user=request.user,
        chapter=2
    ).count()
    # Get completed lessons count for chapter 3
    chapter3_completed_count = UserProgress.objects.filter(
        user=request.user,
        chapter=3
    ).count()
    return render(request, 'main/home.html', {
        'chapter1_completed_count': chapter1_completed_count,
        'chapter2_completed_count': chapter2_completed_count,
        'chapter3_completed_count': chapter3_completed_count
    })

@login_required
def sign_practice(request):
    letter = request.GET.get('letter')
    chapter = request.GET.get('chapter')
    if chapter == '2':
        # Numbers Practice: show numbers 1-15
        numbers = list(range(1, 16))
        number_words = [
            '', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
            'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen'
        ]
        context = {
            'numbers': numbers,
            'selected_number': letter,  # for consistency, use 'letter' param for number too
            'video_url': f'videos/{letter}.mp4' if letter else None,
            'is_numbers': True,
            'number_words': number_words
        }
    else:
        context = {
            'letter': letter,
            'video_url': f'videos/{letter}.mp4' if letter else None,
            'is_numbers': False
        }
    return render(request, 'main/sign_practice.html', context)

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
                {'number': 3, 'title': 'Weather Terms', 'description': 'Learn iconic signs', 'type': 'signs'}
            ]
        },
        3: {
            'title': 'Common words',
            'description': 'Learn essential words and phrases for everyday communication.',
            'lessons': [
                {'number': 1, 'title': 'Emotions & Feelings', 'description': 'Discover new vocabulary', 'type': 'vocabulary'},
                {'number': 2, 'title': 'Time & Calendar', 'description': 'Practice a dialogue', 'type': 'dialogue'},
                {'number': 3, 'title': 'Colors & Objects', 'description': 'Learn iconic signs', 'type': 'signs'},
                {'number': 4, 'title': 'Intermediate Review', 'description': 'Review intermediate signs', 'type': 'review'}
            ]
        }
    }
    return chapters.get(chapter, None)

@login_required
def lesson_list(request, chapter):
    # Get user's completed lessons for this chapter
    completed_lessons = list(UserProgress.objects.filter(
        user=request.user,
        chapter=chapter
    ).values_list('lesson', flat=True))

    # Get the last completed lesson number
    last_completed = UserProgress.objects.filter(
        user=request.user,
        chapter=chapter
    ).aggregate(Max('lesson'))['lesson__max'] or 0

    # Calculate next lesson
    max_lesson = 3 if int(chapter) == 2 else 4
    next_lesson = min(last_completed + 1, max_lesson)
        
    context = {
        'chapter': {'number': chapter, 'title': get_chapter_title(chapter)},
        'lessons': get_chapter_lessons(chapter),
        'completed_lessons': completed_lessons,
        'next_lesson': next_lesson
    }
    return render(request, 'main/lesson_list.html', context)

@login_required
def lesson_view(request, chapter, lesson):
    lesson_title = get_lesson_title(chapter, lesson)
    context = {
        'chapter': chapter,
        'lesson': lesson,
        'lesson_title': lesson_title
    }
    return render(request, 'main/lesson.html', context)

@login_required
def mark_lesson_complete(request):
    if request.method == 'POST':
        chapter = int(request.POST.get('chapter'))
        lesson = int(request.POST.get('lesson'))
        
        # Create or update progress
        UserProgress.objects.get_or_create(
            user=request.user,
            chapter=chapter,
            lesson=lesson
        )
        
        # Calculate next lesson
        max_lesson = 3 if chapter == 2 else 4
        next_lesson = min(lesson + 1, max_lesson)
        
        return JsonResponse({
            'status': 'success',
            'next_lesson': next_lesson,
            'completed_lessons': list(UserProgress.objects.filter(
                user=request.user,
                chapter=chapter
            ).values_list('lesson', flat=True))
        })
    
    return JsonResponse({'status': 'error'}, status=400)

def get_chapter_title(chapter):
    titles = {
        1: 'Alphabet Signs',
        2: 'Numbers Signs',
        3: 'Common Words'
    }
    return titles.get(chapter, '')

def get_chapter_lessons(chapter):
    # You can customize this based on your needs
    max_lesson = 3 if int(chapter) == 2 else 4
    return [
        {'number': i, 'type': 'signs', 'description': f'Lesson {i}'}
        for i in range(1, max_lesson + 1)
    ]

def get_lesson_title(chapter, lesson):
    chapter_info = get_chapter_info(chapter)
    if chapter_info:
        for lesson_info in chapter_info['lessons']:
            if lesson_info['number'] == lesson:
                return lesson_info['title']
    return "Lesson Not Found"

@login_required
def quiz(request):
    # Get the last score for the current user in Chapter 1
    last_score = QuizScore.objects.filter(
        user=request.user,
        chapter=1
    ).order_by('-date_taken').first()
    # Get the last score for the current user in Chapter 2
    last_score_ch2 = QuizScore.objects.filter(
        user=request.user,
        chapter=2
    ).order_by('-date_taken').first()
    # Get the last score for the current user in Chapter 3
    last_score_ch3 = QuizScore.objects.filter(
        user=request.user,
        chapter=3
    ).order_by('-date_taken').first()
    
    # Reset the quiz session when viewing the quiz page
    if 'correct_answers' in request.session:
        del request.session['correct_answers']
    if 'quiz_progress' in request.session:
        del request.session['quiz_progress']
    request.session.modified = True
    
    return render(request, 'main/quiz.html', {
        'last_score': last_score,
        'last_score_ch2': last_score_ch2,
        'last_score_ch3': last_score_ch3
    })

@login_required
def quiz_start(request, chapter):
    # Store the current quiz chapter in session
    request.session['quiz_chapter'] = int(chapter)
    return render(request, 'main/quiz_start.html', {'chapter': chapter})

@login_required
def profile_view(request):
    return render(request, 'main/profile.html')

def alphabet_practice(request):
    # Get the selected letter from query parameters
    selected_letter = request.GET.get('letter')
    
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
        'letter_names': letter_names,
        'selected_letter': selected_letter
    }
    return render(request, 'main/alphabet_practice.html', context)

@register.filter
def get_item(obj, key):
    try:
        if isinstance(obj, dict):
            return obj.get(key)
        elif isinstance(obj, list):
            return obj[int(key)]
    except (KeyError, IndexError, ValueError, TypeError):
        return ''
    return ''

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
    
    # Define which lesson each letter belongs to
    lesson_mapping = {
        'ا': 1, 'ب': 1, 'ت': 1, 'ث': 1, 'ج': 1, 'ح': 1, 'خ': 1,  # Lesson 1
        'د': 2, 'ذ': 2, 'ر': 2, 'ز': 2, 'س': 2, 'ش': 2, 'ص': 2,  # Lesson 2
        'ض': 3, 'ط': 3, 'ظ': 3, 'ع': 3, 'غ': 3, 'ف': 3, 'ق': 3,  # Lesson 3
        'ك': 4, 'ل': 4, 'م': 4, 'ن': 4, 'ه': 4, 'و': 4, 'ي': 4   # Lesson 4
    }
    
    # Get the lesson number for this letter
    lesson_number = lesson_mapping.get(letter, 1)
    
    context = {
        'letter': letter,
        'letter_name': letter_names.get(letter, 'Unknown'),
        'lesson_number': lesson_number
    }
    return render(request, 'main/letter_detail.html', context)

def get_arabic_letters():
    # Return exactly the same letters as the video filenames
    return ['ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي']

@login_required
def quiz_question(request, question_number):
    # Allow chapter selection via GET parameter for direct links
    chapter_param = request.GET.get('chapter')
    if chapter_param:
        request.session['quiz_chapter'] = int(chapter_param)
    chapter = request.session.get('quiz_chapter', 1)
    
    print(f"\n[QUIZ DEBUG] Question {question_number}")
    
    # Initialize session variables if they don't exist
    if 'correct_answers' not in request.session:
        request.session['correct_answers'] = []
    if 'quiz_progress' not in request.session:
        request.session['quiz_progress'] = []
    
    request.session.modified = True

    # If all questions are answered, show completion page
    if question_number > 10:
        correct_answers = request.session.get('correct_answers', [])
        final_score = len([ans for ans in correct_answers if ans.get('correct', False)])
        print(f"[QUIZ COMPLETE] Final score: {final_score}/10")
        print(f"[QUIZ COMPLETE] Answers: {correct_answers}")
        
        # Save the quiz score for the correct chapter
        QuizScore.objects.update_or_create(
            user=request.user,
            chapter=chapter,
            defaults={
                'score': final_score,
                'total_questions': 10
            }
        )
        
        context = {
            'score': final_score,
            'total_questions': 10,
            'results': correct_answers,
            'chapter': chapter
        }
        
        # Clear session for next quiz
        request.session['correct_answers'] = []
        request.session['quiz_progress'] = []
        request.session.modified = True
        
        return render(request, 'main/quiz_complete.html', context)

    # Handle POST request (answer submission) before generating new question
    if request.method == 'POST':
        user_answer = request.POST.get('selected_answer')
        stored_video = request.session.get('current_video')
        stored_answer = request.session.get('current_correct_answer')
        
        print("\n[QUIZ DEBUG] Processing Answer Submission:")
        print(f"- Question: {question_number}")
        print(f"- Stored video: {stored_video}")
        print(f"- Stored correct answer: {stored_answer}")
        print(f"- User answer: {user_answer}")
        
        if stored_video and stored_answer:
            # Get current correct answers list
            correct_answers = request.session.get('correct_answers', [])
            
            # Check if answer is correct
            is_correct = user_answer == stored_answer
            
            # Record the answer
            answer_record = {
                'question': question_number,
                'letter': stored_answer,
                'correct': is_correct,
                'user_answer': user_answer,
                'video_name': stored_video
            }
            
            correct_answers.append(answer_record)
            request.session['correct_answers'] = correct_answers
            request.session.modified = True
            
            print(f"[QUIZ DEBUG] Answer recorded: {answer_record}")
        
        # Clear current question data
        request.session.pop('current_video', None)
        request.session.pop('current_correct_answer', None)
        request.session.modified = True
        
        return redirect('quiz_question', question_number=question_number + 1)

    # Generate new question
    if chapter == 2:
        # Numbers quiz: use static/chapter2/1.mp4 ... 15.mp4
        numbers_dir = os.path.join(settings.BASE_DIR, 'static', 'chapter2')
        video_files = [f for f in os.listdir(numbers_dir) if f.endswith('.mp4')]
        video_numbers = [f.replace('.mp4', '') for f in video_files]
        # Only use numbers 1-15
        video_files = [f for f in video_files if f.replace('.mp4', '').isdigit() and 1 <= int(f.replace('.mp4', '')) <= 15]
        video_numbers = [f.replace('.mp4', '') for f in video_files]
        # Sort by number
        video_files = sorted(video_files, key=lambda x: int(x.replace('.mp4', '')))
        video_numbers = sorted(video_numbers, key=lambda x: int(x))
        if not video_files:
            return render(request, 'main/quiz_error.html', {
                'error': 'No number videos available for the quiz.'
            })
        used_videos = request.session.get('quiz_progress', [])
        available_videos = [(v, n) for v, n in zip(video_files, video_numbers) if v not in used_videos]
        if not available_videos:
            return redirect('quiz_question', question_number=11)
        current_video, correct_number = random.choice(available_videos)
        used_videos.append(current_video)
        request.session['quiz_progress'] = used_videos
        request.session['current_video'] = current_video
        request.session['current_correct_answer'] = str(int(correct_number))
        request.session.modified = True
        # Prepare options as numbers
        all_numbers = list(range(1, 16))
        other_numbers = [n for n in all_numbers if n != int(correct_number)]
        wrong_answers = random.sample(other_numbers, 3)
        all_options = [str(n) for n in wrong_answers] + [str(int(correct_number))]
        random.shuffle(all_options)
        current_score = len([ans for ans in request.session.get('correct_answers', []) if ans.get('correct', False)])
        video_url = static('chapter2/' + current_video)
        return render(request, 'main/quiz_question.html', {
            'question_number': question_number,
            'total_questions': 10,
            'video_path': video_url,
            'options': all_options,
            'correct_answer': str(int(correct_number)),
            'current_score': current_score,
            'debug': True,
            'current_video': current_video,
            'chapter': chapter
        })
    elif chapter == 3:
        # Chapter 3: Common phrases quiz using static/chapter3/*.mp4
        phrases_dir = os.path.join(settings.BASE_DIR, 'static', 'chapter3')
        video_files = [f for f in os.listdir(phrases_dir) if f.endswith('.mp4')]
        phrase_names = [f.replace('.mp4', '') for f in video_files]
        if not video_files:
            return render(request, 'main/quiz_error.html', {
                'error': 'No phrase videos available for the quiz.'
            })
        used_videos = request.session.get('quiz_progress', [])
        available_videos = [(v, n) for v, n in zip(video_files, phrase_names) if v not in used_videos]
        if not available_videos:
            return redirect('quiz_question', question_number=11)
        current_video, correct_phrase = random.choice(available_videos)
        used_videos.append(current_video)
        request.session['quiz_progress'] = used_videos
        request.session['current_video'] = current_video
        request.session['current_correct_answer'] = correct_phrase
        request.session.modified = True
        # Prepare options as phrases
        other_phrases = [n for n in phrase_names if n != correct_phrase]
        wrong_answers = random.sample(other_phrases, 3)
        all_options = wrong_answers + [correct_phrase]
        random.shuffle(all_options)
        current_score = len([ans for ans in request.session.get('correct_answers', []) if ans.get('correct', False)])
        video_url = static('chapter3/' + current_video)
        return render(request, 'main/quiz_question.html', {
            'question_number': question_number,
            'total_questions': 10,
            'video_path': video_url,
            'options': all_options,
            'correct_answer': correct_phrase,
            'current_score': current_score,
            'debug': True,
            'current_video': current_video,
            'chapter': chapter
        })
    else:
        # Chapter 1 (default): Arabic letters
        videos_dir = os.path.join(settings.STATIC_ROOT, 'videos', 'videos')
        if not os.path.exists(videos_dir):
            videos_dir = os.path.join(settings.BASE_DIR, 'static', 'videos', 'videos')
        video_files = [f for f in os.listdir(videos_dir) if f.endswith('.mp4')]
        video_letters = [f.replace('.mp4', '') for f in video_files]
        print(f"\n[QUIZ DEBUG] Available videos and letters:")
        for v, l in zip(video_files, video_letters):
            print(f"- Video: {v}, Letter: {l}")
        if not video_files:
            return render(request, 'main/quiz_error.html', {
                'error': 'No videos available for the quiz.'
            })
        used_videos = request.session.get('quiz_progress', [])
        available_videos = [(v, l) for v, l in zip(video_files, video_letters) if v not in used_videos]
        if not available_videos:
            return redirect('quiz_question', question_number=11)
        current_video, correct_answer = random.choice(available_videos)
        used_videos.append(current_video)
        request.session['quiz_progress'] = used_videos
        request.session['current_video'] = current_video
        request.session['current_correct_answer'] = correct_answer
        request.session.modified = True
        all_letters = get_arabic_letters()
        other_letters = [l for l in all_letters if l != correct_answer]
        wrong_answers = random.sample(other_letters, 3)
        all_options = wrong_answers + [correct_answer]
        random.shuffle(all_options)
        current_score = len([ans for ans in request.session.get('correct_answers', []) if ans.get('correct', False)])
        video_url = f'/static/videos/videos/{current_video}'
        return render(request, 'main/quiz_question.html', {
            'question_number': question_number,
            'total_questions': 10,
            'video_path': video_url,
            'options': all_options,
            'correct_answer': correct_answer,
            'current_score': current_score,
            'debug': True,
            'current_video': current_video,
            'chapter': chapter
        })

def number_detail(request, number):
    number_words = [
        '', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
        'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen'
    ]
    number = int(number)
    lesson_number = ((number - 1) // 5) + 1
    context = {
        'number': number,
        'number_word': number_words[number] if 1 <= number <= 15 else 'Unknown',
        'lesson_number': lesson_number,
        'chapter': 2,
    }
    return render(request, 'main/number_detail.html', context)
