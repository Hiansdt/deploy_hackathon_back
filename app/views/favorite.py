from rest_framework.viewsets import ModelViewSet
from config.decorators import jwt_optional
from rest_framework.permissions import AllowAny
from rest_framework.permissions import BasePermission
from rest_framework.parsers import MultiPartParser, FormParser
from app.models import Favorite
from app.serializers import FavoriteSerializer, FavoriteSerializerCreate
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response

class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return FavoriteSerializer
        return FavoriteSerializerCreate
    permission_classes = [AllowAny]

@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def getFavoritesOfUser(request):
    user_id = request.GET.get("user_id")
    if user_id:
        favorites = Favorite.objects.filter(user_id=user_id)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)
    else:
        return Response({"message": "Please provide a valid user_id parameter."}, status=400)
