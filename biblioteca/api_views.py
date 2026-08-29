from rest_framework import viewsets

from .models import Autor, Livro
from .serializers import AutorSerializer, LivroSerializer


class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all().order_by("nome")
    serializer_class = AutorSerializer


class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.select_related("autor").all().order_by("titulo")
    serializer_class = LivroSerializer