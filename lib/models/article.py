from lib.db.connection import get_connection

class Article:
    def __init__(self, id=None, title=None, author_id=None, magazine_id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (self.title, self.author_id, self.magazine_id)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                (self.title, self.author_id, self.magazine_id, self.id)
            )
        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, article_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row['id'], title=row['title'], author_id=row['author_id'], magazine_id=row['magazine_id'])
        return None

    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row['id'], title=row['title'], author_id=row['author_id'], magazine_id=row['magazine_id']) for row in rows]

    @classmethod
    def find_by_author(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (author_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row['id'], title=row['title'], author_id=row['author_id'], magazine_id=row['magazine_id']) for row in rows]

    @classmethod
    def find_by_magazine(cls, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row['id'], title=row['title'], author_id=row['author_id'], magazine_id=row['magazine_id']) for row in rows]

    # Relationship methods
    def author(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (self.author_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            from lib.models.author import Author
            return Author(id=row['id'], name=row['name'])
        return None

    def magazine(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (self.magazine_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            from lib.models.magazine import Magazine
            return Magazine(id=row['id'], name=row['name'], category=row['category'])
        return None
