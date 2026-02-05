---
name: Dagster Patterns
description: Modern data orchestration with Dagster - Software-Defined Assets, declarative pipelines, observability, and production patterns.
---

# Dagster Patterns

## Overview

Dagster เป็น data orchestrator รุ่นใหม่ที่ใช้แนวคิด Software-Defined Assets แทน task-based DAGs แบบ Airflow ทำให้ focus ที่ "data" แทน "tasks" มี built-in observability, testing, และ type system

## Why This Matters

- **Asset-centric**: Focus ที่ data assets แทน tasks
- **Developer Experience**: Local development, testing, IDE support
- **Observability**: Built-in data lineage และ metadata
- **Type Safety**: Input/output types checked at runtime
- **Modern Stack**: Python-native, cloud-ready

---

## Core Concepts

### 1. Software-Defined Assets

```python
# assets/core.py
from dagster import asset, AssetExecutionContext, MaterializeResult, MetadataValue
import pandas as pd

@asset(
    description="Raw orders from e-commerce database",
    group_name="bronze",
    compute_kind="sql",
)
def raw_orders(context: AssetExecutionContext) -> pd.DataFrame:
    """Extract raw orders from source database"""
    query = """
        SELECT order_id, customer_id, total_amount, status, created_at
        FROM orders
        WHERE created_at >= CURRENT_DATE - INTERVAL '1 day'
    """
    
    df = pd.read_sql(query, get_db_connection())
    
    context.log.info(f"Extracted {len(df)} orders")
    
    # Log metadata
    context.add_output_metadata({
        "row_count": len(df),
        "columns": df.columns.tolist(),
        "sample": MetadataValue.md(df.head().to_markdown()),
    })
    
    return df


@asset(
    description="Cleaned and validated orders",
    group_name="silver",
    deps=["raw_orders"],  # Explicit dependency
)
def cleaned_orders(context: AssetExecutionContext, raw_orders: pd.DataFrame) -> pd.DataFrame:
    """Clean and validate order data"""
    df = raw_orders.copy()
    
    # Remove duplicates
    initial_count = len(df)
    df = df.drop_duplicates(subset=['order_id'])
    
    # Validate amounts
    df = df[df['total_amount'] >= 0]
    
    # Parse dates
    df['created_at'] = pd.to_datetime(df['created_at'])
    
    context.log.info(f"Cleaned {initial_count} -> {len(df)} orders")
    
    return df


@asset(
    description="Daily order aggregations",
    group_name="gold",
    compute_kind="pandas",
)
def daily_order_summary(
    context: AssetExecutionContext,
    cleaned_orders: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate orders by day"""
    df = cleaned_orders.copy()
    df['order_date'] = df['created_at'].dt.date
    
    summary = df.groupby('order_date').agg({
        'order_id': 'count',
        'total_amount': ['sum', 'mean'],
        'customer_id': 'nunique',
    }).reset_index()
    
    summary.columns = ['order_date', 'total_orders', 'total_revenue', 'avg_order_value', 'unique_customers']
    
    context.add_output_metadata({
        "date_range": f"{summary['order_date'].min()} to {summary['order_date'].max()}",
        "total_revenue": float(summary['total_revenue'].sum()),
    })
    
    return summary
```

### 2. Partitioned Assets

```python
# assets/partitioned.py
from dagster import (
    asset,
    DailyPartitionsDefinition,
    TimeWindowPartitionMapping,
    AssetExecutionContext,
)
from datetime import datetime

daily_partitions = DailyPartitionsDefinition(start_date="2024-01-01")

@asset(
    partitions_def=daily_partitions,
    description="Daily raw events from analytics",
    group_name="bronze",
)
def raw_events(context: AssetExecutionContext) -> pd.DataFrame:
    """Extract events for a specific day"""
    partition_date = context.partition_key
    
    query = f"""
        SELECT event_id, user_id, event_type, properties, timestamp
        FROM events
        WHERE DATE(timestamp) = '{partition_date}'
    """
    
    df = pd.read_sql(query, get_db_connection())
    
    context.log.info(f"Extracted {len(df)} events for {partition_date}")
    
    return df


@asset(
    partitions_def=daily_partitions,
    description="Processed user sessions",
    group_name="silver",
)
def user_sessions(
    context: AssetExecutionContext,
    raw_events: pd.DataFrame,
) -> pd.DataFrame:
    """Sessionize events"""
    df = raw_events.copy()
    
    # Session logic
    df = df.sort_values(['user_id', 'timestamp'])
    df['time_diff'] = df.groupby('user_id')['timestamp'].diff()
    df['new_session'] = df['time_diff'] > pd.Timedelta(minutes=30)
    df['session_id'] = df.groupby('user_id')['new_session'].cumsum()
    
    return df


# Monthly aggregation from daily data
monthly_partitions = MonthlyPartitionsDefinition(start_date="2024-01-01")

@asset(
    partitions_def=monthly_partitions,
    description="Monthly user metrics",
    group_name="gold",
    ins={
        "user_sessions": AssetIn(
            partition_mapping=TimeWindowPartitionMapping(start_offset=-1, end_offset=0)
        )
    },
)
def monthly_user_metrics(
    context: AssetExecutionContext,
    user_sessions: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate monthly user metrics from daily sessions"""
    # Aggregation logic
    return metrics_df
```

### 3. IO Managers

```python
# io_managers/s3.py
from dagster import IOManager, OutputContext, InputContext, io_manager
import pandas as pd
import boto3
from io import BytesIO

class S3ParquetIOManager(IOManager):
    def __init__(self, bucket: str, prefix: str):
        self.bucket = bucket
        self.prefix = prefix
        self.s3 = boto3.client('s3')
    
    def _get_path(self, context) -> str:
        asset_key = "/".join(context.asset_key.path)
        if context.has_partition_key:
            return f"{self.prefix}/{asset_key}/{context.partition_key}.parquet"
        return f"{self.prefix}/{asset_key}.parquet"
    
    def handle_output(self, context: OutputContext, obj: pd.DataFrame):
        path = self._get_path(context)
        
        buffer = BytesIO()
        obj.to_parquet(buffer, index=False)
        buffer.seek(0)
        
        self.s3.put_object(
            Bucket=self.bucket,
            Key=path,
            Body=buffer.getvalue(),
        )
        
        context.log.info(f"Wrote {len(obj)} rows to s3://{self.bucket}/{path}")
    
    def load_input(self, context: InputContext) -> pd.DataFrame:
        path = self._get_path(context)
        
        response = self.s3.get_object(Bucket=self.bucket, Key=path)
        df = pd.read_parquet(BytesIO(response['Body'].read()))
        
        context.log.info(f"Loaded {len(df)} rows from s3://{self.bucket}/{path}")
        
        return df

@io_manager(
    config_schema={"bucket": str, "prefix": str},
)
def s3_parquet_io_manager(context):
    return S3ParquetIOManager(
        bucket=context.resource_config["bucket"],
        prefix=context.resource_config["prefix"],
    )


# Snowflake IO Manager
from dagster_snowflake_pandas import SnowflakePandasIOManager

snowflake_io_manager = SnowflakePandasIOManager(
    account="xxx",
    user=EnvVar("SNOWFLAKE_USER"),
    password=EnvVar("SNOWFLAKE_PASSWORD"),
    database="ANALYTICS",
    schema="PUBLIC",
    warehouse="COMPUTE_WH",
)
```

### 4. Resources

```python
# resources/database.py
from dagster import ConfigurableResource, EnvVar
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

class DatabaseResource(ConfigurableResource):
    host: str
    port: int = 5432
    database: str
    user: str
    password: str
    
    def get_connection(self):
        url = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        return create_engine(url)
    
    def execute_query(self, query: str) -> pd.DataFrame:
        engine = self.get_connection()
        return pd.read_sql(query, engine)


class SlackResource(ConfigurableResource):
    webhook_url: str
    
    def send_message(self, message: str):
        import requests
        requests.post(self.webhook_url, json={"text": message})


# Usage in assets
@asset
def my_asset(context: AssetExecutionContext, database: DatabaseResource):
    df = database.execute_query("SELECT * FROM users")
    return df
```

### 5. Sensors and Schedules

```python
# schedules.py
from dagster import (
    ScheduleDefinition,
    schedule,
    RunRequest,
    SkipReason,
    sensor,
    SensorResult,
    AssetSelection,
    define_asset_job,
)

# Simple schedule
daily_refresh = ScheduleDefinition(
    job=define_asset_job("daily_refresh", selection=AssetSelection.groups("gold")),
    cron_schedule="0 6 * * *",  # 6 AM daily
    execution_timezone="Asia/Bangkok",
)

# Dynamic schedule
@schedule(
    cron_schedule="0 * * * *",  # Every hour
    job=define_asset_job("hourly_events"),
)
def hourly_events_schedule(context):
    partition_key = context.scheduled_execution_time.strftime("%Y-%m-%d-%H")
    return RunRequest(
        run_key=partition_key,
        partition_key=partition_key,
        tags={"source": "schedule"},
    )


# S3 Sensor - trigger on new files
@sensor(
    job=define_asset_job("process_uploads"),
    minimum_interval_seconds=60,
)
def s3_file_sensor(context):
    import boto3
    
    s3 = boto3.client('s3')
    bucket = "my-bucket"
    prefix = "uploads/"
    
    # Get last processed marker
    cursor = context.cursor or ""
    
    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix,
        StartAfter=cursor,
    )
    
    new_files = response.get('Contents', [])
    
    if not new_files:
        return SkipReason("No new files")
    
    run_requests = []
    for obj in new_files:
        run_requests.append(
            RunRequest(
                run_key=obj['Key'],
                run_config={
                    "ops": {"process_file": {"config": {"file_path": obj['Key']}}}
                },
            )
        )
    
    return SensorResult(
        run_requests=run_requests,
        cursor=new_files[-1]['Key'],  # Update cursor
    )
```

### 6. Testing

```python
# tests/test_assets.py
from dagster import materialize, build_asset_context
import pandas as pd
import pytest

from assets.core import raw_orders, cleaned_orders, daily_order_summary


def test_cleaned_orders_removes_duplicates():
    """Test that cleaned_orders removes duplicate order_ids"""
    # Create test data with duplicates
    raw_data = pd.DataFrame({
        'order_id': [1, 1, 2, 3],
        'customer_id': [100, 100, 101, 102],
        'total_amount': [50.0, 50.0, 75.0, 100.0],
        'status': ['completed'] * 4,
        'created_at': pd.to_datetime(['2024-01-01'] * 4),
    })
    
    context = build_asset_context()
    result = cleaned_orders(context, raw_data)
    
    assert len(result) == 3
    assert result['order_id'].is_unique


def test_cleaned_orders_removes_negative_amounts():
    """Test that cleaned_orders removes negative amounts"""
    raw_data = pd.DataFrame({
        'order_id': [1, 2, 3],
        'customer_id': [100, 101, 102],
        'total_amount': [50.0, -10.0, 100.0],
        'status': ['completed'] * 3,
        'created_at': pd.to_datetime(['2024-01-01'] * 3),
    })
    
    context = build_asset_context()
    result = cleaned_orders(context, raw_data)
    
    assert len(result) == 2
    assert (result['total_amount'] >= 0).all()


def test_daily_order_summary_aggregation():
    """Test daily aggregation logic"""
    cleaned_data = pd.DataFrame({
        'order_id': [1, 2, 3, 4],
        'customer_id': [100, 100, 101, 102],
        'total_amount': [50.0, 75.0, 100.0, 25.0],
        'status': ['completed'] * 4,
        'created_at': pd.to_datetime([
            '2024-01-01', '2024-01-01', '2024-01-02', '2024-01-02'
        ]),
    })
    
    context = build_asset_context()
    result = daily_order_summary(context, cleaned_data)
    
    assert len(result) == 2
    assert result[result['order_date'] == '2024-01-01']['total_orders'].values[0] == 2


# Integration test with materialization
def test_full_pipeline():
    """Test full materialization of assets"""
    result = materialize(
        [raw_orders, cleaned_orders, daily_order_summary],
        resources={
            "database": mock_database_resource,
        },
    )
    
    assert result.success
    
    # Check output
    summary = result.output_for_node("daily_order_summary")
    assert len(summary) > 0
```

### 7. Definitions

```python
# definitions.py
from dagster import Definitions, load_assets_from_modules, EnvVar
from dagster_dbt import DbtCliResource

from . import assets
from .resources.database import DatabaseResource, SlackResource
from .io_managers.s3 import s3_parquet_io_manager
from .schedules import daily_refresh, s3_file_sensor

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    resources={
        # Database
        "database": DatabaseResource(
            host=EnvVar("DB_HOST"),
            database=EnvVar("DB_NAME"),
            user=EnvVar("DB_USER"),
            password=EnvVar("DB_PASSWORD"),
        ),
        # IO Managers
        "io_manager": s3_parquet_io_manager.configured({
            "bucket": "my-data-lake",
            "prefix": "dagster",
        }),
        # Notifications
        "slack": SlackResource(
            webhook_url=EnvVar("SLACK_WEBHOOK_URL"),
        ),
        # dbt
        "dbt": DbtCliResource(
            project_dir="path/to/dbt/project",
            profiles_dir="path/to/dbt/profiles",
        ),
    },
    schedules=[daily_refresh],
    sensors=[s3_file_sensor],
)
```

## Quick Start

1. **Install Dagster:**
   ```bash
   pip install dagster dagster-webserver dagster-pandas
   ```

2. **Create project:**
   ```bash
   dagster project scaffold --name my_project
   cd my_project
   ```

3. **Define assets:**
   ```python
   # my_project/assets.py
   from dagster import asset
   
   @asset
   def my_first_asset():
       return [1, 2, 3]
   ```

4. **Run development UI:**
   ```bash
   dagster dev
   ```

5. **Open http://localhost:3000**

## Production Checklist

- [ ] IO Managers configured for cloud storage
- [ ] Resources use environment variables
- [ ] Partitions defined for incremental processing
- [ ] Schedules configured with proper timezone
- [ ] Sensors for event-driven triggers
- [ ] Tests for critical assets
- [ ] Alerting configured (Slack/PagerDuty)
- [ ] Dagster Cloud or self-hosted deployment

## Anti-patterns

1. **Task-centric thinking**: Think in assets, not tasks
2. **Skipping IO Managers**: Use IO Managers for production
3. **No partitions for large data**: Use partitions for incremental processing
4. **Ignoring metadata**: Log metadata for observability

## Integration Points

- **dbt**: `dagster-dbt` for dbt assets
- **Snowflake**: `dagster-snowflake` IO Manager
- **BigQuery**: `dagster-gcp` IO Manager
- **Spark**: `dagster-spark` for PySpark
- **Airbyte**: `dagster-airbyte` for sync jobs

## Further Reading

- [Dagster Documentation](https://docs.dagster.io/)
- [Software-Defined Assets](https://docs.dagster.io/concepts/assets/software-defined-assets)
- [Dagster University](https://courses.dagster.io/)
