from django.db import models
from django.contrib.auth.models import User
from forum.models import Post, Comment
# Create your models here.

CHOICES = ((1, 'Like'),(2,'Comment'), (3,'Follow'))

class Notification(models.Model):
    post = models.ForeignKey('forum.Post', on_delete=models.CASCADE, related_name='noti_post', blank=True, null=True)
    comment = models.ForeignKey('forum.Comment', on_delete=models.CASCADE, related_name='noti_comment', blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noti_from_user')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noti_to_user')
    notification_type = models.IntegerField(choices=CHOICES)
    text_preview = models.CharField(max_length=100, blank=True) #short comment of text 
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
