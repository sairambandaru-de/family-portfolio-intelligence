import duckdb


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS owners (
    owner_id BIGINT PRIMARY KEY,
    owner_name VARCHAR NOT NULL,
    owner_type VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id BIGINT PRIMARY KEY,
    owner_id BIGINT NOT NULL,
    account_name VARCHAR NOT NULL,
    account_type VARCHAR NOT NULL,
    provider_name VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS instruments (
    instrument_id BIGINT PRIMARY KEY,
    instrument_name VARCHAR NOT NULL,
    instrument_type VARCHAR NOT NULL,
    currency_code VARCHAR NOT NULL DEFAULT 'INR',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS instrument_identifiers (
    instrument_identifier_id BIGINT PRIMARY KEY,
    instrument_id BIGINT NOT NULL,
    identifier_type VARCHAR NOT NULL,
    identifier_value VARCHAR NOT NULL,
    source_name VARCHAR,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(identifier_type, identifier_value)
);

CREATE TABLE IF NOT EXISTS source_files (
    source_file_id BIGINT PRIMARY KEY,
    file_name VARCHAR NOT NULL,
    file_path VARCHAR NOT NULL,
    file_hash VARCHAR NOT NULL,
    source_type VARCHAR NOT NULL,
    statement_date DATE,
    ingested_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(file_hash)
);

CREATE TABLE IF NOT EXISTS ingestion_runs (
    ingestion_run_id BIGINT PRIMARY KEY,
    source_file_id BIGINT NOT NULL,
    source_name VARCHAR NOT NULL,
    parser_version VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    error_message VARCHAR
);

CREATE TABLE IF NOT EXISTS holding_snapshots (
    holding_snapshot_id BIGINT PRIMARY KEY,
    owner_id BIGINT NOT NULL,
    account_id BIGINT NOT NULL,
    instrument_id BIGINT NOT NULL,
    ingestion_run_id BIGINT NOT NULL,
    snapshot_date DATE NOT NULL,
    quantity DECIMAL(20, 6) NOT NULL,
    average_cost DECIMAL(20, 4),
    market_price DECIMAL(20, 4),
    market_value DECIMAL(20, 4),
    currency_code VARCHAR NOT NULL DEFAULT 'INR',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS validation_results (
    validation_result_id BIGINT PRIMARY KEY,
    ingestion_run_id BIGINT NOT NULL,
    validation_type VARCHAR NOT NULL,
    validation_status VARCHAR NOT NULL,
    entity_type VARCHAR,
    entity_id BIGINT,
    message VARCHAR,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def initialize_database(connection: duckdb.DuckDBPyConnection) -> None:
    """Create all required database tables."""

    connection.execute(SCHEMA_SQL)