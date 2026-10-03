---
name: data-pipeline
description: Build robust data pipelines for ETL, streaming, and batch processing. Orchestrate data movement between sources and destinations.
triggers:
- /data pipeline
- /etl pipeline
---

# Data Pipeline Development

This skill guides you through building robust data pipelines for extracting, transforming, and loading data across various sources and destinations.

## When to use this skill

Use this skill when you need to:
- Build ETL/ELT data pipelines
- Orchestrate data movement between systems
- Process streaming or batch data
- Implement data synchronization workflows
- Create data integration solutions

## Prerequisites

- Understanding of data sources (databases, APIs, files)
- Knowledge of data transformation requirements
- Access to orchestration tools (Airflow, Prefect, Dagster)
- Familiarity with data formats (JSON, Parquet, CSV, Avro)

## Guidelines

### Pipeline Architecture

**Components**
```
Data Source → Extract → Transform → Load → Data Destination
                ↓           ↓          ↓
           Validation  Enrichment  Monitoring
```

**Pipeline Types**
- **Batch**: Scheduled, high-volume processing (hourly/daily)
- **Streaming**: Real-time, low-latency processing (Kafka, Kinesis)
- **Hybrid**: Lambda architecture combining both approaches

### Design Principles

**Idempotency**
- Pipelines should be safe to re-run
- Use UPSERT operations instead of INSERT
- Implement deduplication logic
- Track processed records with watermark pattern

**Fault Tolerance**
- Implement retry logic with exponential backoff
- Use circuit breakers for external service calls
- Maintain dead letter queues for failed records
- Checkpoint progress for long-running jobs

**Scalability**
- Process data in chunks/batches
- Parallelize independent operations
- Use distributed processing (Spark, Dask)
- Scale compute resources elastically

### Implementation Patterns

**Apache Airflow Example**
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def extract_data(**context):
    # Extract from source
    data = source_api.fetch(date=context['ds'])
    return data

def transform_data(**context):
    # Transform data
    ti = context['ti']
    data = ti.xcom_pull(task_ids='extract')
    transformed = clean_and_normalize(data)
    return transformed

def load_data(**context):
    # Load to destination
    ti = context['ti']
    data = ti.xcom_pull(task_ids='transform')
    destination_db.insert(data)

with DAG('data_pipeline', start_date=datetime(2024, 1, 1), schedule_interval='@daily') as dag:
    extract = PythonOperator(task_id='extract', python_callable=extract_data)
    transform = PythonOperator(task_id='transform', python_callable=transform_data)
    load = PythonOperator(task_id='load', python_callable=load_data)
    
    extract >> transform >> load
```

### Data Quality

**Validation Checks**
- Schema validation (columns, types)
- Row count expectations
- Data freshness checks
- Null value thresholds
- Range validation for numeric fields

**Monitoring**
- Track pipeline execution times
- Alert on data volume anomalies
- Monitor error rates and SLA breaches
- Log data lineage for auditing

### Best Practices

**Code Organization**
```
pipelines/
├── dags/               # Airflow DAG definitions
├── tasks/              # Reusable task implementations
├── utils/              # Helper functions
├── tests/              # Unit and integration tests
└── config/             # Environment configurations
```

**Configuration Management**
- Externalize connection strings and credentials
- Use environment-specific configs
- Implement feature flags for gradual rollouts
- Version control all pipeline code

## Examples

See the `examples/` directory for:
- `batch-pipeline.py` - Daily batch ETL workflow
- `streaming-pipeline.py` - Kafka to database streaming
- `data-quality-checks.py` - Great Expectations integration
- `error-handling.py` - Robust error handling patterns

## References

- [Apache Airflow documentation](https://airflow.apache.org/docs/)
- [Prefect documentation](https://docs.prefect.io/)
- [Dagster documentation](https://docs.dagster.io/)
- [Data pipeline patterns](https://www.datanami.com/2022/07/21/data-pipeline-architecture-and-patterns/)
