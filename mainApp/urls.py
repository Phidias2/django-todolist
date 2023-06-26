from django.urls import path
from .views import *

urlpatterns = [
    path('todos/<int:pk>/', DetailTodo.as_view()),
    path('todos/<int:pk>/update', TodoItemUpdateView.as_view()),
    path('todos', ListTodo.as_view()),
    path('todos/favorite', ListFavoriteTodo.as_view()),
    path('todos/completed', ListCompletedTodo.as_view()),
    path('todos/uncompleted', ListUncompletedTodo.as_view()),
    path('todos/create', CreateTodo.as_view()),
    path('todos/delete/<int:pk>', DeleteTodo.as_view()),
    path('signup', signup),
    path('login', login),
    path('logout', logout),
    path('test_token', test_token),
]