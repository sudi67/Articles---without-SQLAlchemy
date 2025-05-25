import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib')))

import pytest
from db.connection import get_connection
from models.author import Author
from models.article import Article
from models.magazine import Magazine
from scripts.setup_db import setup_database

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    setup_database()

def test_add_author_with_articles_transaction_success():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        conn.execute("BEGIN TRANSACTION")
        cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Trans Author",))
        author_id = cursor.lastrowid
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Trans Magazine", "Tech"))
        magazine_id = cursor.lastrowid
        cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", ("Trans Article", author_id, magazine_id))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        pytest.fail("Transaction failed unexpectedly")
    finally:
        conn.close()

    author = Author.find_by_id(author_id)
    magazine = Magazine.find_by_id(magazine_id)
    articles = Article.find_by_author(author_id)
    assert author is not None
    assert magazine is not None
    assert any(a.title == "Trans Article" for a in articles)

def test_transaction_rollback_on_failure():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        conn.execute("BEGIN TRANSACTION")
        cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Rollback Author",))
        author_id = cursor.lastrowid
        cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", ("Rollback Article", author_id, 999999))
        conn.execute("COMMIT")
        pytest.fail("Transaction should have failed but committed")
    except Exception:
        conn.execute("ROLLBACK")
    finally:
        conn.close()

    author = Author.find_by_name("Rollback Author")
    assert author == []

def test_magazine_top_publisher():
    top_magazine = Magazine.top_publisher()
    assert top_magazine is not None
    assert hasattr(top_magazine, 'id')
    assert hasattr(top_magazine, 'name')

def test_find_magazines_with_multiple_authors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.*, COUNT(DISTINCT a.author_id) as author_count
        FROM magazines m
        JOIN articles a ON m.id = a.magazine_id
        GROUP BY m.id
        HAVING author_count >= 2
    """)
    rows = cursor.fetchall()
    assert rows is not None
    conn.close()
