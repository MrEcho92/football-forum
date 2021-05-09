from notification.models import Notification
from django.dispatch import receiver
from forum.models import Comment, Post
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.shortcuts import render

@receiver(post_save, sender=Comment)
def user_comment_post(sender, instance, created, **kwargs):
    if created:
        comment = instance
        post = comment.post
        #reply = comment.reply # No reply when new comment is created
        text_preview = comment.text[:90]
        sender = comment.user
        notify_post_author = Notification.objects.create(post=post, sender=sender, comment=comment, user=post.author, text_preview=text_preview, notification_type=2)
        notify_post_author.save()

        if comment.reply is not None:
            notify_comment_owner = Notification.objects.create(post=post, sender=sender, comment=comment, user=comment.reply.user, text_preview=text_preview, notification_type=2)
            notify_comment_owner.save()
'''
From the model structure :

A new Comment object to a Post would have Comment.reply field as None
A reply (another Comment object) to an existing Comment object would have Comment.reply not as None .Would have a parent Comment object.

So, check in the signal instance if comment.reply is None or not.

if comment.reply is None it is a new comment to a post >>> send notification to Post owner only
if comment.reply is not None it is a new comment (reply) to an existing comment of a post >>> send notification to Post owner and Comment owner

or use another way:
You could check in the same post_save hook if the comment being saved is a reply by performing an EXISTS query accessing it's related manager:

@receiver(post_save, sender=Comment)
def user_comment_post(sender, instance, created, **kwargs):
    if created and entities.replies.exists():
        # your code here

'''
@receiver(post_delete, sender=Comment)
def user_delete_comment_post(sender, instance, created, **kwargs):
    if created:
        comment = instance
        post = comment.post
        #reply = comment.reply
        text_preview = comment.text[:90]
        sender = comment.user
        notify = Notification.objects.create(post=post, sender=sender, comment=comment, user=post.author, text_preview=text_preview, notification_type=2)
        notify.delete()

'''
@receiver(post_save, sender=Post)
def user_like_post(sender, instance, *args, **kwargs):
    post = instance
    sender = Post.objects.filter(likes__id=likes__id)
    notify = Notification(post=post, sender=sender, comment=None, user=post.author, text_preview=None, notification_type=1)
    notify.save()
'''
