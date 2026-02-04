---
name: jn
description: Use JN for data transformation and ETL. Read data with 'jn cat', filter with 'jn filter', write with 'jn put'. Convert between CSV/JSON/Excel/YAML formats. Stream data through Unix pipes. Integrate with VisiData for visual exploration. Use when working with data files, format conversion, filtering data, or ETL pipelines.
allowed-tools: Bash, Read
---

# JN Data Pipeline Tool

JN is a command-line ETL tool that uses NDJSON (newline-delimited JSON) as a universal data format. Chain commands with Unix pipes to build data pipelines.

## Core Concept

All JN commands communicate via NDJSON:
```
{"name": "Alice", "age": 30}
{"name": "Bob", "age": 25}
```

One JSON object per line = streamable, memory-efficient data processing.

## Four Essential Commands

### 1. jn cat - Read Data

Read any data source, output NDJSON:

```bash
# Basic files
jn cat data.csv                     # CSV → NDJSON
jn cat data.json                    # JSON → NDJSON
jn cat data.xlsx                    # Excel → NDJSON
jn cat data.yaml                    # YAML → NDJSON

# Force specific format
jn cat data.txt~csv                 # Treat .txt as CSV
jn cat data.log~json                # Treat .log as JSON

# Format with parameters
jn cat "data.csv~csv?delimiter=;"   # Semicolon-delimited
jn cat "data.csv?limit=100"         # Only read first 100 rows

# Read from stdin
cat data.csv | jn cat "-~csv"       # Pipe stdin as CSV
```

**Filtering at read time:**
```bash
# Filter during cat (applied AFTER reading)
jn cat "data.csv?city=NYC"              # Filter: city equals NYC
jn cat "data.csv?city=NYC&city=LA"      # OR logic: NYC or LA
jn cat "data.csv?city=NYC&age>25"       # AND logic: NYC and age>25
jn cat "data.csv?limit=100&city=NYC"    # Config + filter
```

### 2. jn filter - Transform Data

Filter/transform NDJSON using jq expressions:

```bash
# Simple filters
jn cat data.csv | jn filter '.age > 25'
jn cat data.csv | jn filter '.status == "active"'
jn cat data.csv | jn filter '.price < 100'

# Select specific fields
jn cat data.csv | jn filter '{name, email}'
jn cat data.csv | jn filter '{name, age, city: .location.city}'

# Transform values
jn cat data.csv | jn filter '.price = .price * 1.1'
jn cat data.csv | jn filter '.name = .name | ascii_upcase'

# Combine conditions (AND)
jn cat data.csv | jn filter '.age > 25 and .city == "NYC"'

# Combine conditions (OR)
jn cat data.csv | jn filter '.city == "NYC" or .city == "LA"'

# Select records
jn cat data.csv | jn filter 'select(.active)'
jn cat data.csv | jn filter 'select(.price > 100)'
```

**Aggregation with slurp mode:**
```bash
# Count total records
jn cat data.csv | jn filter -s 'length'

# Group and count
jn cat data.csv | jn filter -s 'group_by(.status) | map({status: .[0].status, count: length})'

# Sort all data
jn cat data.csv | jn filter -s 'sort_by(.age)'

# Get unique values
jn cat data.csv | jn filter -s 'unique_by(.email)'
```

**⚠️ Warning:** Slurp mode (`-s`) loads all data into memory - use only when needed for aggregations.

### 3. jn put - Write Data

Write NDJSON to any format:

```bash
# Basic output
jn cat data.csv | jn put output.json       # NDJSON → JSON
jn cat data.json | jn put output.csv       # JSON → CSV
jn cat data.csv | jn put output.xlsx       # CSV → Excel
jn cat data.json | jn put output.yaml      # JSON → YAML

# Force format
jn cat data.csv | jn put output.txt~json   # Force JSON format

# Format with parameters
jn cat data.json | jn put "output.json?indent=4"        # Pretty JSON
jn cat data.json | jn put "output.csv?delimiter=|"      # Pipe-delimited

# Output to stdout (need -- before -)
jn cat data.json | jn put -- "-"                    # NDJSON to stdout
jn cat data.json | jn put -- "-~json"               # JSON array to stdout
jn cat data.json | jn put -- "-~json?indent=2"      # Pretty JSON to stdout
```

### 4. jn table - Display as Table

Render NDJSON as a formatted table for human viewing:

```bash
# Basic table (grid format)
jn cat data.csv | jn table

# Different formats
jn cat data.csv | jn table -f github        # GitHub markdown
jn cat data.csv | jn table -f simple        # Simple format
jn cat data.csv | jn table -f fancy_grid    # Fancy Unicode
jn cat data.csv | jn table -f markdown      # Markdown
jn cat data.csv | jn table -f html          # HTML table

# With options
jn cat data.csv | jn table --index          # Show row numbers
jn cat data.csv | jn table -w 40            # Max column width 40
jn cat data.csv | jn table --no-header      # Hide header

# Pipeline integration
jn cat data.csv | jn filter '.active' | jn table
jn cat data.csv | jn head -n 10 | jn table -f github
```

**⚠️ Important:** `jn table` output is for humans only - cannot be piped to other jn commands.

## Common Workflows

### Format Conversion

```bash
# CSV to JSON
jn cat input.csv | jn put output.json

# Excel to CSV
jn cat input.xlsx | jn put output.csv

# JSON to YAML
jn cat input.json | jn put output.yaml

# Multiple conversions
jn cat input.xlsx | jn put output.json
jn cat output.json | jn put output.yaml
```

### Filter and Transform

```bash
# Filter rows, write result
jn cat sales.csv | jn filter '.amount > 1000' | jn put high_value.json

# Select specific columns
jn cat users.csv | jn filter '{name, email}' | jn put contacts.csv

# Transform and save
jn cat products.csv | jn filter '.price = .price * 1.1' | jn put updated.csv

# Multi-stage pipeline
jn cat data.csv | \
  jn filter '.status == "active"' | \
  jn filter '{id, name, email}' | \
  jn put active_users.json
```

### Preview Data

```bash
# View first few records
jn cat data.csv | jn head -n 5

# Preview as table
jn cat data.csv | jn head -n 10 | jn table
jn cat data.csv | jn head -n 10 | jn table -f github

# Check last records
jn cat data.csv | jn tail -n 5

# Quick data inspection
jn cat data.json | jn filter 'keys' | jn head -n 1  # Show field names
jn cat data.csv | jn head -n 3 | jn table          # Preview with nice formatting
```

### Data Analysis

```bash
# Count records
jn cat data.csv | jn filter -s 'length'

# Count by status
jn cat data.csv | jn filter -s 'group_by(.status) | map({status: .[0].status, count: length})' | jn table

# Find unique values
jn cat data.csv | jn filter -s 'map(.city) | unique' | jn put cities.json

# Get statistics
jn cat sales.csv | jn filter -s 'map(.amount) | {total: add, avg: (add / length), max: max, min: min}'

# Display summary as table
jn cat data.csv | jn filter -s 'group_by(.category) | map({category: .[0].category, count: length})' | jn table -f github
```

## VisiData Integration

JN has built-in VisiData integration for visual data exploration.

### Using jn vd

```bash
# View NDJSON in VisiData
jn cat data.csv | jn vd

# View source directly
jn vd data.json
jn vd data.csv
jn vd https://api.com/data~json

# Pre-filter before viewing
jn vd data.csv --filter '.age > 30'

# Preview large files
jn head -n 1000 huge_file.csv | jn vd
```

**⚠️ Important:** When using `jn vd` programmatically, it requires tmux (see visidata skill for details).

### Interactive VisiData with tmux

For programmatic control of VisiData through JN:

```bash
SOCKET_DIR=${TMPDIR:-/tmp}/claude-tmux-sockets
mkdir -p "$SOCKET_DIR"
SOCKET="$SOCKET_DIR/claude.sock"
SESSION=claude-jn-vd

# Launch VisiData via JN in tmux
tmux -S "$SOCKET" new -d -s "$SESSION"
jn cat data.csv | jn put /tmp/explore.ndjson
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "jn vd /tmp/explore.ndjson" Enter

echo "VisiData running. Monitor with:"
echo "  tmux -S \"$SOCKET\" attach -t $SESSION"
echo ""
echo "For VisiData commands and usage, see the 'visidata' skill"
```

**For full VisiData capabilities, invoke the visidata skill rather than duplicating documentation here.**

### Explore → Filter → Save Workflow

```bash
# 1. Export data for exploration
jn cat large_dataset.csv | jn put /tmp/explore.csv

# 2. Open in VisiData (see visidata skill for interactive usage)
jn vd /tmp/explore.csv
# User explores data, identifies filter criteria

# 3. Apply filters in JN based on insights
jn cat large_dataset.csv | jn filter '.category == "electronics" and .price > 100' | jn put filtered.json

# 4. Verify with VisiData
jn vd filtered.json
```

## Helper Commands

### jn head / jn tail

```bash
# First N records (default 10)
jn cat data.csv | jn head -n 10
jn head data.csv                    # Can also take input directly

# Last N records (default 10)
jn cat data.csv | jn tail -n 10

# Combine with other operations
jn cat data.csv | jn filter '.age > 25' | jn head -n 5

# Preview with table
jn head data.csv | jn table
```

### jn analyze

```bash
# Get schema and statistics
jn cat data.csv | jn analyze

# Analyze filtered data
jn cat data.csv | jn filter '.status == "active"' | jn analyze
```

## Tips and Best Practices

### 1. Use Pipes for Complex Workflows

```bash
# Multi-stage processing
jn cat raw.csv | \
  jn filter '.status == "active"' | \
  jn filter '{id, name, email, created: .created_at}' | \
  jn filter 'select(.email != null)' | \
  jn put clean.json
```

### 2. Preview Before Writing

```bash
# Check output first
jn cat data.csv | jn filter '.age > 25' | jn head -n 5 | jn table

# Then save
jn cat data.csv | jn filter '.age > 25' | jn put filtered.csv
```

### 3. Use Query Parameters for Config

```bash
# Better than format override
jn cat "data.csv?delimiter=;,limit=1000"

# Combine config and filtering
jn cat "data.csv?limit=1000&status=active"
```

### 4. Temporary Files for Checkpoints

```bash
# Stage 1: Initial cleaning
jn cat raw.csv | jn filter 'select(.email != null)' | jn put /tmp/stage1.ndjson

# Stage 2: Further processing
jn cat /tmp/stage1.ndjson | jn filter '.age > 18' | jn put /tmp/stage2.ndjson

# Stage 3: Final output
jn cat /tmp/stage2.ndjson | jn filter '{name, email}' | jn put final.csv
```

### 5. Use VisiData for Visual Validation

```bash
# Process data
jn cat input.csv | jn filter '.price > 100' | jn put filtered.json

# Visually verify with VisiData
jn vd filtered.json
```

### 6. Avoid Slurp Unless Necessary

```bash
# ❌ Bad - loads everything into memory
jn cat huge.csv | jn filter -s 'sort_by(.date)'

# ✅ Good - processes row by row
jn cat huge.csv | jn filter 'select(.date > "2024-01-01")'

# ✅ Slurp only when needed for aggregation
jn cat small.csv | jn filter -s 'group_by(.category) | map({category: .[0].category, count: length})'
```

## Common Patterns

### Pattern: CSV Cleanup

```bash
# Remove nulls, select columns, save
jn cat messy.csv | \
  jn filter 'select(.email != null and .name != "")' | \
  jn filter '{name, email, phone}' | \
  jn put clean.csv
```

### Pattern: Data Enrichment

```bash
# Add computed fields
jn cat orders.csv | \
  jn filter '.total = (.price * .quantity)' | \
  jn filter '.tax = (.total * 0.08)' | \
  jn put enriched.csv
```

### Pattern: Multi-Format Pipeline

```bash
# Excel → filter → JSON → inspect → CSV
jn cat input.xlsx | \
  jn filter '.department == "sales"' | \
  jn put /tmp/sales.json

jn vd /tmp/sales.json  # Visual inspection

jn cat /tmp/sales.json | jn put final.csv
```

### Pattern: API to Database ETL

```bash
# Fetch from API (simulated with file), transform, save for import
jn cat api_response.json | \
  jn filter '.items[]' | \
  jn filter '{id, name, email, created_at}' | \
  jn filter 'select(.email != null)' | \
  jn put import_ready.csv
```

### Pattern: Quick Data Summary

```bash
# Get overview of data
echo "=== Record count ==="
jn cat data.csv | jn filter -s 'length'

echo -e "\n=== Field names ==="
jn cat data.csv | jn head -n 1 | jn filter 'keys'

echo -e "\n=== Sample records ==="
jn cat data.csv | jn head -n 5 | jn table
```

## Troubleshooting

### Issue: "No plugin found"

```bash
# Check file extension
ls -la data.csv

# Force format explicitly
jn cat data.txt~csv
```

### Issue: "JSON parsing error"

```bash
# Verify input is valid NDJSON
jn cat data.json | jn head -n 1

# Check for JSON arrays vs NDJSON
# JN outputs NDJSON, not JSON arrays
```

### Issue: Memory usage too high

```bash
# Avoid slurp mode for large files
# ❌ Don't do this with huge files:
jn cat huge.csv | jn filter -s 'sort_by(.date)'

# ✅ Process in streaming fashion:
jn cat huge.csv | jn filter 'select(.date > "2024-01-01")'
```

### Issue: VisiData not opening

```bash
# Check VisiData installation
vd --version

# Install if needed
uv tool install visidata

# For programmatic use, use tmux (see visidata skill)
```

## Quick Reference

| Task | Command |
|------|---------|
| Read CSV | `jn cat data.csv` |
| Read JSON | `jn cat data.json` |
| Force format | `jn cat data.txt~csv` |
| Filter | `jn filter '.age > 25'` |
| Select fields | `jn filter '{name, email}'` |
| Write JSON | `jn put output.json` |
| Write CSV | `jn put output.csv` |
| Pretty print | `jn put -- "-~json?indent=2"` |
| Table view | `jn table` |
| GitHub table | `jn table -f github` |
| First 10 | `jn head -n 10` |
| Last 10 | `jn tail -n 10` |
| Count | `jn filter -s 'length'` |
| View in VisiData | `jn vd` |

## Examples

**Example 1: Convert and filter**
```bash
jn cat sales.xlsx | jn filter '.amount > 1000' | jn put high_value.csv
```

**Example 2: Select columns**
```bash
jn cat users.csv | jn filter '{name, email, city}' | jn put contacts.json
```

**Example 3: Multiple filters**
```bash
jn cat data.csv | \
  jn filter '.status == "active"' | \
  jn filter '.age > 18' | \
  jn put adults.csv
```

**Example 4: Preview with VisiData**
```bash
jn cat data.csv | jn filter '.price > 100' | jn vd
```

**Example 5: Aggregation**
```bash
jn cat orders.csv | \
  jn filter -s 'group_by(.product) | map({product: .[0].product, total: map(.amount) | add})' | \
  jn put summary.json
```

## Integration with Other Skills

- **VisiData skill**: For detailed VisiData usage, interactive exploration, and tmux integration
- **tmux skill**: For running VisiData or other interactive tools programmatically

When you need to explore data visually, use `jn vd` and refer to the visidata skill for full capabilities.
