from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import JournalEntryViewSet, PromptResponsePairViewSet
from .views import test_openai_api, generate_reflection_summary, generate_start_prompt, generate_further_prompt

router = DefaultRouter()
router.register(r'entries', JournalEntryViewSet)
router.register(r'prompts', PromptResponsePairViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test-ai/', test_openai_api, name='test-openai_api'),
    path('reflect/', generate_reflection_summary, name='reflection-summary'),
    path('start/', generate_start_prompt, name='start-prompt'),
    path('further/', generate_further_prompt, name='further-prompt')
]
