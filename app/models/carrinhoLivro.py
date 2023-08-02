from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .genero import Genero
from .livro import Livro

class CarrinhoLivro(models.Model):
    carrinho = models.ForeignKey("Carrinho", on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

    class Meta:
        verbose_name_plural = "CarrinhoLivros"

    def __str__(self):
        return self.livro.title
    
@receiver(post_save, sender=CarrinhoLivro)
def create_carrinhoLivro(sender, instance=None, created=False, **kwargs):
    if created:
        instance.carrinho.total += instance.livro.price * instance.quantidade
        instance.carrinho.save()

@receiver(post_delete, sender=CarrinhoLivro)
def delete_carrinhoLivro(sender, instance, **kwargs):
    if instance.carrinho.total > 0:
        instance.carrinho.total -= instance.livro.price * instance.quantidade
        instance.carrinho.save()
    else:
        instance.carrinho.total = 0
        instance.carrinho.save()