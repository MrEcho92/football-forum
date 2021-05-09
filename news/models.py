from django.db import models
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField

# Create your models here.

STATUS = ((0,'Draft'), (1, 'Publish'), (2,'Closed'))

LEAGUE = (('Premier League','Premier League'), ('La Liga', 'La Liga'), ('Seria A','Seria A'), ('Nigeria Professional Football League','Nigeria Professional Football League'),('UEFA Champions League','UEFA Champions League'), ('Others','Others'))


class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50)
    author = models.CharField(max_length=50)
    message = RichTextField()
    image_upload = models.ImageField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS, default=0)
    league = models.CharField(choices=LEAGUE, default='Premier League',  max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news:news_detail", kwargs={'slug':self.slug})

    class Meta:
        verbose_name = ('News')
        verbose_name_plural = ('News')
        ordering = ['-id']
