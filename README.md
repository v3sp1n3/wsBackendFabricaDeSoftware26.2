# Sistema de Biblioteca

Projeto Django desenvolvido para a disciplina de Fábrica de Software.

O sistema permite gerenciar livros e autores e consultar livros em uma API externa.

## Funcionalidades

- Cadastro, listagem, edição, detalhamento e exclusão de livros.
- Relacionamento entre `Autor` e `Livro`: um autor pode possuir vários livros.
- Administração dos dados pelo Django Admin.
- Busca de livros na API pública Open Library.
- Tratamento de erros de conexão, tempo de resposta, status HTTP e dados inválidos da API.

## Tecnologias

- Python
- Django 6.1
- SQLite
- Requests

## Como executar

1. Clone o repositório:

   ```bash
   git clone https://github.com/v3sp1n3/wsBackendFabricaDeSoftware26.2.git
   cd wsBackendFabricaDeSoftware26.2
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   ```

   Windows PowerShell:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Aplique as migrações:

   ```bash
   python manage.py migrate
   ```

5. Inicie o servidor:

   ```bash
   python manage.py runserver
   ```

Abra `http://127.0.0.1:8000/` no navegador.

## Rotas principais

- `/` — lista de livros.
- `/livros/novo/` — cadastro de livro.
- `/buscar/` — busca de livros na Open Library.
- `/admin/` — painel administrativo do Django.
