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
from .models import QuizScore

@login_required
def home(request):
    return render(request, 'main/home.html')

@login_required
def sign_practice(request):
    letter = request.GET.get('letter')
    context = {
        'letter': letter,
        'video_url': f'videos/{letter}.mp4' if letter else None,
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
    # Get the last score for the current user in Chapter 1
    last_score = QuizScore.objects.filter(
        user=request.user,
        chapter=1
    ).order_by('-date_taken').first()
    
    # Reset the quiz session when viewing the quiz page
    if 'correct_answers' in request.session:
        del request.session['correct_answers']
    if 'quiz_progress' in request.session:
        del request.session['quiz_progress']
    request.session.modified = True
    
    return render(request, 'main/quiz.html', {
        'last_score': last_score
    })

@login_required
def quiz_start(request, chapter):
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
        
        # Save the quiz score
        chapter = 1  # Currently only Chapter 1 is implemented
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
            'results': correct_answers
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
    videos_dir = os.path.join(settings.STATIC_ROOT, 'videos', 'videos')
    if not os.path.exists(videos_dir):
        videos_dir = os.path.join(settings.BASE_DIR, 'static', 'videos', 'videos')
    
    # Get list of video files and their corresponding letters
    video_files = [f for f in os.listdir(videos_dir) if f.endswith('.mp4')]
    video_letters = [f.replace('.mp4', '') for f in video_files]
    
    print(f"\n[QUIZ DEBUG] Available videos and letters:")
    for v, l in zip(video_files, video_letters):
        print(f"- Video: {v}, Letter: {l}")
    
    if not video_files:
        return render(request, 'main/quiz_error.html', {
            'error': 'No videos available for the quiz.'
        })

    # Get a random video that hasn't been used yet
    used_videos = request.session.get('quiz_progress', [])
    available_videos = [(v, l) for v, l in zip(video_files, video_letters) if v not in used_videos]
    
    if not available_videos:
        return redirect('quiz_question', question_number=11)  # Redirect to completion

    # Select random video and get its letter
    current_video, correct_answer = random.choice(available_videos)
    used_videos.append(current_video)
    request.session['quiz_progress'] = used_videos
    
    # Store current video and answer in session
    request.session['current_video'] = current_video
    request.session['current_correct_answer'] = correct_answer
    request.session.modified = True
    
    print("\n[QUIZ DEBUG] New Question Generated:")
    print(f"- Question number: {question_number}")
    print(f"- Selected video: {current_video}")
    print(f"- Correct answer: {correct_answer}")
    
    # Get all possible answers
    all_letters = get_arabic_letters()
    other_letters = [l for l in all_letters if l != correct_answer]
    wrong_answers = random.sample(other_letters, 3)
    
    # Combine and shuffle all options
    all_options = wrong_answers + [correct_answer]
    random.shuffle(all_options)
    
    # Calculate current score
    current_score = len([ans for ans in request.session.get('correct_answers', []) if ans.get('correct', False)])
    
    # Create the video URL
    video_url = f'/static/videos/videos/{current_video}'
    
    return render(request, 'main/quiz_question.html', {
        'question_number': question_number,
        'total_questions': 10,
        'video_path': video_url,
        'options': all_options,
        'correct_answer': correct_answer,
        'current_score': current_score,
        'debug': True,
        'current_video': current_video
    })
