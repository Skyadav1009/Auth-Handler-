from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserRegistrationSerializer, UpdateUsernameSerializer, InventorySaleSerializer
from .models import InventorySale

User = get_user_model()

class InventorySaleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=InventorySaleSerializer)
    def post(self, request):
        if request.user.role != 'salesman':
            return Response({'error': 'Only salesman can add inventories.'}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = InventorySaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(salesman=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('email', openapi.IN_QUERY, description="Salesman email (Admin only)", type=openapi.TYPE_STRING),
        openapi.Parameter('date', openapi.IN_QUERY, description="Filter by date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
        openapi.Parameter('sort', openapi.IN_QUERY, description="Sort by date (asc or desc, default desc)", type=openapi.TYPE_STRING)
    ])
    def get(self, request):
        if request.user.role == 'admin':
            email = request.query_params.get('email')
            date_filter = request.query_params.get('date')
            sort_order = request.query_params.get('sort', 'desc')
            
            inventories = InventorySale.objects.all()
            if email:
                inventories = inventories.filter(salesman__email=email)
            if date_filter:
                inventories = inventories.filter(date=date_filter)
                
            if sort_order == 'asc':
                inventories = inventories.order_by('date')
            else:
                inventories = inventories.order_by('-date')
                
            serializer = InventorySaleSerializer(inventories, many=True)
            
            total_items = sum(item.quantity for item in inventories)
            total_revenue = sum((item.quantity * item.price) for item in inventories)
            
            return Response({
                'summary': {
                    'total_items_sold': total_items,
                    'total_revenue': total_revenue
                },
                'sales': serializer.data
            })
            
        elif request.user.role == 'salesman':
            inventories = InventorySale.objects.filter(salesman=request.user).order_by('-date')
            serializer = InventorySaleSerializer(inventories, many=True)
            return Response({
                'sales': serializer.data
            })
        else:
            return Response({'error': 'You do not have permission to view sales.'}, status=status.HTTP_403_FORBIDDEN)

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
