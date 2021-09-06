from django.db import models
from django_quill.fields import QuillField

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=500)
    created = models.DateField()
    content = QuillField()
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title