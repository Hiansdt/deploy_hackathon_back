from rest_framework.serializers import ModelSerializer

from app.models import Autor

class AutorSerializer(ModelSerializer):
    class Meta:
        model = Autor
        fields = "__all__"
        depth = 1