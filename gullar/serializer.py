from rest_framework import serializers
from .models import Gullar

class GullarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gullar
        fields = "__all__"
