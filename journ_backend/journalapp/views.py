from rest_framework import viewsets
from .models import JournalEntry, PromptResponsePair
from .serializers import JournalEntrySerializer, PromptResponsePairSerializer
from openai import OpenAI
from django.http import JsonResponse
from .models import JournalEntry, PromptResponsePair
import os
import datetime
import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
OPENAI_API_KEY = os.getenv('OPEN_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

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
        model="gpt-4o-mini",
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
        "content": "Please give me a prompt that asks about my day and helps me write a journal entry. Ask me a question that will prompt me to write more about my day."
    })

    return messages

# Example usage in a view to generate OpenAI API compatible messages
def generate_start_prompt(request):
    try:
        messages = create_start_messages()
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Specify the correct model
            messages=messages,
            max_tokens=150,  # Adjust as necessary
            stop=["?", "\n"],
            temperature=0.5  # Adjust for creativity variability
        )
        # Extracting and returning the response
        return JsonResponse({'response': response.choices[0].message.content}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def generate_further_prompt(request):
    try:
        messages = create_further_messages()
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Specify the correct model
            messages=messages,
            max_tokens=250,  # Adjust as necessary
            stop=["?", "\n"],
            temperature=0.5  # Adjust for creativity variability
        )
        # Extracting and returning the response
        return JsonResponse({'response': response.choices[0].message.content}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



def create_reflection_messages(date_start, date_end, user_prompt):
    # Start with a message from the developer setting the context
    messages = [
        {
            "role": "system",
            "content": "This AI is a helpful and introspective journalling assistant, below are the users journal entries for you to analyze and report back on"
        }
    ]

    # Get the last five journal entries
    latest_entries = JournalEntry.objects.filter(date__range=[date_start, date_end])

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
        "content": user_prompt
    })

    return messages

@csrf_exempt
def generate_reflection_summary(request):
    # Extract dates and user prompt from the request
    if request.method == 'POST':
        try:
            # Parsing the JSON body of the request
            data = json.loads(request.body)
            start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
            end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
            user_prompt = data.get('user_prompt', '')
            messages = create_reflection_messages(start_date, end_date, user_prompt)
            print(messages)
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # Specify the correct model
                    messages=messages,
                    max_tokens=750,  # Adjust as necessary
                    temperature=0.5  # Adjust for creativity variability
                )
                # Extracting and returning the response
                print(response)
                return JsonResponse({'response': response.choices[0].message.content}, status=200)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except KeyError:
            # Handle missing fields or invalid dates
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        except ValueError as e:
            # Handle invalid date format
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)    
    