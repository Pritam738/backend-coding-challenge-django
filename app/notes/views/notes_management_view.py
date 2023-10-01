from ..models import Note
from ..serializers import NoteSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
import logging

logger = logging.getLogger("NoteManagementView")

class NoteCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = NoteSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(user=request.user)  # Attach the user to the note
            logger.info("Note created successfully.", data=serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning("Issue with Note creation.",error=serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NoteDetailView(APIView):
    '''
        Allow Public Access for Read-Only (GET):
            If a note is public (is_public=True), allow anyone to access it without authentication.
            If a note is private (is_public=False), require authentication to access it.
            
        Disallow Modification for Public Notes (PUT and DELETE):
            If a note is public (is_public=True), disallow modification (PUT and DELETE)
              for all users, even if they are authenticated.
            If a note is private (is_public=False), allow the owner (authenticated user)
              to modify or delete it.
    '''
    permission_classes = [IsAuthenticatedOrReadOnly]
    

    def get(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        if not note.is_public and note.user != request.user:
            # If the note is private and the user is not the creator, return 403 Forbidden
            logger.warning("You do not have permission to view this note.",user=request.user)
            return Response({'detail': 'You do not have permission to view this note.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def put(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        
        if note.user != request.user:
            # If the note is private and the user is not the creator, return 403 Forbidden
            logger.warning("You do not have permission to modify this note.",user=request.user)
            return Response({'detail': 'You do not have permission to modify this note.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = NoteSerializer(note, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)

        if note.user != request.user:
            # If the note is private and the user is not the creator, return 403 Forbidden
            logger.warning("You do not have permission to delete this note.",user=request.user)
            return Response({'detail': 'You do not have permission to delete this note.'}, status=status.HTTP_403_FORBIDDEN)

        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)