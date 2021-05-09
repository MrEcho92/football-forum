from django.db import models
from django.utils import timezone
from django.urls import reverse
from autoslug import AutoSlugField


# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User', related_name='post', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    title = models.CharField(max_length=100)
    slug= AutoSlugField(populate_from='title', blank=True, null=True)
    text = models.TextField(max_length=350, blank=True)
    image = models.ImageField(blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField('auth.User', related_name='post_likes', blank=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("forum:post_detail", kwargs={'pk':self.pk, 'slug':self.slug})

    def get_like_url(self):
        return reverse("forum:like-toggle", kwargs={'pk':self.pk, 'slug':self.slug})

    def get_api_like_url(self):
        return reverse("forum:like-api-toggle", kwargs={'pk':self.pk, 'slug':self.slug})

    class Meta:
        ordering =["-created_date"]

class Comment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post = models.ForeignKey('forum.Post',related_name='comments', on_delete=models.CASCADE)
    reply = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    text = models.TextField(max_length=250, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    likes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("forum:post_detail", kwargs={'pk':self.pk, 'slug':self.slug})

    class Meta:
        ordering =["-created_date", "-pk"]


class Report(models.Model):
    user = models.ForeignKey('auth.User', null=True, on_delete=models.CASCADE)
    comment = models.ForeignKey('forum.Comment',related_name='report',null=True, on_delete=models.CASCADE)
    message = models.TextField(max_length=200,blank=True )
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return 'Report from {}'.format(self.user)

    class Meta:
        ordering = ["-date", "-pk"]
