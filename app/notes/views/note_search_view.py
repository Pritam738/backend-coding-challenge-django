from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from ..models import Note
from ..serializers import NoteSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import generics
import logging

logger = logging.getLogger("NoteSearchView")

class NoteSearchView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        keywords = request.query_params.get('keywords', '')
        logger.info(f"Received search request with keywords: {keywords}")
        if keywords:
            # Perform case-insensitive search in title and body fields for the user's notes
            if request.user.is_authenticated:  # Check if the user is authenticated
                user_notes = Note.objects.filter(
                    Q(title__icontains=keywords) | Q(body__icontains=keywords),
                    Q(user=request.user)
                )
            else:
                user_notes = Note.objects.none()  # If not authenticated, return no user notes

            # Perform case-insensitive search in title and body fields for public notes
            public_notes = Note.objects.filter(
                Q(title__icontains=keywords) | Q(body__icontains=keywords),
                Q(is_public=True)
            )

            # Combine user's notes and public notes
            notes = user_notes | public_notes

            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data)
        else:
            logger.warning("Search request did not provide keywords")
            return Response({'detail': 'Please provide keywords for the search.'}, status=status.HTTP_400_BAD_REQUEST)

class NoteListView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Note.objects.filter(user=self.request.user)
        tags = self.request.query_params.get('tags', '')
        if tags:
            logger.info(f"Received list request with tags: {tags}")
            queryset = queryset.filter(tags__icontains=tags)
        return queryset
