---
name: importing-data
description: Systematic CSV import process - discover structure, design schema, standardize formats, import to database, detect quality issues (component skill for DataPeeker analysis sessions)
---

# Importing Data - Component Skill

## Purpose

Use this skill when:
- Starting a new analysis with CSV data files
- Need to import CSV into relational database systematically
- Want to ensure proper schema design and type inference
- Need quality assessment before cleaning/analysis begins
- Replacing ad-hoc import workflows

This skill is a **prerequisite** for all DataPeeker analysis workflows and is referenced by all process skills.

**Note:** DataPeeker uses SQLite (`data/analytics.db`), but this process applies to any SQL database. For SQLite-specific commands, see the `using-sqlite` skill.

## Prerequisites

- **CSV file accessible** on local filesystem
- **Database** with SQL support (DataPeeker uses SQLite at `data/analytics.db`)
- **Workspace created** for analysis session (via `just start-analysis` or equivalent)
- **Understanding** that this skill creates `raw_*` tables, not final tables (cleaning-data handles finalization)

## Data Import Process

Create a TodoWrite checklist for the 5-phase data import process:

```
Phase 1: CSV Discovery & Profiling - pending
Phase 2: Schema Design & Type Inference - pending
Phase 3: Basic Standardization - pending
Phase 4: Import Execution - pending
Phase 5: Quality Assessment & Reporting - pending
```

Mark each phase as you complete it. Document all findings in numbered markdown files (`01-csv-profile.md` through `05-quality-report.md`) within your analysis workspace directory.

---

## Phase 1: CSV Discovery & Profiling

**Goal:** Understand CSV file structure, detect encoding and delimiter, capture sample data for schema design.

### File Discovery

Identify the CSV file(s) to import:
- Ask user for CSV file path(s)
- Verify file exists and is readable
- Note file size for sampling strategy (>100K rows = sample-based profiling)

**Document:** Record CSV file path, size, timestamp in `01-csv-profile.md`

### Encoding Detection

Detect file encoding to prevent import errors:

```bash
file -I /path/to/file.csv
```

Common encodings:
- `charset=us-ascii` or `charset=utf-8` → Standard, no conversion needed
- `charset=iso-8859-1` or `charset=windows-1252` → May need conversion to UTF-8

**Document:** Record detected encoding. If non-UTF-8, note conversion requirement.

### Delimiter Detection

Analyze first few lines to detect delimiter:

```bash
head -n 5 /path/to/file.csv
```

Check for:
- Comma (`,`) - most common
- Tab (`\t`) - TSV files
- Pipe (`|`) - less common
- Semicolon (`;`) - European CSV files

**Document:** Record detected delimiter character.

### Header Detection

Determine if first row contains headers:
- Read first row
- Check if row contains text labels vs data values
- If ambiguous, ask user to confirm

**Document:** Record whether headers present, list header names if found.

### Sample Data Capture

Capture representative samples for schema inference:

```bash
# First 10 rows
head -n 11 /path/to/file.csv > /tmp/csv_head_sample.txt

# Last 10 rows
tail -n 10 /path/to/file.csv > /tmp/csv_tail_sample.txt

# Row count
wc -l /path/to/file.csv
```

**Document:** Include head and tail samples in `01-csv-profile.md` for reference during schema design.

### Phase 1 Documentation Template

Create `analysis/[session-name]/01-csv-profile.md` with: ./templates/phase-1.md

**CHECKPOINT:** Before proceeding to Phase 2, you MUST have:
- [ ] CSV file path confirmed and file accessible
- [ ] Encoding, delimiter, headers detected
- [ ] Sample data captured (head + tail)
- [ ] `01-csv-profile.md` created with all sections filled
- [ ] Column overview completed with initial observations

---

## Phase 2: Schema Design & Type Inference

**Goal:** Design database schema by inferring types from CSV samples, propose table structure with rationale.

### Analyze Column Types

For each column from Phase 1 profiling, infer appropriate data type:

**Type Inference Rules** (adapt to your database):

1. **Integer types** - Use when:
   - All non-NULL values are whole numbers
   - No decimal points observed
   - Typical for: IDs, counts, years, quantities
   - Examples: INTEGER (SQLite), INT/BIGINT (PostgreSQL/MySQL)

2. **Decimal/Float types** - Use when:
   - Values contain decimal points
   - Monetary amounts, measurements, percentages
   - Examples: REAL (SQLite), NUMERIC/DECIMAL (PostgreSQL), DECIMAL (MySQL)

3. **Text/String types** - Use when:
   - Mixed alphanumeric content
   - Dates/datetimes stored as text (ISO 8601: YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)
   - Categories, names, descriptions
   - Examples: TEXT (SQLite), VARCHAR/TEXT (PostgreSQL/MySQL)
   - **Default choice when unsure**

**Note:** Date/time handling varies by database. SQLite stores dates as TEXT. PostgreSQL/MySQL have native DATE/TIMESTAMP types.

**Document:** For each column, record inferred type with rationale and sample values.

### Handle NULL Representations

Identify NULL representations in CSV:
- Empty cells → `NULL` in database
- Literal strings: "N/A", "null", "NULL", "None", "#N/A" → Convert to `NULL`
- Numeric codes: -999, -1 (if documented as NULL) → Convert to `NULL`

**Document:** List all NULL representations found and conversion strategy.

### Design Table Schema

Propose CREATE TABLE statement:

```sql
CREATE TABLE raw_[table_name] (
  [column_1_name] [TYPE],  -- Rationale for type choice
  [column_2_name] [TYPE],  -- Rationale for type choice
  ...
);
```

**Table naming convention:**
- Prefix with `raw_` to indicate unprocessed data
- Use lowercase with underscores: `raw_sales_data`, `raw_customers`
- Derive from CSV filename or ask user for preferred name

**Document:** Full CREATE TABLE statement with inline comments explaining each type choice.

### Present Schema to User

Use AskUserQuestion tool to present schema proposal:
- Show proposed table name
- Show each column with type and rationale
- Ask user to confirm or request changes

**Document:** User's approval and any requested modifications.

### Phase 2 Documentation Template

Create `analysis/[session-name]/02-schema-design.md` with: ./templates/phase-2.md

**CHECKPOINT:** Before proceeding to Phase 3, you MUST have:
- [ ] All columns analyzed with type inference rationale
- [ ] NULL representations identified and mapped
- [ ] CREATE TABLE statement drafted
- [ ] User approved schema (via AskUserQuestion)
- [ ] `02-schema-design.md` created with all sections filled

---

## Phase 3: Basic Standardization

**Goal:** Define transformation rules for dates, numbers, whitespace, and text formatting to ensure clean, consistent data in raw_* table.

### Date Format Standardization

**Target format:** ISO 8601
- Dates: `YYYY-MM-DD` (e.g., 2025-01-15)
- Datetimes: `YYYY-MM-DD HH:MM:SS` (e.g., 2025-01-15 14:30:00)

**Common source formats to convert:**
- `MM/DD/YYYY` or `M/D/YYYY` → `YYYY-MM-DD`
- `DD/MM/YYYY` or `D/M/YYYY` → `YYYY-MM-DD` (verify with user which is month vs day)
- `YYYY/MM/DD` → `YYYY-MM-DD` (slash to hyphen)
- `Mon DD, YYYY` → `YYYY-MM-DD` (e.g., "Jan 15, 2025" → "2025-01-15")
- Timestamps with T separator: `YYYY-MM-DDTHH:MM:SS` → Keep as-is (valid ISO 8601)

**Document:** List each date column, source format detected, target format, conversion logic.

### Number Format Normalization

**Remove non-numeric characters:**
- Currency symbols: `$123.45` → `123.45`
- Comma separators: `1,234.56` → `1234.56`
- Percentage signs: `45%` → `45` or `0.45` (document choice)
- Units: `25kg`, `100m` → `25`, `100` (document unit in column name/comments)

**Decimal handling:**
- Preserve decimal points
- Convert European format if detected: `1.234,56` → `1234.56` (verify with user)

**Document:** List each numeric column, formatting issues found, normalization rules.

### Whitespace and Text Normalization

**Whitespace cleaning:**
- Trim leading/trailing whitespace from all TEXT columns
- Normalize internal whitespace: multiple spaces → single space
- Normalize line endings: `\r\n` or `\r` → `\n`

**Text case standardization** (optional, apply selectively):
- IDs/codes: Often uppercase for consistency
- Names: Title case or preserve original
- Free text: Preserve original case
- **Document choice per column type**

**Document:** Which columns get whitespace cleaning, which get case normalization.

### NULL Standardization

Apply NULL representation mapping from Phase 2:
- Convert all identified NULL representations to actual SQLite `NULL`
- Empty strings → `NULL` for numeric/date columns
- Empty strings → Preserve as empty string `''` for TEXT columns (document choice)

**Document:** NULL conversion applied, count of conversions per column.

### Phase 3 Documentation Template

Create `analysis/[session-name]/03-standardization-rules.md` with: ./templates/phase-3.md

**CHECKPOINT:** Before proceeding to Phase 4, you MUST have:
- [ ] Date standardization rules defined for all date columns
- [ ] Number normalization rules defined for all numeric columns
- [ ] Whitespace/text rules defined
- [ ] NULL conversion mapping finalized
- [ ] `03-standardization-rules.md` created with verification queries

---

## Phase 4: Import Execution

**Goal:** Execute import with standardization rules, verify row count and data integrity.

### Generate CREATE TABLE Statement

From Phase 2 schema design, finalize CREATE TABLE statement:

```sql
CREATE TABLE IF NOT EXISTS raw_[table_name] (
  [column_1] [TYPE],
  [column_2] [TYPE],
  ...
);
```

**Execute:**
```bash
sqlite3 data/analytics.db < create_table.sql
```

**Verify table created:**
```sql
-- Check table exists
.tables

-- Inspect schema
PRAGMA table_info(raw_[table_name]);
```

**Document:** Paste table creation confirmation and schema output.

### Import CSV with Standardization

**Import method options:**

**Option 1: SQLite `.import` command** (for simple cases):
```bash
sqlite3 data/analytics.db <<EOF
.mode csv
.import /path/to/file.csv raw_[table_name]
EOF
```

**Option 2: Python script** (for complex standardization):
```python
import csv
import sqlite3
from datetime import datetime

conn = sqlite3.connect('data/analytics.db')
cursor = conn.cursor()

with open('/path/to/file.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Apply standardization rules from Phase 3
        row['date_column'] = standardize_date(row['date_column'])
        row['amount_column'] = standardize_number(row['amount_column'])
        # ... apply other rules ...

        cursor.execute("""
            INSERT INTO raw_[table_name]
            ([columns]) VALUES ([placeholders])
        """, tuple(row.values()))

conn.commit()
conn.close()
```

**Document:** Which method used, any import warnings/errors encountered and resolved.

### Verify Import Success

**Row count verification:**
```sql
-- Count rows in table
SELECT COUNT(*) as row_count FROM raw_[table_name];
```

Compare to CSV row count from Phase 1. Should match (or CSV count - 1 if CSV had header row).

**Sample data inspection:**
```sql
-- View first 5 rows
SELECT * FROM raw_[table_name] LIMIT 5;

-- View last 5 rows
SELECT * FROM raw_[table_name]
ORDER BY rowid DESC LIMIT 5;
```

**Column completeness check:**
```sql
-- Check NULL counts per column
SELECT
  COUNT(*) as total_rows,
  COUNT([column_1]) as [column_1]_non_null,
  COUNT([column_2]) as [column_2]_non_null,
  ...
FROM raw_[table_name];
```

**Document:** Paste actual results showing row counts, sample rows, NULL counts.

### Run Verification Queries from Phase 3

Execute all verification queries defined in `03-standardization-rules.md`:
- Date format verification
- Number format verification
- Whitespace verification

**Expected:** All verification queries return 0 rows (no violations).

**If violations found:** Document count and examples, decide whether to:
1. Re-import with adjusted rules
2. Document as acceptable edge cases
3. Flag for cleaning-data phase

**Document:** Results of all verification queries.

### Phase 4 Documentation Template

Create `analysis/[session-name]/04-import-log.md` with: ./templates/phase-4.md

**CHECKPOINT:** Before proceeding to Phase 5, you MUST have:
- [ ] raw_* table created in data/analytics.db
- [ ] CSV data imported with standardization applied
- [ ] Row count verified matches CSV (accounting for headers)
- [ ] Sample data inspected and looks correct
- [ ] All Phase 3 verification queries executed
- [ ] `04-import-log.md` created with all results documented

---

## Phase 5: Quality Assessment & Reporting

**Goal:** Systematically detect data quality issues using sub-agent to prevent context pollution, document findings for cleaning-data skill.

**CRITICAL:** This phase MUST use sub-agent delegation. DO NOT analyze data in main agent context.

### Delegate Quality Assessment to Sub-Agent

**Use dedicated quality-assessment agent**

Invoke the `quality-assessment` agent (defined in `.claude/agents/quality-assessment.md`):

```
Task tool with agent: quality-assessment
Parameters:
- table_name: raw_[actual_table_name]
- columns: [list of all columns from schema]
- numeric_columns: [list of numeric columns for outlier detection]
- text_columns: [list of text columns for uniqueness analysis]
```

The agent will execute all quality checks (NULL analysis, duplicates, outliers, free text) and return structured findings.

**Document agent findings in `05-quality-report.md` using template below.**

### Delegate Foreign Key Detection to Sub-Agent

**If multiple tables exist in the database**, detect foreign key relationships between them.

**Use dedicated detect-foreign-keys agent**

Invoke the `detect-foreign-keys` agent (defined in `.claude/agents/detect-foreign-keys.md`):

```
Task tool with agent: detect-foreign-keys
Parameters:
- database_path: data/analytics.db
- table_names: [list of all raw_* tables in database]
```

**When to run FK detection:**
- **Multiple tables imported:** Run to discover relationships
- **Single table imported:** Skip (no relationships possible), document "N/A - single table" in quality report

The agent will:
1. Identify FK candidate columns based on naming patterns
2. Validate candidates with value overlap analysis
3. Assess cardinality (one-to-one, one-to-many, many-to-many)
4. Quantify referential integrity violations (orphaned records)
5. Return structured relationship catalog with join recommendations

**Document FK findings in `05-quality-report.md` using template below.**

### Create Quality Report for cleaning-data

Create `analysis/[session-name]/05-quality-report.md` with: ./templates/phase-5.md

**CHECKPOINT:** Before concluding importing-data skill, you MUST have:
- [ ] Sub-agent completed quality assessment (NOT done in main context)
- [ ] NULL percentages documented for all columns
- [ ] Duplicates detected and examples captured
- [ ] Outliers identified in all numeric columns
- [ ] Free text columns identified for categorization
- [ ] FK relationships detected (if multiple tables) via detect-foreign-keys sub-agent
- [ ] Referential integrity assessed with orphaned record counts
- [ ] `05-quality-report.md` created with all sections filled (including FK relationships)
- [ ] Quality report ready for cleaning-data skill to consume

---

## Common Rationalizations

### "The CSV looks clean, I can skip profiling and go straight to import"
**Why this is wrong:** Hidden issues (encoding, delimiters, NULL representations) cause import failures or silent data corruption. Even "clean" CSVs have edge cases.

**Do instead:** Always complete Phase 1 profiling. Takes 5 minutes and prevents hours of debugging broken imports.

### "I'll just guess the schema types, they're obvious from the column names"
**Why this is wrong:** Column named "year" might contain "2023-Q1" (TEXT). "amount" might have "$" symbols. Type inference prevents silent casting failures.

**Do instead:** Complete Phase 2 type inference with sample analysis. Document rationale for each type choice.

### "Dates look fine, I don't need standardization rules"
**Why this is wrong:** Mixed formats ("01/15/2025", "2025-01-15", "Jan 15 2025") break date arithmetic and sorting. Standardization is mandatory.

**Do instead:** Complete Phase 3 with explicit date format conversion rules. Verify with queries after import.

### "I'll do the import manually, don't need to document it"
**Why this is wrong:** Undocumented imports can't be reproduced. When re-importing updated data, you'll forget the transformations applied.

**Do instead:** Complete Phase 4 import log with commands, results, and verification. Future-you will thank present-you.

### "The data looks good after import, quality assessment is overkill"
**Why this is wrong:** Duplicates, outliers, and NULL patterns are invisible without systematic checks. These surface as bugs during analysis.

**Do instead:** ALWAYS complete Phase 5 with sub-agent delegation. Quality report saves time in cleaning-data phase.

### "I'll run quality checks in the main agent, it's faster than delegating"
**Why this is wrong:** Analyzing thousands of rows pollutes main agent context, degrading performance for entire session. Sub-agents prevent this.

**Do instead:** ALWAYS delegate Phase 5 to sub-agent with exact sqlite3 commands provided.

### "This CSV has 100K rows, I should skip some profiling steps for speed"
**Why this is wrong:** Large files are MORE likely to have quality issues, not less. Sampling strategies exist for large files.

**Do instead:** Use head/tail sampling (Phase 1) and query-based profiling (Phase 5 sub-agent). Don't skip phases.

### "The import succeeded, I don't need to verify row counts"
**Why this is wrong:** Silent data loss happens. Header rows miscounted, empty rows skipped, encoding issues truncating data.

**Do instead:** Always verify row count matches (Phase 4). If mismatch, investigate before proceeding.

### "I'll clean the data during import, don't need separate cleaning-data skill"
**Why this is wrong:** Import handles technical standardization (formats). Cleaning handles semantic issues (business rules, categorization). Mixing them creates confusion.

**Do instead:** Keep importing-data focused on standardization. Let cleaning-data handle deduplication, outliers, free text.

### "Quality report shows no issues, I can skip cleaning-data"
**Why this is wrong:** cleaning-data is ALWAYS mandatory per design. Even "clean" data needs business rule validation and final verification.

**Do instead:** Proceed to cleaning-data even if quality report shows minimal issues. Document "no cleaning needed" if appropriate.

---

## Summary

This skill ensures systematic, documented CSV import with quality assessment by:

1. **Profiling before importing:** Understand encoding, delimiters, headers, and sample data before designing schema - prevents import failures and silent corruption.

2. **Explicit type inference:** Analyze samples to infer INTEGER/REAL/TEXT types with documented rationale - prevents type casting failures and ensures correct data representation.

3. **Mandatory standardization:** Convert dates to ISO 8601, normalize numbers, clean whitespace, map NULL representations - creates consistent data foundation for analysis.

4. **Verified import execution:** Document CREATE TABLE statements, import methods, row count verification - ensures reproducibility and data integrity.

5. **Systematic quality assessment:** Delegate NULL detection, duplicate finding, outlier identification, and free text discovery to sub-agent - prevents context pollution while ensuring comprehensive quality checks.

6. **Audit trail maintenance:** Create numbered markdown files (01-05) documenting every decision - provides full traceability from raw CSV to raw_* tables.

Follow this process and you'll create clean, well-documented raw_* tables ready for the cleaning-data skill, avoid silent data corruption, and maintain complete audit trail for reproducible imports.

---
