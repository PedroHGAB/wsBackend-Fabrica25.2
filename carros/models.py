from django.db import models

class Garagem(models.Model):
    nome = models.CharField("Nome", max_length=30)

    def __str__(self):
        return self.nome

class CarroSalvo(models.Model):
    garagem = models.ForeignKey(Garagem,
                                 on_delete=models.CASCADE,
                                 related_name="carros"
                                )
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField()
    preco = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.ano}) - R$ {self.preco}"