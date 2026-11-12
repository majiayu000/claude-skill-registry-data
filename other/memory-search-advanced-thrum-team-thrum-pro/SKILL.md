---
name: memory-search-advanced
description: "Use when running thrum memory search with RAG (--near), composing complex predicate stacks, paginating large result sets, interpreting MEM-001..010 hint codes, or diagnosing embedding adapter behavior. Loads three-vector ranking semantics, length-bias caveat, and the full hint catalog."
version: "0.11.0"
license: "Apache-2.0"
---

# memory-search-advanced — RAG, hint codes, complex predicates

Load this sub-skill from `thrum-memory` (umbrella) for predicate needs beyond
tag + kind + recency filtering.

## Predicate surface (shipped)

`thrum memory search` combines all predicates with AND:

```text
Query:
  positional args — FTS query text; `thrum memory search "<topic>"` is
  equivalent to --grep "<topic>" (multiple args join with single spaces;
  giving both positional and --grep is refused as ambiguous)

Identity / structure:
  --kind <kind>, --tag <tag> (SINGLE tag per query), --scope project|agent|role,
  --status <status> ("*" for any; default active)

Text:
  --grep <terms> (full-text MATCH over title + body_oneline/short/full;
  terms matched literally — punctuation is not FTS5 operators)

Semantic (when embedding adapter enabled):
  --near "<text>"

Time:
  --since 7d | <Go duration> | <RFC3339>

Sort & limit:
  --sort created_at_desc|updated_at_desc|relevance|pinned_first
  --limit 10 (default)
  --offset N
```

Output formats: `table` (default), `ids`, `oneline`, `short`, `full`, `json`.

Tag-set OR is NOT expressible in one query — `--tag` takes a single tag. For OR
semantics, run one search per tag and merge.

## DESIGNED — NOT YET SHIPPED (do not use)

The original memory-search design specifies a wider predicate surface that the
shipped CLI does not implement. The flags below DO NOT EXIST today — the CLI
rejects them with `unknown flag`. They are recorded here as the spec diff for
the eventual search-surface implementer, NOT as usable commands:

```text
--id, --kinds (multi-kind), --subkind, --agent / --author, --pinned,
--tags-any (tag-set OR),
--since-created, --since-updated, --until,
--parent <id>, --supersedes <id>, --superseded-by <id>,
--related-to <id>, --derived-from <id>,
--grep-field <oneline|short|full|title>, --regex,
--near-id <id>, --near-limit N
```

Workarounds with the shipped surface: time filtering = `--since` only (no
created-vs-updated split); per-field grep = not available (grep spans title +
all three zooms); edge predicates = not available (edge reads are the
`memory.listByEdge` RPC, no CLI); `--pinned` = `--tag pinned` (pinned is a
tag).

## Pagination patterns

Default `--limit 10` keeps context bounded. Walk a large set:

```bash
thrum memory search --kind session_summary --since 30d --limit 25 --offset 0
thrum memory search --kind session_summary --since 30d --limit 25 --offset 25
```

For counting: `thrum memory count` is the cheap O(1) counter, but it counts by
`--agent` / `--role` only — it accepts NO kind/time filters. To count a filtered
set, read the `total` field from the JSON response (a separate COUNT query,
computed before LIMIT applies):

```bash
thrum memory count --role researcher                  # cheap, coarse
thrum memory search --kind session_summary --since 30d \
  --limit 1 --format json | jq '.total'               # filtered count
```

Do NOT count via `--limit 0 --format ids | wc -l` — the `--limit 0`
streaming/export reservation is currently non-functional (the CLI drops
`limit=0` from the RPC params and the daemon clamps the absent limit to 10, so
output caps at 10 rows regardless of the real match count).

## RAG semantics (`--near`)

`--near "<text>"` runs semantic search against memory embeddings. Three
per-memory vectors are stored — one per zoom level, embedding the title-prefixed
string:

- `<title> — <body_oneline>`
- `<title> — <body_short>`
- `<title> — <body_full>`

Ranking is `score = max(sim_oneline, sim_short, sim_full)`. Each result carries
`matched_zoom` so the CLI can render the zoom level that actually matched.
Per-zoom embeddings let topical queries dock against `oneline` while
deep-content queries dock against `full`.

### Length-bias caveat — read before trusting `--near` results

Title-prefixed `oneline` strings (~40-50 chars) and `body_full` (up to 256 KB)
embed in different subspaces of `granite-30m-english`'s 384-dim space. **Short
queries can systematically match `oneline` over `full` for length-similarity
reasons rather than semantic-relevance reasons.** This is a real bias inherited
from the embedding model.

Detection and recovery (manual in v1; a future MEM-011+ zoom-divergence
detector is reserved for this case; the shipped MEM-008 is the
embed-enqueue-failed warning, not a zoom-divergence detector):

- Inspect `matched_zoom` in each result. If short queries return rows dominated
  by `matched_zoom=oneline`, the ranking may have been misled.
- Re-run with a longer query phrasing.
- Add `--kind <X>` to narrow before semantic re-rank.
- Inspect the full body manually, following the shared 3-step read pattern
  (`thrum-memory`): triage with `thrum memory show <id> --zoom short`
  first, then fetch with `thrum memory show <id> --zoom full` once confirmed.

Mitigations weighed and deferred (don't reach for them yet): weighted
combination, cross-encoder re-rank, per-kind length normalization. v1 ships
max-of-three; tune later only if `matched_zoom` diagnostics surface systematic
problems.

## Hint codes (MEM-001..010)

Hints render as a `hints` array in `--json` mode and as inline notices in human
mode. Suppress everywhere with `THRUM_NO_HINTS=1`. Severity is `warn` for
blocking-shaped advice, `info` for nudges.

| Code      | Trigger                                                           | What it tells you                                                    |
| --------- | ----------------------------------------------------------------- | -------------------------------------------------------------------- |
| `MEM-001` | search returned >50 matches                                       | Narrow with `--kind` / `--tag` / `--since`                           |
| `MEM-002` | `--near` supplied without `--kind`                                | Add `--kind` to narrow before semantic re-rank (deferred)            |
| `MEM-003` | empty result with two or more narrowing predicates                | Drop the most-restrictive flag                                       |
| `MEM-004` | `--near` with embedding adapter disabled                          | Hard refusal — enable the adapter (see setup below)                  |
| `MEM-005` | `--grep` matched nothing AND field is empty for most rows of kind | Broaden: drop `--kind`                                               |
| `MEM-006` | `--near` found rows with `embed_status=pending` → FTS fallback    | Wait for backfill or run `memory.embed.rebuild` (deferred)           |
| `MEM-007` | `--near` skipped rows whose `embedding_model` ≠ configured model  | Run backfill to migrate vectors (deferred)                           |
| `MEM-008` | `memory.create` enqueue to embed worker failed                    | Best-effort; the worker will retry via `memory.embed.rebuild`        |
| `MEM-009` | `memory.edit` projection detected concurrent edit; LWW loser      | Loser's value is preserved in `memory.history` (deferred surfacing)  |
| `MEM-010` | `memory.create` omitted `body_short` or `body_full`               | Three-zoom retrieval works better with all three; non-blocking nudge |

**Deferred triggers:** MEM-002, MEM-006, MEM-007 are registered today but the
emission path lights up in a future epic (`--near` adapter wiring +
multi-model support). MEM-009 emission lights up when LWW-loser surfacing
lands in the projection response. The codes are stable; only the trigger
conditions are in flight.

**Hard refusal:** MEM-004 is the only hint with `AllowForce=false`. There is no
recovery flag — the adapter is either present or absent.

## Embedding adapter awareness

`--near` only works when the embedding adapter is enabled:

```bash
thrum config set llm.embedding.enabled true
thrum config set llm.embedding.provider ollama --force
thrum config set llm.embedding.base_url http://localhost:11434 --force
thrum config set llm.embedding.model "granite-embedding:30m-english"
```

Embedding work is queued on write (OS-nice `+10`, single-flight per memory_id,
exponential backoff). Writes never block on embedding. Searches degrade
gracefully to FTS for not-yet-embedded rows and surface MEM-006 when the
degradation happens.

Edits mark only affected zoom-levels as `embed_status=stale`; tag-only edits
re-embed nothing, title-only edits re-embed all three. Old vectors stay
queryable during the staleness window.

Cold-start backfill runs once on the first daemon boot with the adapter enabled.
Disable with `embedding.backfill_on_boot: false`; rate-limit via
`embedding.max_per_minute` (default 60).

## Composing complex predicates

Stack predicates left-to-right; they AND. Use `--scope` only when you
specifically want to filter by assembly scope (it is NOT visibility — see
umbrella skill).

Example: every active arch decision tagged `substrate`, edited recently,
semantically related to "RPC routing" (tag-set OR = one query per tag):

```bash
thrum memory search \
  --kind arch_decision \
  --tag substrate \
  --status active \
  --since 14d \
  --near "RPC routing" \
  --limit 25
```

Example: every superseded session summary that touched a given epic, paged:

```bash
thrum memory search \
  --kind session_summary \
  --status superseded \
  --tag epic-thrum-abc \
  --sort updated_at_desc \
  --limit 50 --offset 0
```
