from rest_framework import viewsets
from .models import JournalEntry, PromptResponsePair
from .serializers import JournalEntrySerializer, PromptResponsePairSerializer

class JournalEntryViewSet(viewsets.ModelViewSet):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer

class PromptResponsePairViewSet(viewsets.ModelViewSet):
    queryset = PromptResponsePair.objects.all()
    serializer_class = PromptResponsePairSerializer
