from django.db import models

from .livro import Livro
from usuario.models import Usuario

class Favorite(models.Model):
    book = models.ForeignKey(Livro, on_delete=models.CASCADE)
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)