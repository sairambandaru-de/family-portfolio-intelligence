# ADR-002: DuckDB Schema and Storage Strategy

**Status:** Accepted
**Date:** 2026-08-28

---

## Context

Family Portfolio Intelligence requires a local analytical database for
storing portfolio data imported from multiple financial sources.

The initial sources include:

- Zerodha Kite
- Angel One
- Zerodha Coin
- CAMS
- KFintech

The database must support:

- Local development
- SQL analytics
- Portfolio reconciliation
- Snapshot-based holdings
- Multiple accounts and owners
- Future asset classes
- Reproducible ingestion pipelines

The application does not initially require a distributed transactional
database.

---

## Decision

DuckDB will be used as the primary local analytical database for Version 1.

The primary database file will be:

```text
warehouse/portfolio.duckdb
```

The database file will contain the canonical structured portfolio data.

Raw source files will not be stored inside DuckDB. They will remain in
the filesystem under the project data directories.

---

## Storage Layers

The application will use a simplified medallion-style storage architecture:

```text
data/raw
    |
    |  Original source files
    v
data/bronze
    |
    |  Source-normalized data
    v
data/silver
    |
    |  Validated canonical records
    v
DuckDB
    |
    |  Analytical and relational queries
    v
data/gold
    |
    |  Curated reports and exports
```

## Database Responsibilities

DuckDB will store:

- Owners
- Accounts
- Canonical instruments
- Instrument identifiers
- Source file metadata
- Ingestion run metadata
- Holding snapshots
- Validation results

DuckDB will not initially store raw source documents such as:

- PDF files
- Original Excel files
- Original CSV files

---

## Schema Strategy

The database schema will prioritize:

1. Clear entity relationships
2. Stable canonical identifiers
3. Data lineage
4. Reproducible ingestion
5. Extensibility
6. Analytical query performance

The initial implementation will use normalized relational tables.

Denormalized analytical views may be introduced later.
---

## Initial Schema

The initial Version 1 schema will contain:

```text
owners
    |
    +---- accounts
    |
    +---- holding_snapshots

accounts
    |
    +---- holding_snapshots

instruments
    |
    +---- instrument_identifiers
    |
    +---- holding_snapshots

source_files
    |
    +---- ingestion_runs
            |
            +---- holding_snapshots
            |
            +---- validation_results
```
---

## Primary Keys

Each canonical entity will use a generated internal identifier.

Examples:

```text
owner_id
account_id
instrument_id
source_file_id
ingestion_run_id
holding_snapshot_id
```
Natural identifiers such as account numbers, broker symbols, and ISINs
will not be used as the primary key.

They will be stored as attributes or in identifier mapping tables.

---

## Instrument Identity

The `instruments` table represents the canonical financial instrument.

Examples:

- Reliance Industries
- HDFC Bank
- NIFTY 50 ETF

The `instrument_identifiers` table will store identifiers from different
sources.

Example:

```text
Instrument
    |
    +-- ISIN
    |
    +-- NSE Symbol
    |
    +-- BSE Code
    |
    +-- Broker-specific Symbol
```
This prevents source-specific naming from creating duplicate instruments.

---

## Holding Snapshots

The `holding_snapshots` table will store holdings as reported at a
specific point in time.

A holding record will include concepts such as:

- Owner
- Account
- Instrument
- Quantity
- Average cost
- Market price
- Market value
- Currency
- Snapshot date
- Ingestion run

A holding snapshot is immutable once successfully ingested.

Corrections should be represented through a controlled subsequent
ingestion rather than silently overwriting historical data.

---

## Data Lineage

Each holding snapshot should be traceable to:

```text
Holding Snapshot
       |
       v
Ingestion Run
       |
       v
Source File
```
The system will record metadata such as:

- Source filename
- File hash
- Source type
- Parser version
- Ingestion timestamp
- Statement date

---

## Idempotency

The `source_files` table will record a file hash.

Before ingestion, the application will check whether the same source file
has already been successfully processed.

The initial duplicate strategy will be:

```text
Same File Hash
       |
       v
Previously Successfully Processed?
       |
      Yes
       |
       v
Skip ingestion
```
A future version may support controlled reprocessing when parser logic
changes.

---

## DuckDB and Filesystem Boundary

The following responsibility boundary will be maintained:

```text
Filesystem
    |
    +-- Raw source documents
    +-- Intermediate files
    +-- Generated reports

DuckDB
    |
    +-- Canonical portfolio entities
    +-- Ingestion metadata
    +-- Validation metadata
    +-- Analytical datasets
```
---

## Schema Management

Database schema creation will initially be managed through Python.

The project will provide an initialization process that:

1. Creates the DuckDB database file if it does not exist
2. Creates required schemas and tables
3. Is safe to run repeatedly

The initial approach will use idempotent SQL:

```sql
CREATE TABLE IF NOT EXISTS ...
```

---

## Backup Strategy

The DuckDB database file represents important derived portfolio data.

Backups will be stored under:

```text
backups/
```
Raw source files will remain separately preserved under:
```text
data/raw/
```
---

## Explicitly Deferred

The following decisions are deferred:

- Cloud-hosted database
- Multi-user concurrency
- Distributed processing
- Database migration framework
- Full transaction ledger
- Data warehouse partitioning strategy
- Real-time market data storage
- Production-scale orchestration

These capabilities will be introduced only when justified by application
requirements.

---

## Consequences

### Benefits

- Simple local development
- Excellent SQL analytical capabilities
- Minimal operational overhead
- Easy backup and portability
- Strong fit for portfolio analytics
- Easy integration with Python and Pandas

### Trade-offs

- Not intended as a high-concurrency multi-user OLTP database
- Cloud deployment may eventually require architectural changes
- Schema migration discipline will become more important as the project grows

---

## Implementation Plan

The implementation will proceed in the following order:

1. Create database package
2. Create DuckDB connection management
3. Define canonical table schemas
4. Initialize database
5. Verify tables with SQL
6. Add automated tests