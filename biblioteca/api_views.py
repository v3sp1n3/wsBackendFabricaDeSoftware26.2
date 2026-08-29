from rest_framework import filters, viewsets

from .models import Autor, Livro
from .serializers import AutorSerializer, LivroSerializer


class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all().order_by("nome")
    serializer_class = AutorSerializer

    search_fields = ["nome", "nacionalidade"]
    ordering_fields = ["nome", "nacionalidade"]
    ordering = ["nome"]


class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.select_related("autor").all().order_by("titulo")
    serializer_class = LivroSerializer

    search_fields = ["titulo", "autor__nome"]
    ordering_fields = ["titulo", "ano_publicacao", "autor__nome"]
    ordering = ["titulo"]