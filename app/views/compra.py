from rest_framework.viewsets import ModelViewSet

from app.models import Compra
from app.serializers import CompraSerializer, CompraSerializerCreate

class CompraViewSet(ModelViewSet):
    queryset = Compra.objects.all()
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CompraSerializerCreate
        return CompraSerializer
    
