from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from .managers import CustomUserManager
from uploader.models import Image

class Usuario(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(_("e-mail address"), unique=True)
    cpf = models.CharField(_("CPF"), max_length=11, blank=True, null=True)
    telefone = models.CharField(_("Phone"), max_length=11, blank=True, null=True)
    data_nascimento = models.DateField(
        _("Birth Date"), auto_now=False, auto_now_add=False, blank=True, null=True
    )
    foto = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )
    password_reset_token = models.CharField(max_length=6, null=True, blank=True, default=None)
    password_reset_token_created = models.DateTimeField(null=True, blank=True, default=None)
    

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    EMAIL_FIELD = "email"


    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["-date_joined"]


@receiver(post_save, sender=Usuario)
def create_user_carrinho(sender, instance, created, **kwargs):
    if created:
        from app.models import Carrinho

        Carrinho.objects.create(user=instance)
        instance.groups.add(Group.objects.get(name="cliente"))