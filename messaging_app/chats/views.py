from rest_framework import generics, permissions, viewsets
from .models import CustomUser, Conversation, Message
from .serializers import CustomUserSerializer, ConversationSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framwork.exceptions import ValidationError

# Create your views here.

class ConversationListCreateView(generics.ListCreateAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageCreateView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        if self.request.user not in conversation.participants.all():
            raise ValidationError("You are not a participant in this conversation.")
        serializer.save(sender=self.request.user)