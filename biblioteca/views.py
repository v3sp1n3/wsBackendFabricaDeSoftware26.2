import requests

from django.shortcuts import render
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


def buscar_livros_externos(request):
    consulta = request.GET.get("q", "").strip()

    if not consulta:
        return render(request, "biblioteca/busca_externa.html")

    try:
        resposta = requests.get(
            "https://openlibrary.org/search.json",
            params={"q": consulta},
            timeout=10,
        )
        resposta.raise_for_status()

        dados = resposta.json()
        livros = dados.get("docs", [])[:10]

        return render(
            request,
            "biblioteca/busca_externa.html",
            {
                "livros": livros,
                "consulta": consulta,
            },
        )

    except requests.exceptions.Timeout:
        erro = "A consulta demorou muito para responder. Tente novamente."

    except requests.exceptions.HTTPError as erro_http:
        status = erro_http.response.status_code
        erro = f"A API retornou um erro. Código HTTP: {status}."

    except requests.exceptions.RequestException:
        erro = "Não foi possível conectar à API externa."

    except ValueError:
        erro = "A API retornou dados em um formato inválido."

    return render(request, "biblioteca/busca_externa.html", {"erro": erro})