---
name: CSV
slug: csv
version: 1.0.0
description: Parse and generate RFC 4180 compliant CSV that works across tools.
homepage: https://clawic.com/skills/csv
metadata:
  clawdbot:
    emoji: 📊
    os:
    - linux
    - darwin
    - win32
    displayName: CSV
---

## Quoting Rules

- Fields containing comma, quote, or newline MUST be wrapped in double quotes
- Double quotes inside quoted fields escape as `""` (two quotes), not backslash
- Unquoted fields with leading/trailing spaces—some parsers trim, some don't; quote to preserve
- Empty field `,,` vs empty string `,"",`—semantically different; be explicit

## Delimiters

- CSV isn't always comma—detect `;` (European Excel), `\t` (TSV), `|` in legacy systems
- Excel exports use system locale delimiter; semicolon common in non-US regions
- Sniff delimiter from first line but verify—header might not contain special chars

## Encoding

- UTF-8 BOM (`0xEF 0xBB 0xBF`) breaks naive parsers but Excel needs it for UTF-8 detection
- When generating for Excel on Windows: add BOM; for programmatic use: omit BOM
- Latin-1 vs UTF-8 ambiguity—explicitly declare or detect encoding before parsing

## Common Parsing Failures

- Newlines inside quoted fields are valid—don't split on `\n` before parsing
- Unescaped quote in middle of field corrupts rest of file—validate early
- Trailing newline at EOF—some parsers create empty last row; strip or handle
- Inconsistent column count per row—validate all rows match header count

## Numbers & Dates

- `1,234.56` vs `1.234,56`—locale-dependent; standardize or document format
- Dates: ISO 8601 (`2024-01-15`) only unambiguous format; `01/02/24` is chaos
- Leading zeros in numeric fields (`007`)—quote to preserve or document as string

## Excel Quirks

- Formula injection: fields starting with `=`, `+`, `-`, `@` execute as formulas—prefix with `'` or tab
- Long numbers (>15 digits) lose precision—quote and format as text
- Scientific notation triggered by `E` in numbers—quote if literal text needed
