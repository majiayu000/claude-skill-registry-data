---
name: awk
description: >
  Expert GNU awk (gawk) one-liner generation and transformation. Use this skill
  whenever the user asks to process text fields, extract columns, compute sums or
  aggregates, filter structured output, reformat CSV/TSV, parse logs, generate
  reports, or do any record/field processing task. Trigger on keywords like "awk",
  "extract column", "sum a field", "count occurrences", "print field N", "filter
  by column", "reformat output", "aggregate log data", "process CSV", "TSV", or
  any request that maps to a field-oriented text transformation. When in doubt,
  use this skill — awk is often the right tool when sed isn't enough.
---

# GNU awk (gawk) Skill

All output assumes **gawk** (`awk --version` shows GNU Awk). POSIX awk
compatibility is not a goal; gawk extensions are used freely where they help.

---

## Core Principles

1. **Prefer one-liners.** Multi-line awk scripts only when a one-liner becomes
   unreadable.
2. **Use `-F` to set the field separator** explicitly. Never assume space.
3. **Dry-run friendly by default.** awk reads and prints; it never edits files
   in-place. Redirect explicitly (`> out && mv out in`) when the user wants
   in-place behavior.
4. **Use `BEGIN`/`END` blocks** for setup and summary output.
5. **Chain with pipes** when awk alone isn't the cleanest tool.
6. **Never use awk to parse JSON or XML.** Redirect to `jq` / `xmllint` and say
   why.

---

## Mental Model

```
awk 'BEGIN { setup } /pattern/ { action } END { summary }' file
```

- awk reads input **line by line** (records, split by `RS`, default `\n`).
- Each record is split into **fields** by `FS` (default: any whitespace).
- `$0` = entire record. `$1`, `$2`, ... `$NF` = individual fields. `NF` = number
  of fields. `NR` = current record number. `FNR` = record number within current
  file.

---

## Flags

| Flag         | Meaning                                      |
|--------------|----------------------------------------------|
| `-F SEP`     | Set field separator (string or regex)        |
| `-v VAR=VAL` | Set a variable before execution              |
| `-f FILE`    | Read awk program from a file                 |
| `--sandbox`  | Disable `system()`, `getline`, pipe (safe)   |

---

## Command Quick Reference

### Print specific fields

```bash
# Print fields 1 and 3
awk '{print $1, $3}' file.txt

# Print last field
awk '{print $NF}' file.txt

# Print second-to-last
awk '{print $(NF-1)}' file.txt

# Custom output separator
awk '{print $1 "," $2}' file.txt
```

### Filter lines

```bash
# Lines where field 3 > 100
awk '$3 > 100' file.txt

# Lines matching a regex
awk '/error/' file.txt

# Lines where field 2 matches a pattern
awk '$2 ~ /timeout/' file.txt

# Negate match
awk '$2 !~ /debug/' file.txt

# Multiple conditions
awk '$1 == "GET" && $9 >= 500' access.log
```

### Aggregation

```bash
# Sum a column
awk '{sum += $3} END {print sum}' file.txt

# Count matching lines
awk '/error/ {count++} END {print count}' file.txt

# Average
awk '{sum += $2; n++} END {print sum/n}' file.txt

# Min / max
awk 'NR==1 || $3 < min {min=$3} END {print min}' file.txt
awk 'NR==1 || $3 > max {max=$3} END {print max}' file.txt
```

### Frequency / histogram

```bash
# Count occurrences of each value in field 1
awk '{count[$1]++} END {for (k in count) print count[k], k}' file.txt | sort -rn

# Top 10 IPs in nginx log
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10
# Pure awk alternative:
awk '{c[$1]++} END {for (ip in c) print c[ip], ip}' access.log | sort -rn | head -10
```

### Field reformat / transform

```bash
# Swap fields 1 and 2
awk '{print $2, $1}' file.txt

# Prepend a string to field 1
awk '{$1 = "prefix_" $1; print}' file.txt

# Change field separator in output (OFS)
awk 'BEGIN{OFS=","} {print $1,$2,$3}' file.txt

# Remove a field (shift left from field 3)
awk '{out=""; for (i=1;i<=NF;i++) if (i!=2) out = out (out?OFS:"") $i; print out}' file.txt
```

### Line ranges

```bash
# Print lines 5 to 15
awk 'NR>=5 && NR<=15' file.txt

# Print between two patterns (inclusive)
awk '/START/,/END/' file.txt

# Skip the header line
awk 'NR > 1' file.txt

# Print only the header
awk 'NR == 1' file.txt
```

### CSV / TSV processing

```bash
# TSV: print columns 1 and 4
awk -F'\t' '{print $1, $4}' data.tsv

# CSV (simple, no quoted commas): sum column 3
awk -F',' 'NR>1 {sum+=$3} END {print sum}' data.csv

# Add a computed column to CSV
awk -F',' 'BEGIN{OFS=","} NR>1 {$4=$2*$3; print}' data.csv

# Filter CSV rows where column 2 > 50
awk -F',' '$2 > 50' data.csv

# Convert TSV to CSV
awk 'BEGIN{FS="\t"; OFS=","} {$1=$1; print}' data.tsv
```

> For CSV with quoted fields containing commas, use `gawk` with a proper CSV
> library or switch to `miller` (`mlr`) / `csvkit`.

### Log processing

```bash
# Extract HTTP 5xx lines from nginx access log
awk '$9 >= 500 && $9 < 600' access.log

# Sum bytes transferred (field 10) per status code (field 9)
awk '{bytes[$9]+=$10} END {for (s in bytes) print s, bytes[s]}' access.log | sort

# Requests per minute (timestamp in field 4, format [DD/Mon/YYYY:HH:MM:SS])
awk '{match($4, /[0-9]{2}\/[A-Za-z]+\/[0-9]{4}:[0-9]{2}:[0-9]{2}/, m); c[m[0]]++}
     END {for (t in c) print t, c[t]}' access.log | sort

# Strip log prefix, print only message
awk '{$1=$2=$3=""; print substr($0,4)}' app.log
```

### Multi-file processing

```bash
# Print filename alongside each line
awk '{print FILENAME, $0}' *.log

# Process file 1 as a lookup table, file 2 as data
awk 'NR==FNR {map[$1]=$2; next} {print $0, map[$1]}' lookup.txt data.txt
```

### In-place editing

```bash
# Portable awk has no in-place edit; prefer a temp file
awk '{gsub(/foo/, "bar"); print}' file.txt > file.tmp && mv file.tmp file.txt

# gawk-only in-place edit
gawk -i inplace '{gsub(/foo/, "bar"); print}' file.txt

# All .rb files
for f in src/**/*.rb; do
  awk '{gsub(/OldClass/, "NewClass"); print}' "$f" > "$f.tmp" && mv "$f.tmp" "$f"
done
```

---

## Built-in Functions

### String

| Function                  | Description                            |
|---------------------------|----------------------------------------|
| `length(s)`               | String length                          |
| `substr(s, start, len)`   | Substring (1-indexed)                  |
| `index(s, t)`             | Position of t in s (0 = not found)     |
| `split(s, arr, sep)`      | Split s into arr by sep, returns count |
| `gsub(re, rep, s)`        | Global replace in s (default: `$0`)    |
| `sub(re, rep, s)`         | First replace in s                     |
| `match(s, re, arr)`       | Match re in s; fills arr with groups   |
| `sprintf(fmt, ...)`       | Format string (like printf)            |
| `tolower(s)` / `toupper(s)` | Case conversion                      |
| `gensub(re, rep, how, s)` | gawk: replace with back-references (`\1`) |

### Math

| Function          | Description        |
|-------------------|--------------------|
| `int(x)`          | Truncate to integer |
| `sqrt(x)`         | Square root        |
| `log(x)` / `exp(x)` | Natural log / e^x |
| `sin(x)` / `cos(x)` | Trig (radians)   |
| `rand()`          | Random [0,1)       |
| `srand(seed)`     | Seed RNG           |

---

## gawk Extensions Worth Knowing

```bash
# OFMT: control float output precision
awk 'BEGIN{OFMT="%.2f"} {print $1 * 1.15}' prices.txt

# Pipe to a command per line
awk '{print $0 | "mail -s alert ops@example.com"}' alerts.txt

# Time functions
awk 'BEGIN{print strftime("%Y-%m-%d", systime())}'

# Two-way pipe (gawk only): close the writer before reading from sort
awk 'BEGIN{cmd="sort"} {print $0 |& cmd} END{close(cmd, "to"); while ((cmd |& getline line) > 0) print line}' file.txt

# Built-in CSV parsing (gawk 5.3+)
gawk --csv '{print $2}' data.csv

# Legacy/simple CSV only: FPAT misses empty fields and escaped quotes
awk 'BEGIN{FPAT="([^,]+)|(\"[^\"]+\")"} {print $2}' data.csv
```

---

## Combining with Other Tools

```bash
# awk + sort: frequency table
awk '{print $1}' file.txt | sort | uniq -c | sort -rn

# awk + sed: awk extracts, sed cleans
awk '/error/ {print $5}' app.log | sed 's/[^a-z0-9]//g'

# awk + xargs: act on extracted values
awk '$3 > 1000 {print $1}' jobs.txt | xargs kill

# awk as a replacement for cut + grep pipeline
# Instead of: grep 'GET' access.log | cut -d' ' -f7
awk '$6 ~ /GET/ {print $7}' access.log
```

---

## Output Format

When responding to an awk request:

1. **Show the one-liner** in a code block, ready to copy-paste.
2. Add a **one-line comment** per non-obvious part.
3. If the task fits a multi-step pipeline better, show that pipeline.
4. If the task is better served by `jq`, `mlr` (miller), `python`, or `perl`, say
   so briefly and optionally show that alternative too.

---

## Gotchas

- **Portable awk has no in-place editing.** Use `> tmp && mv tmp original` unless
  you intentionally depend on gawk's `-i inplace` extension.
- **Field assignment triggers rebuild of `$0`** using `OFS`. Set `OFS` in
  `BEGIN` if you rely on this.
- **Arrays are associative only** (hash maps). There are no integer-indexed arrays
  with guaranteed order; iterate with `for (k in arr)` (order is undefined). Use
  a separate key list + `asort()`/`asorti()` (gawk) when order matters.
- **Rebuilding vs re-splitting.** Assigning to a field rebuilds `$0` from fields
  using `OFS` (`$1=$1` is the common idiom). Assigning to `$0`, or `sub()`/`gsub()`
  on `$0`, re-splits fields using the current `FS`.
- **Regex constants vs strings.** `/foo/` is a regex literal; `"foo"` is a string.
  `$1 ~ /foo/` is correct; `$1 ~ "foo"` also works but avoids the literal syntax.
- **Integer division.** `5/2` returns `2.5` in awk (unlike shell). Use `int(5/2)`
  for truncation.
- **macOS ships BSD/one-true-awk**, not gawk. `gawk` must be installed via
  Homebrew. `FPAT`, `gensub()`, `strftime()`, and `|&` are gawk-only.
