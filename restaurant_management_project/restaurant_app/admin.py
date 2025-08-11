from django.contrib import admin
from .models import MenuItem, Table, Reservation, Order, OrderItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_available')

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'capacity', 'is_available')
    list_filter = ('is_available', 'capacity')
    search_fields = ('table_number',)
    list_editable = ('is_available',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'table', 'reservation_time', 'number_of_guests', 'is_confirmed')
    list_filter = ('is_confirmed', 'reservation_time')
    search_fields = ('customer_name', 'customer_phone')
    date_hierarchy = 'reservation_time'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'customer_name', 'order_time', 'total_amount', 'status')
    list_filter = ('status', 'order_time', 'table')
    search_fields = ('customer_name', 'id')
    date_hierarchy = 'order_time'
    inlines = [OrderItemInline]
    readonly_fields = ('order_time', 'total_amount')
    fieldsets = (
        (None, {
            'fields': ('table', 'customer_name', 'notes', 'status')
        }),
        ('Order Details', {
            'fields': ('order_time', 'total_amount'),
            'classes': ('collapse',)
        }),
    )

