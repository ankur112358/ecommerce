from rest_framework import serializers
from .models import Product, Order, OrderProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock']


class ProductOrderInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderSerializer(serializers.ModelSerializer):
    products = ProductOrderInputSerializer(many=True, write_only=True)
    products_details = serializers.SerializerMethodField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    status = serializers.CharField(read_only=True)  # Ensure status is read-only

    class Meta:
        model = Order
        fields = ['id', 'products', 'products_details', 'total_price', 'status']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order.objects.create(total_price=0)  # Default status is "pending"
        total_price = 0

        for product_item in products_data:
            product_id = product_item['product_id']
            quantity = product_item['quantity']

            # Retrieve product and validate stock
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with ID {product_id} does not exist.")

            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for {product.name}. Available: {product.stock}"
                )

            # Deduct stock
            product.stock -= quantity
            product.save()

            # Create order-product relationship
            OrderProduct.objects.create(order=order, product=product, quantity=quantity)

            # Calculate total price
            total_price += product.price * quantity

        # Update order total price
        order.total_price = total_price
        order.save()
        return order

    def get_products_details(self, obj):
        """Custom method to return details about products in an order."""
        order_products = OrderProduct.objects.filter(order=obj)
        return [
            {
                "product_id": order_product.product.id,
                "name": order_product.product.name,
                "quantity": order_product.quantity
            }
            for order_product in order_products
        ]