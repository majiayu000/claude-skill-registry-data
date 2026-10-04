---
name: fivetran
description: "Fivetran specialist for fully managed Extract-Load (EL) data pipelines. Deep expertise in connectors, sync modes, CDC, schema management, dbt integration, HVA, Hybrid Deployment, and cost optimization. WHEN: \"Fivetran\", \"Fivetran connector\", \"Fivetran sync\", \"MAR\", \"Monthly Active Rows\", \"Fivetran destination\", \"Fivetran transformations\", \"Quickstart data models\", \"Fivetran dbt\", \"Fivetran CDC\", \"HVA connector\", \"High-Volume Agent\", \"Fivetran Hybrid Deployment\", \"Connector SDK\", \"Fivetran schema drift\", \"Fivetran webhook\", \"Fivetran Terraform\", \"Fivetran REST API\", \"Fivetran vs ADF\", \"Fivetran vs Airbyte\", \"_fivetran_synced\", \"_fivetran_deleted\"."
license: MIT
---

# Fivetran

This skill covers Fivetran, the fully managed Extract-Load (EL) platform that automates data movement from source systems to cloud destinations. Fivetran is a managed SaaS service with no user-facing version numbers -- all accounts run the latest platform release. It provides deep knowledge of:

- Connector ecosystem (700+ pre-built connectors: Standard, Lite, Partner-Built, Custom SDK, HVA)
- Sync modes (full historical, incremental via cursor/API/CDC, soft delete, history mode, live mode)
- Change Data Capture (log-based CDC for all major databases, HVR-derived HVA engine)
- Schema management (automatic detection, net-additive vs live updating, data type promotion)
- Transformations (Quickstart data models, SQL transformations, dbt Core orchestration, dbt Cloud integration)
- Deployment models (SaaS, Hybrid Deployment, High-Volume Agent)
- Infrastructure as Code (REST API, Terraform provider, Postman collections)
- Cost optimization (MAR management, connector consolidation, sync frequency tuning)
- Security (SOC 2 Type 2, HIPAA, HITRUST, GDPR, private networking, customer-managed KMS)

## How to Approach Tasks

When you receive a request:

1. **Classify** the request:
   - **Connector setup / selection** -- Load `references/architecture.md` for connector types, sync modes, CDC methods, and destination support
   - **Performance / best practices** -- Load `references/best-practices.md` for sync frequency tuning, schema mapping, cost optimization, dbt patterns, and alerting
   - **Troubleshooting / diagnostics** -- Load `references/diagnostics.md` for sync failures, data discrepancies, schema drift, and performance issues
   - **dbt integration** -- See the `dbt-core` skill for dbt-specific context, then apply Fivetran integration patterns
   - **Cross-tool comparison** -- See the `integration` skill for Fivetran vs ADF, Glue, NiFi, etc.

2. **Gather context** -- Determine:
   - What source system? (SaaS API, database, file, event stream)
   - What destination? (Snowflake, BigQuery, Redshift, Databricks, etc.)
   - What sync frequency is needed? (real-time, minutes, hours, daily)
   - What deployment model? (SaaS, Hybrid, HVA)
   - Is the concern about cost, freshness, or data quality?

3. **Analyze** -- Apply Fivetran-specific reasoning. Consider connector type (Standard vs Lite vs HVA), CDC method, MAR implications, schema change handling strategy, and downstream transformation approach.

4. **Recommend** -- Provide actionable guidance with specific Fivetran configuration settings, REST API calls, Terraform resources, and dbt integration patterns where appropriate.

5. **Verify** -- Suggest validation steps (sync history review, `_fivetran_synced` freshness checks, row count comparisons, schema change notifications).

## Core Architecture

### Control Plane and Data Plane

```
┌───────────────────────────────────────────────┐
│  Fivetran Control Plane (SaaS)                │
│  ┌────────────┐  ┌────────────┐  ┌─────────┐ │
│  │ Scheduling │  │ Schema Mgmt│  │Dashboard│ │
│  │ & Orchestr.│  │ & Detection│  │ API/TF  │ │
│  └─────┬──────┘  └─────┬──────┘  └────┬────┘ │
│        │               │              │       │
│  ┌─────▼───────────────▼──────────────▼────┐  │
│  │         Connector Execution Engine      │  │
│  └─────────────────┬───────────────────────┘  │
└────────────────────┼──────────────────────────┘
                     │
     ┌───────────────┼───────────────┐
     │               │               │
┌────▼────┐   ┌──────▼──────┐  ┌────▼─────┐
│  Source  │   │  Hybrid /   │  │Destination│
│  System  │   │  HVA Agent  │  │(Warehouse)│
└─────────┘   └─────────────┘  └──────────┘
```

**Control Plane** manages orchestration, scheduling, credential storage (AES-256 encrypted), schema detection, the dashboard UI, REST API, and Terraform provider.

**Data Plane** options determine where data processing occurs:

| Model | Data Processing | Orchestration | Use Case |
|---|---|---|---|
| **SaaS (Fully Managed)** | Fivetran cloud | Fivetran cloud | Default for most customers |
| **Hybrid Deployment** | Customer network (Docker/K8s agent) | Fivetran cloud | Data residency, compliance, on-prem sources |
| **High-Volume Agent (HVA)** | Customer network (dedicated agent) | Fivetran cloud | Enterprise database CDC, high-throughput replication |

### Connector Ecosystem

Fivetran provides **700+ pre-built connectors** -- the largest catalog in the managed EL market:

| Category | Count | Examples |
|---|---|---|
| SaaS Applications | 400+ | Salesforce, HubSpot, Marketo, Zendesk, Jira, ServiceNow, Workday |
| Databases | 30+ | PostgreSQL, MySQL, SQL Server, Oracle, MongoDB, DynamoDB, Cosmos DB |
| ERP / Finance | 20+ | SAP, NetSuite, QuickBooks, Xero, Sage |
| Advertising | 30+ | Google Ads, Facebook Ads, LinkedIn Ads, TikTok Ads |
| Files & Storage | 15+ | S3, GCS, Azure Blob, SFTP, Google Sheets |
| Events & Streaming | 10+ | Webhooks, Kafka, Kinesis, Google Pub/Sub |

**Connector types**:
1. **Standard** -- Full-featured, fully managed, broadest schema coverage
2. **Lite** -- Faster-to-build connectors for non-dynamic schemas; fewer endpoints; no 1-minute sync
3. **Partner-Built** -- Third-party connectors available to all customers
4. **Custom (Connector SDK)** -- Python-based custom connectors for proprietary sources
5. **HVA** -- Enterprise database connectors with log-based CDC, running in customer infrastructure (HVR-derived engine)

### Sync Modes

| Mode | Behavior | Trigger |
|---|---|---|
| **Full (Historical)** | Extracts all data from selected tables on initial setup | First sync or manual re-sync |
| **Incremental** | Extracts only new/changed data since last sync | Every scheduled sync after initial |
| **Soft Delete** | Deleted rows marked `_fivetran_deleted = TRUE`; retained in destination | Default for CDC tables |
| **History Mode** | All row versions retained (SCD Type 2) with `_fivetran_start`, `_fivetran_end`, `_fivetran_active` | Configured per table |
| **Live Mode** | Hard deletes propagated; destination mirrors source exactly | When exact source parity is required |

Incremental detection methods: cursor-based (timestamp/sequence), API-based diffing, log-based CDC, SQL Server Change Tracking.

### CDC Architecture

Fivetran uses **exclusively log-based CDC** for database connectors:

| Database | CDC Method |
|---|---|
| SQL Server | CDC system tables, Change Tracking, Binary Log Reader |
| PostgreSQL | Logical replication (pgoutput / wal2json) |
| MySQL | Binary log (binlog) replication |
| Oracle | LogMiner, Oracle GoldenGate (via HVA) |
| MongoDB | Change streams |

Log-based CDC captures all changes with near-zero source performance impact.

### Schema Management

**Automatic detection**: Fivetran detects source schemas and propagates changes automatically.

**Schema change handling**:
- **Allow all new data** -- New schemas, tables, columns synced automatically
- **Allow new columns** -- Only column additions on existing tables; new tables blocked
- **Block all new data** -- All changes require manual approval

**Schema evolution strategies**:
- **Net-additive** (default) -- Columns never removed; renames create duplicates; safe for downstream consumers
- **Live updating** -- Destination mirrors source exactly; renames and removals propagated

**Data type promotion**: When source types change, Fivetran promotes destination columns to more inclusive types (e.g., integer to double) to prevent data loss.

### Transformations

| Method | Complexity | dbt Required | Scheduling |
|---|---|---|---|
| **Quickstart Data Models** | Zero-code | No (Fivetran-maintained dbt models) | After sync or fixed schedule |
| **SQL Transformations** | Low | No | After sync or fixed schedule |
| **dbt Core Orchestration** | Medium-High | Yes (v1.9.10+ / v1.10.11+) | Triggered by Fivetran after sync |
| **dbt Cloud Integration** | Medium-High | Yes (dbt Cloud) | Triggered by Fivetran after sync |

**Quickstart Data Models** are pre-built, Fivetran-maintained dbt models that convert raw connector output into analytics-ready tables. Available for Salesforce, HubSpot, Stripe, Shopify, Google Ads, Jira, and many more. Zero SQL required.

### Pricing

**Monthly Active Rows (MAR)**: Distinct primary keys synced per connector per month. A row is counted once regardless of how many times it syncs in the month. Since March 2025, MAR is calculated per connection (not across the account).

| Plan | Min Sync Frequency | Key Features |
|---|---|---|
| Free | 5 minutes | 500K MAR, all Standard features |
| Standard | 5 minutes | Pay-as-you-go, core features |
| Enterprise | 1 minute | Private networking, advanced security |
| Business Critical | 1 minute | Customer-managed KMS, HIPAA, dedicated support |

Base charge: $5/connection/month (1 to 1M MAR). Transformations: 5,000 model runs free/month.

### Fivetran + dbt Labs Merger

In October 2025, Fivetran and dbt Labs announced an all-stock merger. The combined entity approaches $600M ARR and aims to build a unified open data infrastructure platform spanning extraction, loading, and transformation.

## Anti-Patterns

1. **Syncing everything** -- Syncing all tables and columns when only a subset is needed. This is the single most expensive mistake. Deselect unused tables and columns before the initial sync.
2. **Over-syncing low-priority data** -- Setting 5-minute sync frequency on data that changes daily (HR data, financial close data). Match sync frequency to business need.
3. **Ignoring MAR on full-refresh tables** -- Full-refresh tables re-sync all rows every cycle, dramatically inflating MAR compared to incremental. Understand which tables are full-refresh and whether the cost is justified.
4. **Skipping schema change notifications** -- Source schemas change without warning. Enable notifications and review changes promptly to prevent downstream breakage.
5. **Modifying Fivetran raw tables directly** -- Never alter Fivetran-managed tables. All transformation should happen in a separate schema via dbt or SQL transformations.
6. **Using Fivetran for complex transformation** -- Fivetran is an EL tool, not an ETL tool. Complex business logic belongs in dbt or the destination warehouse, not in Fivetran SQL transformations.
7. **Starting historical sync at end of billing period** -- Initial syncs generate high MAR. Start large historical syncs at the beginning of a billing period to maximize the month's MAR allowance.
8. **Ignoring the Connector SDK for proprietary sources** -- Building custom API integrations outside Fivetran when the Connector SDK would provide managed scheduling, retry, and state management.

## IaC and API

### REST API

Full CRUD for connectors, destinations, users, groups, schemas, and transformations. Trigger syncs and query status programmatically.

```bash
# Trigger a sync
curl -X POST https://api.fivetran.com/v1/connectors/{connector_id}/force \
  -H "Authorization: Bearer $FIVETRAN_API_KEY"

# Check connector status
curl https://api.fivetran.com/v1/connectors/{connector_id} \
  -H "Authorization: Bearer $FIVETRAN_API_KEY"
```

### Terraform Provider

Official HashiCorp-verified provider: `fivetran/terraform-provider-fivetran`. Manage connectors, destinations, users, and groups as code. Multi-region support (US, EU, AU).

```hcl
resource "fivetran_connector" "salesforce" {
  group_id         = fivetran_group.default.id
  service          = "salesforce"
  sync_frequency   = 15
  destination_schema {
    name = "raw_salesforce"
  }
  config {
    # connector-specific configuration
  }
}
```

## Metadata Columns

Fivetran adds system columns to every synced table:

| Column | Purpose |
|---|---|
| `_fivetran_synced` | Timestamp when the row was last synced to destination |
| `_fivetran_deleted` | Boolean: row was deleted at source (soft delete mode) |
| `_fivetran_id` | System-generated unique ID (when source lacks a primary key) |
| `_fivetran_start` | History mode: when this row version became active |
| `_fivetran_end` | History mode: when this row version was superseded |
| `_fivetran_active` | History mode: whether this is the current version |

Use `_fivetran_synced` for freshness monitoring and `_fivetran_deleted` in dbt staging models to filter soft-deleted rows.

## Reference Files

- `references/architecture.md` -- Platform architecture (control plane, data plane, deployment models), connector ecosystem and types, destinations, sync modes, CDC methods, HVR acquisition, schema management, transformations, IaC
- `references/best-practices.md` -- Connector selection and tiering, sync frequency tuning, schema mapping strategy, cost optimization (MAR management), alerting and monitoring, dbt integration patterns, operational practices
- `references/diagnostics.md` -- Sync failure triage (authentication, network, rate limiting, schema errors), data discrepancy investigation, schema drift detection and mitigation, performance diagnostics, Fivetran metadata columns

## Cross-References

- `dbt-core` skill -- dbt Core context for Fivetran-orchestrated dbt pipelines
- `dbt-cloud` skill -- dbt Cloud context for Fivetran-triggered dbt Cloud jobs
- `adf` skill -- Azure Data Factory for comparison and hybrid architectures
- `overview` skill -- Cross-tool comparisons and paradigm routing
