---
name: processing-data
description: Processes CSV files and pandas DataFrames. Use when working with CSV files, tabular data, spreadsheets, or when the user asks to query, analyze, or manipulate structured data.
---

# Data Processing Tools

Tools for working with CSV files and pandas DataFrames.

## CSV Operations

### List available CSV files

```python
result = await list_csv_files()
# Returns: {"success": True, "data": ["file1", "file2"], "count": 2}
```

### Read CSV content

```python
result = await read_csv_file("mydata", row_limit=100)
# Returns rows as list of dicts
```

### Query with SQL (DuckDB)

```python
result = await query_csv_file("mydata", "SELECT * FROM mydata WHERE value > 10")
```

**Security**: Only SELECT queries allowed. INSERT, UPDATE, DELETE rejected.

### Add/remove CSV files

```python
await add_csv_file("/path/to/file.csv")
await remove_csv_file("filename")
```

## Pandas Operations

### Create DataFrame

```python
# From CSV
result = await create_pandas_dataframe(
    dataframe_name="sales",
    create_using_function="read_csv",
    function_parameters={"filepath_or_buffer": "data.csv"}
)

# From dict
result = await create_pandas_dataframe(
    dataframe_name="mydf",
    create_using_function="DataFrame",
    function_parameters={"data": {"col1": [1, 2], "col2": [3, 4]}}
)
```

**Allowed functions**: DataFrame, read_csv, read_json, read_excel, read_parquet, read_feather, read_orc, read_html, read_xml, read_table, read_sql.

### Run operations

```python
# Get first rows
result = await run_dataframe_operation("sales", "head", {"n": 5})

# Filter data
result = await run_dataframe_operation("sales", "query", {"expr": "amount > 100"})

# Get statistics
result = await run_dataframe_operation("sales", "describe", {})
```

**Allowed operations**: head, tail, describe, query, filter, groupby, sort_values, mean, sum, count, and 100+ more safe operations.

### Export DataFrame

```python
result = await export_dataframe(
    dataframe_name="sales",
    export_function="to_csv",
    export_parameters={"path_or_buf": "output.csv", "index": False}
)
```

### Manage DataFrames

```python
await list_dataframes()           # List all in memory
await get_dataframe_info("sales") # Get details
await delete_dataframe("sales")   # Remove from memory
```

## Security Notes

- CSV queries: Only SELECT statements allowed
- Pandas: Operations restricted to allowlist of safe methods
- No arbitrary code execution via getattr
