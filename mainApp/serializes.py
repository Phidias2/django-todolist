from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User



class ToDOSerializer(serializers.ModelSerializer):
    User = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Todo
        fields = ['id', 'Title','User', 'Description', 'Date', 'Completed', 'is_favorite']
    
    # def partial_update(self, instance, validated_data):
    #     field = self.context['request'].parser_context['kwargs']['field']
    #     setattr(instance, field, validated_data[field])
    #     instance.save()
    #     return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['id', 'username', 'password', 'email']

