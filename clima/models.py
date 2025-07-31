from django.db import models

class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=2, default='CL')
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):
        return f"{self.nombre}, {self.pais}"

class Clima(models.Model):
    ciudad = models.ForeignKey(Ciudad, related_name='climas', on_delete=models.CASCADE)
    fecha_consulta = models.DateTimeField()
    temperatura = models.FloatField()
    humedad = models.IntegerField()
    presion = models.IntegerField()
    descripcion = models.CharField(max_length=100)
    icono = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return f"{self.ciudad.nombre} - {self.fecha_consulta.strftime('%Y-%m-%d %H:%M')}"
