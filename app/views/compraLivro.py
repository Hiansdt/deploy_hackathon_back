from rest_framework.viewsets import ModelViewSet

from app.models import CompraLivro
from app.serializers import CompraLivroSerializer, CompraLivroSerializerCreate

class CompraLivroViewSet(ModelViewSet):
    queryset = CompraLivro.objects.all()
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CompraLivroSerializerCreate
        return CompraLivroSerializer
    
