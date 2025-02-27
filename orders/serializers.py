from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

    def to_internal_value(self, data):
        product_id = data.get('product_id')
        if not product_id:
            raise serializers.ValidationError({"product_id": "Это поле обязательно."})
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"product_id": "Продукт с таким ID не найден."})

        data['product'] = product
        del data['product_id']
        return super().to_internal_value(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product'] = {
            "id": instance.product.id,
            "name": instance.product.name
        }
        return data

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'customer_email', 'customer_phone', 'status', 'shipping_address', 'created_at', 'items']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        items = validated_data.pop("items")
        order = Order.objects.create(**validated_data) #создание заказа
        for item in items:
            order_item = OrderItem(
                order = order,
                product = item['product'], # берем обьект
                quantity = item['quantity'],
                price = item['product'].price # фиксация цены товара
            )
            order_item.save()
        return order