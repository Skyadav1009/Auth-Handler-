from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserRegistrationSerializer, UpdateUsernameSerializer


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                         'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token')}, required=['refresh']))
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out.'},
                            status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': 'Invalid token or token already blacklisted.'},
                            status=status.HTTP_400_BAD_REQUEST)


class UpdateUsernameView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=UpdateUsernameSerializer)
    def put(self, request):
        serializer = UpdateUsernameSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            new_username = serializer.validated_data['new_username']
            user = request.user
            if user.email != email:
                return Response({'error': 'Invalid email or password'},
                                status=status.HTTP_400_BAD_REQUEST)
            if not user.check_password(password):
                return Response({'error': 'Invalid email or password'},
                                status=status.HTTP_400_BAD_REQUEST)
            user.username = new_username
            user.save()
            return Response(
                {'message': f'Username successfully updated to {new_username}.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Delete the logged-in user's account permanently.",
                         responses={204: 'User account successfully deleted.'})
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({'message': 'User account successfully deleted.'},
                        status=status.HTTP_204_NO_CONTENT)
