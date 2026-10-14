---
name: csv-pro
description: CSV processing done right — parsing edge cases, dialects, and large files — use when ingesting or exporting CSV data.
category: document-processing
---

## Overview

CSV looks trivial until it isn't: embedded newlines, quoted commas, BOMs,
inconsistent dialects, and million-row files. This skill covers robust CSV
parsing and generation — the unglamorous work that keeps data pipelines from
silently corrupting data.

## When to use

- Parsing user-uploaded or third-party CSVs with unknown dialects
- Generating CSV exports that open correctly in Excel and other tools
- Streaming multi-gigabyte CSV files without loading them into memory
- Validating CSV schemas (headers, types, required columns)
- Handling encoding issues (BOM, Latin-1 vs UTF-8)

## Core concepts

**Never split on commas.** Real CSV has quoted fields containing commas,
newlines, and escaped quotes (`""`). Always use a proper CSV parser from your
language's standard library or a battle-tested package — hand-rolled splitting
is a bug factory.

**Dialects vary.** Delimiter (comma, semicolon, tab, pipe), quote character,
escape style, and line endings differ by producer and locale (much of Europe
uses `;` because `,` is the decimal separator). Sniff the dialect from a sample
when it's unknown, but let users override — sniffing is heuristic.

**Encoding: expect UTF-8 with BOM.** Excel writes UTF-8 CSVs with a BOM;
strip it or your first header becomes `\ufeffid`. For unknown encodings, try
UTF-8, then fall back to likely candidates (Windows-1252 for Western data) —
and log when you guess.

**Headers are data, not gospel.** Normalize them (trim, lowercase,
deduplicate) and validate against an expected schema. Map by name, not
position — column order changes. Report unknown/missing columns explicitly
rather than silently ignoring them.

**Stream large files.** Process row-by-row with iterators/generators; never
load a 2GB CSV into a list of dicts. Validate and transform in the streaming
pass, collecting only error summaries and aggregates in memory.

## Practical workflow

1. **Detect:** read a sample — sniff delimiter, check for BOM, detect encoding,
   locate the header row (not always row 1).
2. **Define the schema:** expected columns, types, required fields, value
   constraints; normalize header names.
3. **Parse streaming:** iterate rows, coerce types per column with clear error
   messages including the row number and raw value.
4. **Validate:** collect all errors (don't fail on the first); distinguish
   fatal (wrong columns) from row-level (bad value in row 4521).
5. **Generate:** write with the standard library writer, `QUOTE_MINIMAL`,
   `\r\n` line endings for Excel compatibility, UTF-8 with BOM if the audience
   is Excel users, and a header row always.
6. **Test with adversarial fixtures:** quoted commas, embedded newlines,
   empty fields, trailing delimiters, mixed line endings, and a 1M-row file
   for the streaming path.

## Common pitfalls

- **Hand-rolled `line.split(',')`** — breaks on the first quoted comma; use a
  real parser, always.
- **Ignoring the BOM** — invisible character corrupts the first column name
  and breaks header mapping.
- **Loading everything into memory** — fine for 10k rows, fatal for 10M;
  stream by default.
- **Silent type coercion** — `"0123"` becoming `123` loses leading zeros
  (zip codes, SKUs); coerce deliberately per column, not globally.
- **Excel mangling your output** — long digit strings become scientific
  notation, dates get reinterpreted; for Excel audiences consider prefixing
  with `=` or quoting, and document the behavior.
- **No row numbers in error messages** — "invalid value" without a row number
  is unactionable; always report where the problem is.
