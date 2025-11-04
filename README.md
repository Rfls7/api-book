📚 Books API — Web Scraping + API Pública

Pipeline completo para extração de dados de livros do site Books to Scrape, transformação e disponibilização via API REST. Ideal para estudos de engenharia de dados, pipelines e consumo para projetos de Data Science e ML.

🔗 Links Importantes
Recurso	Link
📂 Repositório GitHub	https://github.com/Rfls7/api-book

🎥 Vídeo explicativo	https://www.youtube.com/watch?v=Rvv1ZM7TCUc

🚀 API em produção	https://api-books-tech-1e8a4dddfe4c.herokuapp.com/docs#/default/get_book_api_v1_books__book_id__get

Exemplo de ID: set-me-free_988

Resposta esperada:

{
  "id": "set-me-free_988",
  "title": "Set Me Free",
  "price": 17.46,
  "stock": 19,
  "rating": 5,
  "category": "Young Adult",
  "product_page_url": "https://books.toscrape.com/catalogue/set-me-free_988/index.html",
  "upc": "ce6396b0f23f6ecc",
  "description": "Aaron Ledbetter’s future had been planned...",
  "image_url": "https://books.toscrape.com/catalogue/media/cache/b8/e9/b8e91bd2fc74c3954118999238abb4b8.jpg"
}

✨ Funcionalidades

✅ Web Scraping completo
✅ Armazenamento local em CSV
✅ API REST com FastAPI
✅ Deploy em Heroku / Render / Docker
✅ Pronta para expansão para Machine Learning

🧠 Arquitetura do Sistema
flowchart TD
A[Books.toscrape.com]
--> B[Web Scraper - Python + BeautifulSoup]
B --> C[data/books.csv]
C --> D[FastAPI Service]
D --> E[Usuários / Cientistas de Dados / Sistemas]


Componentes:

Módulo	Função
Scraping	Coleta e parse dos dados
Storage	Salvamento em CSV
API	FastAPI servindo dados em JSON
Consumo	Programas / dashboards / Data Science
🧩 Instalação
✅ Pré-requisitos

Python 3.9+

Pip

Virtualenv (recomendado)

📦 Setup
git clone https://github.com/SEU-USUARIO/books-api.git
cd books-api

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

🕷️ Executando o Web Scraping
python scripts/scrape_books.py


Saída esperada:

data/books.csv

▶️ Executando a API
uvicorn api.main:app --reload --port 8000


Acesse:

Swagger: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

🌐 Rotas da API
Método	Rota	Descrição
GET	/api/v1/health	Status da API
GET	/api/v1/books	Lista livros
GET	/api/v1/books/{id}	Livro específico
GET	/api/v1/books/search?title=&category=	Busca
GET	/api/v1/categories	Categorias
🧪 Exemplos
✅ Listar livros
curl http://localhost:8000/api/v1/books

✅ Buscar por título/categoria
curl "http://localhost:8000/api/v1/books/search?title=light&category=Poetry"

✅ Detalhar livro
curl http://localhost:8000/api/v1/books/a-light-in-the-attic

✅ Listar categorias
curl http://localhost:8000/api/v1/categories

🚀 Deploy
Heroku
heroku create books-api
git push heroku main

Docker
docker build -t books-api .
docker run -p 8000:8080 books-api

📈 Arquitetura e Escalabilidade Futura
Componente	Atual	Futuro
Coleta	BeautifulSoup	Airflow + Scraping distribuído
Storage	CSV	PostgreSQL / Parquet / Data Lake
API	FastAPI local	FastAPI + Redis + pgvector
Deploy	Local/Docker	Kubernetes / Serverless
Monitoramento	Logs	Prometheus + Grafana
Metas

Banco relacional + índices

Cache Redis

ETL orquestrado

Pipeline CI/CD

Suporte a ML / recomendações

🎯 Uso para Data Science e ML

✅ EDA (categorias, preços, ratings)
✅ Recomendação baseada em similaridade
✅ NLP em descrições
✅ Embeddings / busca semântica

🤖 Roadmap de ML
Etapa	Descrição
Feature Engineering	Limpeza e tokenização
Embeddings	Sentence Transformers / OpenAI
Vector Store	pgvector / FAISS
API ML	/api/v1/recommend
👨‍💻 Autor

Projeto desenvolvido para fins acadêmicos e práticos com foco em engenharia de dados e APIs escaláveis.
