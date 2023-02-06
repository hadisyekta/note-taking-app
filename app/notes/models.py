from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tags(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ['title']

    def __str__(self) -> str:
        return self.title


class Notes(models.Model):

    title = models.CharField(max_length=100)
    body = models.TextField()
    tags = models.ManyToManyField(Tags, blank=True, related_name="tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    private = models.BooleanField('Private', default=True)

    class Meta:
        ordering = ['title']

    def __str__(self) -> str:
        return self.title
    
    def is_public(self):
        if not self.private:
            return 'Public'







