from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth import authenticate
from api.models import Task
from api.serializer import *
from django.contrib.auth.models import User


class RegisterUser(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'message':'Succesfully created user.','token': token.key}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            print(user)
            user = authenticate(username=user.username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, 'id': user.id}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class GetUsersView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if request.user.is_superuser:
            try:
                users = User.objects.all()
                serializer = UserSerializer(users, many=True)
            except User.DoesNotExist:
                return Response({'error': 'No users found'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'users': serializer.data}, status=status.HTTP_200_OK)
        return Response({'error': 'Only superusers can access this endpoint'}, status=status.HTTP_403_FORBIDDEN)


class TaskView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    
    def get(self, request):
        filter = request.query_params.get('status')
        if request.user.is_superuser:
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(assigned_to=request.user)
        if filter:
            tasks = tasks.filter(status=filter)
        serializer = TaskSerializer(tasks, many=True)
        return Response({'tasks': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'Only superusers can create and assign tasks'}, status=status.HTTP_403_FORBIDDEN)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.data.get('assigned_to')
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    serializer.save(assigned_to=user)
                except User.DoesNotExist:
                    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                serializer.save()
            return Response({'message': f'Successfully created task: {serializer.data["title"]}'}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        if request.user.is_superuser:
            serializer = TaskSerializer(task, data=request.data, partial=True)
        else:
            if task.assigned_to != request.user:
                return Response({'error': 'You can only update your assigned tasks'}, status=status.HTTP_403_FORBIDDEN)
            serializer = TaskSerializer(task, data={'status': request.data.get('status')}, partial=True)
            if serializer.is_valid():
                user_id = request.data.get('assigned_to')
                if user_id:
                    try:
                        user = User.objects.get(id=user_id)
                        serializer.save(assigned_to=user)
                    except User.DoesNotExist:
                        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
                else:
                    serializer.save()
                return Response({'message': f'Successfully updated task: {serializer.data["title"]}'}, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        if not request.user.is_superuser:
            return Response({'error': 'Only superusers can delete tasks'}, status=status.HTTP_403_FORBIDDEN)
        try:
            task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response({'message': 'Task deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
