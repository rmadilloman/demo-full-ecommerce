from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer
from products.models import Product

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # this is so users can only see their own orders
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        """
        Expected body example:
        {
            "items": [
                {"product_id": 1, "quantity": 2},
                {"product_id": 3, "quantity": 1}
            ]
        }
        """
        items_data = request.data.get('items', [])

        if not items_data:
            return Response(
                {"error": "No items provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order = Order.objects.create(user=request.user, total=0)
        total = 0

        for item in items_data:
            try:
                product = Product.objects.get(id=item['product_id'])
                quantity = int(item.get('quantity', 1))
                price = product.price

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                total += price * quantity
            except Product.DoesNotExist:
                order.delete()
                return Response(
                    {"error": f"Product with id {item['product_id']} not found"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        order.total = total
        order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)