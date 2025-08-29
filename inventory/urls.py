from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, InventoryItemViewSet, InventoryChangeViewSet, inventory_report

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('items', InventoryItemViewSet, basename='items')
router.register('changes', InventoryChangeViewSet, basename='changes')

urlpatterns = [
    path('', include(router.urls)),
     path("reports/", inventory_report, name="inventory-report"),
]