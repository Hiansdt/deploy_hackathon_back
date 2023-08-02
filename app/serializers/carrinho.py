from rest_framework.serializers import ModelSerializer

from app.models import Carrinho

class CarrinhoSerializer(ModelSerializer):
    class Meta:
        model = Carrinho
        fields = "__all__"
        depth = 1