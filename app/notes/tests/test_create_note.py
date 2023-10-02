from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from ..models import Note
from  notes.views.notes_management_view import NoteCreateView

class NoteCreateViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_create_note_success(self):
        request_data = {
            'title': 'Test Note',
            'body': 'This is a test note.'
        }
        request = self.factory.post('/api/notes/create/', request_data, format='json')
        force_authenticate(request, user=self.user)
        view = NoteCreateView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)  # Should have 1 note after creation

    def test_create_note_without_authentication(self):
        request_data = {
            'title': 'Test Note',
            'body': 'This is a test note.'
        }
        request = self.factory.post('/api/notes/create/', request_data, format='json')
        view = NoteCreateView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_note_with_invalid_data(self):
        request_data = {
            'title': '',  # Invalid: Title is required
            'body': 'This is a test note.'
        }
        request = self.factory.post('/api/notes/create/', request_data, format='json')
        force_authenticate(request, user=self.user)
        view = NoteCreateView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Note.objects.count(), 0)  # Should not create a note with invalid data

