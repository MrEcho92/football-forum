from django.db import models

# Create your models here.
class subscriber(models.Model):
    email = models.EmailField(max_length=30)

    def __str__(self):
        return self.email
