from django.db import models
from django.utils import timezone

# Create your models here.

class users(models.Model):

    user_id = models.AutoField(primary_key=True,unique=True)
    user_name = models.CharField(max_length=80)
    user_email = models.CharField(max_length=180)
    user_pass = models.CharField(max_length=100)

    def __str__(self):
        return self.user_name
    
class users_messages(models.Model):

    message_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=1000)  # User identifier
    message_text = models.TextField(default='Default message text')  # Text of the user's message
    ai_response = models.TextField()  # AI's response
    created_at = models.DateTimeField(default=timezone.now)  # Sets the default to the current time

    def __str__(self):
        return f"Message from {self.user_id} at {self.created_at}"

    class Meta:
        ordering = ['created_at']  # Orders messages by creation time by default
    







