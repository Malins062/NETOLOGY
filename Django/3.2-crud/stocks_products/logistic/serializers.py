from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', ]


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        # fields = '__all__'
        fields = ['id', 'product', 'quantity', 'price', ]


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    # products = ProductSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions', ]

    def create(self, validated_data):
        positions = validated_data.pop('positions', False)

        stock = super().create(validated_data)

        for product in positions:
            StockProduct.objects.create(stock=stock, **product)

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')

        stock = super().update(instance, validated_data)

        for product in positions:
            StockProduct.objects.update_or_create(stock=instance, product=product.get('product'), defaults=product)

        return stock
