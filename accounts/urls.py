from django.urls import path
from .views import UserProfileList, SellerRegistrationView, InventoryListCreateView, InventoryDetailView

urlpatterns = [
    path('users/', UserProfileList.as_view()),
    path('register/seller/', SellerRegistrationView.as_view(), name='seller-registration'),
    path('inventory/', InventoryListCreateView.as_view(), name='inventory-list-create'),
    path('inventory/<int:pk>/', InventoryDetailView.as_view(), name='inventory-detail'),
]