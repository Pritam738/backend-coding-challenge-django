from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
import logging

logger = logging.getLogger("UserRegisterView")

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.create_user(username=username, password=password)

        # Create an authentication token for the new user
        token, created = Token.objects.get_or_create(user=user)
        logger.info(f"User created with username '{username}'.")

        return Response({'message': 'User created successfully.', 'token': token.key}, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.warning(f"Failed to create user with username '{username}'.")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
