from rest_framework.viewsets import ModelViewSet
from app.models import CarrinhoLivro
from app.serializers import CarrinhoLivroSerializer, CarrinhoLivroSerializerCreate
from rest_framework.viewsets import ModelViewSet
from config.decorators import jwt_optional
from rest_framework.permissions import AllowAny
from rest_framework.permissions import BasePermission
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response

class CarrinhoLivroViewSet(ModelViewSet):
    queryset = CarrinhoLivro.objects.all()
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CarrinhoLivroSerializer
        return CarrinhoLivroSerializerCreate
    
@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def getBookCartOfUser(request):
    print(request.data)
    cart_id = request.GET.get("cart_id")
    if cart_id:
        bookCart = CarrinhoLivro.objects.filter(carrinho_id=cart_id)
        serializer = CarrinhoLivroSerializer(bookCart, many=True)
        return Response(serializer.data)
    else:
        return Response({"message": "Please provide a valid cart_id parameter."}, status=400)