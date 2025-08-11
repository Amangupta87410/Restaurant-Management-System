from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuItemViewSet, TableViewSet, ReservationViewSet, OrderViewSet, OrderItemViewSet, register_user, login_user

router = DefaultRouter()
router.register(r'menu-items', MenuItemViewSet)
router.register(r'tables', TableViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet) 

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
]