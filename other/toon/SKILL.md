---
name: toon
description: |
  Token-Oriented Object Notation — encode/decode JSON to compact TOON
  format (~40% token reduction for uniform arrays). TRIGGER when user:
  (a) pastes JSON inline (file or `cat X.json | ...`),
  (b) mentions "compress", "shrink", "encode JSON", "TOON", "tokens",
      "context window", "省 token",
  (c) asks to "analyze / summarize / inspect" a JSON dataset,
  (d) processes an API response with >2KB JSON output,
  (e) reads JSON files into context for processing.
  Always check: `cat X.json | ~/.local/bin/toon` is safe to run
  (non-JSON passes through). If output goes to file/DB/written verbatim,
  skip TOON. If nested non-uniform, JSON may be smaller — measure both.
---

# TOON — Token-Oriented Object Notation

## The CLI

```bash
# encode JSON -> TOON
cat data.json | ~/.local/bin/toon

# decode TOON -> JSON
cat data.toon | ~/.local/bin/toon --decode

# non-JSON passes through unchanged (safe to pipe anything)
```

Requires `~/.local/bin/toon` (Node wrapper around `@toon-format/toon`).

## WHEN to auto-encode (you should pipe `| toon`)

Trigger conditions — at least 2 must match:
- Tool output is JSON and **> 2KB**
- Contains **uniform array of objects** (5+ rows, identical keys)
- Will be summarized/analyzed rather than written verbatim
- Mentioned "tokens", "context", "compress" in the task
- Repeated structure (logs, records, time-series)

## WHEN to NOT encode

- Output goes to file/DB/other code (not LLM context)
- Small JSON (< 1KB) — overhead exceeds savings
- Deeply nested non-uniform — JSON-compact wins
- Downstream tool expects JSON (round-trip cost)
- Single record, not tabular

## Self-check before piping

```bash
# count rows + keys homogeneity
cat X.json | jq 'if type == "array" then length else 0 end'
cat X.json | jq '[.[] | keys | join(",")] | unique | length'
# uniform = length matches array length, unique = 1
```

If uniform + ≥5 rows + >2KB → encode. Otherwise skip.

## Format reminder

```
users[3]{id,name,email}:
  1,Alice,a@x
  2,Bob,b@x
  3,Carol,c@x
```

`[N]` = array length, `{fields}` = column schema, CSV rows below.

## Round-trip verification

```bash
echo '{"a":1}' | ~/.local/bin/toon | ~/.local/bin/toon --decode
# must equal '{"a":1}'
```

## Honest caveat

This skill is **descriptive** — I must remember to apply it. True auto-firing
needs: (a) an `AGENTS.md` rule in the workdir, or (b) a Hermes tool-result
hook. Without one of those, I default to JSON unless explicitly told.