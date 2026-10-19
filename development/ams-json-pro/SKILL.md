---
name: json-pro
description: JSON processing mastery — parsing, validation, transformation, and large-file strategies — use when working with JSON data.
category: document-processing
---

## Overview

JSON is the default data interchange format, but production JSON work involves
more than `parse` and `stringify`: schema validation, streaming huge payloads,
querying/transforming nested structures, and handling the format's sharp edges
(precision, duplicates, comments). This skill covers the full toolkit.

## When to use

- Validating JSON payloads against schemas (JSON Schema)
- Processing JSON files too large for memory (streaming parsers, JSONL)
- Transforming nested JSON (flattening, reshaping, querying with JSONPath/jq)
- Handling precision loss, duplicate keys, and non-standard extensions
- Designing JSON APIs and config formats

## Core concepts

**Validate at the boundary.** Every JSON input from outside your code is
untrusted: validate shape and types with JSON Schema (or a typed decoder)
before use. Validation errors should name the exact path (`$.user.address.zip`)
and the violated constraint — this is what makes integrations debuggable.

**Streaming for scale.** Standard parsers build the whole document in memory.
For large files, use streaming parsers (event-based) or newline-delimited
JSON (JSONL — one object per line), which parallelizes and streams naturally.
If you control the producer, prefer JSONL for anything over a few MB.

**Query with the right tool.** `jq` for shell one-liners and pipelines;
JSONPath for in-code queries; your language's native mapping for typed access.
Learn `jq`'s core (`select`, `map`, `group_by`, `to_entries`) — it repays the
hour invested a hundred times over in debugging and data munging.

**JSON's sharp edges.** Numbers are IEEE doubles — 64-bit IDs and money lose
precision; use strings for those. Duplicate keys: behavior is parser-dependent
(last wins, usually, silently). No comments, no trailing commas in strict
JSON — but JSONC/JSON5 exist for configs; know which your parser accepts.

**Canonical form for hashing/signing.** Key order and whitespace affect bytes;
if you hash or sign JSON, canonicalize first (sorted keys, no whitespace) or
use a defined canonicalization — otherwise signatures break across
implementations.

## Practical workflow

1. **Define the schema first** (JSON Schema draft 2020-12 or your framework's
   typed models); generate documentation and validators from it.
2. **Decode strictly:** reject unknown fields in strict contexts (catches
   typos like `emial`), coerce deliberately, and preserve precision for
   IDs/money via strings or decimal types.
3. **Transform functionally:** prefer pure mapping/filtering pipelines over
   mutation; for shell work, compose `jq` filters and keep them in scripts,
   not one-off history.
4. **Stream when large:** switch to JSONL or a streaming parser before the
   file size forces you to; benchmark memory at 10x expected size.
5. **Log and error well:** on validation failure, report the JSON path, the
   expected vs actual, and a snippet of the offending document.
6. **Version your formats:** add a `version` or `$schema` field to persisted
   JSON so migrations are explicit, not archeological.

## Common pitfalls

- **Float IDs and money** — `9007199254740993` parses to `9007199254740992`;
  use strings for identifiers and decimal-safe representations for currency.
- **Assuming key order** — JSON objects are unordered; parsers may preserve
  insertion order but consumers must not depend on it.
- **Deeply nested access without guards** — `a.b.c.d` throws on missing `b`;
  use optional chaining / path queries with defaults.
- **Concatenating JSON with string templates** — injection and escaping bugs;
  always build objects and serialize.
- **Huge single-line JSON in logs** — unreadable and ungreppable; pretty-print
  in dev, keep compact (or JSONL) in production with sampled pretty output.
- **Schema drift without versioning** — producers add fields, consumers break;
  treat JSON formats as contracts with changelogs.
