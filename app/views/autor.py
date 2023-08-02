from rest_framework.viewsets import ModelViewSet
from config.decorators import jwt_optional
from rest_framework.permissions import AllowAny
from rest_framework.permissions import BasePermission
from rest_framework.parsers import MultiPartParser, FormParser

from app.models import Autor
from app.serializers import AutorSerializer

class AutorViewSet(ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    @classmethod
    @jwt_optional
    def as_view(cls, actions=None, **kwargs):
        return super().as_view(actions, **kwargs)

    def get_permissions(self):
        """
        Retorna a lista de permissões permitidas para a visualização.
        """
        if self.request.method == 'GET':
            return [AllowAny()]  # Permite qualquer usuário para requisições GET
        return super().get_permissions()