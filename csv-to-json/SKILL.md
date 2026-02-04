---
name: csv-to-json
description: Converts CSV files to JSON format.
version: 1.0.0
---

# CSV to JSON Converter

## 1. Core Purpose
You are a **Data Transformer**. You convert CSV files into JSON arrays where each row becomes an object with column headers as keys.

## 2. References Loading
* **Script:** `scripts/csv-to-json.py`

## 3. Execution Logic

### Usage
```bash
python .agent/skills/csv-to-json/scripts/csv-to-json.py <input.csv> [output.json]
```

### Parameters
| Parameter | Required | Description |
|-----------|----------|-------------|
| `input.csv` | Yes | Path to the input CSV file |
| `output.json` | No | Path for output JSON file (defaults to stdout) |

### Example
```bash
# Output to stdout
python .agent/skills/csv-to-json/scripts/csv-to-json.py data.csv

# Output to file
python .agent/skills/csv-to-json/scripts/csv-to-json.py data.csv result.json
```

## 4. Output Format
JSON array of objects:
```json
[
  {"column1": "value1", "column2": "value2"},
  {"column1": "value3", "column2": "value4"}
]
```
