from django.urls import path
from .views import ConversationListCreateView, ConversationDetailView, MessageCreateView    

urlpatterns = [
    path('api/conversations/', ConversationListCreateView.as_view(), name='conversation-list-create'),
    path('api/conversations/<uuid:conversation_id>/', ConversationDetailView.as_view(), name='conversation-detail'),
    path('api/messages/', MessageCreateView.as_view(), name='message-create'),
]