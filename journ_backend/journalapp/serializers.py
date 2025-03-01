from rest_framework import serializers
from .models import JournalEntry, PromptResponsePair

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ['id', 'date']

class PromptResponsePairSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptResponsePair
        fields = ['id', 'entry', 'prompt', 'response']
