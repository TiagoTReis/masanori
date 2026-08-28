# Masanori

Projeto individual para demonstrar o uso de um banco NoSQL com MongoDB: uma API de gerenciamento de leads com operações CRUD, validação de dados e documentos flexíveis.

## Estrutura

* `backend/`: Django com endpoints JSON para gerenciamento de leads.

  * `leads/views.py`: camada HTTP, responsável pelas requisições, respostas e métodos HTTP.
  * `leads/services.py`: operações de criação, consulta, atualização e exclusão no MongoDB.
  * `leads/validators.py`: validação dos dados recebidos pela API.
  * `leads/mongodb.py`: conexão com o MongoDB.
  * `leads/tests.py`: testes automatizados da aplicação.
* `config/`: configurações e URLs do Django.
* `.env.example`: exemplo das variáveis de ambiente utilizadas pelo projeto.
* `requirements.txt`: dependências do backend.

## Como executar

Com Python e MongoDB instalados, crie e ative o ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure o arquivo `.env` a partir do `.env.example` e inicie o Django:

```bash
python manage.py runserver
```

A API fica disponível em:

```text
http://127.0.0.1:8000/api/
```

## API

A API possui operações CRUD para leads:

```text
GET     /api/leads/
POST    /api/leads/
GET     /api/leads/<id>/
PATCH   /api/leads/<id>/
DELETE  /api/leads/<id>/
```

Exemplo de documento:

```json
{
  "name": "João Silva",
  "email": "joao@email.com",
  "phone": "12999999999",
  "company": "Empresa Exemplo",
  "status": "new",
  "source": "website"
}
```

Os status disponíveis são:

```text
new
contacted
qualified
```

As fontes disponíveis são:

```text
website
instagram
linkedin
```

A API também realiza validações de campos obrigatórios, formato de e-mail e valores permitidos.

## Testes

O projeto possui testes automatizados para os serviços, endpoints, operações CRUD e validações.

Para executar:

```bash
python manage.py test leads
```

Resultado atual:

```text
Ran 17 tests

OK
```

## Argumentação do trabalho

**Escolha:** MongoDB, um banco orientado a documentos, foi escolhido por permitir armazenar os leads como documentos BSON e oferecer flexibilidade na estrutura dos dados.

**Vantagens:** flexibilidade de esquema; facilidade de integração com APIs; documentos próximos ao formato JSON; boa experiência para desenvolvimento e prototipagem.

**Desvantagens:** exige validação na aplicação; a flexibilidade pode gerar documentos inconsistentes; relacionamentos complexos podem ser menos naturais que em bancos relacionais.

**Fluxo da aplicação:**

```text
Cliente → Django → Views → Services → MongoDB
```

## Status do projeto

Backend funcional com CRUD de leads, validações e testes automatizados.

## About

Repositório para trabalho substitutivo da P1.
