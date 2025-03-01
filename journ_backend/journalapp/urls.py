from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import JournalEntryViewSet, PromptResponsePairViewSet
from .views import test_openai_api

router = DefaultRouter()
router.register(r'entries', JournalEntryViewSet)
router.register(r'prompts', PromptResponsePairViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test-ai/', test_openai_api, name='test-openai_api')
]
