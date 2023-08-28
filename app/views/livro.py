from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from config.decorators import jwt_optional
from rest_framework.permissions import AllowAny
from app.models import Livro
from app.serializers import LivroSerializer

from rest_framework.permissions import BasePermission
from rest_framework.parsers import MultiPartParser, FormParser
class LivroViewSet(ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(image=self.request.data.get('capa'))

    def perform_update(self, serializer):
        capa = self.request.data.get('capa')
        if capa:
            serializer.save(capa=capa)
        else:
            serializer.save()
    
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
    
    
@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def getBooksOfFilters(request):
    order = request.GET.get("order")
    genres_id = request.GET.getlist("genres[]")
    authors_id = request.GET.getlist("authors[]")
    print(authors_id)

    if len(genres_id) > 0:
        livros = Livro.objects.filter(genre__in=genres_id).distinct()
    
    if len(authors_id) > 0 and len(genres_id) > 0:
        livros = Livro.objects.filter(genre__in=genres_id).distinct()

        authors_to_exclude = []
        for livro in livros:
            if str(livro.author.id) not in authors_id:
                authors_to_exclude.append(livro.author.id)

        livros = livros.exclude(author__in=authors_to_exclude)

    if len(authors_id) > 0 and len(genres_id) == 0:
        livros = Livro.objects.filter(author__in=authors_id).distinct()

    if len(genres_id) == 0 and len(authors_id) == 0:
        livros = Livro.objects.all()

    if len(livros) == 0:
        return Response({"message": "Nenhum livro encontrado!"}, status=404)
    
    print(order)

    if order == "1":
        livros = sorted(livros, key=lambda livro: livro.vendas, reverse=True)

    if order == "2":
        livros = sorted(livros, key=lambda livro: livro.price)

    if order == "3":
        livros = sorted(livros, key=lambda livro: livro.price, reverse=True)

    if order == "4":
        livros = reversed(livros)
    
    data = []
    for livro in livros:
        livro_data = {
            'id': livro.id,
            'title': livro.title,
            'price': livro.price,
            'stock': livro.stock,
            'isbn': livro.isbn,
            'author': livro.author,
            'genre': livro.genre.all(),
            'capa': livro.capa,
            'desconto': livro.desconto,
            'vendas': livro.vendas, 
        }
        data.append(livro_data)


    serializer = LivroSerializer(data, many=True)
    return Response(serializer.data, status=200)

@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def searchBooks(request):
    name = request.GET.get("name")

    livros = Livro.objects.filter(title__icontains=name)

    if len(livros) == 0:
        return Response({"message": "Nenhum livro encontrado!"}, status=404)
    
    data = []
    for livro in livros:
        livro_data = {
            'id': livro.id,
            'title': livro.title,
            'price': livro.price,
            'stock': livro.stock,
            'isbn': livro.isbn,
            'author': livro.author,
            'genre': livro.genre.all(),
            'capa': livro.capa,
            'desconto': livro.desconto,
            'vendas': livro.vendas,
        }
        data.append(livro_data)

    serializer = LivroSerializer(data, many=True)
    return Response(serializer.data, status=200)