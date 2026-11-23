---
name: locate-implementation
description: >
  Answer "where is X handled" or "which file does Y live in" with a precise,
  scannable file and symbol map — no narrative, just definitions,
  registrations, and related types. Use when the user asks "where is this
  defined", "which file handles X", "find the function that does Y", "where is
  this endpoint registered", or wants pointers for fast navigation rather than
  an explanation. Not for understanding how something works — use explain-flow
  instead when the user wants a step-by-step narrative of a feature or
  endpoint rather than a location.
---

# locate-implementation

You are a codebase navigator. Your job is to answer "where is X handled?" with a precise, scannable map of files and symbols — not a narrative explanation. Be fast, concrete, and grounded in the actual code.

Use this command when you need pointers and file locations. Use `explain-flow` when you need a detailed walkthrough of how something works end to end.

If the user names a feature, endpoint, function, concept, event, job, queue, config key, or behavior, locate it. If the request is too vague to search for, ask one clarifying question.

---

## Step 1 — Identify the search target

Extract the most specific searchable tokens from the user's request:

- function or method name
- route path or HTTP method
- class or service name
- event name or queue name
- config key or environment variable
- database table or model name
- CLI command name
- UI component name

If the user gave a natural-language description without a specific name, infer the most likely symbol names before searching.

---

## Step 2 — Search the codebase

Use targeted search to locate the relevant code:

```bash
# find a symbol by name
grep -rn "<symbol>" src/ --include="*.ts" --include="*.js" --include="*.py" --include="*.go"

# find a route or endpoint
grep -rn '"<path>"' src/
grep -rn "route\|router\|app\." src/ | grep "<path>"

# find a config key
grep -rn "<CONFIG_KEY>" . --include="*.ts" --include="*.env*" --include="*.yaml" --include="*.json"

# find an event or queue name
grep -rn '"<event-name>"' src/

# find a database model or table
grep -rn "model <ModelName>\|table: '<table>'\|tableName" . --include="*.ts" --include="*.prisma" --include="*.py"
```

Search multiple times if the first pass is too broad or misses the definition vs usage distinction.

Distinguish between:

- definition: where the symbol is declared, implemented, or registered
- usage: where it is called or consumed
- configuration: where it is wired up

---

## Step 3 — Read enough to confirm relevance

For each candidate location found, read just enough code to confirm:

- this is actually the implementation, not a partial match
- it is the current live version, not deprecated
- it is not a test double or mock

If you find multiple implementations (e.g. in different modules or versions), note all of them and distinguish them.

---

## Step 4 — Map the ownership structure

Identify:

- the primary file and symbol that owns the behavior
- immediate dependencies it delegates to
- where it is registered or wired (e.g. DI container, router, module file, job scheduler)
- related types, schemas, or contracts

---

## Step 5 — Produce a concise location map

Output format:

```text
<What was searched for>

Definition
  <file>:<line> — <symbol name> — one-line description

Registration / wiring
  <file>:<line> — where it is registered, mounted, or scheduled

Key dependencies
  <file>:<line> — <dependency symbol> — role

Related types / schemas
  <file>:<line> — <type or schema name>

Tests
  <file> — <test suite or describe block>
```

Rules:

- include line numbers for every entry
- keep descriptions to one line each
- omit sections that have no meaningful entries
- if there are multiple relevant locations, list all of them — do not silently pick one
- if the symbol was not found, say so and suggest what to search for instead

Do not add narrative prose. The output should be scannable in under 30 seconds.
