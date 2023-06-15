from django.contrib import admin
from .models import *



@admin.register(Note)
class NoteDisplay(admin.ModelAdmin):
    list_display = ['title','created_at','user','id'] 

@admin.register(NoteShare)
class NoteShareDisplay(admin.ModelAdmin):
    list_display = ['sender','shared_at','id'] 
    
@admin.register(User)
class UserDisplay(admin.ModelAdmin):
    list_display = ['username','mobile','email'] 
    