# Masanori

Projeto individual desenvolvido para demonstrar a utilização de um banco de dados NoSQL com MongoDB aplicado a um CRM de leads. A aplicação permite cadastrar, consultar, editar e excluir leads, além de acompanhar interações realizadas com cada contato por meio de uma timeline.

## Objetivo

O projeto tem como objetivo demonstrar a utilização do MongoDB em uma aplicação web, explorando o armazenamento de documentos, operações CRUD, filtros, paginação e o uso de documentos com estruturas flexíveis.

O sistema foi desenvolvido como um CRM simplificado para gerenciamento de leads e oportunidades comerciais.

## Estrutura

* `frontend/`: aplicação web desenvolvida com Vue 3 + Vite.

  * `src/components/`: componentes responsáveis pela interface e funcionalidades dos leads.
  * `src/services/api.js`: configuração das requisições para a API.
* `backend/`: API desenvolvida com Django.

  * `leads/`: aplicação responsável pelo gerenciamento dos leads e suas interações.
  * `config/`: configurações e inicialização do projeto Django.
* `.env`: variáveis de ambiente utilizadas pelo backend, incluindo a conexão com o MongoDB.
* MongoDB: banco de dados NoSQL utilizado para persistência dos dados.

## Tecnologias utilizadas

### Frontend

* Vue 3
* Vite
* JavaScript
* HTML
* CSS
* Axios

### Backend

* Python
* Django
* PyMongo

### Banco de dados

* MongoDB

## Como executar

### Backend

Entre na pasta do backend:

```bash
cd backend
```

Ative o ambiente virtual:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure o arquivo `.env` com as variáveis necessárias:

```env
DEBUG=true
SECRET_KEY=troque-esta-chave-em-producao
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=leadtrack
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

Inicie o servidor Django:

```bash
python manage.py runserver
```

### Frontend

Em outro terminal, entre na pasta do frontend:

```bash
cd frontend
```

Instale as dependências:

```bash
npm install
```

Inicie a aplicação:

```bash
npm run dev
```

A aplicação frontend estará disponível no endereço informado pelo Vite, normalmente:

```text
http://localhost:5173/
```

## Banco de dados

O projeto utiliza o MongoDB localmente através da seguinte conexão:

```text
mongodb://localhost:27017
```

O banco utilizado pela aplicação é:

```text
leadtrack
```

A principal collection utilizada pelo sistema é:

```text
leads
```

Cada lead é armazenado como um documento, permitindo que informações adicionais sejam incorporadas ao documento sem a necessidade de uma estrutura rígida de tabelas.

Um documento de lead possui, por exemplo, a seguinte estrutura:

```json
{
  "_id": "...",
  "name": "Carlos Santos",
  "email": "carlos@email.com",
  "phone": "(12) 96666-6666",
  "company": "Empresa Teste",
  "status": "new",
  "source": "website",
  "created_at": "...",
  "updated_at": "...",
  "interactions": []
}
```

## Funcionalidades

### Gerenciamento de leads

O sistema permite:

* cadastrar novos leads;
* visualizar os leads cadastrados;
* editar informações de um lead;
* excluir um lead;
* pesquisar por nome, e-mail ou empresa;
* filtrar leads por status;
* navegar pelos resultados através de paginação.

Os status utilizados atualmente são:

* `new` — Novo
* `contacted` — Contatado
* `qualified` — Qualificado

As origens disponíveis incluem:

* `website`
* `instagram`
* `linkedin`

## Detalhes do lead

Ao clicar no nome de um lead, o sistema abre uma tela de detalhes com suas principais informações.

São apresentados:

* nome;
* empresa;
* e-mail;
* telefone;
* status;
* origem;
* histórico de interações.

O telefone é apresentado no frontend utilizando formatação de número brasileiro.

## Timeline de interações

Cada lead pode possuir um histórico de interações.

As interações são armazenadas dentro do próprio documento do lead, aproveitando a estrutura flexível do MongoDB.

Os tipos de interação disponíveis são:

* Observação;
* Ligação;
* E-mail;
* Reunião.

Cada interação registra informações como:

```json
{
  "type": "call",
  "description": "cliente ligou a respeito do orçamento",
  "created_at": "..."
}
```

As interações são apresentadas no frontend em formato de timeline, permitindo acompanhar cronologicamente o histórico de relacionamento com o lead.

## Paginação, busca e filtros

A listagem de leads possui paginação para evitar a apresentação de todos os registros simultaneamente.

Também é possível:

* buscar leads por nome;
* buscar por e-mail;
* buscar por empresa;
* filtrar pelo status;
* navegar entre as páginas dos resultados.

Quando uma nova busca ou filtro é aplicado, a paginação retorna automaticamente para a primeira página.

## API

A aplicação frontend se comunica com o backend através de uma API HTTP.

Entre as operações utilizadas pelo sistema estão:

```text
GET    /leads/
POST   /leads/
PATCH  /leads/<id>/
DELETE /leads/<id>/
POST   /leads/<id>/interactions/
```

As operações permitem realizar o gerenciamento dos leads e registrar novas interações relacionadas a cada contato.

## MongoDB

A escolha do MongoDB está relacionada principalmente à natureza dos dados utilizados pelo CRM.

Um lead pode possuir diferentes quantidades de interações, e cada interação pode ser armazenada dentro do próprio documento. Esse modelo se adapta naturalmente ao formato utilizado pela aplicação.

### Vantagens

* estrutura flexível de documentos;
* facilidade para armazenar dados relacionados ao lead;
* possibilidade de adicionar novos campos sem migrações tradicionais;
* documentos próximos da estrutura utilizada pela API;
* facilidade para desenvolvimento e prototipagem;
* possibilidade de armazenar o histórico de interações dentro do próprio lead.

### Desvantagens

* exige cuidado com validação dos documentos;
* a flexibilidade pode permitir dados inconsistentes;
* consultas e relacionamentos complexos podem exigir maior planejamento;
* o crescimento de documentos com muitas interações deve ser considerado na modelagem.

## MongoDB Compass

Durante o desenvolvimento, o banco pode ser visualizado e administrado através do MongoDB Compass.

A conexão utilizada é:

```text
mongodb://localhost:27017
```

Após a conexão, o banco utilizado pelo projeto pode ser encontrado em:

```text
leadtrack
└── leads
```

Isso permite visualizar diretamente os documentos persistidos pela aplicação e verificar as alterações realizadas através da API.

## Considerações sobre a modelagem

A modelagem utiliza documentos orientados a leads. As informações principais do contato ficam armazenadas no documento do lead, enquanto o histórico de interações é incorporado ao próprio documento.

Essa abordagem evita a necessidade de criar uma estrutura relacional separada apenas para representar o histórico de interações e aproveita uma das características fundamentais do MongoDB: a possibilidade de trabalhar com documentos aninhados e arrays.

## Argumentação do trabalho

**Escolha:** MongoDB foi escolhido como banco de dados NoSQL por utilizar documentos BSON/JSON e oferecer uma estrutura flexível para representar leads e seus respectivos históricos de interação.

**Vantagens:** flexibilidade na estrutura dos documentos; facilidade para representar informações de um lead; armazenamento de interações diretamente no documento; boa integração com uma API baseada em JSON; facilidade para prototipação e evolução da aplicação.

**Desvantagens:** necessidade de validação dos dados; possibilidade de inconsistência entre documentos; necessidade de planejamento quando os documentos crescem; relacionamentos complexos podem ser menos naturais do que em bancos relacionais.

## Conclusão

O projeto demonstra a utilização prática de um banco de dados NoSQL em uma aplicação web, utilizando o MongoDB para armazenar informações de leads e seus históricos de interação.

A aplicação integra Vue 3 no frontend, Django no backend e MongoDB como camada de persistência, permitindo demonstrar operações de CRUD, filtros, paginação e armazenamento de estruturas aninhadas em documentos.
