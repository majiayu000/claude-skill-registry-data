---
name: id-management
description: |
  Generate unique entity IDs following the project's configured format. The write-side foundation that every entity-creating skill depends on. Use whenever a new entity is being created and needs an ID, or when validating an ID format, or to inspect the project's ID configuration.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-id-management
    version: "1.0.0"
    created: 2026-04-06T00:00:00Z
    category: processkit
    layer: 0
    uses:
      - skill: index-management
        purpose: Query existing entities and keep the SQLite index fresh after writes.
    provides:
      primitives: []
      mcp_tools: [generate_id, validate_id, list_used_ids, format_info]
---

# ID Management

## Intro

`id-management` is the write-side foundation alongside `index-management`.
Where `index-management` answers "what entities exist?", `id-management`
answers "what should this new entity be called?". Every skill that
creates a new entity calls into this one to allocate a unique ID.

> **MCP server.** This skill ships a self-contained MCP server at
> `mcp/server.py` (PEP 723 script — requires `uv` and Python ≥ 3.10 on
> PATH). Agent harnesses reach its tools by reading a single MCP config
> file at startup, so the contents of `mcp/mcp-config.json` must be merged
> into the harness's MCP config and placed at the harness-specific path
> before this skill is usable. If processkit was installed by an installer,
> that wiring is the installer's responsibility; if processkit was
> installed manually, the project owner must do it by hand.

## Overview

### What it provides

- **`generate_id(kind, slug_text?)`** — produce a fresh,
  collision-free ID for the given kind.
- **`validate_id(id)`** — check if a string is a syntactically valid
  processkit ID and parse out its kind/body.
- **`list_used_ids(kind?, limit?)`** — return IDs already in use
  (useful for diagnostics or bulk operations).
- **`vocabulary_status(kind?, intent_text?, allocation_mode?)`** —
  inspect palette capacity and shorthand ambiguity.
- **`format_info()`** — return the project's ID configuration so the
  agent can reason about it.

### ID anatomy

Every processkit entity ID has the shape `<PREFIX>-<body>`:

| Part      | Example                     | How it is set                         |
|-----------|-----------------------------|---------------------------------------|
| Prefix    | `BACK`                      | Determined by the primitive kind.     |
| Body      | `20260409_1449-CalmFox-foo` | Generated from configuration below.  |

The body is composed of up to four axes, all configurable in
`context/skills/id-management/config/settings.toml`:

| Setting          | Values           | Effect on body                              |
|------------------|------------------|---------------------------------------------|
| `format`         | `word` / `uuid`  | Word pair (adj+noun) or UUID fragment       |
| `word_style`     | `camel` / `kebab`| `CalmFox` or `calm-fox`                     |
| `datetime_prefix`| `true` / `false` | Prepend `YYYYMMDD_HHMM` before the pair     |
| `slug`           | `true` / `false` | Append content-derived slug from title      |

Example combinations:

| format | word_style | datetime_prefix | slug  | Result                              |
|--------|------------|-----------------|-------|-------------------------------------|
| word   | camel      | true            | true  | `BACK-20260409_1449-CalmFox-fts5-search` |
| word   | camel      | false           | true  | `BACK-CalmFox-fts5-search`          |
| word   | kebab      | false           | false | `BACK-calm-fox`                     |
| uuid   | —          | false           | false | `BACK-550e8400-e29b-41d4`           |

Default (no settings.toml): `word` + `kebab` + no datetime + no slug.

### Workflow when creating a new entity

This is what every entity-creating skill follows internally — the agent
rarely needs to call `generate_id` directly:

1. Decide the **kind** (`WorkItem`, `LogEntry`, `DecisionRecord`, ...).
2. Optionally provide **slug text** (e.g. the title of a WorkItem).
3. Call `generate_id(kind, slug_text)`.
4. The skill writes the entity file with that ID and updates the index.

### When the agent calls id-management directly

Most of the time, agents create entities via skills like
`workitem-management.create_workitem` and never see `id-management`.
Direct calls are useful when:

- You need to reserve an ID before fully writing the entity (e.g. for a
  multi-step creation flow that references its own ID in the body).
- You want to validate an ID a human typed in.
- You want to list all used IDs of a kind for bulk operations or audits.
- You want to confirm what format the project is configured for.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Hand-rolling an ID instead of calling `generate_id`.** Even if
  the ID format looks simple ("BACK-1234"), do not synthesize one.
  Generators handle collisions, prefix configuration, and project-
  specific format overrides — hand-rolling skips all three and
  silently produces invalid or colliding IDs.
- **Reusing an ID from the index without re-checking.** If you
  cached a "next available ID" earlier in the session, it may
  already be in use by now. Always call `generate_id` fresh at
  write time.
- **Using the wrong prefix for an entity kind.** WorkItems are
  `BACK-`, DecisionRecords are `DEC-`, LogEntries are `LOG-`, etc.
  Calling `generate_id(kind="WorkItem")` ensures the right prefix;
  passing `kind="workitem"` (lowercase) or omitting the kind may
  produce a generic identifier the index can't categorize.
- **Generating an ID before the entity is fully drafted.** If you
  call `generate_id` and then abandon the entity (because the user
  changed their mind), the generated ID is reserved but unused —
  a "phantom" that pollutes the index. Generate at the moment you
  commit to writing.
- **Treating `generate_id` as idempotent.** It is not. Each call
  produces a new fresh ID, even for the same kind. Don't call it
  twice expecting the same answer.
- **Not validating user-supplied IDs.** When the user types an ID
  ("delete BACK-42"), call `validate_id` first. Free-text input
  may have typos, wrong prefix, or be missing entirely.
- **Skipping `format_info()` for unfamiliar projects.** Different
  projects can override the ID format (length, separator, prefix
  case). Before generating IDs in a new project, call
  `format_info()` to learn the local convention rather than
  assuming the default.

## Full reference

### Prefix registry

| Primitive       | Prefix   |
|-----------------|----------|
| WorkItem        | `BACK`   |
| LogEntry        | `LOG`    |
| DecisionRecord  | `DEC`    |
| Actor           | `ACTOR`  |
| Role            | `ROLE`   |
| Binding         | `BIND`   |
| Scope           | `SCOPE`  |
| Category        | `CAT`    |
| Gate            | `GATE`   |
| Schedule        | `SCHED`  |
| Constraint      | `CONST`  |
| Context         | `CTX`    |
| Discussion      | `DISC`   |
| Process         | `PROC`   |
| StateMachine    | `SM`     |
| Artifact        | `ART`    |

The registry is hard-coded in `src/lib/processkit/__init__.py` (`KIND_PREFIXES`).
Adding a new primitive kind requires adding its prefix there.

### Word generation

Word-based IDs are produced from a built-in dictionary of 120 positive
adjectives and 120 concrete nouns (14,400 historical base combinations).
The default generator path preserves that legacy pool unless callers opt
into tagged palettes or high-volume modes.

The accepted vocabulary architecture is:

- **Tagged noun palettes** — broad categories such as landform, stone,
  space, metal/material, wood/tree, cloud/weather, nautical, water,
  navigation, architecture, light/fire, craft/tool, flora, and fauna.
- **`pair` mode** — `AdjNoun`, the normal-volume default.
- **`double_adjective` mode** — `AdjAdjNoun`, the preferred high-volume
  extension because it multiplies capacity without pluralization.
- **`counted` mode** — `SevenAdjPluralNouns`, an optional fallback for
  very high-volume or extra-distinct shorthand.

Category assignment is a hint, not mutable workflow state. For example,
WorkItems can lean toward landform/stone/water/navigation palettes, and
speculative items can add space/cloud hints, but backlog/done state must
not be encoded in the immutable ID.

Palette selection is RAG-assisted in architecture: kind, stable subtype,
title, labels, and slug summary form an ID intent document. processkit
uses deterministic lexical scoring today and is designed to reuse the
existing index-management sqlite/sqlite-vec database for richer semantic
palette ranking later. Embeddings rank candidates; the allocator still
enforces hard constraints such as lexical-token uniqueness, blocked
process words, and capacity thresholds.

The dictionary and helper functions live in `src/lib/processkit/ids.py`.
Projects can inspect readiness with `vocabulary_status()` and pk-doctor's
`id_vocabulary` check.

### Slug generation

When `id_slug = true`, a content-derived slug is appended:

```
slug_text = "Add aibox lint command"
→ slug = "add-aibox-lint" (first 4 tokens, lowercase, kebab-case)
```

The slug is informational — uniqueness is still carried by the word or
UUID portion, not the slug. Two entities can have the same slug as long
as their word/UUID parts differ.

### Collision avoidance

The generator queries the index for `existing_ids(kind)` and excludes
those before picking a new pair. This is fast (a single SQL query) and
correct as long as the index is fresh. The index is kept fresh by every
MCP server calling `index.upsert_entity()` immediately after each write.

If files have been edited outside the MCP path, run `reindex()` first.
The Phase 5 `aibox lint` command will detect a stale index and warn.

### Idempotency

`generate_id` is **not** deterministic — calling it twice produces two
different IDs. This is intentional: multiple agents working in parallel
should not collide on the same ID. If you need a deterministic preview
(e.g. "what ID would I get for this title?"), pass a fixed
`random.Random` to the lib function (`ids.generate_id(..., rng=...)`).
The MCP `generate_id` tool does not yet expose a deterministic mode.

### Validation

`validate_id` accepts a string and returns:

```python
{
  "valid": True,
  "kind": "WorkItem",
  "prefix": "BACK",
  "body": "calm-fox",
  "format_guess": "word",
  "has_slug": False,
}
```

or:

```python
{
  "valid": False,
  "reason": "no known prefix in <id>",
}
```

It checks the prefix against the registry and verifies the body shape
roughly matches a known format. It does NOT check whether the ID is
currently in use — for that, use `list_used_ids` or query the index
directly.

### Relationship to index-management

id-management is a **peer** of index-management at Layer 0, not a
parent or child. Both are foundational. id-management has a soft
dependency on index-management (`uses: [index-management]`) because it
queries the index for collision avoidance — but conceptually they cover
opposite halves of the entity lifecycle:

- **id-management** = write side (allocate identity)
- **index-management** = read side (find what exists)

Every skill that creates entities depends on both.
