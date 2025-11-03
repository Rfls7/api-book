from __future__ import annotations
import csv
import os
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .schemas import Book, BookList

app = FastAPI(
    title="Books API",
    version="1.0.0",
    description="API pública para consulta de livros (dados extraídos de books.toscrape.com)",
    openapi_url="/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "books.csv"


@lru_cache(maxsize=1)
def _load_books() -> List[Book]:
    if not DATA_PATH.exists():
        raise RuntimeError(
            f"Arquivo CSV não encontrado em {DATA_PATH}. Execute o scraper primeiro."
        )

    items: List[Book] = []
    with DATA_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                items.append(
                    Book(
                        id=row.get("id") or "",
                        title=row.get("title") or "",
                        price=float(row.get("price") or 0),
                        stock=int(row.get("stock") or 0),
                        rating=int(row.get("rating") or 0),
                        category=row.get("category") or None,
                        product_page_url=row.get("product_page_url") or "",
                        upc=row.get("upc") or None,
                        description=row.get("description") or None,
                        image_url=row.get("image_url") or None,
                    )
                )
            except Exception:
                # ignora linhas inválidas
                continue

    return items


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}


@app.get("/api/v1/books", response_model=BookList)
def list_books(
    q: Optional[str] = Query(None, description="Busca por título/descrição (case-insensitive)"),
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    min_rating: Optional[int] = Query(None, ge=0, le=5),
    max_rating: Optional[int] = Query(None, ge=0, le=5),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    sort: Optional[str] = Query(None, description="price|rating|title e prefixe com - para desc"),
):
    items = _load_books().copy()

    # filtros
    if q:
        q_low = q.lower()
        items = [
            b for b in items
            if q_low in b.title.lower() or (b.description or "").lower().find(q_low) >= 0
        ]

    if category:
        items = [b for b in items if (b.category or "").lower() == category.lower()]

    if min_price is not None:
        items = [b for b in items if b.price >= min_price]

    if max_price is not None:
        items = [b for b in items if b.price <= max_price]

    if min_rating is not None:
        items = [b for b in items if b.rating >= min_rating]

    if max_rating is not None:
        items = [b for b in items if b.rating <= max_rating]

    # ordenação
    if sort:
        reverse = sort.startswith("-")
        key = sort.lstrip("-")

        if key not in {"price", "rating", "title"}:
            raise HTTPException(
                400, detail="sort inválido. Use price|rating|title com opcional prefixo -"
            )

        items.sort(key=lambda b: getattr(b, key), reverse=reverse)

    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size

    return BookList(total=total, page=page, page_size=page_size, items=items[start:end])


@app.get("/api/v1/books/{book_id}", response_model=Book)
def get_book(book_id: str):
    for b in _load_books():
        if b.id == book_id:
            return b
    raise HTTPException(404, detail="book not found")


@app.get("/api/v1/categories")
def list_categories():
    cats = sorted({b.category for b in _load_books() if b.category})
    return {"count": len(cats), "items": cats}


@app.get("/api/v1/books/search", response_model=BookList)
def search(
    q: str = Query(..., description="Consulta por título/descrição"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
):
    return list_books(q=q, page=page, page_size=page_size)