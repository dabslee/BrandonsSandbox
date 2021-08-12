from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50)

class Post(models.Model):
    title = models.CharField(max_length=500)
    created = models.DateField()
    content = models.TextField(max_length=20000)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title