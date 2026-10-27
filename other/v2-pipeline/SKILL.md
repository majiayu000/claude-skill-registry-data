---
name: v2-pipeline
description: Run all enabled V2 subsystems (§11-§24) against per-target snapshot DB — storage taint, origin trust, DOM clobbering, proto-pollution, parser context, deobfuscation, corpus patterns, sink reachability, auth abuse, worker semantics. Run after async-edges + browser-context-infer, before chain-bestfirst.
---

# v2-pipeline

## Purpose

Single driver that walks every V2 subsystem in plan order, calling
each module's ``run(conn, target_dir)`` against the per-target DB.
Each subsystem persists its own tables / sidecar JSON and tags
relevant nodes so downstream extractors and scorers see them.

Plan reference: ``plans/ARCHITECTURE_EVOLUTION_V2.md``.

## What lands

### Stages and their outputs

| Stage | Env flag (default) | Tables | Sidecar |
|---|---|---|---|
| parser_context | `JS_ENABLE_PARSER_CONTEXT=1` (on) | `sink_contexts` | `sink_contexts.json` |
| persistent_taint | `JS_ENABLE_PERSISTENT_TAINT` (off) | `storage_events`, `storage_edges`, source-tag rows | `persistence_edges.json` |
| origin_trust | `JS_ENABLE_ORIGIN_TRUST` (off) | `origin_validations`, `post_messages`, source/sink tag rows | `origin_trust_graph.json` |
| dom_clobber | `JS_ENABLE_DOM_CLOBBER` (off) | `global_reads`, `clobber_candidates` | `clobber_candidates.json` |
| pp_gadgets | `JS_ENABLE_PP_GADGETS` (off) | `implicit_lookups`, `pp_gadgets` | `pp_gadgets.json` |
| deobfuscation_normalize | `JS_ENABLE_DEOBFUSCATION_NORMALIZE` (off) | `obfuscation_evidence` | `obfuscation_report.json` |
| corpus_patterns | `JS_ENABLE_CORPUS_PATTERNS` (off) | — (chain rows annotated post-hoc) | `corpus_matches.json` |
| sink_reachability | `JS_ENABLE_SINK_REACHABILITY` (off) | `sink_lifecycle`, `route_map` | `sink_reachability.json` |
| auth_abuse | `JS_ENABLE_AUTH_ABUSE` (off) | `auth_state_nodes`, `token_provenance` | `auth_abuse.json` |
| worker_semantics | `JS_ENABLE_WORKER_SEMANTICS` (off) | `worker_pairs`, `worker_messages` | `worker_semantics.json` |

### Stages handled by their own drivers (not v2_pipeline.py)

- `query_dsl` — Python-embedded DSL for analyst queries. Import
  `from modules.js_analyzer.v2.query_dsl import Q`.
- `chain_compression` — pre-LLM canonicalizer. Apply via
  `compress_chain(chain)` to any chain dict before LLM emission.
- `delta_scan` — `from modules.js_analyzer.v2.delta_scan import
  compute_delta` for incremental re-audit.
- `multi_target_corr` — fingerprint persistence under `~/.tlx/corr/`.

## When to run

After `js-index` + `db-isolate snapshot` + `implicit-tags` +
`async-edges` + `browser-context-infer`. Before `chain-bestfirst` /
`extract_chains_bounded` so the new tables / tags influence chain
scoring.

## Steps

```bash
# 0. (Recommended) Generate per-target flag recommendations from
#    detected frameworks + chain sink/source distribution. Reads
#    index/frameworks.json + chains/triage.json + a cheap source scan.
#    Writes targets/<target>/v2_flags.env (sourceable).
python3 bin/recommend_v2_flags.py <target>
source targets/<target>/v2_flags.env

# 1. Run only the env-enabled stages (the recommended set just sourced).
python3 bin/v2_pipeline.py <target>

# Force every stage on for this run (useful for benchmarking)
python3 bin/v2_pipeline.py <target> --all

# Run a specific subset
python3 bin/v2_pipeline.py <target> --only parser_context,persistent_taint,origin_trust

# Re-run best-first with V2 outputs incorporated
JS_ENABLE_SINK_VIABILITY=1 JS_ENABLE_SANITIZER_REALITY=1 \
    python3 bin/extract_chains_bestfirst.py <target>
```

The recommender lists each enabled flag with a one-line reason, and
also writes `status.json.phases.v2_recommend` so subsequent sessions
can resume without re-running it.

## Output JSON shape

```json
{
  "schema_version": "v2.1",
  "stages": {
    "parser_context":    {"classified": 412, "by_context_class": {...}},
    "persistent_taint":  {"events": 84, "pairs": 17, "reader_tags": 12, ...},
    ...
  },
  "stages_enabled_snapshot": {...},
  "target": "<name>",
  "elapsed_s": 4.221
}
```

## Boundary conditions

- Missing per-target DB → exit 2 with status error appended.
- Missing source-tree (used by `origin_trust` + `sink_reachability` to
  classify validation expressions / lifecycle phases) → those stages
  still run but their detail fields are partial.
- A stage's `error` field appearing in the JSON output means that one
  stage crashed; other stages still attempted. Exit code remains 0 to
  avoid blocking the pipeline on a single regression.

## Activation guidance

| Engagement type | Recommended stages on |
|---|---|
| SPA with embedded iframes / OAuth widgets | parser_context, origin_trust, persistent_taint |
| Heavy DOMPurify usage | parser_context, dom_clobber, pp_gadgets |
| Enterprise SaaS with role-gated features | parser_context, sink_reachability, auth_abuse |
| PWA / offline-first | parser_context, persistent_taint, worker_semantics |
| Heavily-minified bundle | parser_context, deobfuscation_normalize |
| Recurring vendor SDK in scope | parser_context, multi_target_corr (separate driver) |

When in doubt: `--all`. Each stage is bounded; total budget for the
14-stage sweep on a 2 k-file target is around 5-10 seconds.
