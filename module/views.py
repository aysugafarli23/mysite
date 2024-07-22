from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import resolve
from contact.forms import ContactForm  
from pathlib import Path
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Word, CustomerRecording
from openai import Client
from django.core.files import File
import re, os
from django.views import View
from django.utils.decorators import method_decorator
from openai import OpenAI

client = OpenAI(api_key="sk-proj-8tsKt51ax7c9AoOO3RYST3BlbkFJkVGybZPjPoHTxK1LZXIm")
# Create your views here.

def modulesPage(request):
     # Contact form logic
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = ContactForm()
    current_url = resolve(request.path_info).url_name

    modules = Module.objects.all()
    context = {
        'current_url': current_url,
        'form': form,
        'modules': modules,
    }
    return render(request, 'module.html', context)


def lessonsPage(request, pk):
    module = get_object_or_404(Module, pk=pk)
    lessons = Lesson.objects.filter(lesson_module=module)

    context = {
        'module': module,
        'lessons': lessons,        
    }

    return render(request, 'lesson.html', context)


def lessonSectionPage(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    sections = Section.objects.filter(section_lesson=lesson)
    section_contents = []

    for section in sections:
        section_contents.append({
            'section': section,
            'contents': Content.objects.filter(content_section=section)
        })

    context = {
        'lesson': lesson,
        'section_contents': section_contents,
    }
    return render(request, 'modulesections.html', context)



# a view to generate the audio files for each word using OpenAI
def generate_speech(request):
    words = Word.objects.all()
    client = Client(api_key="sk-proj-8tsKt51ax7c9AoOO3RYST3BlbkFJkVGybZPjPoHTxK1LZXIm")
    for word in words:
        filename = re.sub(r'[^\w\s-]', '', word.text)[:20].replace(' ', '_')  # Replace invalid characters with underscores
        speech_file_path = Path(__file__).parent / f"words_audio/{filename}_alloy.mp3"  # Add word ID to filename to avoid overwrites

        with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="alloy",
            input=word.text
        ) as response:
            response.stream_to_file(str(speech_file_path))  # Stream to the file path

        with open(speech_file_path, 'rb') as f:
            word.audio_file_alloy.save(speech_file_path.name, File(f), save=True)

    for word in words:
        filename = re.sub(r'[^\w\s-]', '', word.text)[:20].replace(' ', '_')  # Replace invalid characters with underscores
        speech_file_path = Path(__file__).parent / f"words_audio/{filename}_nova.mp3"  # Add word ID to filename to avoid overwrites

        with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="nova",
            input=word.text
        ) as response:
            response.stream_to_file(str(speech_file_path))  # Stream to the file path

        with open(speech_file_path, 'rb') as f:
            word.audio_file_nova.save(speech_file_path.name, File(f), save=True)


    return render(request, 'words.html', {'words': words})


@method_decorator(csrf_exempt, name='dispatch')
class WordView(View):
    template_name = 'word_detail.html'

    def get(self, request, word_id):
        word = get_object_or_404(Word, id=word_id)
        next_word = Word.objects.filter(id__gt=word_id).order_by('id').first()
        previous_word = Word.objects.filter(id__lt=word_id).order_by('-id').first()
        next_word_id = next_word.id if next_word else None
        previous_word_id = previous_word.id if previous_word else None
        return render(request, self.template_name, {
            'word': word,
            'next_word_id': next_word_id,
            'previous_word_id': previous_word_id
        })


    def post(self, request, word_id):
        word = get_object_or_404(Word, id=word_id)
        if 'media' in request.FILES:
            # Delete the previous recording
            CustomerRecording.objects.filter(word=word).delete()

            # Save the new recording
            media_file = request.FILES['media']
            customer_recording = CustomerRecording.objects.create(
                audio_file=media_file,
                word=word
            )
            return JsonResponse({'success': True, 'recording_id': customer_recording.id})
        return JsonResponse({'success': False, 'error': 'No media file found'}, status=400)

def compare_audio(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    recordings = CustomerRecording.objects.filter(word=word)
    next_word = Word.objects.filter(id__gt=word_id).order_by('id').first()
    next_word_id = next_word.id if next_word else None
    return render(request, 'compare_audio.html', {
        'word': word,
        'recordings': recordings,
        'next_word_id': next_word_id
    })

# AI Assessment on user recordings
def transcribe_audio(audio_file_path):
    with open(audio_file_path, 'rb') as audio_file:
        response = client.audio.transcribe(model="whisper-1",
        file=audio_file)
    return response.text

def calculate_native_percentage(transcript, target_text):
    transcript_words = set(transcript.lower().split())
    target_words = set(target_text.lower().split())
    matching_words = transcript_words & target_words
    native_percentage = (len(matching_words) / len(target_words)) * 100
    return native_percentage

def generate_feedback(native_percentage):
    if native_percentage > 90:
        return "Excellent pronunciation!"
    elif native_percentage > 75:
        return "Good job, but there's room for improvement."
    elif native_percentage > 50:
        return "Fair attempt, keep practicing."
    else:
        return "Keep practicing, you'll get better!"

def generate_graph_data(transcript, target_text):
    target_letters = list(target_text)
    transcript_letters = list(transcript)
    graph_data = []

    for i, letter in enumerate(target_letters):
        if i < len(transcript_letters) and transcript_letters[i].lower() == letter.lower():
            graph_data.append((letter, 'green'))
        else:
            graph_data.append((letter, 'red'))

    return graph_data


def transcribe_audio(audio_file_path):
    with open(audio_file_path, 'rb') as audio_file:
        response = client.audio.transcribe(model="whisper-1",
        file=audio_file)
    return response.text

def calculate_native_percentage(transcript, target_text):
    transcript_words = set(transcript.lower().split())
    target_words = set(target_text.lower().split())
    matching_words = transcript_words & target_words
    native_percentage = (len(matching_words) / len(target_words)) * 100
    return native_percentage

def generate_feedback(native_percentage):
    if native_percentage > 90:
        return "Excellent pronunciation!"
    elif native_percentage > 75:
        return "Good job, but there's room for improvement."
    elif native_percentage > 50:
        return "Fair attempt, keep practicing."
    else:
        return "Keep practicing, you'll get better!"

def generate_graph_data(transcript, target_text):
    target_letters = list(target_text)
    transcript_letters = list(transcript)
    graph_data = []

    for i, letter in enumerate(target_letters):
        if i < len(transcript_letters) and transcript_letters[i].lower() == letter.lower():
            graph_data.append((letter, 'green'))
        else:
            graph_data.append((letter, 'red'))

    return graph_data

class PronunciationAssessmentView(View):
    template_name = 'pronunciation_assessment.html'

    def get(self, request, word_id):
        word = get_object_or_404(Word, id=word_id)
        return render(request, self.template_name, {'word': word})

    def post(self, request, word_id):
        word = get_object_or_404(Word, id=word_id)
        if 'media' in request.FILES:
            media_file = request.FILES['media']
            customer_recording = CustomerRecording.objects.create(
                audio_file=media_file,
                word=word
            )

            # Transcribe the audio
            transcript = transcribe_audio(customer_recording.audio_file.path)

            # Calculate nativeness percentage
            native_percentage = calculate_native_percentage(transcript, word.text)

            # Generate feedback
            feedback = generate_feedback(native_percentage)

            # Generate graph data
            graph_data = generate_graph_data(transcript, word.text)

            context = {
                'word': word,
                'transcript': transcript,
                'native_percentage': native_percentage,
                'feedback': feedback,
                'graph_data': graph_data
            }
            return render(request, self.template_name, context)

        return JsonResponse({'success': False, 'error': 'No media file found'}, status=400)