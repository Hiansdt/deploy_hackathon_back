from django.db import models

from usuario.models import Usuario
from app.models import Livro

class Coment(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    title = models.CharField(max_length=45)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    stars = models.IntegerField(default=1)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.title}"