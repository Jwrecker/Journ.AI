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

def create_start_messages():
    # Start with a message from the developer setting the context
    messages = [
        {
            "role": "system",
            "content": "This AI is a helpful and introspective journalling assistant, designed to prompt users to journal and help people recollect on their entries."
        }
    ]

    # Get the last five journal entries
    latest_entries = JournalEntry.objects.order_by('-date')[:5]

    for entry in latest_entries:
        # Retrieve all prompt-response pairs for this entry
        pairs = PromptResponsePair.objects.filter(entry=entry)

        # Append formatted messages
        for pair in pairs:
            messages.append({
                "role": "assistant",
                "content": f"{pair.prompt}"
            })
            messages.append({
                "role": "user",
                "content": f"{pair.response}"
            })

    # Add a final message from the user asking for a prompt about their day
    messages.append({
        "role": "user",
        "content": "Please give me a prompt that asks about my day and helps me write a journal entry. Use my previous entries as context to help me write and retain what happened today."
    })

    return messages


def create_further_messages():
    # Start with a message from the developer setting the context
    messages = [
        {
            "role": "system",
            "content": "This AI is a helpful and introspective journalling assistant, designed to prompt users to journal and help people recollect on their entries. The most recent entries have been entered today and your questions should follow up on them and prompt further response from the user"
        }
    ]

    # Get the last five journal entries
    latest_entries = JournalEntry.objects.order_by('-date')[:5]

    for entry in latest_entries:
        # Retrieve all prompt-response pairs for this entry
        pairs = PromptResponsePair.objects.filter(entry=entry)

        # Append formatted messages
        for pair in pairs:
            messages.append({
                "role": "assistant",
                "content": f"{pair.prompt}"
            })
            messages.append({
                "role": "user",
                "content": f"{pair.response}"
            })

    # Add a final message from the user asking for a prompt about their day
    messages.append({
        "role": "user",
        "content": "Please give me a prompt that asks about my day and helps me write a journal entry. Use my previous entries as context to help me write and retain what happened today. The most recent response pair is from today, and I would like you to keep it in mind to help me write more specific and meaningful entries for today's entry"
    })

    return messages

# Example usage in a view to generate OpenAI API compatible messages
def generate_start_prompt(request):
    try:
        messages = create_start_messages()
        response = client.chat.completions.create(
            model="gpt-4o",  # Specify the correct model
            messages=messages,
            max_tokens=150,  # Adjust as necessary
            temperature=0.5  # Adjust for creativity variability
        )
        # Extracting and returning the response
        return JsonResponse({'response': response['choices'][0]['message']['content'].strip()}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def generate_further_prompt(request):
    try:
        messages = create_further_messages()
        response = client.chat.completions.create(
            model="gpt-4o",  # Specify the correct model
            messages=messages,
            max_tokens=150,  # Adjust as necessary
            temperature=0.5  # Adjust for creativity variability
        )
        # Extracting and returning the response
        return JsonResponse({'response': response['choices'][0]['message']['content'].strip()}, status=200)
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