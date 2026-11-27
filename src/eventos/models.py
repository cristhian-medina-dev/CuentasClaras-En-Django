from tkinter import CASCADE

from django.db import models
from django.conf import settings

# Create your models here.
class Evento(models.Model):
    organizador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="eventos"
    )
    nombre = models.CharField(max_length=120)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado_en"]

    def __str__(self):
        return self.nombre

class Gasto(models.Model):
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name="gastos",
    )
    cargado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gastos_cargados",
    )
    descripcion = models.CharField(max_length=140)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    dividir_entre = models.PositiveIntegerField(default=1)
    creado_en = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-creado_en"]

    @property
    def monto_por_persona(self):
        if self.dividir_entre > 0:
            return self.monto / self.dividir_entre
        return self.monto
    
    def __str__(self):
        return f"{self.descripcion} (${self.monto})"