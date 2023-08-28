from django.db import models

from usuario.models import Usuario
from .carrinhoLivro import CarrinhoLivro

class Carrinho(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.user} - {self.total}'
