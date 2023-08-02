from rest_framework.viewsets import ModelViewSet
from config.decorators import jwt_optional
from rest_framework.permissions import AllowAny
from app.models import Genero
from app.serializers import GeneroSerializer
from rest_framework.permissions import BasePermission
from rest_framework.parsers import MultiPartParser, FormParser

class GeneroViewSet(ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    @classmethod
    @jwt_optional
    def as_view(cls, actions=None, **kwargs):
        return super().as_view(actions, **kwargs)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()] 
        return super().get_permissions()