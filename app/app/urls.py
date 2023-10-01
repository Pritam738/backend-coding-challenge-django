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
from users.views.user_login_view import user_login
from users.views.user_registration_view import register_user
from notes.views.notes_management_view import NoteCreateView, NoteDetailView
from notes.views.note_search_view import NoteSearchView, NoteListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/notes/search/', NoteSearchView.as_view(), name='note-search'), # user can search notes based on keywords 
    path('api/notes/list/', NoteListView.as_view(), name='note-filter'), # get all notes of a user also user can filter based on tags
    path('api/notes/create/', NoteCreateView.as_view(), name='note-create'), # user can create notes
    path('api/notes/detail/<int:note_id>/', NoteDetailView.as_view(), name='note-detail'), # user can get, edit, delete a note
    path('api/login/', user_login, name='user_login'), # user login api
    path('api/register/', register_user, name='register_user'), #user register api
]
