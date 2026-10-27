---
name: naming-heuristic
description: Function-name regex seeder for implicit sinks/sources missed by taxonomy + closure expander. Off by default (--enable required). Use when target has sourcemaps or un-obfuscated bundles. Run after js-index + db-isolate.
---

# naming-heuristic

## Purpose

Catch security-relevant wrapper functions whose names announce
their behaviour (`renderHTML`, `unsafeInject`, `getQueryParam`,
`handleMessageData`, …) but which the regex taxonomy misses because
they don't textually contain a known primitive. Closure-expansion
(`implicit-tags`) also misses these when the wrapper IS the primitive
at the call-site level — i.e. it doesn't internally call a tagged
function.

Confidence 0.3-0.4 is intentionally LOWER than implicit-closure
(0.49 at hop=2) so the chain-triage scoring multiplier
(`src_conf × sink_conf`) buries naming-rooted chains below
closure-rooted ones. They only surface to `hot.jsonl` when no
higher-confidence chain is available.

## When to run

**Opt-in.** Default `--enable` is OFF (script is dry-run-only). Run on:
- Targets with restored sourcemaps where function names retain
  natural-language semantics.
- Targets where the regex taxonomy + implicit-closure pass yielded
  weak coverage and audit budget remains.

Skip on:
- Heavily minified production bundles. Symbol names like `eu`,
  `aa`, `M` can't match heuristic patterns; running just wastes time.
- Targets where audit budget is already exhausted by direct chains.

## Inputs

- `targets/<name>/db/js_analyzer.db` (per-target snapshot).
- Optional `--rules <name>[,<name>...]` to scope to a subset.
- Optional `--min-confidence 0.0` floor.

## Steps

1. **Dry-run first** to gauge candidate count + rule distribution.
   ```bash
   python3 bin/naming_heuristic.py <target_name>
   ```
   Inspect `by_rule` and `by_kind`. If `from_message` dominates with
   hundreds of hits on a non-message-heavy target, the heuristic is
   matching false patterns; restrict via `--rules render_html,
   unsafe_html,read_query`.

2. **Enable + persist** when satisfied with the dry-run breakdown.
   ```bash
   python3 bin/naming_heuristic.py <target_name> --enable
   ```
   Appends to `tags_discovered.jsonl` and inserts
   `source='implicit_naming'` rows into the per-target DB. Idempotent
   — prior `implicit_naming` rows are cleared before re-insert.

3. **Re-run chain extraction** to pick up new tags:
   ```bash
   python3 bin/extract_chains_bounded.py targets/<name>
   ```
   The 2-pass scheduler already handles confidence-aware ordering;
   naming chains will land in pass 2 only if direct chains haven't
   filled the cap.

## Rules

| name | kind | conf | pattern intent |
|------|------|------|----------------|
| render_html | sink | 0.40 | render/set/append/inject/write + (Raw)?(Html\|HTML\|Markup) |
| unsafe_html | sink | 0.35 | `unsafe.*(html|markup|inject)`, `raw.*(html|markup)` |
| dangerous_eval | sink | 0.30 | run/exec/eval + (User\|Raw\|Dynamic)?(Code\|Script\|Expression)? |
| redirect_to | sink | 0.30 | redirect/navigate/goTo/open + (To)?(Url\|Page\|External)? |
| read_query | source | 0.40 | get/read/parse/extract + …(Query\|Param\|Hash\|Search\|Url)Param |
| user_input | source | 0.35 | get/read + …(User\|External\|Raw\|Untrusted)(Input\|Data\|Value) |
| from_storage | source | 0.30 | read/load/get/restore + (LocalStorage\|SessionStorage\|Cookie\|Hash\|Fragment) |
| from_message | source | 0.30 | handle/on/process + …(Message\|PostMessage\|Event)(Data)? |

All patterns are case-insensitive and anchored against the *bare* function
name (last segment after `.`).

## Outputs

```
targets/<name>/
├── tags_discovered.jsonl       # appended (NOT overwritten) with HeuristicTag rows
└── db/js_analyzer.db           # node_tags rows added with source='implicit_naming'

status.json.phases.naming_heuristic
  ├── status: done
  ├── candidate_count
  ├── by_kind: {sink, source}
  ├── by_rule: {<rule_name>: count}
  ├── inserted, cleared, elapsed_s
  └── rules_enabled
```

## Failure modes / pitfalls

- **Minified bundle FP**: short symbol names (`eu`, `M`, `aa`) won't
  match the heuristics. Output is harmless empty set; no rollback
  needed.
- **`from_message` over-fire**: catches React event handlers
  (`handleMessage`, `onMessage`) that AREN'T cross-frame
  postMessage. Restrict with `--rules` if your target uses many
  internal `Message` events.
- **Naming → real sink override**: heuristic confidence (0.3-0.4) is
  below implicit-closure (0.49). If a function has BOTH a naming
  match and an implicit-closure tag, the closure tag wins via the
  highest-confidence-per-(node, taxonomy_id) tie-break in
  `extract_chains_bounded._load_nodes_tags`.

## Plan reference

Phase 4 of `project_implicit_tags_plan.md`. Independent of Phase 1
(closure expander) and Phase 2 (sanitizer-on-path); can run in any
order against the same per-target DB.
