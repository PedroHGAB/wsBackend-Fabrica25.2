# iGarage — Django + FIPE + Docker (PostgreSQL)

Um app Django para navegar na **API da Tabela FIPE** (marcas → modelos → anos → detalhes) e salvar carros em **garagens**. A stack roda com **Docker** e **PostgreSQL 17**.

> A API pública usada é a FIPE do Deivid Fortuna (REST/JSON). Documentação: deividfortuna.github.io/fipe. 

## Requisitos

* Docker e Docker Compose instalados.

## Estrutura (resumo)

```
app/
├─ carros/                # app Django (views, models, templates)
├─ iGarage/               # projeto Django (settings/urls)
├─ .env                   # variáveis de ambiente
├─ Dockerfile             # imagem da app (Python 3.13)
├─ docker-compose.yml     # serviços: web + db (Postgres 17)
├─ manage.py
└─ requirements.txt
```

## Variáveis de ambiente

O Compose lê automaticamente o arquivo `.env` na raiz do projeto para interpolar variáveis. Não precisa referenciar `env_file` — é padrão do Compose.

O projeto já está com um `.env` mínimo para subir com Postgres:

```env
# Banco usado pelo Django
DB_ENGINE=django.db.backends.postgresql
DB_NAME=igarage
DB_USER=postgres
DB_PASSWORD=1234
DB_HOST=db
DB_PORT=5432

# Inicialização do container postgres oficial
POSTGRES_DB=igarage
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1234
```

> As variáveis `POSTGRES_DB`, `POSTGRES_USER` e `POSTGRES_PASSWORD` são as esperadas pela **imagem oficial** do Postgres. 

> O Django usa `ENGINE='django.db.backends.postgresql'`. 

## Subindo o projeto

Dentro de `app/`:

```bash
# 1) build e up (a primeira vez cria o banco e roda as migrações)
docker compose up --build
```

A app ficará disponível em: `http://localhost:8000/`

### (Opcional) criar superusuário do Django

Em outro terminal:

```bash
docker compose exec web python manage.py createsuperuser
```

Acesse `http://localhost:8000/admin/` para gerenciar via admin.

## Como usar (fluxo)

1. **Home** → menu principal.
2. **Marcas (FIPE)** (`/marcas/`) → lista marcas da API.
3. Clique numa **marca** → **Modelos** (`/marcas/<marca_id>/modelos/`).
4. Clique num **modelo** → **Anos** (`/marcas/<marca_id>/modelos/<modelo_id>/anos/`).
5. Clique num **ano** → **Detalhe** (`/marcas/<marca_id>/modelos/<modelo_id>/anos/<ano_codigo>/`):

   * Mostra **Marca/Modelo/Ano** e **Valor FIPE**.
   * Selecione uma **garagem** e **Salvar** para gravar o carro.
6. **Minhas Garagens** (`/garagens/`):

   * **+ Nova Garagem** (`/garagens/nova/`)
   * **Detalhe da Garagem** (`/garagens/<id>/`): lista carros, **Editar nome** (`/garagens/<id>/editar/`) e **Excluir** (`/garagens/<id>/excluir/`).
7. **Meus Carros** (`/meus-carros/`): lista todos os carros salvos (com a garagem entre parênteses).
8. Pode **remover** um carro por `/carros/<id>/excluir/`.

> A FIPE é consultada em tempo real via endpoints REST. A doc oficial descreve marcas/modelos/anos/detalhes.  

## Rotas (resumo)

* `GET /` — Home
* `GET /marcas/`
* `GET /marcas/<marca_id>/modelos/`
* `GET /marcas/<marca_id>/modelos/<modelo_id>/anos/`
* `GET|POST /marcas/<marca_id>/modelos/<modelo_id>/anos/<ano_codigo>/`
* `GET /garagens/` — lista
* `GET|POST /garagens/nova/` — criar
* `GET /garagens/<id>/` — detalhe
* `GET|POST /garagens/<id>/editar/` — editar nome
* `GET|POST /garagens/<id>/excluir/` — excluir
* `GET /meus-carros/` — todos os carros
* `GET|POST /carros/<id>/excluir/` — remover carro

## Banco de dados

* O serviço `db` usa **PostgreSQL 17**

## Comandos úteis

```bash
# Recriar tudo do zero (cuidado: apaga dados do Postgres)
docker compose down -v
docker compose up --build
```

---

### Referências

* **FIPE API** (docs): deividfortuna.github.io/fipe • deividfortuna.github.io/fipe/v2 