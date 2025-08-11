from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50, default='Main Course')
    stock = models.IntegerField(default=0) 
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
        ordering = ['name']

    def __str__(self):
        return self.name

class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Table"
        verbose_name_plural = "Tables"
        ordering = ['table_number']

    def __str__(self):
        return f"Table {self.table_number} (Capacity: {self.capacity})"

class Reservation(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, related_name='reservations')
    reservation_time = models.DateTimeField()
    number_of_guests = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        ordering = ['reservation_time']

    def __str__(self):
        return f"Reservation for {self.customer_name} at {self.reservation_time.strftime('%Y-%m-%d %H:%M')}"

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup/Serve'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    customer_name = models.CharField(max_length=100, blank=True, null=True) # For takeout/delivery
    order_time = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-order_time']

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

    def calculate_total(self):
        """Calculates the total amount of the order based on its items."""
        total = sum(item.get_total_price() for item in self.items.all())
        self.total_amount = total
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT) 
    quantity = models.IntegerField(default=1)
    price_at_order = models.DecimalField(max_digits=6, decimal_places=2) 

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        unique_together = ('order', 'menu_item') 

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} in Order #{self.order.id}"

    def get_total_price(self):
        return self.quantity * self.price_at_order

    def save(self, *args, **kwargs):
        if not self.pk: 
            self.price_at_order = self.menu_item.price
        super().save(*args, **kwargs)