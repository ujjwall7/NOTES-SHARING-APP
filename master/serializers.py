from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password','user_permissions','groups','is_staff','is_active','last_login','date_joined','is_superuser']

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        exclude = ['user']

class AddSendNotesSerializer(serializers.ModelSerializer):
    note = NoteSerializer(read_only = True)
    shared_with = UserSerializer(read_only=True)
    class Meta:
        model = NoteShare
        exclude = ['sender']

class SendNotesSerializer(serializers.ModelSerializer):
    shared_with = UserSerializer(read_only=True,many=True)
    note = NoteSerializer(read_only=True,many=True)
    class Meta:
        model = NoteShare
        exclude = ['sender']