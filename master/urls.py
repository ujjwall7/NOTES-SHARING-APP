from django.urls import path
from . import views


urlpatterns = [

    #Authentication
    path('user_registration/',views.UserRegistrationAPIView.as_view()),
    path('login/',views.Login.as_view()),
    path('logout/',views.Logout.as_view()),

    #Notes
    path('notes/',views.NoteAPI.as_view()),
    path('all_notes/',views.AllNotesAPI.as_view()),
    path('send_notes/',views.SendNotesAPI.as_view()),


]


