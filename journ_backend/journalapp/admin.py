from django.contrib import admin

from .models import JournalEntry, PromptResponsePair

from django.contrib import admin
from .models import JournalEntry, PromptResponsePair

# Register your models here.
admin.site.register(JournalEntry)
admin.site.register(PromptResponsePair)

