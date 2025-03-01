from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import JournalEntryViewSet, PromptResponsePairViewSet

router = DefaultRouter()
router.register(r'entries', JournalEntryViewSet)
router.register(r'prompts', PromptResponsePairViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
