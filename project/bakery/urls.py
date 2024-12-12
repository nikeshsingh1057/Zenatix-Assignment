from django.urls import path
from .views import (
    UserRegistrationView,
    AddIngredientView,
    CreateBakeryItemView,
    BakeryItemDetailView,
    ListProductsView,
    PlaceOrderView,
    OrderHistoryView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Authentication
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Admin Endpoints
    path('admin/ingredients/', AddIngredientView.as_view(), name='add_ingredient'),
    path('admin/bakery-items/', CreateBakeryItemView.as_view(), name='create_bakery_item'),
    path('admin/bakery-items/<int:pk>/', BakeryItemDetailView.as_view(), name='bakery_item_detail'),

    # Customer Endpoints
    path('products/', ListProductsView.as_view(), name='list_products'),
    path('orders/', PlaceOrderView.as_view(), name='place_order'),
    path('orders/history/', OrderHistoryView.as_view(), name='order_history'),
]
