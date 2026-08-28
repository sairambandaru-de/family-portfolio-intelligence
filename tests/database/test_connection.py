from family_portfolio.database.connection import database_connection


def test_database_connection():
    """Database connection can execute a simple query."""

    with database_connection() as connection:
        result = connection.execute("SELECT 42").fetchone()

    assert result == (42,)