---
name: data-pipeline-design
description: Data pipeline design for ETL/ELT workflows, streaming architectures, data validation, and orchestration. Use when building data pipelines, choosing batch vs.
---

# Data Pipeline Design

End-to-end guidance for designing, implementing, and operating data pipelines that move, transform, and validate data across systems. Covers batch and streaming architectures, orchestration frameworks, data quality enforcement, and production monitoring.

## When to Use This Skill

Use this skill for:

- Designing ETL or ELT pipelines for analytics and reporting
- Choosing between batch processing and stream processing
- Implementing data orchestration with Airflow, Prefect, or Dagster
- Building transformation layers with dbt or Apache Spark
- Setting up Kafka or Pub/Sub event streaming
- Implementing data validation and quality checks
- Designing data lake or data warehouse architectures (medallion pattern, star schema)
- Planning Change Data Capture (CDC) from operational databases
- Building idempotent and fault-tolerant data workflows
- Creating backfill strategies for historical data reprocessing

**Trigger phrases**: "data pipeline", "ETL", "ELT", "Airflow DAG", "dbt model", "Kafka", "streaming", "data quality", "data validation", "data lake", "data warehouse", "medallion architecture", "CDC", "batch processing", "orchestration"

## What This Skill Does

Provides production-grade data pipeline patterns including:

- **Architecture**: ETL vs ELT trade-offs, lambda vs kappa architectures
- **Batch Processing**: dbt models, Spark jobs, SQL transformations
- **Stream Processing**: Kafka consumers, Flink jobs, Pub/Sub subscriptions
- **Orchestration**: Airflow DAGs, Prefect flows, Dagster assets
- **Data Quality**: Validation frameworks, anomaly detection, data contracts
- **Storage**: Medallion architecture, star schema, partitioning strategies
- **Operations**: Monitoring, alerting, backfill, idempotency

## Instructions

### Step 1: Choose Your Architecture Pattern

**ETL vs ELT Decision Matrix**:

| Factor | ETL (Extract-Transform-Load) | ELT (Extract-Load-Transform) |
|--------|------------------------------|-------------------------------|
| Compute | Transform before loading | Transform inside warehouse |
| Best for | Legacy warehouses, limited storage | Cloud warehouses (Snowflake, BigQuery) |
| Data volume | Small to medium | Large to massive |
| Flexibility | Schema-on-write | Schema-on-read |
| Tooling | Informatica, Talend, custom code | dbt, Spark SQL, warehouse-native |

**Batch vs Streaming Decision Matrix**:

| Factor | Batch | Streaming |
|--------|-------|-----------|
| Latency tolerance | Minutes to hours | Seconds to milliseconds |
| Data completeness | Full dataset available | Events arrive continuously |
| Complexity | Lower | Higher |
| Cost | Generally lower | Higher (always-on infrastructure) |
| Use cases | Reports, ML training, backfills | Real-time dashboards, alerting, fraud |

**Medallion Architecture (Bronze-Silver-Gold)**:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Bronze     │────▶│   Silver     │────▶│    Gold      │
│  (Raw Data)  │     │  (Cleaned)   │     │ (Aggregated) │
├──────────────┤     ├──────────────┤     ├──────────────┤
│ Exact copy   │     │ Deduplicated │     │ Business     │
│ of source    │     │ Type-cast    │     │ metrics      │
│ Append-only  │     │ Validated    │     │ Star schema  │
│ Partitioned  │     │ Joined       │     │ SLA-governed │
│ by ingest dt │     │ Standardized │     │ Documented   │
└──────────────┘     └──────────────┘     └──────────────┘
```

### Step 2: Implement Orchestration with Airflow

**Airflow DAG: Complete ELT Pipeline**:

```python
"""
ELT pipeline: extract from Postgres, load to warehouse, transform with dbt.
Runs daily at 06:00 UTC.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['data-alerts@company.com'],
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=2),
}

dag = DAG(
    'elt_daily_pipeline',
    default_args=default_args,
    description='Daily ELT from Postgres to BigQuery with dbt transforms',
    schedule_interval='0 6 * * *',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=['elt', 'production'],
)

# ── Extract Phase ──────────────────────────────────────────────────

with TaskGroup('extract', dag=dag) as extract_group:
    tables = ['customers', 'orders', 'order_items', 'products']

    for table in tables:
        PostgresToGCSOperator(
            task_id=f'extract_{table}',
            postgres_conn_id='source_postgres',
            sql=f"""
                SELECT * FROM {table}
                WHERE updated_at >= '{{{{ ds }}}}'
                  AND updated_at <  '{{{{ next_ds }}}}'
            """,
            bucket='data-lake-raw',
            filename=f'bronze/{table}/{{{{ ds }}}}/{table}.parquet',
            export_format='parquet',
            dag=dag,
        )

# ── Load Phase ─────────────────────────────────────────────────────

with TaskGroup('load', dag=dag) as load_group:
    for table in tables:
        GCSToBigQueryOperator(
            task_id=f'load_{table}',
            bucket='data-lake-raw',
            source_objects=[f'bronze/{table}/{{{{ ds }}}}/*.parquet'],
            destination_project_dataset_table=f'warehouse.bronze.{table}',
            source_format='PARQUET',
            write_disposition='WRITE_APPEND',
            create_disposition='CREATE_IF_NEEDED',
            dag=dag,
        )

# ── Transform Phase (dbt) ─────────────────────────────────────────

dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command=(
        'cd /opt/dbt/project && '
        'dbt run --profiles-dir /opt/dbt/profiles --target production '
        '--vars \'{"run_date": "{{ ds }}"}\''
    ),
    dag=dag,
)

dbt_test = BashOperator(
    task_id='dbt_test',
    bash_command=(
        'cd /opt/dbt/project && '
        'dbt test --profiles-dir /opt/dbt/profiles --target production'
    ),
    dag=dag,
)

# ── Data Quality Checks ───────────────────────────────────────────

def run_quality_checks(**context):
    """Run post-transform data quality assertions."""
    from google.cloud import bigquery
    client = bigquery.Client()

    checks = [
        ("Row count > 0", "SELECT COUNT(*) as cnt FROM warehouse.gold.daily_sales WHERE sale_date = @run_date", lambda r: r > 0),
        ("No null revenue", "SELECT COUNT(*) as cnt FROM warehouse.gold.daily_sales WHERE revenue IS NULL AND sale_date = @run_date", lambda r: r == 0),
        ("Revenue positive", "SELECT MIN(revenue) as min_rev FROM warehouse.gold.daily_sales WHERE sale_date = @run_date", lambda r: r >= 0),
    ]

    failures = []
    for name, query, assertion in checks:
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("run_date", "DATE", context['ds']),
            ]
        )
        result = list(client.query(query, job_config=job_config))[0][0]
        if not assertion(result):
            failures.append(f"FAILED: {name} (got {result})")

    if failures:
        raise ValueError("Data quality checks failed:\n" + "\n".join(failures))

quality_checks = PythonOperator(
    task_id='data_quality_checks',
    python_callable=run_quality_checks,
    dag=dag,
)

# ── DAG Dependencies ──────────────────────────────────────────────

extract_group >> load_group >> dbt_run >> dbt_test >> quality_checks
```

### Step 3: Build Transformation Models with dbt

**dbt Project Structure**:

```
dbt_project/
  dbt_project.yml
  models/
    staging/          # 1:1 with source tables (bronze to silver)
      stg_customers.sql
      stg_orders.sql
      stg_order_items.sql
      _staging_models.yml
    intermediate/     # Business logic joins
      int_order_totals.sql
    marts/            # Gold layer, consumer-facing
      fct_daily_sales.sql
      dim_customers.sql
      _marts_models.yml
  tests/
    assert_positive_revenue.sql
  macros/
    cents_to_dollars.sql
```

**Staging Model** (`stg_orders.sql`):

```sql
-- models/staging/stg_orders.sql
{{
    config(
        materialized='incremental',
        unique_key='order_id',
        partition_by={
            'field': 'order_date',
            'data_type': 'date',
            'granularity': 'day'
        }
    )
}}

WITH source AS (
    SELECT * FROM {{ source('bronze', 'orders') }}
    {% if is_incremental() %}
    WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
    {% endif %}
),

renamed AS (
    SELECT
        id                              AS order_id,
        customer_id,
        status                          AS order_status,
        CAST(total AS NUMERIC(14, 2))   AS order_total,
        CAST(created_at AS TIMESTAMP)   AS order_date,
        CAST(updated_at AS TIMESTAMP)   AS updated_at
    FROM source
    WHERE id IS NOT NULL
)

SELECT * FROM renamed
```

**Mart Model** (`fct_daily_sales.sql`):

```sql
-- models/marts/fct_daily_sales.sql
{{
    config(
        materialized='table',
        partition_by={
            'field': 'sale_date',
            'data_type': 'date',
            'granularity': 'month'
        }
    )
}}

WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
    WHERE order_status NOT IN ('cancelled', 'refunded')
),

order_items AS (
    SELECT * FROM {{ ref('stg_order_items') }}
),

daily_metrics AS (
    SELECT
        DATE(o.order_date)          AS sale_date,
        COUNT(DISTINCT o.order_id)  AS order_count,
        COUNT(DISTINCT o.customer_id) AS unique_customers,
        SUM(o.order_total)          AS revenue,
        SUM(oi.quantity)            AS items_sold,
        AVG(o.order_total)          AS avg_order_value
    FROM orders o
    LEFT JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY 1
)

SELECT * FROM daily_metrics
```

**dbt Schema Tests** (`_marts_models.yml`):

```yaml
# models/marts/_marts_models.yml
version: 2

models:
  - name: fct_daily_sales
    description: Daily aggregated sales metrics
    columns:
      - name: sale_date
        description: Calendar date of sales
        tests:
          - not_null
          - unique
      - name: order_count
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
      - name: revenue
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
```

### Step 4: Implement Stream Processing with Kafka

**Kafka Producer (Python)**:

```python
"""Publish order events to Kafka when orders are created or updated."""
import json
from datetime import datetime
from confluent_kafka import Producer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry.json_schema import JSONSerializer

KAFKA_CONFIG = {
    'bootstrap.servers': 'kafka-broker-1:9092,kafka-broker-2:9092',
    'client.id': 'order-service',
    'acks': 'all',                  # Wait for all replicas
    'retries': 3,
    'retry.backoff.ms': 1000,
    'enable.idempotence': True,     # Exactly-once semantics
    'compression.type': 'snappy',
}

producer = Producer(KAFKA_CONFIG)

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}")

def publish_order_event(order: dict, event_type: str):
    """Publish an order event to Kafka with guaranteed delivery."""
    event = {
        'event_type': event_type,
        'event_time': datetime.utcnow().isoformat(),
        'order_id': order['id'],
        'customer_id': order['customer_id'],
        'total': float(order['total']),
        'status': order['status'],
    }

    producer.produce(
        topic='orders.events',
        key=str(order['id']).encode('utf-8'),   # Partition by order_id
        value=json.dumps(event).encode('utf-8'),
        callback=delivery_report,
    )
    producer.flush()  # Ensure delivery in synchronous contexts
```

**Kafka Consumer (Python)**:

```python
"""Consume order events and update analytics tables."""
import json
import signal
import sys
from confluent_kafka import Consumer, KafkaException

CONSUMER_CONFIG = {
    'bootstrap.servers': 'kafka-broker-1:9092,kafka-broker-2:9092',
    'group.id': 'analytics-consumer-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,      # Manual commit for at-least-once
    'max.poll.interval.ms': 300000,
    'session.timeout.ms': 45000,
}

consumer = Consumer(CONSUMER_CONFIG)
running = True

def shutdown(sig, frame):
    global running
    running = False

signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

def process_event(event: dict):
    """Idempotent event processing using event_id for deduplication."""
    event_id = f"{event['order_id']}_{event['event_time']}"

    # Upsert pattern: insert or update based on unique event_id
    # This ensures reprocessing the same event is safe
    upsert_to_analytics_table(event_id, event)

def run_consumer():
    consumer.subscribe(['orders.events'])

    try:
        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())

            event = json.loads(msg.value().decode('utf-8'))
            process_event(event)

            # Commit offset after successful processing
            consumer.commit(asynchronous=False)

    finally:
        consumer.close()

if __name__ == '__main__':
    run_consumer()
```

### Step 5: Implement Data Validation

**Great Expectations Checkpoint**:

```python
"""Define data quality expectations for the orders dataset."""
import great_expectations as gx

context = gx.get_context()

# Create a data source pointing to the warehouse
datasource = context.sources.add_or_update_sql(
    name="warehouse",
    connection_string="bigquery://project/dataset",
)

# Define expectations as a suite
suite = context.add_or_update_expectation_suite("orders_quality_suite")

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="order_id")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(column="order_id")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="order_total", min_value=0, max_value=1_000_000
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="order_status",
        value_set=["pending", "confirmed", "shipped", "delivered", "cancelled"]
    )
)
suite.add_expectation(
    gx.expectations.ExpectTableRowCountToBeBetween(min_value=1)
)

suite.save()
```

**Pydantic Models for Record Validation**:

```python
"""Validate individual records before loading into the warehouse."""
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator
from typing import Literal

class OrderRecord(BaseModel):
    order_id: str = Field(..., min_length=1, max_length=50)
    customer_id: str = Field(..., min_length=1)
    status: Literal['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
    total: Decimal = Field(..., ge=0, le=1_000_000, decimal_places=2)
    created_at: datetime

    @field_validator('created_at')
    @classmethod
    def not_in_future(cls, v: datetime) -> datetime:
        if v > datetime.utcnow():
            raise ValueError('created_at cannot be in the future')
        return v

def validate_batch(records: list[dict]) -> tuple[list[dict], list[dict]]:
    """Split a batch into valid and invalid records."""
    valid, invalid = [], []
    for record in records:
        try:
            validated = OrderRecord(**record)
            valid.append(validated.model_dump())
        except Exception as e:
            invalid.append({'record': record, 'error': str(e)})
    return valid, invalid
```

### Step 6: Implement Change Data Capture (CDC)

**Debezium CDC Configuration (Kafka Connect)**:

```json
{
  "name": "postgres-cdc-source",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "source-db.internal",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "${secrets:db-password}",
    "database.dbname": "production",
    "database.server.name": "prod-db",
    "table.include.list": "public.customers,public.orders,public.order_items",
    "plugin.name": "pgoutput",
    "slot.name": "debezium_slot",
    "publication.name": "debezium_pub",
    "topic.prefix": "cdc",
    "snapshot.mode": "initial",
    "tombstones.on.delete": true,
    "transforms": "route",
    "transforms.route.type": "org.apache.kafka.connect.transforms.RegexRouter",
    "transforms.route.regex": "cdc\\.public\\.(.*)",
    "transforms.route.replacement": "cdc.$1",
    "heartbeat.interval.ms": 10000,
    "errors.tolerance": "all",
    "errors.deadletterqueue.topic.name": "cdc-dlq",
    "errors.deadletterqueue.context.headers.enable": true
  }
}
```

### Step 7: Build Idempotent and Backfill-Safe Pipelines

**Idempotency Patterns**:

```python
def load_daily_partition(df, target_table: str, run_date: str):
    """
    Idempotent load: delete-then-insert for a specific date partition.
    Safe to re-run without duplicating data.
    """
    from google.cloud import bigquery
    client = bigquery.Client()

    # Delete existing data for this partition
    delete_query = f"""
        DELETE FROM `{target_table}`
        WHERE DATE(created_at) = @run_date
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("run_date", "DATE", run_date),
        ]
    )
    client.query(delete_query, job_config=job_config).result()

    # Insert fresh data
    load_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )
    client.load_table_from_dataframe(df, target_table, job_config=load_config).result()
```

**Backfill DAG Pattern (Airflow)**:

```python
"""
Backfill DAG: reprocess historical data for a specific date range.
Trigger manually with configuration:
  {"start_date": "2025-01-01", "end_date": "2025-12-31"}
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

dag = DAG(
    'backfill_pipeline',
    schedule_interval=None,  # Manual trigger only
    start_date=datetime(2025, 1, 1),
    catchup=False,
    params={
        'start_date': '2025-01-01',
        'end_date': '2025-12-31',
        'batch_size_days': 7,
    },
    tags=['backfill', 'manual'],
)

def run_backfill(**context):
    from datetime import timedelta
    params = context['params']
    start = datetime.strptime(params['start_date'], '%Y-%m-%d').date()
    end = datetime.strptime(params['end_date'], '%Y-%m-%d').date()
    batch_size = timedelta(days=params['batch_size_days'])

    current = start
    while current <= end:
        batch_end = min(current + batch_size - timedelta(days=1), end)
        print(f"Processing batch: {current} to {batch_end}")
        # Re-run the same idempotent load for each batch
        process_date_range(current, batch_end)
        current = batch_end + timedelta(days=1)

backfill_task = PythonOperator(
    task_id='run_backfill',
    python_callable=run_backfill,
    dag=dag,
)
```

### Step 8: Monitor Pipeline Health

**Key Pipeline Metrics to Track**:

| Metric | Alert Threshold | Tool |
|--------|----------------|------|
| DAG run duration | > 2x average | Airflow/Datadog |
| Task failure rate | > 0% on critical paths | PagerDuty |
| Data freshness (SLA) | > 1 hour stale | Monte Carlo, custom |
| Row count anomaly | > 30% deviation from 7-day average | Great Expectations |
| Schema drift | Any unexpected column change | dbt, Soda |
| Consumer lag (Kafka) | > 10,000 messages | Kafka metrics |

**Airflow SLA Monitoring**:

```python
from airflow import DAG
from datetime import datetime, timedelta

dag = DAG(
    'monitored_pipeline',
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    sla_miss_callback=notify_sla_miss,
)

def notify_sla_miss(dag, task_list, blocking_task_list, slas, blocking_tis):
    """Send alert when SLA is missed."""
    message = f"SLA missed for {dag.dag_id}: {[t.task_id for t in task_list]}"
    send_slack_alert(channel='#data-alerts', message=message)
```

## Best Practices

- **Idempotency first**: Every pipeline step should be safe to re-run without side effects
- **Partition by date**: Enables efficient backfills and reduces reprocessing scope
- **Validate early**: Catch bad data at the bronze layer before it propagates downstream
- **Use schema tests**: dbt tests and Great Expectations prevent silent data corruption
- **Separate extract from transform**: ELT scales better with modern cloud warehouses
- **Monitor data freshness**: SLAs should be automated, not checked manually
- **Dead-letter queues**: Route invalid records to a DLQ instead of dropping them silently
- **Version your pipelines**: DAGs and dbt models should be in version control with code review
- **Keep transforms declarative**: SQL-based transforms (dbt) are easier to audit than imperative code
- **Document data lineage**: Track which sources feed each downstream table

## Common Patterns

### Pattern 1: Slowly Changing Dimension (SCD Type 2)

```sql
-- dbt snapshot for SCD Type 2 (track historical changes)
-- snapshots/scd_customers.sql
{% snapshot scd_customers %}
{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='timestamp',
        updated_at='updated_at',
    )
}}

SELECT
    id AS customer_id,
    email,
    name,
    plan_type,
    updated_at
FROM {{ source('bronze', 'customers') }}

{% endsnapshot %}
```

### Pattern 2: Fan-Out Processing

```python
# Process each source table in parallel using Airflow dynamic task mapping
@task
def extract_table(table_name: str, run_date: str) -> str:
    """Extract a single table. Returns the GCS path."""
    return export_postgres_to_gcs(table_name, run_date)

@task
def load_table(gcs_path: str, table_name: str):
    """Load a single file from GCS to BigQuery."""
    load_gcs_to_bigquery(gcs_path, f"bronze.{table_name}")

# Dynamic fan-out: one task per table, runs in parallel
tables = ['customers', 'orders', 'order_items', 'products']
for table in tables:
    path = extract_table(table, "{{ ds }}")
    load_table(path, table)
```

## Quality Checklist

- [ ] Pipeline architecture documented (ETL vs ELT, batch vs streaming)
- [ ] All pipeline steps are idempotent (safe to re-run)
- [ ] Data is partitioned by date for efficient backfills
- [ ] Schema tests defined for all silver and gold layer models
- [ ] Data validation runs after every transform step
- [ ] Dead-letter queue configured for invalid records
- [ ] Backfill mechanism tested and documented
- [ ] SLA monitoring and alerting configured
- [ ] Pipeline DAGs and models are in version control
- [ ] Consumer lag and data freshness dashboards operational
- [ ] CDC configured with snapshot for initial load
- [ ] Data lineage documented from source to gold layer

## Related Skills

- `database-design` - Source database schema and indexing
- `cicd-architect` - Deploying pipeline code changes
- `cloud-architect` - Managed services (BigQuery, Redshift, Kafka on Confluent)
- `observability-setup` - Pipeline monitoring and alerting infrastructure

---

**Version**: 1.0.0
**Last Updated**: March 2026

### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
