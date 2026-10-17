---
type: Skill
name: mcp-ai-wpoos-model-foundry
description: "Operational guide for the NV oOS Model Foundry (Proposal 067) — the cluster fine-tuning flywheel. Phase 1 shipped: the Corpus Foundry (Pro addon, addons/pro/includes/model-foundry/) — consent-gated, deduplicated, PII-scrubbed corpus exporters (trajectory_v1, preference_v1, docs_v1) with deterministic holdout splits and R12 provenance manifests. Covers the governance contract, row schemas, output layout, filter seams, the registration pattern for foundry tool slices, how to add a new exporter, and the test/validation gates. Use when extending the Corpus Foundry, debugging corpus exports, wiring a new data source, or continuing Phases 2–6 (train-worker, registry/serving, eval gate, fleet sharing)."
license: Proprietary. See LICENSE.txt
metadata:
  plugin: mcp-ai-wpoos
  plugin-version: "1.2.3"
  plugin-version-tested: "1.2.3"
  last-updated: "2026-10-11"
---

# NV oOS Model Foundry — Corpus Foundry (Phase 1)

Operational playbook for the **Corpus Foundry** slice of the Model Foundry
(Proposal 067). Distilled from the Phase 1 implementation
(`feature/model-foundry`): the consent-gated pipeline that turns harness
traces, preference pairs, and docs-hub markdown into versioned,
trainer-agnostic fine-tuning corpora. Phases 2–6 (train-worker sidecar,
registry/serving, eval gate, automation) append to this skill as they land.

Key docs: [proposal](../../docs/project/proposals/067-cluster-fine-tuning-model-foundry.md) ·
[implementation plan](../../docs/project/proposals/067-cluster-fine-tuning-model-foundry-implementation-plan.md) ·
[feature doc](../../docs/features/model-foundry.md) ·
[folder README](../../addons/pro/includes/model-foundry/README.md).

## 1. Component map

| Component | File | Role |
|---|---|---|
| `WP_MCP_AI_Corpus_Schema_Registry` | `addons/pro/includes/model-foundry/class-wp-mcp-ai-corpus-schema-registry.php` | Versioned row schemas + validation |
| `WP_MCP_AI_Corpus_Deduper` | `…/class-wp-mcp-ai-corpus-deduper.php` | Exact → fuzzy → opt-in semantic dedup |
| `WP_MCP_AI_Corpus_Pii` | `…/class-wp-mcp-ai-corpus-pii.php` | Deterministic PII scrub + provider-backed seam |
| `WP_MCP_AI_Corpus_Governance` | `…/class-wp-mcp-ai-corpus-governance.php` | Consent, pipeline order, holdout split, manifest, guarded writes |
| `WP_MCP_AI_Preference_Pair_Store` | `…/class-wp-mcp-ai-preference-pair-store.php` | Bounded FIFO DPO pair store |
| `WP_MCP_AI_Tool_Export_Trajectory_Corpus` | `…/class-wp-mcp-ai-tool-export-trajectory-corpus.php` | `export_trajectory_corpus` |
| `WP_MCP_AI_Tool_Export_Preference_Pairs` | `…/class-wp-mcp-ai-tool-export-preference-pairs.php` | `export_preference_pairs` |
| `WP_MCP_AI_Tool_Export_Plugin_Docs_Corpus` | `…/class-wp-mcp-ai-tool-export-plugin-docs-corpus.php` | `export_plugin_docs_corpus` |

Registration: `model-foundry-init.php` hooks `wp_mcp_ai_pro_tools`; the
`model_foundry` module in `addons/pro/includes/class-wp-mcp-ai-pro-module-registry.php`
requires it. Slugs live in the `ai_ml` preset of
`includes/helpers/class-wp-mcp-ai-tool-presets-helper.php`.

## 2. Non-negotiable contracts

- **Consent fails closed.** Post meta `_wp_mcp_ai_training_consent` = `'1'`
  grants consent; absent/other → `WP_Error( 'wp_mcp_ai_training_consent_required' )`
  **before any source data is read**. Site-level override:
  `wp_mcp_ai_model_foundry_assistant_consented` filter (bool; null = use meta).
  The admin UI for the meta ships in Phase 3 — until then the filter is the
  operational path.
- **Pipeline order is fixed:** per-case caps → exact dedup → fuzzy dedup →
  (opt-in) semantic dedup → PII scrub → deterministic holdout split → R12
  manifest → guarded write. Never reorder without the ADR.
- **Holdout split** is `md5(canonical row) % 5 == 0` → holdout (~20%),
  computed **after** dedup. Holdout rows are never written into `train.jsonl`;
  the split is stable across exports (decontamination by construction).
- **Skip, never truncate.** Named skip reasons (`skipped_too_large`,
  `skipped_no_user_input`, `skipped_low_margin`, `skipped_invalid_row`) — a
  truncated row would poison the corpus.
- **Exporters never call the chat model.** Semantic dedup is the only
  provider-bound path (embeddings), opt-in via `semantic_dedup`, capped, and
  filter-seamed (`wp_mcp_ai_model_foundry_embed_text`).

## 3. Row schemas

| Schema | Format | Shape |
|---|---|---|
| `chat_v1` | `openai_chat_jsonl` | `{"messages":[{role,content},…]}` |
| `trajectory_v1` | `openai_chat_jsonl` | tool-calling rows: assistant `tool_calls` + `role:tool` answers + final assistant content |
| `preference_v1` | `openai_preference_jsonl` | DPO: exactly `prompt`/`chosen`/`rejected` strings (R4, no lists) |
| `docs_v1` | `text_jsonl` | `{"text", "meta":{source,path,hash,bytes}}` |

New shapes get a **new key**, never a mutated one.

## 4. Output layout

```
wp-content/uploads/mcp-ai/model-foundry/<assistant_id>/<corpus_id>/
    train.jsonl / holdout.jsonl / manifest.json / .htaccess / index.php
```

`corpus_id` = `{schema}-{Ymd-His}`. The manifest is written **last** so its
presence signals a complete corpus — shard metadata must be attached to the
manifest payload *before* the file write (the Phase-1 bug: the manifest file
was written with `shards: []` because the envelope was updated after the
write — tests assert the file and envelope agree).

## 5. Filter seams

| Hook | Purpose |
|---|---|
| `wp_mcp_ai_model_foundry_assistant_consented` | Consent override |
| `wp_mcp_ai_model_foundry_embed_text` | Semantic-dedup embedding callable |
| `wp_mcp_ai_model_foundry_extra_scrub` | Provider-backed free-text PII scrub |
| `wp_mcp_ai_model_foundry_run_user_prompt` | User prompt for retrieval-less trace runs |
| `wp_mcp_ai_model_foundry_preference_pairs` | Contributed preference pairs |
| `wp_mcp_ai_model_foundry_trajectory_per_case_char_cap` | Trajectory row size cap |
| `wp_mcp_ai_model_foundry_docs_per_file_char_cap` | Docs per-file size cap |

## 6. Data-source facts (verified against the code)

- **Trace runs** (`WP_MCP_AI_Harness_Trace_Store`): artifacts per run are
  `tool_calls.jsonl`, `model_response.txt`, `retrieval.json` (has `query`),
  `profile.json`, `cost.json`, `self_refine.json`, `reasoning_trace.json`,
  `dspark.json`. **User prompts are NOT stored** — the trajectory exporter
  uses the retrieval query, falling back to the run-user-prompt filter.
  `list_runs()` caps at **100** runs (newest first) — do not advertise a
  higher `max_runs`.
- **Preference pairs** have no pre-existing store with full chosen/rejected
  text (eval run stores keep summaries only) — `WP_MCP_AI_Preference_Pair_Store::record()`
  is the intake API; chat-UI thumbs and eval-based rejection sampling wire in
  during later phases.
- **Docs source** default is `wp_upload_dir()['basedir'] . '/nvoos-docs-hub/content'`
  (`NV_oOS_Docs_Hub_Plugin::uploads_docs_dir()` when active). Explicit `dir`
  arguments must realpath inside the uploads basedir (symlink-escape hardened);
  `.md`/`.markdown`/`.txt` only; dotfiles and `vendor`/`node_modules`/`.git`
  skipped.

## 7. Adding a new exporter (checklist)

1. New tool class in `addons/pro/includes/model-foundry/` implementing the
   four interfaces (canonical envelope, two-gate sanitisation,
   `manage_options`, flags `pro/read-only/local-only/idempotent/cacheable`).
2. Register in `model-foundry-init.php` (`wp_mcp_ai_pro_tools` map).
3. Add the slug to the `ai_ml` preset in
   `includes/helpers/class-wp-mcp-ai-tool-presets-helper.php`
   (pattern 58 — the all-tools-accounted-for gate).
4. **No coverage-manifest entry** — the manifest test only scans
   `includes/tools` + `addons/pro/includes/tools`; foundry tools follow the
   harness-slice precedent (folder outside `tools/`, no manifest row).
5. Consent first: `WP_MCP_AI_Corpus_Governance::assert_consent()` before any
   source read.
6. Route rows through `WP_MCP_AI_Corpus_Governance::build()` — never hand-roll
   dedup/scrub/split/write.
7. Tests in `addons/pro/tests/test-model-foundry-*.php` — include dry-run
   shape assertions, capability gate, consent fail-closed, skip accounting,
   and shard/manifest agreement.
8. Update the folder README + this skill + `docs/features/model-foundry.md`.

## 8. Validation gates (the commands that ran green)

```bash
# phpcs (root standard covers Pro; the CI gate counts ERRORS):
php vendor/bin/phpcs --standard=phpcs.xml.dist --error-severity=1 --warning-severity=0 \
  --report=summary addons/pro/includes/model-foundry/ <other changed files>

# PHPUnit — WP 6.9 (primary) and WP 7.1 (second validation), cross-worktree runner:
MSYS_NO_PATHCONV=1 docker run --rm \
  -e WP_CORE_DIR=/var/www/html -e WP_DB_HOST=db -e WP_DB_NAME=wordpress_test \
  -e WP_DB_USER=wordpress -e WP_DB_PASSWORD=wordpress \
  -v oos-wp_wp_core:/var/www/html \
  -v F:/GITHUB/mcp-ai-wpoos:/var/www/html/wp-content/plugins/mcp-ai-wpoos \
  -v mcp-ai-wpoos-vendor:/var/www/html/wp-content/plugins/mcp-ai-wpoos/vendor \
  --network oos-wp_default wordpress:6.9-php8.2-apache \
  sh -c 'cd /var/www/html/wp-content/plugins/mcp-ai-wpoos && php -d memory_limit=1G vendor/bin/phpunit \
    addons/pro/tests/test-model-foundry-governance.php \
    addons/pro/tests/test-model-foundry-exporters.php --no-coverage'
# WP 7.1: swap WP_CORE_DIR=/tmp/wp71 + WP_DB_NAME=wordpress_test_wp71 and mount
# the mf-wp71-core volume (see the mcp-ai-wpoos-test-suite skill, "When /tmp/wp71 is gone").
```

Baseline: 33 tests / 156 assertions on both WP 6.9 and WP 7.1.3; regression
batch (`test-harness-fine-tune-curriculum` + `test-workflow-suggestion-miner`
+ `test-tool-registry-coverage`) 36/36 on both.

## 9. Gotchas

- **Holdout-split flake in tests:** with a single row, it lands in either
  shard — assert shard-agnostically (sum of `rows.train` + `rows.holdout`,
  or read whichever shard file exists). Never assert `train.jsonl` contains
  a specific single row.
- **Filesystem fixture accumulation** (test-suite pattern 71): tests scanning
  the fixed docs-hub dir must wipe it first (`wipe_dir()` + `$cleanup_dirs`
  in `tearDown`), or pass `uniqid()`-suffixed explicit dirs.
- **Manifest/shards ordering:** attach `shards` to the manifest array before
  `write_corpus()` encodes the file — the envelope and the file must agree.
- **`max_runs` honesty:** the trace store caps at 100 regardless of schema;
  keep tool schemas ≤ 100.

## 10. References

- Proposal + plan + feature doc (top of this file)
- `mcp-ai-wpoos-test-suite` skill — Docker runners, patterns 57/58/71
- `docs/features/llm-harness.md` — Layers A–H the foundry builds on
- `mcp-ai-wpoos-toolkit-creation` skill — full toolkit path (the foundry is a
  tool *slice*, not a toolkit: no SA Toolkit Manager surface, no WP-CLI
  commands yet)
