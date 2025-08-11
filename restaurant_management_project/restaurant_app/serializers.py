from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MenuItem, Table, Reservation, Order, OrderItem


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, for registration.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class MenuItemSerializer(serializers.ModelSerializer):
    """Serializer for MenuItem model."""
    class Meta:
        model = MenuItem
        fields = '__all__' 

class TableSerializer(serializers.ModelSerializer):
    """Serializer for Table model."""
    class Meta:
        model = Table
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    """Serializer for Reservation model."""
    table_number = serializers.ReadOnlyField(source='table.table_number') 

    class Meta:
        model = Reservation
        fields = ['id', 'customer_name', 'customer_phone', 'table', 'table_number', 'reservation_time', 'number_of_guests', 'notes', 'is_confirmed']

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model."""
    menu_item_name = serializers.ReadOnlyField(source='menu_item.name') 

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_name', 'quantity', 'price_at_order']
        read_only_fields = ['price_at_order'] 

class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model, including nested OrderItems."""
    items = OrderItemSerializer(many=True, read_only=True) 
    table_number = serializers.ReadOnlyField(source='table.table_number') 

    class Meta:
        model = Order
        fields = ['id', 'table', 'table_number', 'customer_name', 'order_time', 'total_amount', 'status', 'notes', 'items']
        read_only_fields = ['order_time', 'total_amount', 'status', 'items'] 
    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        return order
