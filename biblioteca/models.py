from django.db import models

# Create your models here.

from django.db import models

class Autor(models.Model):
    nome = models.CharField(max_length=100)
    nacionalidade = models.CharField(max_length=60)

    def __str__(self):
        return self.nome


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    ano_publicacao = models.PositiveIntegerField()
    autor = models.ForeignKey(
        Autor,
        on_delete=models.CASCADE,
        related_name="livros"
    )

    def __str__(self):
        return self.titulo