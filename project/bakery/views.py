from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Ingredient, BakeryItem, BakeryItemIngredient, Order, OrderItem
from .serializers import (
    UserSerializer, 
    IngredientSerializer, 
    BakeryItemSerializer, 
    OrderSerializer
)

# User Registration
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Admin: Add Ingredient
class AddIngredientView(generics.CreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAdminUser]

# Admin: Create Bakery Item
class CreateBakeryItemView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        data = request.data
        bakery_item_data = {
            "name": data.get("name"),
            "cost_price": data.get("cost_price"),
            "selling_price": data.get("selling_price"),
        }
        serializer = BakeryItemSerializer(data=bakery_item_data)
        if serializer.is_valid():
            bakery_item = serializer.save()
            for ingredient in data.get("ingredients", []):
                BakeryItemIngredient.objects.create(
                    bakery_item=bakery_item,
                    ingredient_id=ingredient["ingredient_id"],
                    percentage_quantity=ingredient["percentage_quantity"],
                )
            return Response({"message": "Bakery item created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Admin: Get Bakery Item Details
class BakeryItemDetailView(generics.RetrieveAPIView):
    queryset = BakeryItem.objects.all()
    serializer_class = BakeryItemSerializer
    permission_classes = [permissions.IsAdminUser]

# Customer: List/Search Products
class ListProductsView(generics.ListAPIView):
    queryset = BakeryItem.objects.all()
    serializer_class = BakeryItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None  # You can define custom pagination here

# Customer: Place Order
class PlaceOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        customer = request.user
        if not customer.is_customer:
            return Response({"error": "Only customers can place orders"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        order = Order.objects.create(customer=customer, total_price=data.get("total_price"))
        for item in data.get("items", []):
            OrderItem.objects.create(
                order=order,
                bakery_item_id=item["bakery_item_id"],
                quantity=item["quantity"],
            )
        return Response({"message": "Order placed successfully"}, status=status.HTTP_201_CREATED)

# Customer: View Order History
class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)
