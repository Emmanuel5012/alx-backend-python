from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
# Conversation model to represent a chat between users
class Conversation(models.Model):
    participants = models.ManyToManyField(CustomUser, related_name='conversations')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation between {self.pk}"
    
# Message model to represent messages in a conversation
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} in conversation {self.conversation.pk}"