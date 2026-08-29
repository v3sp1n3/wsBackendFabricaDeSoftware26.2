from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Livro


class LivroListView(ListView):
    model = Livro
    template_name = "biblioteca/lista_livros.html"
    context_object_name = "livros"


class LivroCreateView(CreateView):
    model = Livro
    fields = ["titulo", "ano_publicacao", "autor"]
    template_name = "biblioteca/livro_form.html"
    success_url = reverse_lazy("lista_livros")


class LivroDetailView(DetailView):
    model = Livro
    template_name = "biblioteca/livro_detail.html"


class LivroUpdateView(UpdateView):
    model = Livro
    fields = ["titulo", "ano_publicacao", "autor"]
    template_name = "biblioteca/livro_form.html"
    success_url = reverse_lazy("lista_livros")


class LivroDeleteView(DeleteView):
    model = Livro
    template_name = "biblioteca/livro_confirm_delete.html"
    success_url = reverse_lazy("lista_livros")