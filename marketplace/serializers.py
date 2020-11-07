from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = ['item', 'description', 'category', 'image', 'cost', 'available', 'quantity', 'vendor', 'date_added']
        fields = '__all__'
        # depth = 1
