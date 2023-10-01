from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Note

class NoteAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

    def test_create_note_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        data = {
            "title": "Test Note",
            "body": "This is a test note.",
            "tags": "tag1,tag2",
            "is_public": False
        }

        response = self.client.post('/api/notes/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the note was created
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()
        self.assertEqual(note.title, "Test Note")
        self.assertEqual(note.user, self.user)

    def test_create_note_unauthenticated(self):
        data = {
            "title": "Test Note",
            "body": "This is a test note.",
            "tags": "tag1,tag2",
            "is_public": False
        }

        response = self.client.post('/api/notes/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Check if the note was not created
        self.assertEqual(Note.objects.count(), 0)

    def test_view_public_note_unauthenticated(self):
        public_note = Note.objects.create(user=self.user, title='Public Note', body='This is a public note.', is_public=True)
        
        response = self.client.get(f'/api/notes/detail/{public_note.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_private_note_unauthenticated(self):
        private_note = Note.objects.create(user=self.user, title='Private Note', body='This is a private note.', is_public=False)
        
        response = self.client.get(f'/api/notes/detail/{private_note.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modify_public_note_unauthenticated(self):
        public_note = Note.objects.create(user=self.user, title='Public Note', body='This is a public note.', is_public=True)

        data = {
            "title": "Updated Public Note",
            "body": "This is the updated content of the public note.",
            "tags": "tag3,tag4",
            "is_public": True
        }
        
        response = self.client.put(f'/api/notes/detail/{public_note.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_modify_private_note_unauthenticated(self):
        private_note = Note.objects.create(user=self.user, title='Private Note', body='This is a private note.', is_public=False)

        data = {
            "title": "Updated Private Note",
            "body": "This is the updated content of the private note.",
            "tags": "tag3,tag4",
            "is_public": False
        }
        
        response = self.client.put(f'/api/notes/detail/{private_note.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_modify_private_note_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        private_note = Note.objects.create(user=self.user, title='Private Note', body='This is a private note.', is_public=False)

        data = {
            "title": "Updated Private Note",
            "body": "This is the updated content of the private note.",
            "tags": "tag3,tag4",
            "is_public": False
        }
        
        response = self.client.put(f'/api/notes/detail/{private_note.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the note was updated
        updated_note = Note.objects.get(pk=private_note.id)
        self.assertEqual(updated_note.title, "Updated Private Note")

    def test_delete_private_note_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        private_note = Note.objects.create(user=self.user, title='Private Note', body='This is a private note.', is_public=False)
        
        response = self.client.delete(f'/api/notes/detail/{private_note.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the note was deleted
        self.assertEqual(Note.objects.count(), 0)
