---
name: cargo-segmentation
description: "Define and use segments — named, saved filters over a Cargo model that become the audience for a batch run, a play trigger, or an export. Triggers: \"build a segment of\", \"filter my contacts where\", \"who matches this criteria\", \"save this as a list\", \"how many companies match\", \"the Closed-Won segment\", \"everyone who has not been emailed\", \"target only accounts that\", \"what is in this segment\", \"narrow this down to\". Filter JSON uses `conjonction` (not `conjunction`) — misspelling it fails silently. Skip when: running something over the segment — use cargo-orchestration; exporting its rows — use cargo-analytics; ad-hoc SQL over the model — use cargo-storage."
version: "1.0.1"
compatibility: Requires @cargo-ai/cli (npm). Sign in or create an account with `cargo-ai login --email` (emailed code, no browser), `--oauth`, or an API token
homepage: https://github.com/getcargohq/cargo-skills
metadata:
  author: getcargo
  openclaw:
    requires:
      bins:
        - cargo-ai
    install:
      - kind: node
        package: "@cargo-ai/cli@latest"
        bins:
          - cargo-ai
    homepage: https://github.com/getcargohq/cargo-skills
---

# Cargo CLI — Segmentation

Segments are the **audience layer** of a Cargo workspace: a named, saved filter over one model that answers "which records do I mean?" Everything downstream — a batch run, a play trigger, a CSV export, a change feed — takes a segment (or a segment-shaped filter) as its input.

> See `references/response-shapes.md` for full JSON response structures.
> See `references/troubleshooting.md` for common errors and how to fix them.
> Filter condition kinds and operators live in [`../cargo-orchestration/references/filter-syntax.md`](../cargo-orchestration/references/filter-syntax.md) — the single source of truth for filter JSON.

## Bootstrap

Already signed in (`cargo-ai whoami` returns a workspace)? Skip to the next section.

```bash
npm install -g @cargo-ai/cli            # no global install? prefix every command with `npx @cargo-ai/cli`
cargo-ai login --email you@company.com  # emailed code, no browser; creates the account on first use
                                        # alternatives: --oauth (browser) · --token <api-token> (CI)
cargo-ai whoami                         # confirm the active workspace before any write
```

Every command prints JSON to stdout; failures exit non-zero with `{"errorMessage": "..."}`. Anything that creates a run or a batch is async — pass `--wait-until-finished` or poll the matching `get`. When the full skill bundle is installed, [`../cargo/references/prerequisites.md`](../cargo/references/prerequisites.md) adds the CLI version pin, token scopes, and the admin-only surface.

## Key concepts

| Term | What it is |
|---|---|
| **Filter** | A JSON object (`{conjonction, groups[].conditions[]}`) evaluated against one model's columns. Ephemeral on its own. |
| **Segment** | A filter **saved** with a name, a `modelUuid`, and a `slug`. Has a `uuid`, a live `recordsCount`, and a history. This is what plays, batches, and exports reference. |
| **Change** | One computed delta of a segment between two syncs — how many records were `added`, `updated`, `removed`, `unchanged`. The basis of every "notify me when someone enters this audience" motion. |
| **Tracking columns** | The subset of columns (`--tracking-column-slugs`) whose value changes count as an `updated` record. Without them a record only ever registers as added or removed. |

**Filter vs segment — pick deliberately.** A one-off question ("how many companies have >100 employees?") wants `segment fetch` with an inline filter and no saved object. An audience you will run something against, schedule against, or track over time wants a real `segment create` — because only a saved segment produces changes.

## Discover resources first

Always list before creating. A workspace usually already holds the segment you are about to duplicate.

```bash
cargo-ai segmentation segment list                    # all segments (uuid, name, slug, modelUuid, recordsCount)
cargo-ai storage model list                           # find the modelUuid a segment must target
cargo-ai storage column list --model-uuid <uuid>      # the column slugs your filter conditions reference
```

Segments created automatically by a play are named `GENERATED_PLAY_SEGMENT` and carry `fromPlay: true` — **never edit or remove those by hand**; they belong to the play that owns them.

**Retrieve in the UI:** segments live under the model at `app.getcargo.io/workspaces/<WORKSPACE_UUID>/models/<MODEL_UUID>`. Get `<WORKSPACE_UUID>` from `cargo-ai whoami`.

## Quick reference

```bash
cargo-ai segmentation segment list
cargo-ai segmentation segment get <segment-uuid>
cargo-ai segmentation segment create --name "<name>" --model-uuid <uuid> --filter '<json>'
cargo-ai segmentation segment update --uuid <segment-uuid> --filter '<json>'
cargo-ai segmentation segment remove <segment-uuid>
cargo-ai segmentation segment fetch    --model-uuid <uuid> --filter '<json>' --limit 50
cargo-ai segmentation segment download --model-uuid <uuid> --filter '<json>'
cargo-ai segmentation change list  --segment-uuid <segment-uuid>
cargo-ai segmentation change fetch --uuid <change-uuid> --kinds added --limit 50
cargo-ai segmentation record fetch --model-uuid <uuid> --ids <id[,id…]>
```

## Building a filter

The full condition catalogue — every `kind` (`string`, `number`, `date`, `boolean`, `array`, `relation`) and every operator — is in [`../cargo-orchestration/references/filter-syntax.md`](../cargo-orchestration/references/filter-syntax.md). The shape:

```json
{
  "conjonction": "and",
  "groups": [
    {
      "conjonction": "and",
      "conditions": [
        { "kind": "number", "columnSlug": "employee_count", "operator": "greaterThan", "value": 100 },
        { "kind": "string", "columnSlug": "email", "operator": "isNotEmpty" }
      ]
    }
  ]
}
```

> **`conjonction`, not `conjunction`.** The French spelling is intentional and it is the single most expensive typo in the CLI: a misspelled key does not error — the filter silently matches nothing, and you conclude the data is empty. Grep your JSON for `conjunction` before every call.

Match-everything filter: `{"conjonction":"and","groups":[]}`.

## Size the audience before you build it

Counting is free; running anything over an audience is not. Establish the size first, then decide.

```bash
# 1. How many records match? — inline filter, no saved object, 1 row back
cargo-ai segmentation segment fetch \
  --model-uuid <uuid> \
  --filter '{"conjonction":"and","groups":[{"conjonction":"and","conditions":[
      {"kind":"number","columnSlug":"employee_count","operator":"greaterThan","value":100}]}]}' \
  --limit 1

# 2. Happy with the shape? Save it as the real audience.
cargo-ai segmentation segment create \
  --name "Mid-market accounts" \
  --model-uuid <uuid> \
  --filter '<same json>' \
  --column-slugs "name,domain,employee_count" \
  --tracking-column-slugs "employee_count,funding_stage"
```

`segment get <uuid>` then reports `recordsCount` — the authoritative size. Cite that number, not your own estimate, before proposing a paid run over the segment.

## Fetch vs download vs record fetch

| Command | Returns | Use for |
|---|---|---|
| `segment fetch --model-uuid --filter` | Records inline as JSON, paginated (`--fetching-limit`, `--fetching-offset`) | Inspecting a handful of rows, counting, previewing a filter before saving it |
| `segment download --model-uuid --filter` | A signed URL to the full dataset | Handing the whole audience to the user or another tool — see [`../cargo-analytics/SKILL.md`](../cargo-analytics/SKILL.md) |
| `record fetch --model-uuid --ids <ids>` | Specific records by id | Re-reading rows a change feed just told you about |

`segment fetch --sync` refreshes the underlying data sources before evaluating; `--enrich` returns joined/derived values. Both cost time, so leave them off for a size check.

**Never page a large segment into the conversation.** Use `--limit 3` to see the shape, then `download` for the rest.

## Changes — the delta feed

Every time a segment syncs, Cargo computes a change: how the membership moved. This is what turns a static list into a signal.

```bash
# What deltas exist for this segment?
cargo-ai segmentation change list --segment-uuid <segment-uuid>
# → { "changes": [ { "uuid", "totalRecordsCount", "addedRecordsCount",
#                    "updatedRecordsCount", "removedRecordsCount",
#                    "unchangedRecordsCount", "createdAt" } ] }

# Which records actually entered the audience in that delta?
cargo-ai segmentation change fetch --uuid <change-uuid> --kinds added --limit 50
```

`--kinds` is **required** on `change fetch` and takes `added`, `updated`, `removed`, or `unchanged` (comma-separated). Returned rows carry the `_kind`, `_id`, `_title`, and `_time` meta-columns alongside the model's own columns.

`updatedRecordsCount` is always `0` unless the segment was created with `--tracking-column-slugs` — the tracked columns define what "updated" means. Set them at creation time when the segment is meant to feed a monitoring motion.

A segment's most recent delta is also inlined on `segment list` / `segment get` as `lastChange`, so a "what moved?" question rarely needs a second call.

## What consumes a segment

Segments are an input, not an outcome. Once one exists:

- **Run something over it** — batch a connector action or workflow across every member: [`../cargo-orchestration/SKILL.md`](../cargo-orchestration/SKILL.md). Batches enroll from a segment; sample 10–20 records and get explicit approval before enrolling the full audience.
- **Trigger a play on entry** — a play whose trigger is a segment fires as records enter it. Play triggers use `kind: "filter"` and generate their own `GENERATED_PLAY_SEGMENT`; see [`../cargo-orchestration/references/examples/plays.md`](../cargo-orchestration/references/examples/plays.md).
- **Export it** — [`../cargo-analytics/SKILL.md`](../cargo-analytics/SKILL.md) (`segment download` needs `--model-uuid`, *not* `--segment-uuid` — a frequent 400).
- **Watch it** — alert when the audience empties, stalls, or spikes: [`../cargo-observability/SKILL.md`](../cargo-observability/SKILL.md).
- **Act on it as GTM** — signal segments (job change, funding, tech intent) drive the recipes in [`../cargo-gtm/SKILL.md`](../cargo-gtm/SKILL.md).
- **Declare it as code** — `defineSegment` in [`../cargo-project/SKILL.md`](../cargo-project/SKILL.md) when the audience should live in git.

## Gotchas

- **`conjonction`, never `conjunction`** — silent empty result, no error.
- **`segment download` takes `--model-uuid`, not `--segment-uuid`.** The filter travels with the request; the segment UUID is not a valid input there.
- **`change fetch` needs `--uuid` (the *change* UUID) plus `--kinds`.** Passing the segment UUID returns a 400.
- **`change list` needs `--segment-uuid`.** Calling it bare returns a 400 complaining that `segmentUuid` is undefined.
- **`--help` on `change` and `record` subcommands prints the parent help** rather than the subcommand's flags (CLI ≥ 1.0.48). Use the Quick reference above; file a report if it still bites.
- **A segment belongs to exactly one model.** Cross-model audiences are a relationship + filter on the joined column, not two segments.
- **`fromPlay: true` segments are owned by a play.** Editing one changes what that play targets; removing one breaks it.
- **`--limit` on a segment caps membership**, it is not a display page size — `--fetching-limit` is the page size.

## When the CLI fails

Two failed attempts on the same command, or behavior that contradicts this skill, goes to the team:

```bash
cargo-ai workspaceManagement report create \
  --title "<one-line summary>" \
  --description "<commands run, errorMessage verbatim, expected vs actual, UUIDs>"
```
