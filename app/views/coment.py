from rest_framework.viewsets import ModelViewSet
from config.decorators import jwt_optional
from rest_framework.permissions import AllowAny
from rest_framework.permissions import BasePermission
from rest_framework.parsers import MultiPartParser, FormParser
from app.models import Coment
from app.serializers import ComentSerializer, ComentSerializerCreate

class ComentViewSet(ModelViewSet):
    queryset = Coment.objects.all()
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ComentSerializer
        return ComentSerializerCreate
    parser_classes = (MultiPartParser, FormParser)
    
    @classmethod
    @jwt_optional
    def as_view(cls, actions=None, **kwargs):
        return super().as_view(actions, **kwargs)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()] 
        return super().get_permissions()