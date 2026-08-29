from django.urls import path

from .views import (
    AutorCreateView,
    AutorDeleteView,
    AutorDetailView,
    AutorListView,
    AutorUpdateView,
    LivroCreateView,
    LivroDeleteView,
    LivroDetailView,
    LivroListView,
    LivroUpdateView,
    ImportarLivroExternoView,
    buscar_livros_externos,
)

urlpatterns = [
    path("", LivroListView.as_view(), name="lista_livros"),
    path("livros/novo/", LivroCreateView.as_view(), name="criar_livro"),
    path("livros/<int:pk>/", LivroDetailView.as_view(), name="detalhe_livro"),
    path("livros/<int:pk>/editar/", LivroUpdateView.as_view(), name="editar_livro"),
    path("livros/<int:pk>/excluir/", LivroDeleteView.as_view(), name="excluir_livro"),
    path(
        "livros/importar/",
        ImportarLivroExternoView.as_view(),
        name="importar_livro_externo",
    ),

    path("autores/", AutorListView.as_view(), name="lista_autores"),
    path("autores/novo/", AutorCreateView.as_view(), name="criar_autor"),
    path("autores/<int:pk>/", AutorDetailView.as_view(), name="detalhe_autor"),
    path("autores/<int:pk>/editar/", AutorUpdateView.as_view(), name="editar_autor"),
    path("autores/<int:pk>/excluir/", AutorDeleteView.as_view(), name="excluir_autor"),

    path("buscar/", buscar_livros_externos, name="buscar_livros_externos"),
]
