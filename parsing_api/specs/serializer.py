from rest_framework import serializers

from specs.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['domain', 'data']


class ProductServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'data']
