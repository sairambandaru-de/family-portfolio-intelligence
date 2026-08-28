import duckdb

from family_portfolio.database.schema import initialize_database


def test_initialize_database_creates_all_tables():
    """Schema initialization creates all required tables."""

    connection = duckdb.connect(":memory:")

    initialize_database(connection)

    tables = {
        row[0]
        for row in connection.execute("SHOW TABLES").fetchall()
    }

    expected_tables = {
        "owners",
        "accounts",
        "instruments",
        "instrument_identifiers",
        "source_files",
        "ingestion_runs",
        "holding_snapshots",
        "validation_results",
    }

    assert expected_tables == tables

    connection.close()