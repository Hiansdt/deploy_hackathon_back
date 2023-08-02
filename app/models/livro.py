from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from .autor import Autor
from .genero import Genero


class Livro(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    author = models.ForeignKey(Autor, on_delete=models.PROTECT)
    genre = models.ManyToManyField(Genero)
    capa = models.ImageField(upload_to='livros/', blank=True, null=True)
    sinopse = models.TextField(blank=True, null=True)
    data_pub = models.DateField(blank=True, null=True)
    paginas = models.IntegerField(blank=True, null=True)
    vendas = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return f"{self.title} - {self.price}"
    
@receiver(post_save, sender=Livro)
def update_qnt_livros(sender, instance, created, **kwargs):
    if created:
        for genero in instance.genre.all():
            genero.qntLivros += 1
            genero.save()
    




