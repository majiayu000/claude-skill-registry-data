---
name: tonl-tool
description: Deterministic wrapper for tonl CLI (npm package) for structured data operations in JSON/TONL formats. Use when converting JSON↔TONL, querying structured data, validating TONL schemas, or generating statistics. Maps directly to CLI subcommands (encode, decode, query, get, validate, stats).
---

# TONL Tool

## Overview

Provides deterministic access to the `tonl` CLI for working with structured data in JSON and TONL formats. Acts as a thin, faithful wrapper - all operations invoke the CLI directly without re-implementing behavior.

## What is TONL

TONL (Token-Optimized Notation Language) is a compact, human‑readable data serialization format designed to minimize tokenization cost for large language models while remaining easy to parse and edit. It represents objects, arrays, and primitives with terser syntax (including optional inline tables and concise delimiters), supports schema validation and path queries, and is intended for efficient round‑trip conversion to/from JSON using the `tonl` CLI.

## When to Use

Trigger this skill when the user requests:

- Converting JSON to TONL or TONL to JSON
- Querying structured data using path expressions
- Retrieving specific values from JSON/TONL files
- Validating TONL data against schemas
- Generating statistics about structured data (token counts, size analysis)

Keywords: `tonl`, `json`, `convert`, `query`, `validate`, `stats`, `structured data`

## Supported Operations

All operations map directly to `tonl` CLI subcommands:

### 1. ENCODE (JSON → TONL)

Convert JSON to TONL format.

**CLI**: `tonl encode <file.json> [--smart]`

**Flags**:

- `--smart` - Use smart formatting with inline tables for compact output

**Input**: File path or raw JSON content
**Output**: TONL string (verbatim from CLI)

### 2. DECODE (TONL → JSON)

Convert TONL to JSON format.

**CLI**: `tonl decode <file.tonl>`

**Input**: File path or raw TONL content
**Output**: JSON string (verbatim from CLI)

### 3. QUERY

Query structured data using JSONPath-style expressions.

**CLI**: `tonl query <file> '<path-expression>'`

**Examples**:

- `'users[*]'` - All users
- `'users[0].name'` - First user's name
- `'*.email'` - All email fields

**Input**: File path or raw content + query expression
**Output**: Query results (verbatim from CLI)

### 4. GET

Retrieve a single value from structured data.

**CLI**: `tonl get <file> "<path>"`

**Example**: `tonl get data.tonl "user.name"`

**Input**: File path or raw content + field path
**Output**: Single value (verbatim from CLI)

### 5. VALIDATE

Validate TONL data against a TONL schema.

**CLI**: `tonl validate --schema <schema.tonl> <data.tonl>`

**Input**: Schema file + data file (or raw content)
**Output**: Validation results or errors (verbatim from CLI)

### 6. STATS

Generate statistics about structured data.

**CLI**: `tonl stats <file> [--tokenizer <model>]`

**Flags**:

- `--tokenizer claude-sonnet-4.5` - Use specific tokenizer for token counting
- `--tokenizer gpt-4` - GPT-4 tokenizer

**Output**: Size, depth, token count statistics (verbatim from CLI)

## Instructions

1. **Determine operation** from user request (encode/decode/query/get/validate/stats)

2. **Handle input translation**:

   - If user provides file path → use path directly
   - If user provides raw content → use helper script to create temp file or stdin

3. **Construct CLI command**:

   - Use exact `tonl` subcommand syntax
   - Include all user-specified flags
   - Quote path expressions properly

4. **Execute via Bash tool**:

   ```bash
   tonl <subcommand> <args>
   ```

5. **Return output verbatim**:

   - Do NOT post-process, summarize, reformat, or interpret
   - Surface all CLI errors verbatim
   - Do NOT attempt to recover from invalid input

6. **Use helper script for complex input handling**:
   - `scripts/tonl-helper.py` handles stdin/file translation
   - Only when file path is not directly provided

## Bundled Resources

**scripts/tonl-helper.py** - Input handling for raw content (creates temp files when needed)

## Examples

```
User: "Convert this JSON to TONL: {\"name\": \"Alice\", \"age\": 30}"
Claude:
  1. Recognizes ENCODE operation
  2. Creates temp file with JSON content
  3. Runs: tonl encode temp.json --smart
  4. Returns TONL output verbatim

User: "Query all usernames from users.tonl with path 'users[*].name'"
Claude:
  1. Recognizes QUERY operation
  2. Runs: tonl query users.tonl 'users[*].name'
  3. Returns results verbatim

User: "Get token count stats for config.json using claude-sonnet-4.5 tokenizer"
Claude:
  1. Recognizes STATS operation
  2. Runs: tonl stats config.json --tokenizer claude-sonnet-4.5
  3. Returns statistics verbatim

User: "Validate data.tonl against schema.tonl"
Claude:
  1. Recognizes VALIDATE operation
  2. Runs: tonl validate --schema schema.tonl data.tonl
  3. Returns validation results verbatim (success or errors)
```

## Strict Non-Goals

- ❌ Do NOT manually transform JSON or TONL
- ❌ Do NOT infer schemas or paths
- ❌ Do NOT add comments, metadata, or explanations to output
- ❌ Do NOT generate structured data without invoking CLI
- ❌ Do NOT post-process CLI output
- ❌ Do NOT attempt error recovery

This skill is a deterministic, spec-compliant backend. All transformations must go through the `tonl` CLI.
