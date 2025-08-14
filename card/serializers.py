from rest_framework import serializers
from .models import CardItem, Card

class CardItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CardItem
        fields = ['id', 'card', 'product', 'amount', 'created_at', 'updated_at', 'total_price']

class CardSerializer(serializers.ModelSerializer):
    items = CardItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()
    class Meta:
        model = Card
        fields = ['id', 'user', 'create_at', 'total_price', 'items']

