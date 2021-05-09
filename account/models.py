from django.db import models
from django.utils import timezone
from django.urls import reverse
#from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from PIL import Image
# Create your models here.

class UserProfile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=250, blank=True, null=True)
    #slug= model.SlugField(populate_from="user.username", blank=True,  null=True)
    profile_pic = models.ImageField(default='view_avatar.png', blank=True, null=True)
    country= CountryField(blank_label='(select country)',  null=True)
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    joined_date = models.DateTimeField(auto_now_add=True, null=True)
    comment_count=models.PositiveIntegerField(default=0)
    post_count= models.PositiveIntegerField(default=0)
    email_confirmed = models.BooleanField(default=False, blank=True)


    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        return reverse("account:dashboard", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)
        #Resizing large image to small size
        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width> 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)

    class Meta:
        verbose_name = ('User Profile')
        verbose_name_plural = ('User Profiles')
