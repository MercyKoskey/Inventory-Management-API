from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db.models import F, Q, Sum
from .models import Category, InventoryItem, InventoryChange
from .serializers import CategorySerializer, InventoryItemSerializer, InventoryChangeSerializer
from .permissions import IsOwner

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    search_fields = ['name', 'category__name']
    ordering_fields = ['name', 'quantity', 'price', 'date_added']

    def get_queryset(self):
        qs = InventoryItem.objects.filter(created_by=self.request.user)

        # Optional filters: category, price range, low stock
        category_id = self.request.query_params.get('category')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        low_stock = self.request.query_params.get('low_stock')  # boolean-like
        threshold = int(self.request.query_params.get('threshold', 5))

        if category_id:
            qs = qs.filter(category_id=category_id)
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)
        if low_stock in ('1', 'true', 'True', 'yes'):
            qs = qs.filter(quantity__lt=threshold)

        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        old_qty = instance.quantity
        instance = serializer.save()
        if old_qty != instance.quantity:
            InventoryChange.objects.create(
                item=instance,
                user=self.request.user,
                old_quantity=old_qty,
                new_quantity=instance.quantity,
            )

    @action(detail=False, methods=['get'])
    def levels(self, request):
        """
        Inventory levels endpoint: returns current quantities (with filters applied).
        """
        items = self.get_queryset()
        data = self.get_serializer(items, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def changes(self, request, pk=None):
        """
        Change history for a single item.
        """
        item = self.get_object()
        changes = item.changes.select_related('user').all()
        return Response(InventoryChangeSerializer(changes, many=True).data)

class InventoryChangeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Global change history (for the logged-in user’s items).
    """
    serializer_class = InventoryChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InventoryChange.objects.filter(item__created_by=self.request.user).select_related('item', 'user')



@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def inventory_report(request):
    user = request.user

    # Total value of inventory
    total_value = InventoryItem.objects.filter(created_by=user).aggregate(
        total=Sum(F("quantity") * F("price"))
    )["total"] or 0

    # Stock levels
    stock_levels = InventoryItem.objects.filter(created_by=user).values(
        "id", "name", "quantity", "price"
    )

    # Sales & Restocking history
    changes_qs = InventoryChange.objects.filter(item__created_by=user).order_by("-timestamp")

    changes = []
    for change in changes_qs:
        if change.new_quantity > change.old_quantity:
            change_type = "restock"
            quantity_changed = change.new_quantity - change.old_quantity
        else:
            change_type = "sale"
            quantity_changed = change.old_quantity - change.new_quantity

        changes.append({
            "id": change.id,
            "item": change.item.name,
            "change_type": change_type,
            "quantity_changed": quantity_changed,
            "changed_by": change.user.username,
            "timestamp": change.timestamp
        })

    return Response({
        "total_value": total_value,
        "stock_levels": list(stock_levels),
        "changes": changes
    })