from django.urls import path

from .views import (
    LivroCreateView,
    LivroDeleteView,
    LivroDetailView,
    LivroListView,
    LivroUpdateView,
    buscar_livros_externos,
)

urlpatterns = [
    path("", LivroListView.as_view(), name="lista_livros"),
    path("livros/novo/", LivroCreateView.as_view(), name="criar_livro"),
    path("livros/<int:pk>/", LivroDetailView.as_view(), name="detalhe_livro"),
    path("livros/<int:pk>/editar/", LivroUpdateView.as_view(), name="editar_livro"),
    path("livros/<int:pk>/excluir/", LivroDeleteView.as_view(), name="excluir_livro"),
    path("buscar/", buscar_livros_externos, name="buscar_livros_externos"),
]