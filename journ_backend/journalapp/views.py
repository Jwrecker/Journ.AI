from rest_framework import viewsets
from .models import JournalEntry, PromptResponsePair
from .serializers import JournalEntrySerializer, PromptResponsePairSerializer
from openai import OpenAI
from django.http import JsonResponse
from .models import JournalEntry, PromptResponsePair
import os
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class JournalEntryViewSet(viewsets.ModelViewSet):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer

class PromptResponsePairViewSet(viewsets.ModelViewSet):
    queryset = PromptResponsePair.objects.all()
    serializer_class = PromptResponsePairSerializer


def test_openai_api(request):
    # Ensure the API key is set right before making a request

    try:
        response = client.chat.completions.create(
        messages=[
            {
                "role": "developer",
                "content": ("Pretend you are a pretentious French Teacher."
                "You will help with french questions.")
            },
            {
                "role": "assistant",
                "content": "What would you like me to translate to French?"
            },
            {
                "role": "user",
                "content": "Hello World!"
            }
        ],
        model="gpt-4o",
        max_tokens=60)
        return JsonResponse({'response': response.choices[0].message.content.strip()}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

def generate_today_prompt(request):
    # Collect the last five journal entries for context
    latest_entries = JournalEntry.objects.order_by('-date')[:5]
    previous_context = []

    for entry in latest_entries:
        # Retrieve all prompt-response pairs for each entry
        pairs = PromptResponsePair.objects.filter(entry=entry)
        for pair in pairs:
            # Format and append both prompt and response to the context
            previous_context.append(f"Q: {pair.prompt}")
            previous_context.append(f"A: {pair.response}")

    # Join all elements to form a complete previous context
    previous_context_text = " ".join(previous_context)

    # Construct the prompt for generating the starter question of the day
    prompt_question = (f"Based on my previous journal entries: {previous_context_text} "
                       "Please ask a starter question about my day that will help me write and reflect in a journal entry.")

    try:
        response = client.completions.create(engine="davinci",
        prompt=prompt_question,
        max_tokens=100,
        stop=["\n"],  # Stops at the first newline to get a concise question
        temperature=0.7)  # Slightly creative to generate engaging and thoughtful prompts)
        starter_prompt = response.choices[0].text.strip()
        return JsonResponse({'prompt': starter_prompt}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



def generate_further_prompt(request):
    # Get today's date and collect the journal entry for today if it exists
    today = date.today()
    today_entry = JournalEntry.objects.filter(date=today).first()

    # Context for today's responses
    today_context = []
    if today_entry:
        today_pairs = PromptResponsePair.objects.filter(entry=today_entry)
        for pair in today_pairs:
            today_context.append(f"Q: {pair.prompt}")
            today_context.append(f"A: {pair.response}")

    # Collect the last five journal entries including today, with their prompts and responses
    latest_entries = JournalEntry.objects.order_by('-date')[:6]  # fetch one extra to ensure we have enough if today is included
    previous_context = []

    for entry in latest_entries:
        if entry != today_entry:  # Avoid duplicating today's entry
            pairs = PromptResponsePair.objects.filter(entry=entry)
            for pair in pairs:
                previous_context.append(f"Q: {pair.prompt}")
                previous_context.append(f"A: {pair.response}")

    # Construct the full prompt with clearly separated contexts
    previous_context_text = " ".join(previous_context)
    today_context_text = " ".join(today_context)
    prompt_question = (f"Reflecting on my previous entries: {previous_context_text} "
                       f"And today's responses: {today_context_text} "
                       "Generate an open-ended follow-up question to help me continue writing and reflecting on my day.")

    try:
        response = client.completions.create(engine="davinci",
        prompt=prompt_question,
        max_tokens=150,
        stop=["\n\n"],  # Stops at first double newline, may adjust based on desired output
        temperature=0.6)  # Moderately creative to generate thoughtful, engaging prompts)
        prompt_text = response.choices[0].text.strip()
        return JsonResponse({'prompt': prompt_text}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def generate_reflection_summary(request):
    # Extract dates and user prompt from the request
    data = request.GET
    start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
    end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
    user_prompt = data.get('user_prompt', '')

    # Fetch entries within the specified date range
    entries = JournalEntry.objects.filter(date__range=[start_date, end_date])
    context_responses = []

    for entry in entries:
        pairs = PromptResponsePair.objects.filter(entry=entry)
        for pair in pairs:
            # Format responses as quotes for the context
            context_responses.append(f"\"{pair.response}\"")

    # Join all quotes to form the historical context
    context_text = " ".join(context_responses)

    # Construct the final prompt for the reflection
    full_prompt = (f"{user_prompt} Reflecting on the period from {start_date} to {end_date}: "
                   f"{context_text} Please provide a nostalgic summary and a reflective look over this timeframe.")

    try:
        response = client.completions.create(engine="davinci",
        prompt=full_prompt,
        max_tokens=500,  # Longer tokens for more detailed reflection
        stop=None,  # No specific stop character, allow to complete the thought
        temperature=0.6,  # Lower temperature for coherent and focused output
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
        reflective_summary = response.choices[0].text.strip()
        return JsonResponse({'summary': reflective_summary}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)