from django.conf import settings
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Note
from .serializer import ToDoSerializer, QueryParamsSerializer


def about(request):
    params = {
        'user': request.user,
        'version': settings.SERVER_VERSION
    }
    return render(request, 'about.html', params)


class ToDoGetView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            get_model = Note.objects.order_by('-pubdate', '-importance').filter(Q(author=request.user) | Q(public=True))
        else:
            get_model = Note.objects.order_by('-pubdate', '-importance').filter(public=True)
        query_params = QueryParamsSerializer(data=request.query_params)
        if query_params.is_valid():
            if query_params.data.get('importance'):
                get_model = get_model.filter(importance__in=query_params.data['importance'])
            if query_params.data.get('public'):
                get_model = get_model.filter(public__in=query_params.data['public'])
            if query_params.data.get('state'):
                get_model = get_model.filter(state__in=query_params.data['state'])
        else:
            return Response(query_params.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = ToDoSerializer(get_model, many=True)
        return Response(serializer.data)


class ToDoDetailedGetView(APIView):
    def get(self, request, note_id):
        if request.user.is_authenticated:
            new_model = Note.objects.filter(Q(pk=note_id) & Q(author=request.user))
        else:
            new_model = Note.objects.filter(Q(pk=note_id) & Q(public=True))
        if not new_model:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ToDoSerializer(new_model, many=True)
        return Response(serializer.data)


class ToDoPostView(APIView):
    def post(self, request):
        new_model = ToDoSerializer(data=request.data)
        if new_model.is_valid():
            new_model.save(author=request.user)
            return Response(new_model.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_model.errors, status=status.HTTP_400_BAD_REQUEST)


class ToDoPatchView(APIView):
    def patch(self, request, note_id):
        # Добавив фильтр по автору, тем самым ограничил возможность редактирования записей только автором
        model = Note.objects.filter(pk=note_id, author=request.user).first()
        if not model:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ToDoSerializer(model, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ToDoDeleteView(APIView):
    def delete(self, request, note_id):
        model = Note.objects.filter(pk=note_id, author=request.user)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

