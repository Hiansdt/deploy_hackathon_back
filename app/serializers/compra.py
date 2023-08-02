from rest_framework.serializers import ModelSerializer

from app.models import Compra

class CompraSerializer(ModelSerializer):
    class Meta:
        model = Compra
        fields = "__all__"
        depth = 1

class CompraSerializerCreate(ModelSerializer):
    class Meta:
        model = Compra
        fields = "__all__"

