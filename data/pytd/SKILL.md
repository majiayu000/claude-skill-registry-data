---
name: pytd
description: Expert assistance for using pytd (Python SDK) to query and import data with Treasure Data. Use this skill when users need help with Python-based data analysis, querying Presto/Hive, importing pandas DataFrames, bulk data uploads, or integrating TD with Python analytical workflows.
---

# pytd - Treasure Data Python SDK

Expert assistance for querying and importing data to Treasure Data using pytd, the official Python driver for analytical workflows.

## When to Use This Skill

Use this skill when:
- Querying Treasure Data from Python scripts or Jupyter notebooks
- Importing pandas DataFrames to TD tables
- Running Presto or Hive queries from Python
- Building data pipelines with Python and TD
- Performing bulk data imports or exports
- Migrating from deprecated pandas-td library
- Integrating TD with Python data science workflows
- Handling large result sets with iterative retrieval

## Core Principles

### 1. Installation

**Standard Installation:**
```bash
pip install pytd
```

**Requirements:**
- Python 3.9 or later
- pandas 2.0 or later

### 2. Authentication & Configuration

**Environment Variables (Recommended):**
```bash
export TD_API_KEY="your_api_key_here"
export TD_API_SERVER="https://api.treasuredata.com/"
```

**Client Initialization:**
```python
import pytd

# Using environment variables
client = pytd.Client(database='sample_datasets')

# Explicit credentials (not recommended for production)
client = pytd.Client(
    apikey='your_api_key',
    endpoint='https://api.treasuredata.com/',
    database='your_database',
    default_engine='presto'  # or 'hive'
)
```

**Configuration Options:**
- `apikey`: TD API key (read from `TD_API_KEY` env var if not specified)
- `endpoint`: TD API server URL (read from `TD_API_SERVER` env var)
- `database`: Default database name for queries
- `default_engine`: Query engine - `'presto'` (default) or `'hive'`

**Regional Endpoints:**
- US: `https://api.treasuredata.com/`
- Tokyo: `https://api.treasuredata.co.jp/`
- EU: `https://api.eu01.treasuredata.com/`

### 3. Querying Data

#### Basic Query Execution

```python
import pytd

client = pytd.Client(database='sample_datasets')

# Execute Presto query
result = client.query('SELECT symbol, COUNT(1) as cnt FROM nasdaq GROUP BY symbol LIMIT 10')

# Result format: {'columns': ['symbol', 'cnt'], 'data': [['AAIT', 590], ['AAL', 82], ...]}
print(result['columns'])  # ['symbol', 'cnt']
print(result['data'])     # [['AAIT', 590], ['AAL', 82], ...]
```

#### Query with Hive Engine

```python
# Create Hive client
client_hive = pytd.Client(
    database='sample_datasets',
    default_engine='hive'
)

# Execute Hive query
result = client_hive.query('SELECT hivemall_version()')
```

#### Convert Results to pandas DataFrame

```python
import pandas as pd

result = client.query('SELECT * FROM nasdaq LIMIT 100')

# Convert to DataFrame
df = pd.DataFrame(result['data'], columns=result['columns'])
print(df.head())
```

### 4. Writing Data to TD

#### Load DataFrame to Table

```python
import pandas as pd
import pytd

# Create sample DataFrame
df = pd.DataFrame({
    'user_id': [1, 2, 3, 4],
    'event_name': ['login', 'purchase', 'logout', 'login'],
    'amount': [None, 99.99, None, None],
    'timestamp': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-02', '2024-01-03'])
})

# Initialize client
client = pytd.Client(database='your_database')

# Upload DataFrame
client.load_table_from_dataframe(
    df,
    'events',  # table name
    writer='bulk_import',  # writer type
    if_exists='overwrite'  # or 'append', 'error', 'ignore'
)
```

**Parameters:**
- `df`: pandas DataFrame to upload
- `table`: Target table name (can be `'database.table'` or just `'table'`)
- `writer`: Import method - `'bulk_import'` (default), `'insert_into'`, or `'spark'`
- `if_exists`: What to do if table exists - `'error'` (default), `'overwrite'`, `'append'`, or `'ignore'`

## Common Patterns

### Pattern 1: ETL Pipeline - Query, Transform, Load

```python
import pytd
import pandas as pd

# Initialize client
client = pytd.Client(database='analytics')

# Step 1: Extract - Query data from TD
query = """
    SELECT
        user_id,
        event_name,
        event_date,
        COUNT(*) as event_count
    FROM raw_events
    WHERE TD_INTERVAL(time, '-1d', 'JST')
    GROUP BY user_id, event_name, event_date
"""

result = client.query(query)
df = pd.DataFrame(result['data'], columns=result['columns'])

# Step 2: Transform - Process data with pandas
df['event_date'] = pd.to_datetime(df['event_date'])
df['is_weekend'] = df['event_date'].dt.dayofweek >= 5
df['event_count_log'] = df['event_count'].apply(lambda x: pd.np.log1p(x))

# Add metadata
df['processed_at'] = pd.Timestamp.now()
df['pipeline_version'] = '1.0'

# Step 3: Load - Write back to TD
client.load_table_from_dataframe(
    df,
    'analytics.user_daily_events',
    writer='bulk_import',
    if_exists='append'
)

print(f"Loaded {len(df)} rows to user_daily_events")
```

**Explanation:** Complete ETL workflow that extracts yesterday's data, performs pandas transformations, and loads results back to TD. Uses bulk_import for efficient loading.

### Pattern 2: Incremental Data Loading

```python
import pytd
import pandas as pd
from datetime import datetime, timedelta

client = pytd.Client(database='sales')

def load_incremental_data(source_file, table_name, date_column='import_date'):
    """Load new data incrementally, avoiding duplicates"""

    # Read new data from source
    new_data = pd.read_csv(source_file)
    new_data[date_column] = datetime.now()

    # Get max date from existing table
    try:
        result = client.query(f"""
            SELECT MAX({date_column}) as max_date
            FROM {table_name}
        """)

        max_date = result['data'][0][0] if result['data'][0][0] else None

        if max_date:
            # Filter only new records
            new_data = new_data[new_data[date_column] > max_date]
            print(f"Loading {len(new_data)} new records after {max_date}")
        else:
            print(f"Table empty, loading all {len(new_data)} records")

    except Exception as e:
        # Table doesn't exist yet
        print(f"Creating new table with {len(new_data)} records")

    if len(new_data) > 0:
        client.load_table_from_dataframe(
            new_data,
            table_name,
            writer='bulk_import',
            if_exists='append'
        )
        print("Load complete")
    else:
        print("No new data to load")

# Usage
load_incremental_data('daily_sales.csv', 'sales.transactions')
```

**Explanation:** Implements incremental loading by checking the latest timestamp in the target table and only loading newer records. Handles first-time loads gracefully.

### Pattern 3: Large Result Set Processing with DB-API

```python
import pytd
from pytd.dbapi import connect

client = pytd.Client(database='large_dataset')

# Create DB-API connection
conn = connect(client)
cursor = conn.cursor()

# Execute query that might timeout with standard query()
cursor.execute("""
    SELECT user_id, event_name, event_time, properties
    FROM events
    WHERE TD_INTERVAL(time, '-7d', 'JST')
""")

# Process results iteratively (memory efficient)
batch_size = 10000
processed_count = 0

while True:
    rows = cursor.fetchmany(batch_size)
    if not rows:
        break

    # Process batch
    for row in rows:
        user_id, event_name, event_time, properties = row
        # Process each row
        process_event(user_id, event_name, event_time, properties)

    processed_count += len(rows)
    print(f"Processed {processed_count} rows...")

cursor.close()
conn.close()

print(f"Total processed: {processed_count} rows")
```

**Explanation:** Uses DB-API for iterative retrieval of large result sets. Prevents memory issues and query timeouts by fetching data in batches. Essential for processing millions of rows.

### Pattern 4: Multi-Database Operations

```python
import pytd
import pandas as pd

# Connect to different databases
source_client = pytd.Client(database='raw_data')
target_client = pytd.Client(database='analytics')

# Query from source database
query = """
    SELECT
        customer_id,
        product_id,
        purchase_date,
        amount
    FROM purchases
    WHERE TD_INTERVAL(time, '-1d', 'JST')
"""

result = source_client.query(query)
df = pd.DataFrame(result['data'], columns=result['columns'])

# Enrich data by querying another source
product_query = "SELECT product_id, product_name, category FROM products"
products_result = source_client.query(product_query)
products_df = pd.DataFrame(products_result['data'], columns=products_result['columns'])

# Join data
enriched_df = df.merge(products_df, on='product_id', how='left')

# Calculate metrics
daily_summary = enriched_df.groupby(['category', 'purchase_date']).agg({
    'amount': ['sum', 'mean', 'count'],
    'customer_id': 'nunique'
}).reset_index()

daily_summary.columns = ['category', 'date', 'total_sales', 'avg_sale', 'transaction_count', 'unique_customers']

# Write to analytics database
target_client.load_table_from_dataframe(
    daily_summary,
    'daily_category_sales',
    writer='bulk_import',
    if_exists='append'
)

print(f"Loaded {len(daily_summary)} rows to analytics.daily_category_sales")
```

**Explanation:** Demonstrates working with multiple databases, joining data, performing aggregations, and writing to a different target database.

### Pattern 5: Handling Time-based Data with TD Functions

```python
import pytd
import pandas as pd
from datetime import datetime

client = pytd.Client(database='events')

# Query with TD time functions
query = """
    SELECT
        TD_TIME_FORMAT(time, 'yyyy-MM-dd', 'JST') as date_jst,
        COUNT(*) as event_count,
        COUNT(DISTINCT user_id) as unique_users,
        APPROX_PERCENTILE(session_duration, 0.5) as median_duration,
        APPROX_PERCENTILE(session_duration, 0.95) as p95_duration
    FROM user_sessions
    WHERE TD_INTERVAL(time, '-7d', 'JST')
    GROUP BY 1
    ORDER BY 1 DESC
"""

result = client.query(query)
df = pd.DataFrame(result['data'], columns=result['columns'])

# Convert date strings to datetime
df['date_jst'] = pd.to_datetime(df['date_jst'])

# Add derived metrics
df['events_per_user'] = df['event_count'] / df['unique_users']

# Write summary back
client.load_table_from_dataframe(
    df,
    'weekly_session_summary',
    writer='bulk_import',
    if_exists='overwrite'
)
```

**Explanation:** Shows proper use of TD time functions (TD_INTERVAL, TD_TIME_FORMAT) in queries and how to handle the results in pandas.

## Writer Types Comparison

pytd supports three writer methods for loading data:

### 1. bulk_import (Default - Recommended)

**Best for:** Most use cases, especially large datasets

```python
client.load_table_from_dataframe(
    df,
    'table_name',
    writer='bulk_import',
    if_exists='append'
)
```

**Characteristics:**
- ✓ Scalable to large datasets
- ✓ Memory efficient (streams data)
- ✓ No special permissions required
- ✓ Best balance of performance and simplicity
- ✗ Slower than Spark for very large datasets
- Uses CSV format internally

**When to use:** Default choice for most data loads (100s of MB to GBs)

### 2. insert_into

**Best for:** Small datasets, real-time updates

```python
client.load_table_from_dataframe(
    df,
    'table_name',
    writer='insert_into',
    if_exists='append'
)
```

**Characteristics:**
- ✓ Simple, no dependencies
- ✓ Good for small datasets (<1000 rows)
- ✗ Not scalable (issues individual INSERT queries)
- ✗ Slow for large datasets
- ✗ Uses Presto query capacity
- Uses Presto INSERT INTO statements

**When to use:** Only for small datasets or when you need immediate writes without bulk import delay

### 3. spark (High Performance)

**Best for:** Very large datasets, high-performance pipelines

```python
from pytd.writer import SparkWriter

writer = SparkWriter(
    td_spark_path='/path/to/td-spark-assembly.jar'  # Optional
)

client.load_table_from_dataframe(
    df,
    'table_name',
    writer=writer,
    if_exists='append'
)
```

**Characteristics:**
- ✓ Highest performance
- ✓ Direct writes to Plazma storage
- ✓ Best for very large datasets (10s of GBs+)
- ✗ Requires `pytd[spark]` installation
- ✗ Requires Plazma Public API access (contact support)
- ✗ Additional dependencies

**When to use:** Large-scale data pipelines requiring maximum throughput

**Enabling Spark Writer:**
1. Install: `pip install pytd[spark]`
2. Contact `support@treasuredata.com` to enable Plazma Public API access
3. (Optional) Download td-spark JAR for custom versions

## Best Practices

1. **Use Environment Variables for Credentials**
   ```bash
   export TD_API_KEY="your_api_key"
   export TD_API_SERVER="https://api.treasuredata.com/"
   ```
   Never hardcode API keys in scripts

2. **Choose the Right Writer**
   - `bulk_import`: Default choice for most scenarios
   - `insert_into`: Only for small datasets (<1000 rows)
   - `spark`: For very large datasets with proper setup

3. **Use TD Time Functions in Queries**
   ```python
   # Good: Uses partition pruning
   query = "SELECT * FROM table WHERE TD_INTERVAL(time, '-1d', 'JST')"

   # Avoid: Scans entire table
   query = "SELECT * FROM table WHERE date = '2024-01-01'"
   ```

4. **Handle Large Results with DB-API**
   Use `pytd.dbapi` for queries returning millions of rows to avoid memory issues

5. **Specify Database in Table Name**
   ```python
   # Explicit database (recommended)
   client.load_table_from_dataframe(df, 'database.table')

   # Uses client's default database
   client.load_table_from_dataframe(df, 'table')
   ```

6. **Add Time Column for Partitioning**
   ```python
   df['time'] = pd.to_datetime(df['timestamp']).astype(int) // 10**9
   client.load_table_from_dataframe(df, 'table')
   ```

7. **Use Presto for Analytics, Hive for Special Functions**
   - Presto: Faster for most analytical queries
   - Hive: Required for Hivemall, UDFs, some advanced features

8. **Batch Processing for Large ETL**
   Process data in chunks to avoid memory issues:
   ```python
   for chunk in pd.read_csv('large_file.csv', chunksize=100000):
       # Process chunk
       client.load_table_from_dataframe(chunk, 'table', if_exists='append')
   ```

9. **Error Handling**
   ```python
   try:
       result = client.query(query)
   except Exception as e:
       print(f"Query failed: {e}")
       # Handle error appropriately
   ```

10. **Close Connections in Long-Running Scripts**
    ```python
    from pytd.dbapi import connect

    conn = connect(client)
    try:
        # Use connection
        cursor = conn.cursor()
        cursor.execute(query)
        # Process results
    finally:
        conn.close()
    ```

## Common Issues and Solutions

### Issue: Import Errors or Module Not Found

**Symptoms:**
- `ModuleNotFoundError: No module named 'pytd'`
- `ImportError: cannot import name 'SparkWriter'`

**Solutions:**
1. **Verify Installation**
   ```bash
   pip list | grep pytd
   ```

2. **Install/Upgrade pytd**
   ```bash
   pip install --upgrade pytd
   ```

3. **For Spark Support**
   ```bash
   pip install pytd[spark]
   ```

4. **Check Python Version**
   ```bash
   python --version  # Should be 3.9+
   ```

### Issue: Authentication Errors

**Symptoms:**
- `Unauthorized: Invalid API key`
- `403 Forbidden`

**Solutions:**
1. **Verify Environment Variables**
   ```bash
   echo $TD_API_KEY
   echo $TD_API_SERVER
   ```

2. **Check API Key Format**
   ```python
   # Verify API key is set correctly
   import os
   print(os.getenv('TD_API_KEY'))
   ```

3. **Verify Regional Endpoint**
   ```python
   # US
   endpoint = 'https://api.treasuredata.com/'
   # Tokyo
   endpoint = 'https://api.treasuredata.co.jp/'
   # EU
   endpoint = 'https://api.eu01.treasuredata.com/'
   ```

4. **Check API Key Permissions**
   - Ensure key has appropriate read/write permissions
   - Regenerate key if necessary from TD console

### Issue: Query Timeout or Memory Errors

**Symptoms:**
- Query times out after several minutes
- `MemoryError` when fetching large results
- Connection drops during query execution

**Solutions:**
1. **Use DB-API for Large Results**
   ```python
   from pytd.dbapi import connect

   conn = connect(client)
   cursor = conn.cursor()
   cursor.execute(query)

   # Fetch in batches
   for row in cursor.fetchmany(10000):
       process(row)
   ```

2. **Add Time Filters for Partition Pruning**
   ```python
   query = """
       SELECT * FROM large_table
       WHERE TD_INTERVAL(time, '-1d', 'JST')  -- Add this!
   """
   ```

3. **Limit Result Size**
   ```python
   query = "SELECT * FROM table WHERE ... LIMIT 100000"
   ```

4. **Use Aggregations Instead of Raw Data**
   ```python
   # Instead of fetching all rows
   query = "SELECT * FROM table"

   # Aggregate first
   query = """
       SELECT date, user_id, COUNT(*) as cnt
       FROM table
       GROUP BY 1, 2
   """
   ```

### Issue: DataFrame Upload Fails

**Symptoms:**
- `ValueError: DataFrame is empty`
- Type errors during upload
- Data corruption in uploaded table

**Solutions:**
1. **Check DataFrame is Not Empty**
   ```python
   if df.empty:
       print("DataFrame is empty, skipping upload")
   else:
       client.load_table_from_dataframe(df, 'table')
   ```

2. **Handle Data Types Properly**
   ```python
   # Convert timestamps to Unix epoch
   df['time'] = pd.to_datetime(df['timestamp']).astype(int) // 10**9

   # Handle NaN values
   df['amount'] = df['amount'].fillna(0)

   # Convert to appropriate types
   df['user_id'] = df['user_id'].astype(str)
   df['count'] = df['count'].astype(int)
   ```

3. **Check Column Names**
   ```python
   # TD column names should be lowercase and use underscores
   df.columns = df.columns.str.lower().str.replace(' ', '_')
   ```

4. **Remove Invalid Characters**
   ```python
   # Remove or replace problematic characters
   df = df.applymap(lambda x: str(x).replace('\x00', '') if isinstance(x, str) else x)
   ```

5. **Try Different Writer**
   ```python
   # If bulk_import fails, try insert_into for debugging
   client.load_table_from_dataframe(
       df.head(10),  # Test with small sample
       'table',
       writer='insert_into'
   )
   ```

### Issue: Spark Writer Not Working

**Symptoms:**
- `ImportError: Spark writer not available`
- Spark job fails
- Permission denied errors

**Solutions:**
1. **Install Spark Dependencies**
   ```bash
   pip install pytd[spark]
   ```

2. **Enable Plazma Public API**
   - Contact `support@treasuredata.com`
   - Request Plazma Public API access for your account

3. **Specify JAR Path (if needed)**
   ```python
   from pytd.writer import SparkWriter

   writer = SparkWriter(
       td_spark_path='/path/to/td-spark-assembly.jar'
   )
   ```

4. **Check Permissions**
   - Ensure API key has write access to target database
   - Verify Plazma access is enabled

## Advanced Topics

### Custom Query Options

```python
# Query with custom parameters
result = client.query(
    'SELECT * FROM table',
    engine='presto',
    priority=1,  # Higher priority (1-2, default 0)
    retry_limit=3
)
```

### Working with Job Status

```python
# Start query asynchronously
job = client.query('SELECT COUNT(*) FROM large_table', wait=False)

# Check job status
print(f"Job ID: {job.job_id}")
print(f"Status: {job.status()}")

# Wait for completion
job.wait()

# Get results
if job.success():
    result = job.result()
else:
    print(f"Job failed: {job.error()}")
```

### Custom Writers

```python
from pytd.writer import BulkImportWriter

# Configure writer with custom options
writer = BulkImportWriter(
    chunk_size=10000,  # Rows per chunk
    time_column='time'  # Specify time column
)

client.load_table_from_dataframe(
    df,
    'table',
    writer=writer,
    if_exists='append'
)
```

### Migrating from pandas-td

If you have existing code using the deprecated `pandas-td` library:

**Before (pandas-td):**
```python
import pandas_td as td

con = td.connect(apikey='your_api_key', endpoint='https://api.treasuredata.com/')
df = td.read_td('SELECT * FROM sample_datasets.nasdaq', con)
```

**After (pytd):**
```python
import pytd.pandas_td as td

con = td.connect(apikey='your_api_key', endpoint='https://api.treasuredata.com/')
df = td.read_td('SELECT * FROM sample_datasets.nasdaq', con)
```

Or use the modern pytd API:
```python
import pytd
import pandas as pd

client = pytd.Client(database='sample_datasets')
result = client.query('SELECT * FROM nasdaq')
df = pd.DataFrame(result['data'], columns=result['columns'])
```

## Testing and Development

### Test Connection

```python
import pytd

try:
    client = pytd.Client(database='sample_datasets')
    result = client.query('SELECT 1 as test')
    print("Connection successful!")
    print(result)
except Exception as e:
    print(f"Connection failed: {e}")
```

### Verify Data Upload

```python
import pandas as pd
import pytd

# Create test data
test_df = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'value': [100, 200, 300],
    'time': [1704067200, 1704153600, 1704240000]  # Unix timestamps
})

client = pytd.Client(database='test_db')

# Upload
print("Uploading test data...")
client.load_table_from_dataframe(
    test_df,
    'test_table',
    writer='bulk_import',
    if_exists='overwrite'
)

# Verify
print("Verifying upload...")
result = client.query('SELECT * FROM test_table ORDER BY id')
verify_df = pd.DataFrame(result['data'], columns=result['columns'])

print("\nUploaded data:")
print(verify_df)

# Check counts match
assert len(test_df) == len(verify_df), "Row count mismatch!"
print("\nVerification successful!")
```

### Performance Testing

```python
import pytd
import pandas as pd
import time

client = pytd.Client(database='test_db')

# Generate test data
df = pd.DataFrame({
    'id': range(100000),
    'value': range(100000),
    'time': int(time.time())
})

# Test bulk_import
start = time.time()
client.load_table_from_dataframe(df, 'perf_test_bulk', writer='bulk_import', if_exists='overwrite')
bulk_time = time.time() - start
print(f"bulk_import: {bulk_time:.2f}s for {len(df)} rows")

# Test insert_into (small sample only!)
small_df = df.head(100)
start = time.time()
client.load_table_from_dataframe(small_df, 'perf_test_insert', writer='insert_into', if_exists='overwrite')
insert_time = time.time() - start
print(f"insert_into: {insert_time:.2f}s for {len(small_df)} rows")
```

## Jupyter Notebook Integration

pytd works seamlessly with Jupyter notebooks:

```python
# Notebook cell 1: Setup
import pytd
import pandas as pd
import matplotlib.pyplot as plt

client = pytd.Client(database='analytics')

# Notebook cell 2: Query data
query = """
    SELECT
        TD_TIME_FORMAT(time, 'yyyy-MM-dd', 'JST') as date,
        COUNT(*) as events
    FROM user_events
    WHERE TD_INTERVAL(time, '-30d', 'JST')
    GROUP BY 1
    ORDER BY 1
"""

result = client.query(query)
df = pd.DataFrame(result['data'], columns=result['columns'])
df['date'] = pd.to_datetime(df['date'])

# Notebook cell 3: Visualize
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['events'])
plt.title('Daily Events - Last 30 Days')
plt.xlabel('Date')
plt.ylabel('Event Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Notebook cell 4: Write results back
summary = df.describe()
# Process and save summary back to TD if needed
```

## Resources

- **Documentation**: https://pytd-doc.readthedocs.io/
- **GitHub Repository**: https://github.com/treasure-data/pytd
- **PyPI Package**: https://pypi.org/project/pytd/
- **TD Python Guide**: https://docs.treasuredata.com/
- **Example Notebooks**: See GitHub repository for Google Colab examples

## Related Skills

- **trino**: Understanding Trino SQL syntax for queries in pytd
- **hive**: Using Hive-specific functions and syntax
- **digdag**: Orchestrating Python scripts using pytd in workflows
- **td-javascript-sdk**: Browser-based data collection (frontend) vs pytd (backend/analytics)

## Comparison with Other Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| **pytd** | Full-featured Python driver | Analytics, data pipelines, pandas integration |
| **td-client-python** | Basic REST API wrapper | Simple CRUD, when pytd is too heavy |
| **pandas-td** (deprecated) | Legacy pandas integration | Don't use - migrate to pytd |
| **TD Toolbelt** | CLI tool | Command-line operations, shell scripts |

**Recommendation:** Use pytd for all Python-based analytical work and ETL pipelines. Use td-client-python only for basic REST API operations.

---

*Last updated: 2025-01 | pytd version: Latest (Python 3.9+)*
