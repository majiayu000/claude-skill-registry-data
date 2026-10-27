---
name: bucket-inversion
description: Seed untagged sibling methods as implicit sinks/sources when N>=3 siblings share a tag for the same taxonomy_id. Targets coverage gaps missed by regex + AST + closure-expansion. Run after js-index + db-isolate, optionally after implicit-tags + naming-heuristic.
---

# bucket-inversion

## Purpose

Pattern: a class has 5 `render*` methods; 3 are tagged `innerHTML_assign`
via regex/AST; the other 2 likely also reach `innerHTML_assign` but
weren't tagged because their bodies passed the user-controlled value
into a wrapper the static analyzer didn't follow. Bucket inversion
seeds those siblings as derived sinks at confidence 0.5 — between
implicit_naming (0.3-0.4) and implicit_closure-hop1 (0.7) — so the
chain-triage scorer doesn't dilute the hot list while still surfacing
the missed coverage in `all.jsonl`.

## When to run

After `js-index` + `db-isolate` snapshot. Can run before or after
`implicit-tags` / `naming-heuristic`; by default it ignores other
implicit sources when counting sibling density (so implicit tags
can't snowball into bucket tags). Pass
`--count-implicit-siblings` to relax that.

Skip if:
- Target bundle is heavily minified and most functions have
  `parent=null` (no class context). Bucket inversion only operates
  on (file, parent) tuples; output will be near-zero.
- The target is already over-tagged (audit budget exhausted).

## Inputs

- `targets/<name>/db/js_analyzer.db` (per-target snapshot).
- Flags: `--min-siblings 3`, `--confidence 0.5`,
  `--count-implicit-siblings`, `--dry-run`.

## Steps

1. **Dry-run.**
   ```bash
   python3 bin/bucket_inversion.py <target_name> --dry-run
   ```
   Inspect `by_taxonomy_top`. If a category is unexpected (e.g.
   `sanitizer_*` taxonomies — sanitizers aren't really inferable
   from siblings), restrict by patching the script or accept the
   noise (low confidence demotes it).

2. **Persist.**
   ```bash
   python3 bin/bucket_inversion.py <target_name>
   ```
   Inserts `source='implicit_bucket'` rows + appends to
   `tags_discovered.jsonl`. Idempotent — prior `implicit_bucket`
   rows are cleared first.

3. **Re-run chain extraction** if you ran bucket inversion AFTER
   `extract_chains_bounded.py`:
   ```bash
   python3 bin/extract_chains_bounded.py targets/<name>
   ```

## Algorithm

1. Group all nodes of kind `function`/`arrow`/`method` by
   `(file, parent)`. NULL parent excluded.
2. For each group with `>= min_siblings + 1` members:
   - Count direct (non-`implicit_*`) tags per taxonomy_id across
     members.
   - Any taxonomy with `>= min_siblings` tagged members triggers
     inference.
3. For each triggering taxonomy, every untagged sibling gets a
   `BucketTag` with:
   - `confidence = --confidence` (default 0.5).
   - `evidence = {rule: "sibling_density", file, parent,
     tagged_siblings: N, total_siblings: M}`.
4. Dedup against ALL existing tags (including other implicit
   sources) so we never duplicate a (node, taxonomy) pair.

## Outputs

```
targets/<name>/
├── tags_discovered.jsonl       # appended with BucketTag rows
└── db/js_analyzer.db           # node_tags: source='implicit_bucket', conf=0.5

status.json.phases.bucket_inversion
  ├── status: done
  ├── discovered, by_kind, by_taxonomy_top
  ├── inserted, cleared, elapsed_s
  ├── min_siblings, confidence
  └── ts
```

## Failure modes

- **Minified bundles**: most fns have NULL parent → empty output.
  Not a failure, just no signal.
- **Over-fire on uninteresting taxonomies** (e.g. `sanitizer_*`,
  `JSON_parse_call` as a source): the low 0.5 confidence demotes
  these in chain scoring. If they still leak into `hot.jsonl`,
  bump `--min-siblings 4` or use `--confidence 0.4`.
- **Snowball protection**: `direct_only=True` (default) prevents
  implicit-source tags from driving more implicit tags. Override
  with `--count-implicit-siblings` only when you want a 2-stage
  inference (after closure expansion + naming).

## Plan reference

Phase 5 of `project_implicit_tags_plan.md`. Final phase of the
implicit-tags build. Combined with Phase 1 (closure) + Phase 4
(naming), provides three independent inference paths over the same
callgraph, each with distinct confidence bands so chain triage stays
direct-dominant by default but can fall back to inferred chains when
audit budget remains.

## Calibration (coolblue-intigriti)

| Metric | Value |
|---|---|
| candidates discovered | 28 |
| by kind | 8 sink, 17 source, 3 sanitizer |
| dominant taxonomies | JSON_parse_call (13), postMessage_send (8) |
| runtime | 0.22s |

Modest signal on this target because most functions are file-level
(no parent class). React class components / Vue SFCs / Angular
services produce richer groups.
