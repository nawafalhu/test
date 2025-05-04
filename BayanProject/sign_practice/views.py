import cv2
import torch
import numpy as np
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from torchvision import transforms
from PIL import Image
import torch.nn.functional as F
import json
import base64
import os

# Load the model once at startup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'model_7.pt')
model = torch.jit.load(model_path)  # Make sure your model is in the project root directory
model.eval()

# Define transformation for frames
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])

# Function to process frames and make predictions
def detect_sign_language(frame):
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(image)
        probabilities = F.softmax(output, dim=1)  # Convert logits to probabilities
        print("Raw Model Output:", output)  # Debugging
        prediction = probabilities.argmax(dim=1).item()
        probs = probabilities.squeeze().numpy()
        
        return {
            'prediction': prediction,
            'yes_prob': f"{probs[1]*100:.1f}",
            'no_prob': f"{probs[0]*100:.1f}"
        }

# Generator function to capture and process video frames
def video_stream():
    cap = cv2.VideoCapture(0)  # Open the webcam

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        prediction = detect_sign_language(frame)

        # Overlay prediction text on frame
        cv2.putText(frame, f"Prediction: {prediction['prediction']}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Encode frame to JPEG
        _, jpeg = cv2.imencode(".jpg", frame)
        frame_bytes = jpeg.tobytes()

        # Yield frame in a format suitable for streaming
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n\r\n")

    cap.release()

@csrf_exempt
def video_feed(request):
    if request.method == 'POST':
        # Get frame from POST request
        frame_file = request.FILES.get('frame')
        if not frame_file:
            return JsonResponse({'error': 'No frame provided'}, status=400)
            
        # Convert frame to numpy array
        frame_array = np.frombuffer(frame_file.read(), np.uint8)
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
        
        # Get prediction
        result = detect_sign_language(frame)
        
        return JsonResponse(result)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Django view to serve the live video page
def live_detection(request):
    return render(request, "live_video.html")


@login_required
def practice_home(request):
    return render(request, 'sign_practice/home.html')    

@login_required
def common_phrases_practice(request):
    # List of words/phrases from chapter 3 lessons, in order, with translations
    phrases = [
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
    return render(request, 'sign_practice/common_phrases_practice.html', {'phrases': phrases})    

@login_required
def phrase_detail(request, phrase):
    # Map phrases to video filenames
    phrase_to_video = {
        'السلام عليكم': 'السلام عليكم.mp4',
        'وعليكم السلام': 'وعليكم السلام.mp4',
        'صباح الخير': 'صباح الخير.mp4',
        'صباح النور': 'صباح النور.mp4',
        'كيف هي أمورك ؟': 'كيف هي أمورك ؟.mp4',
        'كيف صحتك ؟': 'كيف صحتك ؟.mp4',
        'كيف حالك ؟': 'كيف حالك ؟.mp4',
        'كيف حال أولادك ؟': 'كيف حال أولادك ؟.mp4',
        'أتوصي بشيء ؟': 'أتوصي بشيء ؟.mp4',
        'اعتن بنفسك': 'اعتن بنفسك.mp4',
        'أراك قريبا': 'أراك قريبا.mp4',
        'مع السلامة': 'مع السلامة.mp4',
    }
    # Map phrases to lesson number in chapter 3
    phrase_to_lesson = {
        'السلام عليكم': 1,
        'وعليكم السلام': 1,
        'صباح الخير': 1,
        'صباح النور': 1,
        'كيف هي أمورك ؟': 2,
        'كيف صحتك ؟': 2,
        'كيف حالك ؟': 2,
        'كيف حال أولادك ؟': 2,
        'أتوصي بشيء ؟': 3,
        'اعتن بنفسك': 3,
        'أراك قريبا': 3,
        'مع السلامة': 3,
    }
    # Map phrases to translations
    phrase_to_translation = {
        'السلام عليكم': 'Peace be upon you',
        'وعليكم السلام': 'And peace be upon you',
        'صباح الخير': 'Good morning',
        'صباح النور': 'Good morning (response)',
        'كيف هي أمورك ؟': '? How are things',
        'كيف صحتك ؟': '? How is your health',
        'كيف حالك ؟': '? How are you',
        'كيف حال أولادك ؟': '? How are your children',
        'أتوصي بشيء ؟': '? Do you need anything',
        'اعتن بنفسك': 'Take care of yourself',
        'أراك قريبا': 'See you soon',
        'مع السلامة': 'Goodbye',
    }
    video_file = phrase_to_video.get(phrase)
    video_url = f'chapter3/{video_file}' if video_file else None
    lesson_number = phrase_to_lesson.get(phrase, 1)
    translation = phrase_to_translation.get(phrase, "")
    return render(request, 'sign_practice/phrase_detail.html', {
        'phrase': phrase,
        'video_url': video_url,
        'lesson_number': lesson_number,
        'translation': translation
    })

