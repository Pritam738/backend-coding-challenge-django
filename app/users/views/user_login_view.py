# views.py
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
import logging

logger = logging.getLogger("UserLoginView")
    
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        logger.info(f"User '{username}' logged in successfully.")
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        logger.warning(f"Failed login attempt for username '{username}'.")
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)