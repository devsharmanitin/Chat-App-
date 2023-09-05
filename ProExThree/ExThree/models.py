from django.db import models
from django.contrib.auth.models import User

# Create your models here.




class Message(models.Model):
    sender = models.ForeignKey(User , related_name='sent_messages', on_delete=models.CASCADE , null= True , blank=True)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE , null= True , blank= True)
    content = models.TextField( )
    timestamp = models.CharField(max_length=200 )
    
    
    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"
    