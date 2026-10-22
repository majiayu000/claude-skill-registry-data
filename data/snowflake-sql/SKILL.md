---
name: snowflake-sql
description: >-
  Writes and reviews Snowflake-specific SQL: QUALIFY, FLATTEN, VARIANT/OBJECT/ARRAY handling, streams,
  tasks, stages, and warehouse-aware patterns. Use when generic SQL is not enough on Snowflake —
  semi-structured data, incremental pipelines, or Snowflake DDL.
---

# Snowflake SQL Expert

Snowflake is not just SQL — it has its own DDL patterns, semi-structured types, streaming primitives, and compute model. Apply the right Snowflake-specific pattern for every situation.

---

## DDL Foundations

### Tables
```sql
-- Standard table with clustering
create or replace table raw_db.crm.accounts (
    account_id      varchar(36)     not null,
    account_name    varchar(255),
    account_type    varchar(50),
    amount          number(18, 2),
    metadata        variant,                  -- JSON blob
    tags            array,
    created_at      timestamp_ntz   not null,
    _loaded_at      timestamp_ntz   default current_timestamp()
)
cluster by (date_trunc('month', created_at), account_type)
data_retention_time_in_days = 7
comment = 'Raw CRM accounts from Salesforce';

-- Transient table (no time travel, lower cost — good for staging)
create or replace transient table staging.temp_load as
select * from raw_db.crm.accounts;

-- Clone (zero-copy, instant)
create or replace table dev_db.crm.accounts clone raw_db.crm.accounts;
```

### Views
```sql
-- Secure view (column-level access control)
create or replace secure view analytics.crm.vw_accounts as
select account_id, account_name, account_type
from raw_db.crm.accounts
where is_deleted = false;
```

---

## Snowflake-Only SQL Functions

### QUALIFY — filter window function results
```sql
-- Get the most recent record per account (replaces CTE + WHERE)
select *
from orders
qualify row_number() over (partition by account_id order by created_at desc) = 1;

-- Top 3 orders per customer by amount
select *
from orders
qualify rank() over (partition by customer_id order by amount desc) <= 3;
```

### FLATTEN — unnest arrays and objects
```sql
-- Expand a JSON array field
select
    o.order_id,
    f.value:product_id::varchar  as product_id,
    f.value:quantity::int        as quantity,
    f.value:price::number(10,2)  as unit_price
from orders o,
lateral flatten(input => o.line_items) f;

-- Flatten nested JSON
select
    account_id,
    f.key   as attribute_name,
    f.value as attribute_value
from accounts,
lateral flatten(input => metadata) f;
```

### PARSE_JSON, TRY_PARSE_JSON, GET_PATH
```sql
-- Safe JSON parsing (returns NULL on error instead of failing)
select try_parse_json(raw_json_string) as parsed;

-- Navigate nested JSON
select
    metadata:address:city::varchar   as city,
    metadata['address']['zipcode']   as zipcode,
    get_path(metadata, 'address.state') as state
from accounts;
```

### OBJECT_CONSTRUCT, ARRAY_AGG, ARRAY_CONSTRUCT
```sql
-- Build JSON objects dynamically
select object_construct(
    'id',   account_id,
    'name', account_name,
    'type', account_type
) as account_json
from accounts;

-- Aggregate rows into an array
select
    customer_id,
    array_agg(object_construct('order_id', order_id, 'amount', amount)) as orders
from orders
group by customer_id;
```

### MATCH_CONDITION (Snowflake ASOF JOIN)
```sql
-- Join on the closest timestamp (time-series alignment)
select
    trades.trade_id,
    trades.price,
    quotes.bid,
    quotes.ask
from trades
asof join quotes
    match_condition(trades.ts >= quotes.ts)
    on trades.symbol = quotes.symbol;
```

---

## Dynamic Tables

Dynamic tables are Snowflake's declarative streaming materialization — they auto-refresh based on source changes, no tasks or streams needed.

```sql
create or replace dynamic table analytics.marts.fct_orders
    target_lag = '5 minutes'
    warehouse = transform_wh
as
select
    o.order_id,
    o.customer_id,
    c.customer_name,
    o.amount,
    o.status,
    o.created_at
from raw_db.oms.orders o
join raw_db.crm.customers c on o.customer_id = c.customer_id
where o.is_test = false;
```

**When to use dynamic tables vs streams+tasks:**
- Dynamic table: you want Snowflake to manage refresh timing, no custom logic needed
- Streams+Tasks: you need custom processing logic, branching, external calls, or fine-grained control

**Inspect lag:**
```sql
show dynamic tables like 'fct_orders';
select * from information_schema.dynamic_table_refresh_history
where name = 'FCT_ORDERS';
```

---

## Streams (Change Data Capture)

Streams track inserts/updates/deletes on a table.

```sql
-- Create stream on a source table
create or replace stream raw_db.crm.accounts_stream
on table raw_db.crm.accounts
append_only = false;  -- tracks inserts + updates + deletes

-- Consume the stream (reads and advances the offset)
select
    account_id,
    account_name,
    metadata$action,          -- INSERT, DELETE
    metadata$isupdate,        -- true if this is the new row of an UPDATE
    metadata$row_id            -- stable row identifier
from raw_db.crm.accounts_stream
where metadata$action = 'INSERT' or metadata$isupdate = true;
```

**Merge from stream** (standard CDC pattern):
```sql
merge into analytics.marts.dim_accounts target
using (
    select * from raw_db.crm.accounts_stream
    qualify row_number() over (partition by account_id order by metadata$action desc) = 1
) source
on target.account_id = source.account_id
when matched and source.metadata$action = 'DELETE' then
    update set target.is_deleted = true, target.deleted_at = current_timestamp()
when matched then
    update set
        target.account_name = source.account_name,
        target.updated_at = current_timestamp()
when not matched then
    insert (account_id, account_name, created_at)
    values (source.account_id, source.account_name, current_timestamp());
```

---

## Tasks (Scheduled / Event-driven Execution)

```sql
-- Root task (scheduled)
create or replace task raw_db.public.process_accounts_task
    warehouse = transform_wh
    schedule = 'USING CRON 0 * * * * UTC'  -- hourly
as
merge into analytics.marts.dim_accounts target
using raw_db.crm.accounts_stream source
...;

-- Serverless task (Snowflake manages compute — no warehouse needed)
create or replace task raw_db.public.process_accounts_task
    user_task_managed_initial_warehouse_size = 'SMALL'
    schedule = '5 MINUTES'
as ...;

-- Child task (triggered by parent completion, builds a DAG)
create or replace task raw_db.public.aggregate_after_load_task
    after raw_db.public.process_accounts_task
as ...;

-- Control
alter task raw_db.public.process_accounts_task resume;   -- must resume to activate
alter task raw_db.public.process_accounts_task suspend;
execute task raw_db.public.process_accounts_task;         -- manual run
```

---

## Stages and File Formats

```sql
-- External stage (S3)
create or replace stage raw_db.public.s3_landing
    url = 's3://my-bucket/landing/'
    credentials = (aws_role = 'arn:aws:iam::123:role/snowflake-role')
    file_format = (type = 'PARQUET');

-- Internal named stage
create or replace stage raw_db.public.internal_stage
    file_format = (type = 'CSV' field_optionally_enclosed_by = '"' skip_header = 1);

-- File format object
create or replace file_format raw_db.public.csv_format
    type = 'CSV'
    field_delimiter = ','
    record_delimiter = '\n'
    skip_header = 1
    null_if = ('NULL', 'null', '')
    empty_field_as_null = true;

-- List files in stage
ls @raw_db.public.s3_landing;

-- COPY INTO table
copy into raw_db.crm.accounts_raw
from @raw_db.public.s3_landing/accounts/
file_format = (format_name = 'raw_db.public.csv_format')
on_error = 'CONTINUE'
purge = false;

-- Query stage directly (without loading)
select $1, $2, $3
from @raw_db.public.s3_landing/accounts/2024-01-01.csv
(file_format => 'raw_db.public.csv_format');
```

---

## Time Travel and Cloning

```sql
-- Query historical state
select * from accounts at (timestamp => '2024-01-15 10:00:00'::timestamp_ntz);
select * from accounts at (offset => -3600);      -- 1 hour ago
select * from accounts before (statement => '<query_id>');

-- Restore accidentally deleted rows
insert into accounts
select * from accounts before (statement => '<delete_query_id>')
minus
select * from accounts;

-- Undrop
undrop table accounts;
undrop schema raw;

-- Clone at a point in time
create table accounts_backup clone accounts
at (timestamp => '2024-01-15 10:00:00'::timestamp_ntz);
```

---

## Performance Patterns

### Clustering Keys
```sql
-- Cluster on the columns most used in WHERE and JOIN predicates
alter table fct_orders cluster by (date_trunc('day', created_at), account_id);

-- Check cluster depth (lower = better; > 1.2 triggers reclustering)
select system$clustering_depth('fct_orders', '(date_trunc(\'day\', created_at))');
select system$clustering_information('fct_orders');
```

### Search Optimization
```sql
-- For point lookups and substring searches on large tables
alter table customers add search optimization on equality(email), substring(account_name);
```

### Query Acceleration Service
```sql
-- Enable for long-running, scan-heavy queries
alter warehouse transform_wh set enable_query_acceleration = true
    query_acceleration_max_scale_factor = 8;
```

### Result Cache
```sql
-- Snowflake caches results for 24h; disable for benchmarking
alter session set use_cached_result = false;
```

---

## Data Vault Patterns in Snowflake

```sql
-- Hub (unique business keys)
create table dv_raw.hub_customer (
    h_customer_hk   binary(20) not null,           -- SHA1 hash of business key
    customer_id     varchar(36) not null,
    load_dts        timestamp_ntz not null,
    rec_src         varchar(100) not null,
    constraint pk_hub_customer primary key (h_customer_hk)
);

-- Satellite (descriptive attributes with history)
create table dv_raw.sat_customer_crm (
    h_customer_hk   binary(20) not null,
    load_dts        timestamp_ntz not null,
    load_end_dts    timestamp_ntz,
    rec_src         varchar(100) not null,
    hash_diff       binary(20) not null,           -- hash of all attribute values
    customer_name   varchar(255),
    email           varchar(255),
    constraint pk_sat_customer_crm primary key (h_customer_hk, load_dts)
);

-- Link (relationships)
create table dv_raw.lnk_order_customer (
    l_order_customer_hk  binary(20) not null,
    h_order_hk           binary(20) not null,
    h_customer_hk        binary(20) not null,
    load_dts             timestamp_ntz not null,
    rec_src              varchar(100) not null
);
```

---

## Snowpark (Python in Snowflake)

```python
# Snowpark DataFrame API — runs SQL pushed down to Snowflake
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, lit, when, sum as snow_sum

session = Session.builder.configs({
    "account": "my-account",
    "user": "my-user",
    "password": "...",
    "database": "RAW_DB",
    "schema": "CRM",
    "warehouse": "TRANSFORM_WH",
}).create()

# Read
df = session.table("accounts")

# Transform
result = (
    df.filter(col("is_active") == lit(True))
    .with_column("full_name", col("first_name") + lit(" ") + col("last_name"))
    .group_by("account_type")
    .agg(snow_sum("amount").alias("total_amount"))
)

# Write
result.write.save_as_table("analytics.marts.account_summary", mode="overwrite")
```

---

## Useful System Queries

```sql
-- Query history (last hour)
select query_text, execution_time / 1000 as seconds, bytes_scanned / 1e9 as gb_scanned
from table(information_schema.query_history(
    dateadd('hour', -1, current_timestamp()), current_timestamp()
))
where execution_status = 'SUCCESS'
order by execution_time desc
limit 20;

-- Warehouse credit usage
select warehouse_name, sum(credits_used) as total_credits
from table(information_schema.warehouse_metering_history(
    dateadd('day', -7, current_timestamp()), current_timestamp()
))
group by 1 order by 2 desc;

-- Table storage
select table_catalog, table_schema, table_name,
    round(active_bytes / 1e9, 2) as active_gb,
    round(time_travel_bytes / 1e9, 2) as time_travel_gb
from information_schema.table_storage_metrics
order by active_bytes desc;

-- Long-running active queries
select query_id, user_name, execution_time / 1000 as seconds, query_text
from table(information_schema.query_history_by_session())
where execution_status = 'RUNNING'
order by execution_time desc;
```
