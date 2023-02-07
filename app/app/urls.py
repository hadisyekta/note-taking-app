"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import notes.views
import notes.api_views

# TODO: change urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', notes.api_views.NotesList.as_view()),
    path('mynotes/add', notes.api_views.NotesCreate.as_view()),
    path('mynotes/<int:id>/',
         notes.api_views.NotesRetrieveUpdateDestroy.as_view()),

    path('tags/', notes.api_views.TagsListCreateAPIView.as_view()),

    # with templates
    path('v1', notes.views.noteList, name='notes-list'),
    path('v1/notes/<int:id>/', notes.views.noteDetails, name='note-details')
]
