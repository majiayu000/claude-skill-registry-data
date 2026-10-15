---
name: data-analyst
description: This skill should be used when the user asks to "analyze data", "run statistics", "chart this", "visualize this", "SQL query", "summarize this dataset", "데이터 분석", "CSV 분석", "통계 내줘", "시각화", or provides a data file for analysis.
arguments:
  - name: source
    description: Path to data file (CSV, JSON, SQLite, TSV) or inline data.
    default: ""
  - name: question
    description: What to analyze or extract from the data.
    default: ""
tools:
  - Bash
  - Read
  - Write
  - Glob
---

# Data Analyst

> Analyze structured data files — CSV, JSON, SQLite. Summarize, query, and visualize with CLI tools.

---

## WHEN TRIGGERED - EXECUTE IMMEDIATELY

If a source file is provided, start analysis immediately.

---

## Preflight: Dependency Check

Before starting, verify required libraries are installed and install any that are missing.

```bash
python3 -c "import pandas" 2>/dev/null || python3 -m pip install pandas
python3 -c "import openpyxl" 2>/dev/null || python3 -m pip install openpyxl
python3 -c "import matplotlib" 2>/dev/null || python3 -m pip install matplotlib
```

**Important**: Do not skip this step — the workflow below will fail without these libraries.

---

## Workflow

### Step 1: Detect data format and tools
**Type**: script

```bash
# Check available tools
command -v python3 >/dev/null 2>&1 && echo "PYTHON=yes"
command -v sqlite3 >/dev/null 2>&1 && echo "SQLITE=yes"
command -v duckdb >/dev/null 2>&1 && echo "DUCKDB=yes"
command -v jq >/dev/null 2>&1 && echo "JQ=yes"
```

Detect source format by extension: `.csv`, `.json`, `.sqlite`, `.db`, `.tsv`, `.xlsx`

### Step 2: Preview data
**Type**: script

Show first 5 rows and column summary:

```bash
# CSV
head -6 "$SOURCE" | column -s, -t

# JSON
cat "$SOURCE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(type(d), len(d) if isinstance(d,list) else list(d.keys())[:10])"

# SQLite
sqlite3 "$SOURCE" ".tables" && sqlite3 "$SOURCE" "SELECT * FROM $(sqlite3 "$SOURCE" ".tables" | head -1) LIMIT 5;"
```

Report: row count, column names, data types, null counts.

### Step 3: Analyze based on question
**Type**: prompt

If `$ARGUMENTS` includes a question, answer it using the data.

Common analysis patterns:
- **Summary stats**: min, max, mean, median, count per column
- **Group by**: aggregate by a categorical column
- **Filter**: find rows matching criteria
- **Trend**: sort by date/time column, detect patterns
- **Correlation**: relationship between numeric columns

Use Python one-liners or sqlite3/duckdb SQL for computation. Prefer DuckDB if available (fast, SQL on CSV).

```bash
# DuckDB example
duckdb -c "SELECT category, COUNT(*), AVG(amount) FROM read_csv_auto('$SOURCE') GROUP BY category ORDER BY COUNT(*) DESC"
```

### Step 4: Output results
**Type**: generate

Format results as:
```
Data Analysis: {filename}
Rows: {N} | Columns: {N}

{Answer to question or summary}

| Column | Type | Non-null | Unique |
|--------|------|----------|--------|
| ...    | ...  | ...      | ...    |

{Key findings as bullet points}
```

If user asked for visualization, generate an ASCII chart or suggest saving to CSV for external charting.

---

## Edge Cases

**Large files (>100MB)**: Sample first 10,000 rows. Warn: "Large file — analyzing sample."
**Malformed data**: Report parsing errors and attempt recovery (skip bad rows).
**No question provided**: Generate a general summary with top insights.
**Excel files**: Use `python3 -c "import openpyxl..."` if available, otherwise guide conversion to CSV.

---

## Integration Points

- **deep-research**: Data analysis as part of research workflow.
- **/daily-review**: Analyze workspace metrics (file counts, commit frequency, etc.).
- **document-converter**: Export analysis results as PDF report.
