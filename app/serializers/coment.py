from rest_framework.serializers import ModelSerializer

from app.models import Coment

class ComentSerializer(ModelSerializer):
    class Meta:
        model = Coment
        fields = "__all__"
        depth = 1

class ComentSerializerCreate(ModelSerializer):
    class Meta:
        model = Coment
        fields = "__all__"