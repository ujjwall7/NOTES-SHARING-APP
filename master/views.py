from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from .serializers import *


#-------------Authentication-------------------
class UserRegistrationAPIView(APIView):
    def post(self,request):
        username    = request.data.get('username')
        password    = request.data.get('password')
        email       = request.data.get('email')
        mobile      = request.data.get('mobile')
        first_name  = request.data.get('first_name','')
        last_name   = request.data.get('last_name','')

        if not (username and password and email and mobile):
            return Response({'error': 'Missing required fields'}, status=400)

        try:
            existing_user = User.objects.filter(Q(username=username) | Q(email=email) | Q(mobile=mobile)).last()
            if existing_user:
                error_message = ''
                if existing_user.username == username:
                    error_message += r'Username already exists. '
                if existing_user.email == email:
                    error_message += r'Email already exists. '
                if existing_user.mobile == mobile:
                    error_message += 'Mobile number already exists. '
                return Response({'error': error_message}, status=400)
        except User.DoesNotExist:
            pass

        hashed_password = make_password(password)
        user = User(username=username, email=email, password=hashed_password, mobile=mobile,
                    first_name=first_name, last_name=last_name)
        user.save()
        return Response({'success': 'User registered successfully','Is_Success':True}, status=201)

class Login(APIView):
    def post(self,request):
        get_user = request.data.get("username")
        password = request.data.get("password")
        cond = Q(username = get_user) | Q(email = get_user) |Q(mobile = get_user)
        username = User.objects.filter(cond).first()

        if not username:
            data = {'User':False,'msg':'Invalid Username'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        user = authenticate(request,username=username.username,password=password)

        if user is not None:
            try:
                Token.objects.create(user=user)
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.get(user=user)

            data = {
                'user':True,
                'token':str(token),
            }
            return Response(data,status=status.HTTP_200_OK)
        else:
            data = {'User':False,'msg':'Invalid password'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        token = Token.objects.get(user = request.user)
        token.delete()
        data = {'status':'You Are Successfully Logout'}
        return Response(data, status=status.HTTP_200_OK)


#-------------Store the Notes----------------
class NoteAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        try:
            id = self.request.query_params.get('id')
            data = Note.objects.get(id = id)
            serializer = NoteSerializer(data,many=False)
            return Response(serializer.data)
        except:
            user = request.user
            notes = Note.objects.filter(user = user)
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            f = serializer.save(user = request.user)
            return Response({'msg':'Notes created Sucessfully','IsSuccess':'True'}, status=status.HTTP_201_CREATED)
        errors = serializer.errors
        errors['IsSuccess'] = 'False'
        return Response(serializer.errors, status=status.HTTP_201_CREATED)

    def put(self,request):
        try:
            id = self.request.query_params.get('id')
            foo = Note.objects.get(id=id)
            serializer = NoteSerializer(foo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Notes Updated Sucessfully','Is_Success':True})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)})

    def delete(self,request):
        try:
            id = self.request.query_params.get('id')
            foo = Note.objects.get(id=id)
            foo.delete()
            return Response({'msg': 'Notes Deleted successfully'})
        except Exception as e:
            return Response({'error': str(e)})

#---------show all Notes-----------
class AllNotesAPI(APIView):
    def get(self,request):
        try:
            id = self.request.query_params.get('id')
            data = Note.objects.get(id = id)
            serializer = NoteSerializer(data,many=False)
            return Response(serializer.data)
        except:
            user = request.user
            notes = Note.objects.all()
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

#--------Send Notes to Many Users--------
class SendNotesAPI(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self,request):
        try:
            id = self.request.query_params.get('id')
            data = NoteShare.objects.get(id = id)
            serializer = SendNotesSerializer(data,many=False)
            return Response(serializer.data)
        except:
            user = request.user
            notes = NoteShare.objects.filter(sender = user)
            serializer = SendNotesSerializer(notes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        serializer = AddSendNotesSerializer(data=request.data)
        if serializer.is_valid():
            
            #handle Many To Many in shared with 
            get_shared_with = request.data.get('shared_with')
            c_py_shared = eval(get_shared_with)
            shared_with_obj = User.objects.filter(id__in = c_py_shared)
            if not shared_with_obj:
                return Response({"msg":'Your selected user are not available'})
            
            #handle 
            get_note = request.data.get('note')
            c_py_note = eval(get_note)
            note_obj = Note.objects.filter(id__in = c_py_note)
            if not note_obj:
                return Response({"msg":'Your selected Notes are not available'})

            f = serializer.save(sender = request.user)
            f.shared_with.set(shared_with_obj)
            f.note.set(note_obj)
            f.save()
            return Response({'msg':'Notes send Sucessfully','IsSuccess':'True'}, status=status.HTTP_201_CREATED)
        errors = serializer.errors
        errors['IsSuccess'] = 'False'
        return Response(serializer.errors, status=status.HTTP_201_CREATED)






