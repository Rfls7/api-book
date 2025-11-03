import os
from fastapi.testclient import TestClient
from api.main import app, _load_books, DATA_PATH

# garante um CSV vazio controlado para teste se não existir
if not DATA_PATH.exists():
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
DATA_PATH.write_text(
"id,title,price,stock,rating,category,product_page_url,upc,description,image_url\n"
"test-book,Example,10.0,5,4,Fiction,https://example.com,UPC123,Desc,https://img\n",
encoding="utf-8",
)

client = TestClient(app)

def test_health():
    r = client.get("/v1/health")
    assert r.status_code == 200

def test_list_books():
    r = client.get("/v1/books")
    assert r.status_code == 200
    data = r.json()
    assert "items" in data

def test_get_book():
    r = client.get("/v1/books/test-book")
    assert r.status_code == 200
