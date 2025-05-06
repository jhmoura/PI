from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class TipoServico(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoServico, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
