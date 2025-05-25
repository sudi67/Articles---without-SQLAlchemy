import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.transaction import add_author_with_articles
from scripts.setup_db import setup_database

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    setup_database()

def test_author_save_and_find():
    author = Author(name="Test Author")
    author.save()
    assert author.id is not None

    found = Author.find_by_id(author.id)
    assert found is not None
    assert found.name == "Test Author"

def test_author_articles_and_magazines():
    author = Author(name="Article Author")
    author.save()
    magazine = Magazine(name="Test Magazine", category="Tech")
    magazine.save()
    article = author.add_article(magazine, "Test Article")
    assert article.id is not None

    articles = author.articles()
    assert any(a.title == "Test Article" for a in articles)

    magazines = author.magazines()
    assert any(m.name == "Test Magazine" for m in magazines)

def test_add_author_with_articles_transaction():
    articles_data = [
        {"title": "Trans Article 1", "magazine_id": 1},
        {"title": "Trans Article 2", "magazine_id": 1}
    ]
    result = add_author_with_articles("Transaction Author", articles_data)
    assert result is True
    author = Author.find_by_name("Transaction Author")
    assert author is not None
    articles = author.articles()
    assert len(articles) >= 2
