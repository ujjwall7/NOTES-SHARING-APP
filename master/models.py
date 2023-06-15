from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile = models.CharField(max_length=15)

class Note(models.Model):
    NOTE_TYPES = (
        ('Text', 'Text'),
        ('Audio', 'Audio'),
        ('Video', 'Video')
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    note_type = models.CharField(max_length=10, choices=NOTE_TYPES,null=True)
    file = models.FileField(upload_to='media/',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class NoteShare(models.Model):
    note = models.ManyToManyField(Note, related_name='shares')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notes')
    shared_with = models.ManyToManyField(User, related_name='received_notes')
    shared_at = models.DateTimeField(auto_now_add=True)



