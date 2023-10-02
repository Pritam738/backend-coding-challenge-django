from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from ..models import Note 

class NoteDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a test note belonging to the user
        self.note = Note.objects.create(
            user=self.user,
            title='Test Note',
            body="This is the content of your note.",
            tags="tag1,tag2",
            is_public=False
        )

    def test_get_note_with_permission(self):
        response = self.client.get(f'/api/notes/detail/{self.note.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_note_without_permission(self):
        # Create another user who does not own the note
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpassword'
        )
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + other_token.key)

        response = self.client.get(f'/api/notes/detail/{self.note.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_note_with_permission(self):
        updated_data = {
            'title': 'Updated Note',
            "body": "This is the content of your note.",
            "tags": "tag1,tag2",
            "is_public": False
        }
        response = self.client.put(f'/api/notes/detail/{self.note.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the note has been updated
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, updated_data['title'])

    def test_get_public_note_without_permission(self):
        # Create another user who does not own the note, 
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpassword'
        )
        other_token = Token.objects.create(user=other_user)
        # make the note public
        updated_data = {
            'title': 'Updated Note',
            "body": "This is the content of your note.",
            "tags": "tag1,tag2",
            "is_public": True
        }
        response = self.client.put(f'/api/notes/detail/{self.note.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + other_token.key)
        response = self.client.get(f'/api/notes/detail/{self.note.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_note_without_permission(self):
        # Create another user who does not own the note
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpassword'
        )
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + other_token.key)

        updated_data = {
            'title': 'Updated Note',
        }
        response = self.client.put(f'/api/notes/detail/{self.note.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_note_with_permission(self):
        response = self.client.delete(f'/api/notes/detail/{self.note.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the note has been deleted
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_delete_note_without_permission(self):
        # Create another user who does not own the note
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpassword'
        )
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + other_token.key)

        response = self.client.delete(f'/api/notes/detail/{self.note.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
