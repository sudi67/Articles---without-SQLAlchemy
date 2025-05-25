import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine
from scripts.setup_db import setup_database

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    setup_database()

def test_article_save_and_find():
    author = Author(name="Article Author")
    author.save()
    magazine = Magazine(name="Article Magazine", category="Tech")
    magazine.save()
    article = Article(title="Test Article", author_id=author.id, magazine_id=magazine.id)
    article.save()
    assert article.id is not None

    found = Article.find_by_id(article.id)
    assert found is not None
    assert found.title == "Test Article"

def test_article_find_by_methods():
    author = Author(name="Find Author")
    author.save()
    magazine = Magazine(name="Find Magazine", category="Business")
    magazine.save()
    article = Article(title="Find Article", author_id=author.id, magazine_id=magazine.id)
    article.save()

    by_title = Article.find_by_title("Find Article")
    assert any(a.id == article.id for a in by_title)

    by_author = Article.find_by_author(author.id)
    assert any(a.id == article.id for a in by_author)

    by_magazine = Article.find_by_magazine(magazine.id)
    assert any(a.id == article.id for a in by_magazine)

def test_article_relationships():
    author = Author(name="Rel Author")
    author.save()
    magazine = Magazine(name="Rel Magazine", category="Lifestyle")
    magazine.save()
    article = Article(title="Rel Article", author_id=author.id, magazine_id=magazine.id)
    article.save()

    assert article.author().id == author.id
    assert article.magazine().id == magazine.id

def test_article_find_by_title_not_found():
    articles = Article.find_by_title("Nonexistent Title")
    assert articles == []

def test_article_find_by_author_no_articles():
    author = Author(name="No Articles Author")
    author.save()
    articles = Article.find_by_author(author.id)
    assert articles == []

def test_article_find_by_magazine_no_articles():
    magazine = Magazine(name="No Articles Magazine", category="Misc")
    magazine.save()
    articles = Article.find_by_magazine(magazine.id)
    assert articles == []
