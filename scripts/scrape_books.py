#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Scraper para https://books.toscrape.com/
Extrai informações de todos os livros e salva no arquivo data/books.csv

Campos extraídos:
- id (slug da URL)
- title
- price
- stock
- rating
- category
- product_page_url
- upc
- description
- image_url

Execução:
    python scripts/scrape_books.py
"""

import csv
import time
import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from typing import Optional, List

BASE_URL = "https://books.toscrape.com/"
CATALOG_URL = BASE_URL + "catalogue/"
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "books.csv"

# rating map do site
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


@dataclass
class BookRow:
    id: str
    title: str
    price: float
    stock: int
    rating: int
    category: Optional[str]
    product_page_url: str
    upc: Optional[str]
    description: Optional[str]
    image_url: Optional[str]


def fix_url(href: str) -> str:
    """Construir URL absoluta corrigindo paths faltando catalogue/"""
    if href.startswith("http"):
        return href
    href = href.replace("../", "").lstrip("/")
    if not href.startswith("catalogue/"):
        href = "catalogue/" + href
    return BASE_URL + href


def fetch(url: str, retries: int = 3) -> requests.Response:
    """Faz request com retentativas"""
    for i in range(retries):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            return r
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(0.5)


def parse_book(url: str) -> BookRow:
    """Extrai os dados de um livro individual"""
    resp = fetch(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    title = soup.select_one(".product_main h1").get_text(strip=True)

    # preço limpando qualquer caractere estranho
    price_txt = soup.select_one(".price_color").get_text(strip=True)
    price_clean = re.sub(r"[^0-9.]", "", price_txt)
    price = float(price_clean)

    # estoque
    stock_txt = soup.select_one(".availability").get_text(" ", strip=True)
    stock_match = re.search(r"(\d+)", stock_txt)
    stock = int(stock_match.group(1)) if stock_match else 0

    # rating
    rating_cls = soup.select_one(".star-rating")
    rating = 0
    if rating_cls:
        for cls in rating_cls["class"]:
            if cls in RATING_MAP:
                rating = RATING_MAP[cls]

    # category
    breadcrumb = soup.select(".breadcrumb li a")
    category = None
    if len(breadcrumb) > 2:
        category = breadcrumb[-1].get_text(strip=True)
        if category == title:
            category = breadcrumb[-2].get_text(strip=True)

    # UPC
    upc = None
    for tr in soup.select("table tr"):
        th = tr.select_one("th").get_text(strip=True)
        td = tr.select_one("td").get_text(strip=True)
        if th == "UPC":
            upc = td
            break

    # descrição
    desc_el = soup.select_one("#product_description ~ p")
    description = desc_el.get_text(strip=True) if desc_el else None

    # imagem
    img_el = soup.select_one(".thumbnail img")
    image_url = fix_url(img_el.get("src")) if img_el else None

    # id = slug
    slug = url.rstrip("/").split("/")[-2]

    return BookRow(
        id=slug,
        title=title,
        price=price,
        stock=stock,
        rating=rating,
        category=category,
        product_page_url=url,
        upc=upc,
        description=description,
        image_url=image_url
    )


def scrape():
    """Percorre todas as páginas de catálogo e coleta links"""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    url = CATALOG_URL + "page-1.html"
    book_links = []

    print("📚 Iniciando scraping...")

    # pegar links de todas as páginas
    while True:
        resp = fetch(url)
        soup = BeautifulSoup(resp.text, "html.parser")

        for a in soup.select("article.product_pod h3 a"):
            href = a.get("href")
            book_links.append(fix_url(href))

        next_btn = soup.select_one("li.next a")
        if not next_btn:
            break

        next_href = next_btn.get("href")
        url = fix_url(next_href)

        time.sleep(0.2)

    print(f"🔗 {len(book_links)} livros encontrados. Extraindo dados...\n")

    rows: List[BookRow] = []
    total = len(book_links)

    for i, link in enumerate(book_links, start=1):
        try:
            row = parse_book(link)
            rows.append(row)
            print(f"[{i}/{total}] ✅ {row.title}")
        except Exception as e:
            print(f"[{i}/{total}] ❌ Erro ao processar {link}: {e}")

        time.sleep(0.15)  # respeitar site

    # salvar CSV
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for r in rows:
            writer.writerow(asdict(r))

    print(f"\n✅ Concluído! {len(rows)} livros salvos em {OUTPUT_PATH}")


if __name__ == "__main__":
    scrape()
