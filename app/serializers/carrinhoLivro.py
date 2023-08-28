from rest_framework.serializers import ModelSerializer

from app.models import CarrinhoLivro

class CarrinhoLivroSerializer(ModelSerializer):
    class Meta:
        model = CarrinhoLivro
        fields = "__all__"
        depth = 2

class CarrinhoLivroSerializerCreate(ModelSerializer):
    class Meta:
        model = CarrinhoLivro
        fields = "__all__"

