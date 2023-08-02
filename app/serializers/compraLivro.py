from rest_framework.serializers import ModelSerializer

from app.models import CompraLivro

class CompraLivroSerializer(ModelSerializer):
    class Meta:
        model = CompraLivro
        fields = "__all__"
        depth = 1

class CompraLivroSerializerCreate(ModelSerializer):
    class Meta:
        model = CompraLivro
        fields = "__all__"

