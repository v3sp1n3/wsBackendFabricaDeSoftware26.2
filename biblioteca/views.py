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
from django.views.generic.edit import FormView

from .forms import ImportarLivroExternoForm
from .models import Autor, Livro


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

class AutorListView(ListView):
    queryset = Autor.objects.prefetch_related("livros").all().order_by("nome")
    template_name = "biblioteca/lista_autores.html"
    context_object_name = "autores"


class AutorCreateView(CreateView):
    model = Autor
    fields = ["nome", "nacionalidade"]
    template_name = "biblioteca/autor_form.html"
    success_url = reverse_lazy("lista_autores")


class AutorDetailView(DetailView):
    model = Autor
    template_name = "biblioteca/autor_detail.html"


class AutorUpdateView(UpdateView):
    model = Autor
    fields = ["nome", "nacionalidade"]
    template_name = "biblioteca/autor_form.html"
    success_url = reverse_lazy("lista_autores")


class AutorDeleteView(DeleteView):
    model = Autor
    template_name = "biblioteca/autor_confirm_delete.html"
    success_url = reverse_lazy("lista_autores")


class ImportarLivroExternoView(FormView):
    template_name = "biblioteca/importar_livro_externo.html"
    form_class = ImportarLivroExternoForm
    success_url = reverse_lazy("lista_livros")

    def get_initial(self):
        initial = super().get_initial()
        ano_publicacao = self.request.GET.get("ano_publicacao", "").strip()

        initial.update(
            {
                "titulo": self.request.GET.get("titulo", "").strip(),
                "nome_autor": self.request.GET.get("nome_autor", "").strip(),
            }
        )

        if ano_publicacao.isdigit():
            initial["ano_publicacao"] = ano_publicacao

        return initial

    def form_valid(self, form):
        nome_autor = form.cleaned_data["nome_autor"].strip()
        autor = Autor.objects.filter(nome__iexact=nome_autor).first()

        if autor is None:
            autor = Autor.objects.create(
                nome=nome_autor,
                nacionalidade="Não informada",
            )

        Livro.objects.create(
            titulo=form.cleaned_data["titulo"],
            ano_publicacao=form.cleaned_data["ano_publicacao"],
            autor=autor,
        )

        return super().form_valid(form)


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
