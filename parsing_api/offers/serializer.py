from rest_framework import serializers

from offers.models import Offer, Product


class OfferSerializer(serializers.ModelSerializer):
    data = serializers.JSONField()

    class Meta:
        model = Offer
        fields = ['data']


class ProductSerializer(serializers.ModelSerializer):
    offers = OfferSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['region', 'domain', 'link', 'status', 'offers']


class ProductServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'data']
