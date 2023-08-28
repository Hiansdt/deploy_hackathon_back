from django.db import models
from usuario.models import Usuario

class Compra(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.user.username} - {self.id}'