from django.db import models

class JournalEntry(models.Model):
    date = models.DateField(unique=True)

class PromptResponsePair(models.Model):
    entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name='prompts')
    prompt = models.TextField()
    response = models.TextField()

