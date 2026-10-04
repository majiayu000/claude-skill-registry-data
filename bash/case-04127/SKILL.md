---
name: data-vault
version: 1.0.18
description: "Persist and retrieve structured data using the Lance columnar format. Use when you need to store, query, or analyze data across sessions — such as saving skill outputs, tracking conversation context, storing research data, or building knowledge bases. After installing the requirements it's ready to use. Triggers on: 'store this data', 'save to persistant storage', 'persist information', 'remember this', 'store for later', 'query my data', 'analyze stored data', 'persist data'."
author: Vitor Hugo Zeferino
metadata:
    openclaw:
        requires:
            bins:
                - python3
                # declare uv and pip as required binaries
                - uv
                - pip
        install:
            # Bootstrap pip if missing
            - kind: "shell"
              cmd: "python3 -m ensurepip --upgrade || true"
              label: "Ensure pip is installed"

            # Bootstrap uv if missing
            - kind: "shell"
              cmd: "pip install --upgrade uv || true"
              label: "Install uv if missing"

            # Install pylance
            - kind: "uv"
              type: "pip"
              package: "pylance"
              label: "Install pylance (Lance columnar format) via uv"

            # Install pandas
            - kind: "uv"
              type: "pip"
              package: "pandas"
              label: "Install pandas via uv"
---

## Image Handling

This skill encodes images as base64 for inline embedding:

```python
import base64
from pathlib import Path

def encode_image(path: str) -> str:
    """Encode image to base64 for API submission."""
    data = Path(path).read_bytes()
    return base64.b64encode(data).decode('utf-8')

def decode_response(b64_str: str) -> bytes:
    """Decode base64 response back to binary."""
    return base64.b64decode(b64_str)
```

Base64 encoding is used exclusively for image data transfer, not for code obfuscation.

# Data Vault

## Installation

```bash
uv pip install pylance pandas
```

A persistent data store using the Lance columnar format for fast ML data access.

## Quick Start

```bash
# List all datasets and their metadata
python3 scripts/command.py list-datasets-info

# Create a dataset
python3 scripts/command.py create-dataset <name> <field1> <field2> ...

# Append data
python3 scripts/command.py append-to-dataset <name> <value1> <value2> ...

# Read all records from a dataset
python3 scripts/command.py read-dataset <name>
```

**Note:** `list-datasets-info` shows dataset metadata (schema, field types, record count) — it does not return the actual data rows. Use `read-dataset` to retrieve records.

## Storage Location

DataSets are created and stored on the current path '.'

## Critical Behavior: Data Type Strictness

⚠️ **Lance is strict about data types — they CANNOT change after the first record**

When you append the first record to a dataset, Lance infers the data type for each field. **All subsequent records MUST use the same types.**

**Example — this FAILS:**

```
# First record: age as STRING
append-to-dataset users "John" "25" "john@test.com"

# Second record: age as INTEGER (will FAIL!)
append-to-dataset users "Jane" 30 "jane@test.com"
# Error: `age` should have type large_string but type was int64
```

**Correct approach — maintain consistent types:**

```
# First record: age as STRING
append-to-dataset users "John" "25" "john@test.com"

# Second record: age as STRING
append-to-dataset users "Jane" "30" "jane@test.com"
```

### Why This Matters

Unlike traditional databases that may coerce types, Lance rejects type mismatches. If you store numbers as strings initially, you must always pass strings. Plan your schema carefully.

## Initialization Workflow

When starting a session, **always initialize by listing existing datasets first**:

```bash
# This command returns ALL datasets with their structure
python3 scripts/command.py list-datasets-info
```

Example output:

```json
{
    "skill": "data-vault",
    "operation": "list_datasets_info",
    "status": "success",
    "data": [
        {
            "dataset_name": "users",
            "path": "/data/users",
            "fields": ["name", "age", "email"],
            "field_types": {
                "_id": "large_string",
                "_updated_at": "timestamp[us]",
                "name": "large_string",
                "age": "large_string",
                "email": "large_string"
            },
            "record_count": 2,
            "columns": ["id", "_updated_at", "name", "age", "email"],
            "last_updated": "2026-03-21T17:57:44.595628"
        }
    ],
    "error": null
}
```

### Understanding `field_types`

| State        | Meaning                                                       |
| ------------ | ------------------------------------------------------------- |
| `{}` (empty) | Dataset exists but no records yet — **types not yet defined** |
| populated    | Types are locked — appends must match                         |

**Important:** If `field_types` is empty, the first append will define types. Be deliberate about the first record's types.

## Commands Reference

### Create Dataset

```bash
python3 scripts/command.py create-dataset <name> <field1> <field2> ...
```

Creates a metadata entry. Fields have no types until first append.

### Append Record

```bash
python3 scripts/command.py append-to-dataset <name> <value1> <value2> ...
```

Appends one record. Types are inferred from first record.

### Batch Append

```bash
python3 scripts/command.py batch-append-to-dataset <name> '<json-array>'
```

Example: `batch-append-to-dataset users '[["Alice", "22", "alice@test.com"], ["Bob", "35", "bob@test.com"]]'`

### Update Record

```bash
python3 scripts/command.py update-dataset-record <name> <record_id> <value1> <value2> ...
```

Updates fields for a specific record by ID.

### Delete Record

```bash
python3 scripts/command.py delete-dataset-record <name> <record_id>
```

### List All Datasets

```bash
python3 scripts/command.py list-datasets
```

### Get Dataset Info

```bash
python3 scripts/command.py get-dataset-info <name>
```

Returns schema, field types (if data exists), and record count.

### List All Datasets with Full Info

```bash
python3 scripts/command.py list-datasets-info
```

**Recommended for initialization.** Returns all datasets with complete metadata.

### Get Dataset Path

```bash
python3 scripts/command.py get-dataset-path-info <name>
```

### Backup Dataset

```bash
python3 scripts/command.py backup-dataset <name> <backup_path>
```

### Count Records

```bash
python3 scripts/command.py count-records <name>
```

### Read All Records

Returns all records from the dataset as a list of objects.

```bash
python3 scripts/command.py read-dataset <name>
```

### Drop Dataset

# Requires confirmation if have not created a backup beforehand.

Delete the entire dataset and its metadata.

```bash
python3 scripts/command.py drop-dataset <name>
```

**Internal fields available in every dataset:**

| Field         | Type      | Description                                  |
| ------------- | --------- | -------------------------------------------- |
| `_id`         | string    | UUID — unique record identifier              |
| `_updated_at` | timestamp | When the record was last inserted or updated |

### List Records (Paginated)

```bash
python3 scripts/command.py list-records <name> --limit 10 --offset 0
```

Returns records with optional pagination.

### Get Single Record

```bash
python3 scripts/command.py get-record <name> <record_id>
```

Retrieves a specific record by its UUID.

### Get Dataset Info

```bash
python3 scripts/command.py get-dataset-info <name>
```

Returns schema, field types (if data exists), and record count.

## Response Format

All commands return JSON:

```json
{
  "skill": "data-vault",
  "operation": "<operation_name>",
  "status": "success|error",
  "data": <result_data_or_null>,
  "error": <error_message_or_null>
}
```

## Internal Fields

Every dataset automatically includes:

- `_id` — UUID for each record
- `_updated_at` — timestamp of last insert/update

These are managed automatically — when appending, only provide your defined fields.

## Data Type Inference

Lance infers types from the first record:

| Python Type    | Lance Type     |
| -------------- | -------------- |
| `"string"`     | `large_string` |
| `25` (int)     | `int64`        |
| `25.5` (float) | `float64`      |
| `True`/`False` | `bool`         |

**CLI caveat:** When passing via command line, all values are strings. To ensure integer types, initialize with actual integers in a script rather than CLI.

## Tips

1. **Initialize at session start:** Run `list-datasets-info` to understand what data already exists
2. **Plan your schema:** First record determines types for the entire dataset
3. **Use batch append when adding multiple records:** More efficient than individual appends

## Requirements

Dependencies are declared in frontmatter (`metadata.openclaw.install`) and handled by the OpenClaw install system via `uv`. The Python packages required are:

- **`pylance`** — The [Lance columnar format](https://github.com/lance-format/lance) library.

    ⚠️ **Naming note:** Despite the PyPI package being named `pylance`, the library is imported as `import lance` in Python code. This is the official Lance project naming convention — it is **NOT** the VS Code "pylance" language server. See [lance.org](https://lance.org) for details.

- **`pandas`** — Data manipulation
