from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Note


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ToDoSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ['author', ]


class QueryParamsSerializer(serializers.Serializer):
    state = serializers.ListField(child=serializers.ChoiceField(choices=Note.STATE), required=False)
    importance = serializers.ListField(child=serializers.BooleanField(), required=False)
    public = serializers.ListField(child=serializers.BooleanField(), required=False)
