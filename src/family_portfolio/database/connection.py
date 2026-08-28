from collections.abc import Generator
from contextlib import contextmanager

import duckdb

from family_portfolio.config.settings import settings


def get_connection() -> duckdb.DuckDBPyConnection:
    """Create a connection to the portfolio DuckDB database."""

    settings.database_path.parent.mkdir(parents=True, exist_ok=True)

    return duckdb.connect(str(settings.database_path))


@contextmanager
def database_connection() -> Generator[duckdb.DuckDBPyConnection, None, None]:
    """Provide a DuckDB connection and close it after use."""

    connection = get_connection()

    try:
        yield connection
    finally:
        connection.close()