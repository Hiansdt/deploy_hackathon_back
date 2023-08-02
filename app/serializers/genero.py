from rest_framework.serializers import ModelSerializer

from app.models import Genero

class GeneroSerializer(ModelSerializer):
    class Meta:
        model = Genero
        fields = "__all__"
        depth = 1