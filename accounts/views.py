from rest_framework import generics, permissions
from .models import UserProfile, Inventory
from .serializers import UserProfileSerializer, SellerRegistrationSerializer, InventorySerializer

class UserProfileList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class SellerRegistrationView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = SellerRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class IsSeller(permissions.BasePermission):
    """
    Custom permission to only allow sellers to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == 'seller'


class InventoryListCreateView(generics.ListCreateAPIView):
    serializer_class = InventorySerializer
    permission_classes = [IsSeller]

    def get_queryset(self):
        return Inventory.objects.filter(seller=self.request.user)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InventorySerializer
    permission_classes = [IsSeller]

    def get_queryset(self):
        return Inventory.objects.filter(seller=self.request.user)