from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from ..models import Note
from notes.views.note_search_view import NoteSearchView

class NoteSearchViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.public_user = User.objects.create_user(
            username='publicuser',
            password='publicpassword'
        )

        # Create test notes for the search view
        self.user_note_1 = Note.objects.create(
            user=self.user,
            title='User Note 1',
            body='This is a user note 1.',
            is_public=False
        )

        self.user_note_2 = Note.objects.create(
            user=self.user,
            title='User Note 2',
            body='This is a user note 2.',
            is_public=True
        )

        self.public_note = Note.objects.create(
            user=self.public_user,
            title='Public Note',
            body='This is a public note.',
            is_public=True
        )

    def test_search_with_keywords_authenticated_user(self):
        request = self.factory.get('/api/notes/search/', {'keywords': 'user note'}, format='json')
        force_authenticate(request, user=self.user)
        view = NoteSearchView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 notes matching the keywords "user note"

    def test_search_with_keywords_unauthenticated_user(self):
        request = self.factory.get('/api/notes/search/', {'keywords': 'public note'}, format='json')
        view = NoteSearchView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return 1 public note matching the keywords "public note"

    def test_search_with_no_keywords(self):
        request = self.factory.get('/api/notes/search/', format='json')
        view = NoteSearchView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_with_nonexistent_keywords(self):
        request = self.factory.get('/api/notes/search/', {'keywords': 'nonexistent'}, format='json')
        view = NoteSearchView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Should return no results for nonexistent keywords

    def test_search_with_special_characters(self):
        request = self.factory.get('/api/notes/search/', {'keywords': '!@#$%^&*()'}, format='json')
        view = NoteSearchView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Should return no results for special characters
