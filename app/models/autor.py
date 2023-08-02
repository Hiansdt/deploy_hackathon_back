from django.db import models

class Autor(models.Model):
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Autores"

    def __str__(self):
        return self.name