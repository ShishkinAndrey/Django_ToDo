from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about),
    path('api/v1/notes/', views.ToDoGetView.as_view()),
    path('api/v1/notes/<int:note_id>', views.ToDoDetailedGetView.as_view()),
    path('api/v1/add/', views.ToDoPostView.as_view()),
    path('api/v1/edit/<int:note_id>',views.ToDoPatchView.as_view()),
    path('api/v1/delete/<int:note_id>', views.ToDoDeleteView.as_view()),
]
