from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import User, Patient, Scheduler, Provider
from ..serializers import UserSerializer

@api_view(['GET', 'POST', 'DELETE'])
def restore_user(request):
    """Session endpoint.

    GET    - restore user from Django session (for "keep me logged in" flows)
    POST   - log in (sets session user_id)
    DELETE - log out (clears session user_id)
    """

    if request.method == 'GET':
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({'errors': ['User not authenticated']}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'errors': ['User not found']}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response({'user': serializer.data})

    if request.method == 'POST':
        username = request.data.get('username')
        pin = request.data.get('pin')

        if not username or not pin:
            return Response({'errors': ['Username and pin required']}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'errors': ['Invalid credentials']}, status=status.HTTP_401_UNAUTHORIZED)

        if user.pin != int(pin):
            return Response({'errors': ['Invalid credentials']}, status=status.HTTP_401_UNAUTHORIZED)

        request.session['user_id'] = user.id
        serializer = UserSerializer(user)
        return Response({'user': serializer.data})

    if request.method == 'DELETE':
        if 'user_id' in request.session:
            del request.session['user_id']
        return Response(status=status.HTTP_204_NO_CONTENT)
        