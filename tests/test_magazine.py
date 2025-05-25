import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from lib.models.magazine import Magazine
from lib.models.author import Author
from scripts.setup_db import setup_database

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    setup_database()

def test_magazine_save_and_find():
    magazine = Magazine(name="Test Magazine", category="Tech")
    magazine.save()
    assert magazine.id is not None

    found = Magazine.find_by_id(magazine.id)
    assert found is not None
    assert found.name == "Test Magazine"
    assert found.category == "Tech"

def test_magazine_articles_and_contributors():
    author = Author(name="Contributor Author")
    author.save()
    magazine = Magazine(name="Contributor Magazine", category="Business")
    magazine.save()
    article = author.add_article(magazine, "Contributor Article")
    assert article.id is not None

    articles = magazine.articles()
    assert any(a.title == "Contributor Article" for a in articles)

    contributors = magazine.contributors()
    assert any(c.id == author.id for c in contributors)

def test_magazine_article_titles():
    magazine = Magazine(name="Title Magazine", category="Lifestyle")
    magazine.save()
    author = Author(name="Title Author")
    author.save()
    article = author.add_article(magazine, "Title Article")
    assert article.id is not None

    titles = magazine.article_titles()
    assert "Title Article" in titles

def test_magazine_contributing_authors():
    magazine = Magazine(name="Contrib Magazine", category="Science")
    magazine.save()
    author = Author(name="Contrib Author")
    author.save()
    for i in range(3):
        author.add_article(magazine, f"Article {i+1}")

    contrib_authors = magazine.contributing_authors()
    assert any(a.id == author.id for a in contrib_authors)
