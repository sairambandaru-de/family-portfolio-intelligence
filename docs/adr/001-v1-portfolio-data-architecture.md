# ADR-001: V1 Portfolio Data Architecture

**Status:** Accepted  
**Date:** 2026-08-28

---

## Context

Family Portfolio Intelligence is being built as a personal and family portfolio management application.

The system will eventually support multiple asset classes, including:

- Indian equities
- Mutual funds
- ETFs
- Foreign equities
- EPF
- PPF
- NPS
- Fixed deposits
- Bonds
- Gold
- PMS and AIF investments
- Other manually entered assets
- Liabilities

However, implementing all asset classes in the first version would add significant complexity.

The first implementation will focus on reliable ingestion and validation of current investment holdings.

---

## Decision

Version 1 will focus on:

1. Indian equity holdings from Zerodha Kite
2. Indian equity holdings from Angel One
3. Mutual fund holdings from supported statements in later phases
4. Validation and reconciliation before building the UI

The user interface will be implemented only after the ingestion and validation layers are reliable.

---

## Core Data Model

The initial architecture will use the following core concepts:

```text
Owner
  |
  v
Account
  |
  v
Holding Snapshot
  |
  +------------------> Instrument
  |
  v
Source File
  |
  v
Ingestion Run
```
The core database entities will initially include:

- owners
- accounts
- instruments
- instrument_identifiers
- holding_snapshots
- source_files
- ingestion_runs
- validation_results
```
---

## Instrument Identity Strategy

An instrument must have a canonical identity independent of the source that reports it.

Broker-specific names or symbols will not be treated as the canonical instrument identity.

Where available, stable identifiers such as ISIN will be used.

This prevents the same investment from being duplicated during multi-broker consolidation.

---

## Holdings Strategy

Version 1 will use holding snapshots rather than a complete transaction ledger.

A holding snapshot represents the holdings reported by a source at a specific point in time.

This approach allows the system to establish reliable current holdings before implementing transaction-level analytics.

A transaction ledger may be introduced later for:

- XIRR
- Capital gains
- FIFO calculations
- Historical portfolio reconstruction
- Detailed cash-flow analysis

---

## Data Lineage

Every imported holding should be traceable back to its source.

The architecture will support recording:

- source file
- source row number where practical
- ingestion run
- parser version
- ingestion timestamp
- source statement date

---

## Idempotency

Importing the same source statement multiple times must not result in duplicate portfolio holdings.

The ingestion process will support file identification using metadata and/or file hashes.

The system will detect previously processed files and either:

- skip duplicate ingestion, or
- explicitly create a new controlled ingestion version

Duplicate behavior will be clearly recorded.

---

## Validation Strategy

Validation will occur before data is considered canonical.

### Schema Validation

- Required fields exist
- Data types are valid
- Dates can be parsed

### Business Validation

- Quantity is valid
- Monetary values are valid
- Instrument identity is present where expected

### Arithmetic Validation

Imported values should be checked for reasonable arithmetic consistency.

Example:

```text
Quantity × Market Price ≈ Market Value
```

### Reconciliation

Imported totals should reconcile with source statement totals where those totals are available.

Example:

```text
Source Statement Total
        vs
Imported Holdings Total
```

---

## Asset Taxonomy

The architecture will distinguish between asset classes and more specific
instrument types.

Examples of asset classes:

- Equity
- Debt
- Gold
- Cash
- Real Estate
- Alternatives

Examples of equity instrument types:

- Indian Stock
- Foreign Stock
- ETF
- REIT

Version 1 will implement only the asset classes required for supported
equity holdings.

The schema should remain extensible for future asset classes.

---

## Ownership Model

The architecture will separate portfolio ownership from source accounts.

An owner may eventually represent:

- Individual
- Joint ownership
- HUF
- Trust
- Other legal entity

An owner may have multiple accounts.

Example:

```text
Owner
  |
  +-- Zerodha Account
  |
  +-- Angel One Account
  |
  +-- Mutual Fund Folio
```
---

## Currency Strategy

Version 1 will primarily support INR.

However, monetary data models should not permanently assume that all assets
are denominated in INR.

Future versions may support:

- Foreign stocks
- Multiple currencies
- FX rates
- Portfolio reporting currency conversion


---

## Explicitly Deferred

The following capabilities are intentionally deferred:

- Complete transaction ledger
- Corporate action processing
- Tax calculations
- XIRR and advanced performance calculations
- Foreign stock ingestion
- FX rate ingestion
- EPF / PPF / NPS ingestion
- Liabilities
- Financial goals
- Look-through mutual fund exposure
- Risk analytics
- Web user interface

These features will be introduced incrementally after reliable holdings ingestion is established.

---

## Consequences

### Benefits

- Faster delivery of the first working milestone
- Reliable and auditable ingestion pipeline
- Clear separation between source-specific parsers and canonical models
- Easier validation and reconciliation
- Extensible architecture for future asset classes

### Trade-offs

- Snapshot data alone cannot fully support capital gains calculations
- Advanced performance analytics will require transaction data later
- Some portfolio events may require future historical data enrichment

---

## First Milestone

The first production-quality milestone is:

```text
Zerodha Holdings Statement
        |
        v
Source File Registration
        |
        v
Parser
        |
        v
Canonical Holding Snapshot
        |
        v
Validation
        |
        v
DuckDB Storage
        |
        v
Reconciliation Report
```

After this pipeline is reliable, Angel One support will be added using the same canonical data model.