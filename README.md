Biblioteca_API
============================================================================

Uma REST API completa para um sistema de gestão de biblioteca, desenvolvida em Python com Flask.

Funcionalidades
============================================================================

-  Autenticação com JWT - (Token seguro)

-  Gestão de utilizadores - (signup/login)

-  CRUD completo de livros (Adição, Edição, )

-  Controlo de permissões - (admin / Utilizador comum)

-  Validação de dados

-  Status codes HTTP corretos -( Status como: 404 de rota não encontrada.)


Como usar?
============================================================================

Clonar o repositório


Criar um ambiente virtual


Instalar as dependências


Executar a aplicação - (python3 app.py)



A API estará disponível em `http://localhost:8000`

Endpoints
============================================================================

Autenticação

- POST /api/auth/signup - Registar novo utilizador

- POST /api/auth/login - Fazer login (retorna JWT token)

- GET /api/auth/me - Ver dados do utilizador (requer token)

Livros

- GET /api/items - Listar todos os livros

- GET /api/items/<id> - Ver detalhes de um livro

- POST /api/items - Criar novo livro (admin only)

- PUT /api/items/<id> - Editar livro (admin only)

- DELETE /api/items/<id> - Apagar livro (admin only)

Porque eu o fiz?
===========================================================================

Eu já tinha um projeto muito parecido, o Flask Server, continha semelhantes funcionalidades,
mas esta API aqui ainda é apenas Back End [02/05/2026], em breve, ele terá o seu Front End em JavaScript.

O meu aprendizado ao longo de este projeto
===========================================================================

Neste projeto adquiri varias competencias uteis, entre elas:
- REST API - ()
- RESTful API - (API REST com todas as boas práticas)
- CRUD - (Create [POST], Read[GET], Update[PUT], Delete[DELETE])
- POO básico - ( Isso foi o que eu achei mais importante e interessante Classes e Modelos.)
- JWT - (Para keys e autenticação segura)
- SQLALChemy ORM (Bem melhor do que SQL puro como no primeiro servidor.)