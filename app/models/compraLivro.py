from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .livro import Livro
from .compra import Compra

class CompraLivro(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.livro.title} - {self.quantidade}"

@receiver(post_save, sender=CompraLivro)
def change_total_compra_add(sender, instance, created, **kwargs):
    if created:
        instance.compra.total += instance.livro.price * instance.quantidade
        instance.compra.save()

        instance.livro.stock -= instance.quantidade
        instance.livro.save()

        instance.livro.vendas += instance.quantidade
        instance.livro.save()

@receiver(post_delete, sender=CompraLivro)
def change_total_compra_delete(sender, instance, **kwargs):
    if instance.compra.total > 0:
        instance.compra.total -= instance.livro.price * instance.quantidade
        instance.compra.save()
    else:
        instance.compra.total = 0
        instance.compra.save()