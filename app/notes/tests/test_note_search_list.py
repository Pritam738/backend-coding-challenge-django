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

    def test_note_search_view(self):
        # Create notes for the authenticated user
        Note.objects.create(user=self.user, title='Note 1', body='This is the first note.', is_public=False)
        Note.objects.create(user=self.user, title='Note 2', body='This is the second note.', is_public=True)
        
        # Create a public note
        Note.objects.create(user=User.objects.create_user(username='otheruser', password='otherpassword'),
                            title='Public Note', body='This is a public note.', is_public=True)

        # Authenticate the client with the user's token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Test searching for notes
        response = self.client.get('/api/notes/search/?keywords=second')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one note with "second" in its content

    def test_note_list_view(self):
        # Create notes for the authenticated user
        Note.objects.create(user=self.user, title='Note 1', body='This is the first note.', is_public=False)
        Note.objects.create(user=self.user, title='Note 2', body='This is the second note.', is_public=True)
        
        # Create notes for another user (should not be included in the list)
        User.objects.create_user(username='otheruser', password='otherpassword')
        Note.objects.create(user=User.objects.get(username='otheruser'), title='Other User Note', body='This is another user\'s note.', is_public=False)
        
        # Authenticate the client with the user's token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Test listing user's notes
        response = self.client.get('/api/notes/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Only the user's own notes should be listed

        # Test filtering notes by tags
        response = self.client.get('/api/notes/list/?tags=tag1,tag2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No notes with "tag1" or "tag2" should be found

        # Create notes with tags for the user
        Note.objects.create(user=self.user, title='Note with Tags', body='This note has tags.', is_public=False, tags='tag1,tag2')

        # Test filtering notes by tags again
        response = self.client.get('/api/notes/list/?tags=tag1,tag2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # One note with "tag1" and "tag2" should be found
