# Articles Project (Without SQLAlchemy)

This project manages articles, authors, and magazines using a custom database connection and transaction handling without relying on SQLAlchemy.

## Project Structure

- `lib/db/connection.py`: Database connection management.
- `lib/db/transaction.py`: Transaction handling utilities.
- `lib/models/`: Contains models for articles, authors, and magazines.
- `scripts/setup_db.py`: Script to set up the database schema.
- `tests/`: Contains test cases for transactions and complex queries.

## Setup

1. Ensure you have Python 3.12 installed.
2. Run the database setup script:
   ```
   python3 scripts/setup_db.py
   ```
3. The database file `articles.db` will be created in the project root.

## Running Tests

Run the tests using pytest:
```
pytest tests/
```

## Notes

- This project does not use SQLAlchemy; it uses custom database connection and transaction management.
- The database schema is defined in `lib/db/schema.sql`.

## Additional Information

- The project uses Python 3.12.
- Cache files (`__pycache__`) are generated during runtime and can be ignored or added to `.gitignore`.
- The database file `articles.db` is created and updated during development.
- Tests are located in the `tests/` directory and can be run using `pytest`.

## File Structure

```
/home/sudeis/Articles---without-SQLAlchemy
├── README.md
├── articles.db
├── lib
│   ├── db
│   │   ├── connection.py
│   │   ├── schema.sql
│   │   └── transaction.py
│   └── models
│       ├── article.py
│       ├── author.py
│       └── magazine.py
├── scripts
│   └── setup_db.py
└── tests
    ├── test_article.py
    ├── test_author.py
    ├── test_magazine.py
    └── test_transaction_and_complex_queries.py
```
