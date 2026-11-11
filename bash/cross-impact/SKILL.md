---
name: cross-impact
description: |
  Run the cross-area scanner against a concept contract or a list of files and
  print the top-3 adjacent areas with score breakdowns. Use when: the user
  types `/cross-impact <contract-path>` or `/cross-impact <comma-separated-files>`,
  or asks "what other areas would this contract affect?", "what's adjacent to
  this set of files?", or "before I run /design-first, what would this touch?".

  This is the user-invocable wrapper around `.claude/scripts/cross_area_scan.py`.
  The same script is invoked by `data-architect` Step 4.5 automatically; this
  skill is the manual exploration path.
---

# /cross-impact

Surface the top-3 adjacent areas for a contract or a synthetic file list.

## Invocation patterns

- `/cross-impact .claude/concepts/2026-05-18-eval-workflow-guidance.md`
  Run against an existing contract. Uses the contract's `## Files to touch` list
  as input.

- `/cross-impact <a backend.roots entry>/Ingestion/EarningsJob.cs,<the same entry>/Ingestion/FundamentalsJob.cs`
  Run against a synthetic file list. Useful before drafting a contract — lets
  you see which areas the work would span.

- `/cross-impact <path> --json`
  Emit machine-readable JSON instead of human text. Useful when chaining the
  output into another tool.

- `/cross-impact <path> --no-cache`
  Bypass the content-hash cache and force a fresh scan.

## What it does

1. Resolves the input to a list of file paths (via the contract's
   `## Files to touch` section or the comma-separated list).
2. Runs three signal scans:
   - **CodeGraph signal** (weight 3): shells out to the `codegraph` CLI if
     present and parses its impact data. Falls back gracefully when
     CodeGraph is unavailable or the impact subcommand is missing.
   - **JOURNAL co-occurrence** (weight 2): greps `.claude/registries/JOURNAL.md` and `JOURNAL/*.md` (the domain files) for
     entries whose source contract or tags reference the contract's primary
     area, then maps each match's source contract to its own area set.
   - **MECHANISMS co-citation** (weight 1): for each mechanism the contract
     reuses, greps `.claude/registries/MECHANISMS.md` and `MECHANISMS/*.md` (the domain files) and pulls file path tokens
     from the surrounding description; matches them through area patterns.
   - **Seed adjacency** (weight 1): reads optional `seed_adjacency` field
     per area in `.claude/area-mapping.json`.
3. Aggregates per area; areas with score >= 2 (the noise floor) survive.
4. Returns the top 3 by score (ties broken alphabetically).

## Output

Each line: `<area-slug>\t<score>\t<signal-breakdown>`

Example:

```
warning: codegraph CLI present but `impact` subcommand failed on all inputs ...
primary: ingestion-job
signalr-hub                7  codegraph(3)+journal(2)+mechanism:IExternalDataDispatcher(1)+seed:ingestion-job(1)
admin-ui-ingestion-dashboard  4  codegraph(3)+mechanism:ProviderCallLog(1)
data-element               2  journal(2)
```

When no signal clears the threshold:

```
primary: ingestion-job
(no adjacent areas above threshold)
```

## When to use this skill vs. let data-architect run it

- **data-architect Step 4.5** runs the scan automatically during `/design-first`
  drafting. The output lands in the contract's `## Adjacent Areas` table.
- **`/cross-impact`** is for exploration BEFORE drafting, or for second-guessing
  what `data-architect` chose to put in the table. The skill never writes to
  any contract — it only prints to stdout.

## Implementation

```
py -3 .claude/scripts/cross_area_scan.py <args>
```

The skill is a thin shell over the script. See the script's module docstring
for the full signal model, scoring weights, threshold, and cache behavior.
