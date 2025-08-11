from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.db import transaction
from .models import MenuItem, Table, Reservation, Order, OrderItem
from .serializers import MenuItemSerializer, TableSerializer, ReservationSerializer, OrderSerializer, OrderItemSerializer, UserSerializer




@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': serializer.data,
            'token': token.key,
            'role': 'customer' 
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        role = 'admin' if user.is_superuser else 'customer'
        return Response({
            'message': 'Login successful!',
            'token': token.key,
            'role': role
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class MenuItemViewSet(viewsets.ModelViewSet):
    
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    @action(detail=True, methods=['post'])
    @permission_classes([AllowAny])

    def update_stock(self, request, pk=None):
    
        menu_item = self.get_object()
        new_stock = request.data.get('stock')
        if new_stock is not None:
            try:
                new_stock = int(new_stock)
                if new_stock < 0:
                    return Response({"error": "Stock cannot be negative."}, status=status.HTTP_400_BAD_REQUEST)
                menu_item.stock = new_stock
                menu_item.save()
                return Response(self.get_serializer(menu_item).data)
            except ValueError:
                return Response({"error": "Invalid stock value."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Stock value not provided."}, status=status.HTTP_400_BAD_REQUEST)

class TableViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tables to be viewed or edited.
    """
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    @action(detail=True, methods=['post'])
    @permission_classes([AllowAny])

    def set_availability(self, request, pk=None):
        """Custom action to set table availability."""
        table = self.get_object()
        is_available = request.data.get('is_available')
        if is_available is not None:
            table.is_available = bool(is_available)
            table.save()
            return Response(self.get_serializer(table).data)
        return Response({"error": "Availability status not provided."}, status=status.HTTP_400_BAD_REQUEST)

class ReservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reservations to be viewed or created/edited.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        table_id = serializer.validated_data.get('table').id
        try:
            table = Table.objects.get(id=table_id)
            if not table.is_available:
                return Response({"error": f"Table {table.table_number} is not available."},
                                status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                reservation = serializer.save()
                table.is_available = False
                table.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Table.DoesNotExist:
            return Response({"error": "Table not found."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        table = instance.table
        with transaction.atomic():
            self.perform_destroy(instance)
            if table: 
                table.is_available = True
                table.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows orders to be viewed, created, or edited.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated] 


    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Custom action to update the status of an order."""
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status and new_status in [choice[0] for choice in order.ORDER_STATUS_CHOICES]:
            order.status = new_status
            order.save()
            return Response(self.get_serializer(order).data)
        return Response({"error": "Invalid or missing status."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """Custom action to add an item to an existing order."""
        order = self.get_object()
        menu_item_id = request.data.get('menu_item_id')
        quantity = request.data.get('quantity', 1)

        try:
            menu_item = MenuItem.objects.get(id=menu_item_id)
        except MenuItem.DoesNotExist:
            return Response({"error": "Menu item not found."}, status=status.HTTP_404_NOT_FOUND)

        if not isinstance(quantity, int) or quantity <= 0:
            return Response({"error": "Quantity must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

        if menu_item.stock < quantity:
            return Response({"error": f"Not enough {menu_item.name} in stock. Available: {menu_item.stock}"},
                            status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            order_item, created = OrderItem.objects.get_or_create(
                order=order,
                menu_item=menu_item,
                defaults={'quantity': quantity, 'price_at_order': menu_item.price}
            )
            if not created:
                order_item.quantity += quantity
                order_item.save()

            menu_item.stock -= quantity
            menu_item.save()
            order.calculate_total() 

            return Response(self.get_serializer(order).data)

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        """Custom action to remove an item from an existing order."""
        order = self.get_object()
        order_item_id = request.data.get('order_item_id')

        try:
            order_item = OrderItem.objects.get(id=order_item_id, order=order)
        except OrderItem.DoesNotExist:
            return Response({"error": "Order item not found in this order."}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            order_item.menu_item.stock += order_item.quantity
            order_item.menu_item.save()
            order_item.delete()
            order.calculate_total() 
            return Response(self.get_serializer(order).data)


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows order items to be viewed or edited.
    Generally, order items are managed via the OrderViewSet, but this provides direct access.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
