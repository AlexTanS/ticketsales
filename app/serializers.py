from rest_framework import serializers

from .models import ListOfServices


class ListOfServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfServices
        fields = "__all__"

