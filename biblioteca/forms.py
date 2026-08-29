from django import forms


class ImportarLivroExternoForm(forms.Form):
    titulo = forms.CharField(max_length=200, label="Título")
    ano_publicacao = forms.IntegerField(
        label="Ano de publicação",
        min_value=0,
        max_value=9999,
    )
    nome_autor = forms.CharField(max_length=100, label="Autor")

