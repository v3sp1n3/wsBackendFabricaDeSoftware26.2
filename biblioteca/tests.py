from django.test import TestCase

# Create your tests here.

import requests

from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Autor, Livro


class BibliotecaApiTests(APITestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username="usuario_teste",
            password="senha_segura_123",
        )

        self.autor = Autor.objects.create(
            nome="Machado de Assis",
            nacionalidade="Brasileira",
        )

        self.livro = Livro.objects.create(
            titulo="Dom Casmurro",
            ano_publicacao=1899,
            autor=self.autor,
        )

    def test_obter_token_jwt(self):
        resposta = self.client.post(
            reverse("token_obtain_pair"),
            {
                "username": "usuario_teste",
                "password": "senha_segura_123",
            },
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertIn("access", resposta.data)
        self.assertIn("refresh", resposta.data)

    def test_api_exige_autenticacao(self):
        resposta = self.client.get(reverse("livro-list"))

        self.assertEqual(
            resposta.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_usuario_autenticado_lista_livros(self):
        self.client.force_authenticate(user=self.usuario)

        resposta = self.client.get(reverse("livro-list"))

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 1)
        self.assertEqual(resposta.data[0]["titulo"], "Dom Casmurro")

    def test_usuario_autenticado_cria_livro(self):
        self.client.force_authenticate(user=self.usuario)

        resposta = self.client.post(
            reverse("livro-list"),
            {
                "titulo": "Memórias Póstumas de Brás Cubas",
                "ano_publicacao": 1881,
                "autor": self.autor.id,
            },
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Livro.objects.count(), 2)

    @patch("biblioteca.views.requests.get")
    def test_busca_externa_trata_timeout(self, mock_get):
        mock_get.side_effect = TimeoutError()
        mock_get.side_effect = requests.exceptions.Timeout()

        resposta = self.client.get(
            reverse("buscar_livros_externos"),
            {"q": "Django"},
        )

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)