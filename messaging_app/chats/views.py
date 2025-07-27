"""Views for the chat messaging app using DRF ViewSets."""
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsOwner


# Explicit class name: ConversationViewSet
class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)
    def perform_create(self, serializer):
        instance = serializer.save()
        instance.participants.add(self.request.user)

# Explicit class name: MessageViewSet
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Only return messages where the current user is the sender
        return Message.objects.filter(sender=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        if self.request.user not in conversation.participants.all():
            raise ValidationError("You are not a participant in this conversation.")
        serializer.save(sender=self.request.user)
