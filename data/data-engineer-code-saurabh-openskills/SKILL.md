---
name: data-engineer
description: Design and build production-grade data pipelines, ETL/ELT workflows, data warehouses, and streaming architectures. Use when the user asks about data pipelines, ETL/ELT, dbt models, Airflow DAGs, Kafka, data warehouses (Snowflake, BigQuery, Redshift), data quality, schema design for analytics, event streaming, or says "build a pipeline", "transform this data", or "set up a data warehouse".
---

# Data Engineering

Approach every data pipeline as a senior engineer who has been paged at 3am because a downstream dashboard showed zero rows. Data pipelines fail silently. They process the wrong data, miss records, duplicate records, or apply transformations incorrectly — and nobody notices until a business decision is made on corrupt numbers.

Your job is not to move data from A to B. Your job is to move data from A to B reliably, observably, and reproducibly — so that every downstream consumer can trust what they receive.

---

## Data Engineering Principles

- **Data quality is a first-class requirement, not an afterthought.** Bad data reaching a dashboard or a model is worse than no data. Build quality checks at every stage, before data moves downstream.
- **Pipelines must be idempotent.** Running a pipeline twice must produce the same result as running it once. This is the only property that makes recovery from failure safe.
- **Schema is a contract.** Changing a schema without coordinating with downstream consumers is a breaking change. Schema evolution must be managed deliberately.
- **Lineage is mandatory.** You must be able to answer: where did this number come from? Which source records contributed to it? Which transformation changed it?
- **Make it observable before it breaks.** Logs, metrics, and data quality alerts must be in place before a pipeline goes to production. A pipeline without observability cannot be debugged.
- **Batch and streaming are different beasts.** Understand which model fits the use case before designing. Do not use streaming because it sounds impressive if batch is simpler and sufficient.

---

## Step 0: Ground the Data Problem

Before designing any pipeline:

1. **What data is the source?** Source system, format (CSV, JSON, Parquet, Avro, database), volume (rows/day), change rate, access method (API, SFTP, CDC, Kafka topic, database replication).
2. **What does the consumer need?** Specific tables/columns, freshness SLA (real-time, hourly, daily), row-level access control, query patterns (aggregations, point lookups, full scans).
3. **What is the transformation logic?** Joins, aggregations, deduplication, enrichment, cleansing, business rule application.
4. **What is the freshness requirement?** Real-time (<1 minute), near-real-time (<15 minutes), hourly, daily? This determines batch vs streaming.
5. **What are the failure modes?** Source goes offline, schema changes, late-arriving data, duplicate records, network interruptions.
6. **What does done look like?** Define the data quality assertions that must pass before the pipeline is considered healthy.

---

## Choosing the Right Architecture

| Pattern | When to use | When to avoid |
|---------|------------|---------------|
| **Batch ETL** | Daily/hourly reports, historical loads, large volume transforms, cost-sensitive workloads | When freshness < 15 min is required |
| **ELT** (load raw, transform in warehouse) | When the warehouse has compute power (BigQuery, Snowflake, Redshift), source data is complex to transform before loading | When raw data contains PII that must not land in the warehouse |
| **Streaming** (Kafka, Kinesis, Pub/Sub) | Real-time dashboards, fraud detection, event-driven microservices, continuous ML scoring | When batch is sufficient — streaming adds operational complexity |
| **CDC** (Change Data Capture) | Syncing operational databases to analytics without full re-scans | Source DB doesn't support binlog/WAL, or change volume is too high |
| **Lambda architecture** | When both real-time and historical accuracy are needed | Most cases — it is complex to maintain two processing paths |
| **Kappa architecture** | Real-time-first, reprocess from log when needed | When the event log cannot be replayed |

---

## Pipeline Design Patterns

### Extract — Pull Data from Sources

**Rules:**
- Always use pagination when pulling from APIs — never assume one call returns all records
- Checkpoint your position — record the last successfully extracted watermark (timestamp, offset, cursor)
- Retry with exponential backoff on transient failures; circuit-break on sustained failures
- Validate the schema of source data immediately on extraction — fail fast before storing corrupt data
- Never extract more data than you need — push predicates to the source when possible

```python
def extract_orders(source_client, watermark: datetime) -> Iterator[dict]:
    """
    Extract orders modified after watermark.
    Yields records one page at a time to avoid memory issues.
    """
    cursor = None
    while True:
        response = source_client.get_orders(
            modified_after=watermark.isoformat(),
            cursor=cursor,
            page_size=500,
        )
        
        for record in response.data:
            validate_schema(record, ORDER_SCHEMA)  # fail fast on schema mismatch
            yield record
        
        if not response.has_more:
            break
        cursor = response.next_cursor
```

### Transform — Apply Business Logic

**Rules:**
- Transformations must be pure and deterministic: same input always produces same output
- Document every business rule in a comment — why is this transformation done, not just what it does
- Handle NULLs explicitly — never silently drop or coerce NULL values without documenting why
- Deduplication must use a stable, documented key — not arbitrary first/last record
- Apply data quality checks before and after transformation

```python
def transform_order(raw: dict) -> dict:
    """
    Apply business rules to raw order records.
    
    Business rules:
    - Amount stored as integer cents (prevents floating point rounding errors)
    - status mapped to internal enum (source uses legacy codes: 'O'=open, 'C'=closed)
    - customer_id prefixed with 'cust_' for consistency with user service IDs
    """
    return {
        "id": raw["order_id"],
        "customer_id": f"cust_{raw['customer_id']}",
        "amount_cents": round(float(raw["amount"]) * 100),  # float->cents
        "status": ORDER_STATUS_MAP[raw["status_code"]],     # documented mapping
        "created_at": parse_iso8601(raw["created_at"]),
        "updated_at": parse_iso8601(raw["updated_at"]),
    }

# Every transformation has a corresponding test
def test_transform_order_converts_amount_to_cents():
    raw = create_raw_order(amount="19.99")
    result = transform_order(raw)
    assert result["amount_cents"] == 1999

def test_transform_order_maps_legacy_status_code():
    raw = create_raw_order(status_code="O")
    result = transform_order(raw)
    assert result["status"] == "OPEN"
```

### Load — Write to Destination

**Rules:**
- **Upsert, not insert** for incremental loads — prevents duplicates when a pipeline reruns
- Write to a staging table first, validate, then swap to production (atomic swap pattern)
- Use transactions for multi-table writes that must be consistent
- Partition destination tables by date/time for efficient querying and data retention management
- Log every load: rows written, rows skipped, rows updated, duration, watermark advanced to

```sql
-- Atomic swap pattern: load to staging, validate, swap
BEGIN;

-- 1. Load new data into staging
INSERT INTO orders_staging SELECT * FROM orders_new_batch;

-- 2. Run quality checks
-- (run in application layer; rollback if any fail)

-- 3. Upsert from staging to production
INSERT INTO orders (id, customer_id, amount_cents, status, created_at, updated_at)
SELECT id, customer_id, amount_cents, status, created_at, updated_at
FROM orders_staging
ON CONFLICT (id) DO UPDATE SET
    amount_cents = EXCLUDED.amount_cents,
    status       = EXCLUDED.status,
    updated_at   = EXCLUDED.updated_at;

-- 4. Truncate staging
TRUNCATE orders_staging;

COMMIT;
```

---

## dbt (Data Build Tool) Standards

### Project Structure
```
dbt_project/
├── models/
│   ├── staging/          # 1:1 with source tables, minimal transform, rename columns
│   │   └── stg_orders.sql
│   ├── intermediate/     # Business logic joins, not exposed to end users
│   │   └── int_orders_enriched.sql
│   └── marts/            # Final analytics tables exposed to BI tools
│       ├── finance/
│       │   └── fct_revenue.sql
│       └── product/
│           └── fct_user_activity.sql
├── tests/
│   └── generic/          # Custom generic tests
├── macros/               # Reusable SQL macros
├── seeds/                # Static reference data CSVs
└── sources/              # Source declarations
    └── sources.yml
```

### Model Standards
```sql
-- models/staging/stg_orders.sql
-- Staging model: 1:1 with source table, only renames and type casts

{{
  config(
    materialized = 'view',
    tags = ['staging', 'orders']
  )
}}

with source as (
    select * from {{ source('ecommerce', 'raw_orders') }}
),

renamed as (
    select
        order_id                    as order_id,
        customer_id                 as customer_id,
        cast(amount as numeric)     as amount,
        status_code                 as status_code,
        cast(created_at as timestamp) as created_at
    from source
)

select * from renamed
```

### dbt Testing Standards
```yaml
# models/staging/schema.yml
version: 2
models:
  - name: stg_orders
    description: "Staged orders from the ecommerce source system"
    columns:
      - name: order_id
        description: "Unique order identifier"
        tests:
          - unique
          - not_null
      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('stg_customers')
              field: customer_id
      - name: status_code
        tests:
          - accepted_values:
              values: ['O', 'C', 'P', 'R']
      - name: amount
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
```

**dbt rules:**
- Every model has a schema.yml with `unique` and `not_null` tests on primary keys
- `ref()` for inter-model dependencies — never hardcode schema.table
- `source()` for raw source tables — never hardcode source schema
- Staging models are views; marts are tables or incremental models
- Every model has a `description` — required, not optional

---

## Apache Airflow DAG Standards

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# DAG-level defaults — applied to all tasks unless overridden
DEFAULT_ARGS = {
    "owner": "data-engineering",
    "depends_on_past": False,           # Don't block on previous run failures
    "retries": 3,                       # Retry transient failures
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
    "email_on_failure": True,
    "email": ["data-alerts@company.com"],
}

with DAG(
    dag_id="orders_pipeline",
    description="Extract orders from source, load to warehouse, transform with dbt",
    schedule_interval="0 * * * *",       # Hourly
    start_date=days_ago(1),
    catchup=False,                        # Don't backfill missed runs automatically
    default_args=DEFAULT_ARGS,
    tags=["orders", "finance"],
) as dag:

    extract = PythonOperator(
        task_id="extract_orders",
        python_callable=extract_orders_task,
        # Each task is idempotent — safe to retry
    )

    load = PythonOperator(
        task_id="load_to_staging",
        python_callable=load_orders_task,
    )

    quality_check = PythonOperator(
        task_id="run_data_quality_checks",
        python_callable=run_quality_checks_task,
    )

    transform = BashOperator(
        task_id="dbt_transform",
        bash_command="dbt run --select tag:orders --target prod",
    )

    # Task dependencies define the DAG
    extract >> load >> quality_check >> transform
```

**Airflow rules:**
- `catchup=False` by default — explicit backfill only when needed
- Every task idempotent — safe to re-run after failure
- `retries` and `retry_delay` on every task
- Alerting configured before DAG goes to production
- SLA defined on business-critical DAGs

---

## Data Quality Framework

Data quality checks run at three points in every pipeline:
1. **On extraction** — validate raw source data against expected schema
2. **After transformation** — validate business rules are correctly applied
3. **Before promoting to production** — final quality gate

```python
class DataQualityCheck:
    """Run data quality checks against a dataframe. Fail loudly."""

    def check_no_nulls(self, df, column: str):
        null_count = df[column].isnull().sum()
        assert null_count == 0, f"Column {column} has {null_count} nulls — expected 0"

    def check_unique(self, df, column: str):
        dupe_count = df[column].duplicated().sum()
        assert dupe_count == 0, f"Column {column} has {dupe_count} duplicates — expected unique"

    def check_row_count(self, df, min_rows: int, max_rows: int = None):
        count = len(df)
        assert count >= min_rows, f"Got {count} rows, expected at least {min_rows}"
        if max_rows:
            assert count <= max_rows, f"Got {count} rows, expected at most {max_rows}"

    def check_no_future_dates(self, df, column: str):
        future = df[df[column] > pd.Timestamp.now()]
        assert len(future) == 0, f"Column {column} has {len(future)} future dates"

    def check_referential_integrity(self, df, fk_col: str, ref_df, pk_col: str):
        orphans = ~df[fk_col].isin(ref_df[pk_col])
        count = orphans.sum()
        assert count == 0, f"{count} records in {fk_col} have no match in reference"
```

**Quality checks that must exist on every pipeline:**
- [ ] Row count within expected range (catches empty loads and unexpected volume spikes)
- [ ] No NULLs on primary keys
- [ ] Primary key uniqueness
- [ ] Referential integrity for foreign keys
- [ ] No future-dated timestamps
- [ ] Numeric values within expected ranges
- [ ] Categorical values in allowed set
- [ ] No duplicate records on the business key

---

## Streaming with Kafka

```python
from confluent_kafka import Consumer, KafkaError
import json

def consume_events(topic: str, group_id: str, processor):
    """
    Consume events from Kafka with at-least-once semantics.
    
    Offset is committed only after successful processing + downstream write.
    This means an event may be processed twice on failure — processor must be idempotent.
    """
    consumer = Consumer({
        "bootstrap.servers": KAFKA_BROKERS,
        "group.id": group_id,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,    # Manual commit after processing
    })
    consumer.subscribe([topic])

    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            raise KafkaException(msg.error())

        try:
            event = json.loads(msg.value())
            validate_schema(event, EVENT_SCHEMA)    # fail fast on bad schema
            processor(event)                        # must be idempotent
            consumer.commit(asynchronous=False)     # commit only on success
        except SchemaValidationError as e:
            dead_letter(msg, reason=str(e))          # route to DLQ, don't crash
            consumer.commit(asynchronous=False)
        except Exception as e:
            log.error(f"Processing failed: {e}", exc_info=True)
            # Do not commit — message will be redelivered
```

**Kafka rules:**
- Manual offset commit — never auto-commit
- Every consumer is idempotent — messages may be delivered more than once
- Dead-letter queue (DLQ) for messages that cannot be processed — never lose a message
- Schema registry for Avro/Protobuf schemas — enforce compatibility before producing
- Consumer lag monitored — alert when lag exceeds threshold

---

## Data Warehouse Design

### Fact & Dimension Tables (Star Schema)
```sql
-- Fact table: one row per event, foreign keys to dimensions, measures
CREATE TABLE fct_orders (
    order_id        VARCHAR PRIMARY KEY,
    customer_key    INTEGER REFERENCES dim_customers(customer_key),
    product_key     INTEGER REFERENCES dim_products(product_key),
    date_key        INTEGER REFERENCES dim_date(date_key),
    amount_cents    BIGINT NOT NULL,
    quantity        INTEGER NOT NULL,
    created_at      TIMESTAMP NOT NULL
)
PARTITION BY RANGE (created_at);  -- partition by date for query performance

-- Dimension table: descriptive attributes, slowly changing
CREATE TABLE dim_customers (
    customer_key    SERIAL PRIMARY KEY,     -- surrogate key
    customer_id     VARCHAR NOT NULL,       -- natural/business key
    name            VARCHAR,
    email           VARCHAR,
    tier            VARCHAR,
    valid_from      DATE NOT NULL,
    valid_to        DATE,                   -- NULL = current record (SCD Type 2)
    is_current      BOOLEAN DEFAULT TRUE
);
```

**Warehouse design rules:**
- Fact tables contain measures and foreign keys — no descriptive attributes
- Dimension tables contain descriptive attributes — no measures
- Surrogate keys on dimension tables — business keys change; surrogate keys do not
- Slowly Changing Dimensions (SCD Type 2) for attributes that must preserve history
- Partition fact tables by date — queries almost always filter by time range
- Cluster/sort keys aligned to the most common query patterns

---

## Observability Checklist

Every pipeline in production must have:

- [ ] **Run logs** — start time, end time, rows extracted, rows loaded, rows skipped, watermark advanced to
- [ ] **Data quality check results** — pass/fail for every check, with failed row counts
- [ ] **Row count anomaly detection** — alert if today's row count deviates > 20% from the 7-day average
- [ ] **Freshness monitoring** — alert if a table's `max(updated_at)` is older than the SLA
- [ ] **Schema change detection** — alert if the source schema changes unexpectedly
- [ ] **Pipeline duration tracking** — alert if a run takes > 2x the normal duration
- [ ] **Dead letter queue monitoring** — alert on any DLQ accumulation

---

## Definition of Done — Data Pipeline

A data pipeline is production-ready when:

- [ ] All extraction logic is paginated and watermarked
- [ ] All transformations are pure, deterministic, and tested
- [ ] All loads are idempotent (safe to re-run)
- [ ] Data quality checks pass at extract, transform, and load stages
- [ ] Pipeline is observable: logs, metrics, freshness and anomaly alerts
- [ ] Schema documented with column descriptions and data types
- [ ] Data lineage documented: source → transformations → destination
- [ ] Failure and retry behaviour defined and tested
- [ ] Dead-letter queue configured for streaming pipelines
- [ ] SLA defined and monitored
- [ ] Runbook written for common failure scenarios
- [ ] Backfill procedure documented and tested
