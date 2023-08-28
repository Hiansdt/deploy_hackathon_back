from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from app.models import Coment
from app.serializers import ComentSerializer, ComentSerializerCreate
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response

class ComentViewSet(ModelViewSet):
    queryset = Coment.objects.all()
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ComentSerializer
        return ComentSerializerCreate
    
    permission_classes = [AllowAny]

@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def getComentsOfBook(request):
    id = request.GET.get("id")
    coments = Coment.objects.filter(livro=id)
    serializer = ComentSerializer(coments, many=True)

    return Response(serializer.data)