from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .serializes import *
from .models import *

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from rest_framework import status
from rest_framework.response import Response



#CRUD Operations
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class ListTodo(generics.ListAPIView):
    serializer_class = ToDOSerializer
    def get_queryset(self):
        user = self.request.user
        print(user)
        queryset = Todo.objects.filter(User=user)
        return queryset
    
    
#route to get favorite todo
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class ListFavoriteTodo(generics.ListAPIView):
    serializer_class = ToDOSerializer
    def get_queryset(self):
        user = self.request.user
        print(user)
        queryset = Todo.objects.filter(User=user, is_favorite=True)
        return queryset

#route to get completed todo
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class ListCompletedTodo(generics.ListAPIView):
    serializer_class = ToDOSerializer
    def get_queryset(self):
        user = self.request.user
        print(user)
        queryset = Todo.objects.filter(User=user, Completed=True)
        return queryset

#route to get uncompleted todo
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class ListUncompletedTodo(generics.ListAPIView):
    serializer_class = ToDOSerializer
    def get_queryset(self):
        user = self.request.user
        print(user)
        queryset = Todo.objects.filter(User=user, Completed=False)
        return queryset

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class TodoItemUpdateView(generics.UpdateAPIView):
    queryset = Todo.objects.all()
    serializer_class = ToDOSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.User != request.user:
            return Response({"error": "Vous n'êtes pas autorisé à modifier ce todo."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)



@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class DetailTodo(generics.RetrieveAPIView):
    serializer_class = ToDOSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Todo.objects.filter(User=user)
        print("my print", queryset)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.User != request.user:
            return Response({"error": "Vous n'êtes pas autorisé à accéder à ce todo."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class CreateTodo(generics.CreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = ToDOSerializer

    def perform_create(self, serializer):
        serializer.save(User=self.request.user)


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class DeleteTodo(generics.DestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = ToDOSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.User != request.user:
            return Response({"error": "Vous n'êtes pas autorisé à supprimer ce todo."}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response({"message": "Suppression réussie."}, status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    token = request.auth
    if token:
        token.delete()
        return Response({"success": "Vous avez été déconnecté avec succès."})
    else:
        return Response({"error": "Impossible de trouver le jeton d'authentification."}, status=status.HTTP_400_BAD_REQUEST)
