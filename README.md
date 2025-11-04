📚 Books API — Web Scraping + API Pública

Link para o projeto no github: https://github.com/Rfls7/api-book#
Link para o vídeo: https://www.youtube.com/watch?v=Rvv1ZM7TCUc
Link para o projeto já em produção: https://api-books-tech-1e8a4dddfe4c.herokuapp.com/docs#/default/get_book_api_v1_books__book_id__get
book_id de exemplo: set-me-free_988
resposta esperada: {
  "id": "set-me-free_988",
  "title": "Set Me Free",
  "price": 17.46,
  "stock": 19,
  "rating": 5,
  "category": "Young Adult",
  "product_page_url": "https://books.toscrape.com/catalogue/set-me-free_988/index.html",
  "upc": "ce6396b0f23f6ecc",
  "description": "Aaron Ledbetterâs future had been planned out for him since before he was born. Each year, the Ledbetter family vacation on Tybee Island gave Aaron a chance to briefly free himself from his familyâs expectations. When he meets Jonas âLuckyâ Luckett, a caricature artist in town with the traveling carnival, he must choose between the life thatâs been mapped out for him, and Aaron Ledbetterâs future had been planned out for him since before he was born. Each year, the Ledbetter family vacation on Tybee Island gave Aaron a chance to briefly free himself from his familyâs expectations. When he meets Jonas âLuckyâ Luckett, a caricature artist in town with the traveling carnival, he must choose between the life thatâs been mapped out for him, and the chance at true love. ...more",
  "image_url": "https://books.toscrape.com/catalogue/media/cache/b8/e9/b8e91bd2fc74c3954118999238abb4b8.jpg"
}

Este projeto consiste em um pipeline completo para extração de dados de livros do site Books to Scrape
, transformação e disponibilização via API pública, possibilitando que cientistas de dados e aplicações façam consultas e análises de forma simples e escalável.

A solução inclui:

🕷️ Web Scraping completo dos livros do site

📁 Armazenamento dos dados em CSV local

⚙️ API RESTful em FastAPI

🚀 Pronta para deploy em nuvem (Heroku / Render / Docker)

📊 Estrutura preparada para expansão para Machine Learning

🧠 Arquitetura do Sistema
flowchart TD
    A[Books.toscrape.com] --> B[Web Scraper - Python + BeautifulSoup]
    B --> C[data/books.csv]
    C --> D[API FastAPI]
    D -->|JSON / HTTP| E[Usuários / Cientistas de Dados / Sistemas]


Componentes

Scraping: coleta e parse dos dados

Storage: salvamento em arquivo CSV

Serviço: FastAPI lendo o CSV e servindo via HTTP

Clientes: aplicações, analistas e cientistas de dados

🧩 Instalação e Configuração
✅ Pré-requisitos

Python 3.9+

Pip

Virtualenv (recomendado)

🛠️ Setup do projeto
git clone https://github.com/SEU-USUARIO/books-api.git
cd books-api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

🕷️ Rodando o Web Scraping
python scripts/scrape_books.py


Saída esperada:

data/books.csv criado com os dados de todos os livros

▶️ Executando a API
uvicorn api.main:app --reload --port 8000


Acesse:

Documentação Swagger: http://localhost:8000/docs

Documentação ReDoc: http://localhost:8000/redoc

🌐 Rotas da API
Método	Endpoint	Descrição
GET	/api/v1/health	Verifica saúde da API
GET	/api/v1/books	Lista todos os livros
GET	/api/v1/books/{id}	Detalhes de um livro específico
GET	/api/v1/books/search?title=&category=	Busca por título e/ou categoria
GET	/api/v1/categories	Lista de categorias
📎 Exemplos de Requests & Responses
✅ Listar livros
curl http://localhost:8000/api/v1/books


Response exemplo

{
  "total": 1000,
  "page": 1,
  "page_size": 20,
  "items": [
    {
      "id": "a-light-in-the-attic",
      "title": "A Light in the Attic",
      "price": 51.77,
      "stock": 22,
      "rating": 3,
      "category": "Poetry",
      "product_page_url": "...",
      "upc": "A12345",
      "description": "Some description...",
      "image_url": "https://..."
    }
  ]
}

✅ Buscar por título e categoria
curl "http://localhost:8000/api/v1/books/search?title=light&category=Poetry"

✅ Detalhar livro
curl http://localhost:8000/api/v1/books/a-light-in-the-attic

✅ Ver categorias disponíveis
curl http://localhost:8000/api/v1/categories

🚀 Deploy
Heroku (exemplo)
heroku create books-api
git push heroku main

Docker
docker build -t books-api .
docker run -p 8000:8080 books-api

✅ Conclusão

Este projeto demonstra:

Coleta automatizada de dados web

Estruturação e disponibilização pública

API escalável e documentada

Base para projetos de ML e recomendação

👨‍💻 Autor

Projeto desenvolvido para fins acadêmicos e práticos com foco em engenharia de dados e APIs escaláveis.
