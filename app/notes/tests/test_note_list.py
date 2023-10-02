from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from ..models import Note
from notes.views.note_search_view import NoteListView

class NoteListViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # Create test notes for the list view
        self.user_note_1 = Note.objects.create(
            user=self.user,
            title='Test Note 1',
            body='This is test note 1.',
            tags='tag1,tag2'
        )

        self.user_note_2 = Note.objects.create(
            user=self.user,
            title='Test Note 2',
            body='This is test note 2.',
            tags='tag3'
        )

        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpassword'
        )

        self.other_user_note = Note.objects.create(
            user=self.other_user,
            title='Other User Note',
            body='This is another user\'s note.',
            tags='tag1,tag4'
        )

    def test_get_notes_by_authenticated_user(self):
        request = self.factory.get('/api/notes/list/')
        force_authenticate(request, user=self.user)
        view = NoteListView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 notes created by the authenticated user

    def test_get_notes_by_authenticated_user_with_tags(self):
        request = self.factory.get('/api/notes/list/', {'tags': 'tag1'})
        force_authenticate(request, user=self.user)
        view = NoteListView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return 1 notes with tag1

    def test_get_notes_by_authenticated_user_with_nonexistent_tags(self):
        request = self.factory.get('/api/notes/list/', {'tags': 'nonexistent'})
        force_authenticate(request, user=self.user)
        view = NoteListView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Should return no results for nonexistent tag

    def test_get_notes_by_unauthenticated_user(self):
        request = self.factory.get('/api/notes/list/')
        view = NoteListView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
