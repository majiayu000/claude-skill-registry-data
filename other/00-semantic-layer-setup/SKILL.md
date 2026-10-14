---
name: semantic-layer-setup
description: >
  End-to-end orchestrator for building the Databricks semantic layer including Metric Views,
  Table-Valued Functions (TVFs), and Genie Spaces. Guides users through
  metric view creation, TVF development, Genie Space setup, and API-driven deployment.
  Orchestrates mandatory dependencies on semantic-layer skills
  (metric-views-patterns, databricks-table-valued-functions, genie-space-patterns,
  genie-space-export-import-api) and common skills
  (databricks-asset-bundles, databricks-expert-agent, databricks-python-imports).
  Use when building the semantic layer end-to-end, creating Metric Views and TVFs for Genie,
  or setting up Genie Spaces.
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: jobs
deploy_verb: bundle_deploy
deploy_note: "Combined semantic_layer_job (Metric Views -> TVFs -> Genie) deployed via `bundle deploy --target dev` from the bundle-folder page; Genie Spaces follow the RULE_8 tier model (see 04-genie-space-export-import-api). On Genie Code the deploy verb runs through runDatabricksCli. Write generated metric-view YAML / TVF SQL under the cloned repo root (`{REPO_ROOT}` = `state_file_root` from `skills/vibecoding-state`), not a bare relative path \u2014 relative paths resolve against the page CWD (see `skills/genie-code-environment` \u00a78)."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "1.0.0"
  domain: semantic-layer
  role: orchestrator
  pipeline_stage: 6
  pipeline_stage_name: semantic-layer
  next_stages:
    - observability-setup
  workers:
    - metric-views-patterns
    - databricks-table-valued-functions
    - genie-space-patterns
    - genie-space-export-import-api
  common_dependencies:
    - databricks-asset-bundles
    - databricks-expert-agent
    - databricks-python-imports
    - naming-tagging-standards
    - databricks-autonomous-operations
  consumes:
    - plans/manifests/semantic-layer-manifest.yaml
  consumes_policy: required  # STOP if manifest is missing — no self-discovery fallback
  dependencies:
    - metric-views-patterns
    - databricks-table-valued-functions
    - genie-space-patterns
    - genie-space-export-import-api
    - databricks-asset-bundles
    - databricks-expert-agent
    - databricks-python-imports
  last_verified: "2026-02-07"
  volatility: medium
  upstream_sources: []  # Internal orchestrator
---

# Semantic Layer Setup Orchestrator

End-to-end workflow for building the Databricks semantic layer — Metric Views, Table-Valued Functions, and Genie Spaces — on top of a completed Gold layer.

**Predecessor (acceleration mode):** `gold-layer-setup` skill — Gold tables must exist before this orchestrator deploys production semantic assets.

**Predecessor (workshop mode):** ANY of `bronze-layer-setup`, `silver-layer-setup`, `gold-layer-design`, or `gold-layer-setup`. Workshop mode builds Metric Views, TVFs, and Genie Spaces directly on top of whichever planning-source layer the manifest declares.

**Layer-aware workshop deployment (NEW):** This orchestrator now honors `planning_source.selected_layer` from the planning manifest:

- `deployed_gold` / `gold_design` — production path (existing behavior).
- `deployed_silver` / `deployed_bronze` — **workshop deployment is allowed**. The orchestrator prints an advisory (Genie quality caveats, Gold promotion recommended for production) and continues to build the semantic layer against the Silver/Bronze schema.
- `source_csv` — STOP. There are no live tables to query; the plan is a contract only.

The previous "stop before deployment for any non-Gold workshop draft" guardrail has been replaced with this layer-aware behavior. Acceleration-mode strict Gold rules are unchanged.

**Time Estimate:** 3-4 hours for initial setup, 1-2 hours per additional domain

**What You'll Create:**
1. Metric Views — YAML-based semantic definitions for each Gold table
2. Table-Valued Functions (TVFs) — parameterized SQL functions for Genie
3. Genie Spaces — configured with agent instructions, data assets, benchmark questions

## File Organization

| Artifact | Output Path (from repo root) |
|----------|------------------------------|
| Metric View YAML definitions | `src/{project}_semantic/metric_views/*.yaml` |
| Metric View creation script | `src/{project}_semantic/create_metric_views.py` |
| TVF SQL definitions | `src/{project}_semantic/table_valued_functions.sql` |
| Genie Space JSON configs | `src/{project}_semantic/genie_configs/*.json` |
| Genie deployment notebook | `src/{project}_semantic/deploy_genie_spaces.py` |
| Combined Asset Bundle job | `resources/semantic/semantic_layer_job.yml` |
| Bundle config additions | `databricks.yml` (sync + resource references) |

> `{project}` = project name from Asset Bundle variables (e.g., `wanderbricks`).

---

## Decision Tree

| Question | Action |
|----------|--------|
| Building semantic layer end-to-end? | **Use this skill** — it orchestrates everything |
| Only need Metric Views? | Read `semantic-layer/01-metric-views-patterns/SKILL.md` directly |
| Only need TVFs? | Read `semantic-layer/02-databricks-table-valued-functions/SKILL.md` directly |
| Only need Genie Space setup? | Read `semantic-layer/03-genie-space-patterns/SKILL.md` directly |
| Need Genie API automation? | Read `semantic-layer/04-genie-space-export-import-api/SKILL.md` directly |
| Authoring Discover domains / Pages / a routing Page (Genie Accelerator track)? | Read `semantic-layer/06-genie-discover-ontology/SKILL.md` directly — **standalone**, not a pipeline phase (UI-authored, no bundle deploy) |

### Routing Safety Net

> If a user asks to **deploy TVFs, Metric Views, and/or Genie Spaces** and `@`-references only leaf skills (e.g., `databricks-asset-bundles`, `genie-space-export-import-api`), **this orchestrator still applies**. Any task touching 2+ semantic-layer asset types must route here first — the leaf skills handle individual assets; this orchestrator handles Phase 0 (gold inventory), phase gates, and template-first workflow. Skipping it is the documented root cause of multi-cycle debug spirals.

---

## Mandatory Skill Dependencies

**CRITICAL: Before generating ANY code for the semantic layer, you MUST read and follow the patterns in these common skills. Do NOT generate these patterns from memory.**

| Phase | MUST Read Skill (use Read tool on SKILL.md) | What It Provides |
|-------|---------------------------------------------|------------------|
| All phases | `skills/databricks-expert-agent` | Core extraction principle: extract names from source, never hardcode |
| Metric Views | `common/databricks-python-imports` | Pure Python module patterns for helpers |
| Deployment | `skills/databricks-asset-bundles` | Job YAML, deployment patterns |
| All phases | `common/naming-tagging-standards` | Dual-purpose COMMENTs, v3.0 TVF comments, enterprise naming |
| Troubleshooting | `common/databricks-autonomous-operations` | Deploy → Poll → Diagnose → Fix → Redeploy loop when jobs fail |

### Semantic-Domain Dependencies

| Skill | Requirement | What It Provides |
|-------|-------------|------------------|
| `semantic-layer/01-metric-views-patterns` | **MUST read** at Phase 1 | YAML syntax, validation, joins, window measures |
| `semantic-layer/02-databricks-table-valued-functions` | **MUST read** at Phase 2 | STRING params, Genie compatibility, null safety |
| `semantic-layer/03-genie-space-patterns` | **MUST read** at Phase 3 | 8-section deliverable, agent instructions, SQL expressions, benchmark Qs |
| `semantic-layer/04-genie-space-export-import-api` | **MUST read** at Phase 3 (JSON config) and Phase 6 (API deployment) | REST API JSON schema, programmatic deployment |

### Enforcement: Confirm Common Skills Read (MANDATORY GATE)

**STOP. Before proceeding past Phase 0, confirm you have read the common skills by listing the key pattern from each:**

| Skill | Key Pattern to Confirm |
|-------|-----------------------|
| `databricks-python-imports` | Bundle root: `rsplit('/src/', 1)[0]` |
| `databricks-asset-bundles` | Job `base_parameters` must include all widget params |
| `databricks-expert-agent` | "Extract names from source, never hardcode" |
| `naming-tagging-standards` | CM-02 dual-purpose COMMENT with PURPOSE/BEST FOR/NOT FOR |

**If you cannot produce these patterns from memory, you have not read the skills. Read them now.** Skipping common skills is the #1 cause of downstream bugs in semantic layer setup (see retrospective evidence: fragile workspace paths, missing job parameters, wrong ID fields).

---

## 🔴 Non-Negotiable Defaults

| Default | Value | Applied Where | NEVER Do This Instead |
|---------|-------|---------------|----------------------|
| **Manifest required** | `plans/manifests/semantic-layer-manifest.yaml` | Phase 0 — before any implementation | ❌ NEVER create artifacts via self-discovery; STOP if manifest is missing |
| **Metric View syntax** | `WITH METRICS LANGUAGE YAML` | Every Metric View DDL | ❌ NEVER use non-YAML metric views |
| **TVF parameters** | All `STRING` type | Every TVF signature | ❌ NEVER use DATE, INT, or other non-STRING params (Genie incompatible) |
| **Genie warehouse** | Serverless SQL Warehouse | Every Genie Space | ❌ NEVER use Classic or Pro warehouse |
| **Benchmark questions** | Minimum 10 per Genie Space | Every Genie Space | ❌ NEVER deploy without benchmarks |
| **Column comments** | Required on all Gold tables | Before Genie Space creation | ❌ NEVER create Genie Space without column comments |

---

## Working Memory Management & Progressive Disclosure

This orchestrator spans 7 phases (0–6). To maintain coherence without context pollution, follow these progressive disclosure principles from [AgentSkills.io](https://agentskills.io/specification) and [Anthropic's context engineering guidance](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents):

### Just-in-Time Skill Loading (CRITICAL)

**DO NOT read all worker skills at the start.** Read each skill ONLY when you enter its phase:
- **Phase 1:** Read `01-metric-views-patterns/SKILL.md` → work → persist notes → **discard skill from working memory**
- **Phase 2:** Read `02-databricks-table-valued-functions/SKILL.md` → work → persist notes → **discard**
- **Phase 3:** Read `03-genie-space-patterns/SKILL.md` + `04-genie-space-export-import-api/SKILL.md` → work → persist notes → **discard**
- **Phase 4-6:** Read `skills/databricks-asset-bundles/SKILL.md` → work → done

Each worker skill ends with a "**Notes to Carry Forward**" section that tells you exactly what to persist for downstream phases. Use those notes — not the full skill content — as your handoff.

### Context Handoff Protocol

At each phase boundary, your working memory should contain ONLY:
1. **`gold_inventory` dict** (from Phase 0 — persists through all phases)
2. **Previous phase's "Notes to Carry Forward"** (structured summary of outputs)
3. **Current phase's worker skill** (read just-in-time)

**Discard** after each phase: full YAML bodies, SQL source code, complete JSON configs — they are on disk and retrievable via file paths in the notes.

### Phase Summary Notes

**After each phase, persist a brief summary note** capturing:
- **Phase 0 output:** Manifest loaded, planning_mode, artifact counts, **`gold_inventory` dict**
- **Phase 1 output:** Use "Metric Views Notes to Carry Forward" from `01-metric-views-patterns` (MV names, paths, grain, measure counts, composability notes)
- **Phase 2 output:** Use "TVF Notes to Carry Forward" from `02-databricks-table-valued-functions` (TVF names, paths, parameter signatures, domain assignments)
- **Phase 3 output:** Use "Genie Space Notes to Carry Forward" from `03-genie-space-patterns` (space names, JSON paths, asset counts, benchmark counts)
- **Phase 4 output:** Job YAML path, `databricks.yml` changes
- **Phase 5 output:** Deployment status, job run ID, task statuses
- **Phase 6 output:** API deployment status, space IDs for idempotent re-deployment

### Why This Matters

Context is a finite resource with diminishing marginal returns. Each worker skill is 400-600 lines. Loading all 4 workers simultaneously (~2000 lines) would consume your attention budget on content irrelevant to the current phase. Progressive loading keeps each phase focused on the smallest set of high-signal tokens needed for that phase's work.

---

## Phased Implementation Workflow

### Phase 0: Read Plan — MANDATORY (5 minutes)

**The semantic layer manifest is REQUIRED. Do NOT proceed without it.**

This orchestrator implements exactly what the project plan defined — no more, no less. The manifest `plans/manifests/semantic-layer-manifest.yaml` is generated by the `planning/00-project-planning` skill (stage 5) and serves as the implementation contract.

**🔴 If the manifest does not exist, STOP and tell the user:**
> *"The semantic layer manifest (`plans/manifests/semantic-layer-manifest.yaml`) is missing. This orchestrator requires a project plan to define which Metric Views, TVFs, and Genie Spaces to create. Please run the `planning/00-project-planning` skill first (stage 5), then return here."*

```python
import yaml
from pathlib import Path

manifest_path = Path("plans/manifests/semantic-layer-manifest.yaml")

if not manifest_path.exists():
    raise FileNotFoundError(
        "REQUIRED: plans/manifests/semantic-layer-manifest.yaml not found. "
        "Run planning/00-project-planning (stage 5) first to generate the "
        "semantic layer manifest, then re-run this orchestrator."
    )

with open(manifest_path) as f:
    manifest = yaml.safe_load(f)

# Respect planning mode — workshop mode means strict artifact caps
planning_mode = manifest.get('planning_mode', 'acceleration')
if planning_mode == 'workshop':
    print("⚠️  Workshop mode active — creating ONLY the artifacts listed in the manifest")
```

#### Phase 0 — Layer-Aware Manifest Read (NEW)

Read the layer-aware fields written by Planning Phase 0. These are additive and **only change behavior when present**:

```python
planning_source = manifest.get("planning_source", {})
selected_layer  = planning_source.get("selected_layer", "deployed_gold")
readiness       = manifest.get("implementation_readiness", "gold_ready")
requires_promo  = manifest.get("requires_gold_promotion", False)  # advisory only

# Schema selection — preserves the existing gold_schema-only flow when
# the manifest is Gold-based; differs only for non-Gold workshop runs.
catalog          = manifest.get("catalog")
gold_schema      = manifest.get("gold_schema")
semantic_schema  = manifest.get("semantic_schema") or gold_schema
silver_schema    = manifest.get("silver_schema")
bronze_schema    = manifest.get("bronze_schema")

# The schema we inspect for the inventory — Gold by default; for non-Gold
# workshop runs we inspect the actual planning-source schema.
SOURCE_SCHEMA_BY_LAYER = {
    "deployed_gold":   gold_schema,
    "gold_design":     gold_schema,         # YAML-driven; live schema may not exist
    "deployed_silver": silver_schema,
    "deployed_bronze": bronze_schema,
    "source_csv":      None,                # no live schema
}
inventory_schema = SOURCE_SCHEMA_BY_LAYER.get(selected_layer, gold_schema)

# --- Layer-aware policy ---
# Acceleration must always be Gold-based (Phase 0 of the planning skill enforces this).
if planning_mode == "acceleration" and selected_layer not in {"deployed_gold", "gold_design"}:
    raise RuntimeError(
        f"Acceleration mode received a non-Gold planning_source.selected_layer="
        f"`{selected_layer}`. This is a planning-skill bug; re-run planning."
    )

# Workshop + source_csv has no live tables to query — STOP.
if selected_layer == "source_csv":
    raise RuntimeError(
        "Semantic layer setup cannot run when planning_source.selected_layer is "
        "`source_csv`. The plan is a planning contract only — there are no live "
        "tables to build Metric Views, TVFs, or Genie Spaces against. "
        "Either deploy the underlying tables (run bronze/silver/gold setup against "
        "the source CSV first) and re-run planning, or run this orchestrator only "
        "after at least one live layer exists."
    )

# Workshop + Silver/Bronze: ALLOWED. Print advisory and continue.
if planning_mode == "workshop" and selected_layer in {"deployed_silver", "deployed_bronze"}:
    print(
        f"⚠ Workshop mode: building the semantic layer on top of `{selected_layer}` "
        f"(`{inventory_schema}`).\n"
        "  - Metric Views, TVFs, and Genie Space assets will reference this layer "
        "directly.\n"
        "  - Genie NL accuracy is typically lower than on Gold because raw "
        "Bronze/Silver tables often lack curated COMMENTs, dimensional joins, "
        "and pre-aggregated measures.\n"
        "  - For production, re-run planning with `planning_source.selected_layer="
        "deployed_gold` after promoting the relevant tables to Gold."
    )

if readiness == "gold_design_only":
    print("ℹ Manifest is gold_design_only — Gold YAML present but live Gold may not "
          "be deployed yet. Phase 0 inventory will use YAML; live-catalog checks "
          "are advisory.")
```

**Compatibility rules for the rest of the orchestrator:**

- For `selected_layer in {deployed_gold, gold_design}`: the existing YAML + live-catalog cross-reference flow runs unchanged.
- For `selected_layer in {deployed_silver, deployed_bronze}`: skip the YAML step entirely; build the inventory purely from `information_schema.columns` for `inventory_schema`. The dict shape is identical so downstream phases consume it the same way.
- `semantic_schema` (or per-artifact `target_schema`) is the deploy target for Metric Views and TVFs; `inventory_schema` is the **source** schema for queries. They may differ — never assume `inventory_schema == gold_schema`.
- `unified_genie_space` (singular, top-level): the orchestrator MUST check this BEFORE iterating per-domain `genie_spaces[]`. If present, create that single space and skip per-domain spaces (matches the existing manifest template).
- `requires_gold_promotion` is **advisory only** — it never gates deployment; it is a hint for production hardening.

**Workshop mode error handling:** When `planning_mode: workshop`, creation scripts should log failures but exit 0 to allow downstream tasks to run:

```python
if failures and planning_mode == "workshop":
    print(f"WARNING: {len(failures)} artifact(s) failed (workshop mode -- continuing)")
elif failures:
    raise RuntimeError(f"{len(failures)} artifact(s) failed")
```

```python
# Extract implementation checklist from manifest
domains = manifest.get('domains', {})
total_mvs, total_tvfs, total_genie = 0, 0, 0
for domain_name, domain_config in domains.items():
    mvs = domain_config.get('metric_views', [])
    tvfs = domain_config.get('tvfs', [])
    genie = domain_config.get('genie_spaces', [])
    total_mvs += len(mvs)
    total_tvfs += len(tvfs)
    total_genie += len(genie)
    print(f"Domain {domain_name}: {len(mvs)} MVs, {len(tvfs)} TVFs, {len(genie)} Genie Spaces")

print(f"\nTotal: {len(domains)} domains, {total_mvs} Metric Views, "
      f"{total_tvfs} TVFs, {total_genie} Genie Spaces")

# Validate summary counts match actual artifact counts
summary = manifest.get('summary', {})
assert total_mvs == int(summary.get('total_metric_views', total_mvs)), \
    f"MV count mismatch: {total_mvs} actual vs {summary.get('total_metric_views')} in summary"
assert total_tvfs == int(summary.get('total_tvfs', total_tvfs)), \
    f"TVF count mismatch: {total_tvfs} actual vs {summary.get('total_tvfs')} in summary"
assert total_genie == int(summary.get('total_genie_spaces', total_genie)), \
    f"Genie count mismatch: {total_genie} actual vs {summary.get('total_genie_spaces')} in summary"
```

**What the manifest provides:**
- `domains{}` — one entry per agent domain, each containing:
  - `metric_views[]` — name, source table, dimensions, measures, business questions
  - `tvfs[]` — name, parameters (all STRING), Gold tables used, business questions
  - `genie_spaces[]` — name, warehouse type, asset assignments, benchmark questions
- `summary` — expected artifact counts for validation
- `planning_mode` — `acceleration` (full) or `workshop` (capped artifacts; do NOT expand via self-discovery)

**Key principle:** Create ONLY the artifacts listed in the manifest. Do NOT add Metric Views, TVFs, or Genie Spaces beyond what the plan specified. If the plan missed something, update the plan first — then re-run this orchestrator.

**User-referenced file check:** If the user's request references specific plan addendum files (e.g., `plans/phase1-addendum-1.2-tvfs.md`), verify each exists before proceeding. **Always verify the filename against [`planning/00-project-planning/assets/addendum-numbering.md`](../../planning/00-project-planning/assets/addendum-numbering.md) — the canonical numbering table.** A common failure mode is referencing a stale name (e.g. `phase1-addendum-1.1-dashboards.md`) that no longer exists; the orchestrator must halt and prompt the user to reconcile, never silently skip.

If any referenced files are missing, inform the user:

> "The following referenced files do not exist: {list}. The manifest contains sufficient detail to proceed. Continue with only the manifest, or create these files first?"

Do NOT silently skip missing user-referenced files.

#### Planning-Source Inventory Extraction (Anti-Hallucination — MANDATORY)

**After the manifest check, build a verified `gold_inventory` dict before any artifact creation begins.** This dict is the ONLY source of table/column names for Phases 1-3. No artifact may reference a table or column not in this inventory.

> **Layer-aware naming note:** the variable is named `gold_inventory` for backward compatibility. Conceptually it is a **planning-source inventory** keyed off whatever layer the manifest's `planning_source.selected_layer` declares.

**Extraction strategy by selected layer:**

| `selected_layer` | YAML step | Live-catalog step | Cross-reference behavior |
|---|---|---|---|
| `deployed_gold` | Parse `gold_layer_design/yaml/{domain}/*.yaml` (table_name, columns, PK, FK) | Query `information_schema.columns` for `inventory_schema` (= `gold_schema`) | Mismatches are **fatal** (existing fail-loud behavior) |
| `gold_design` | Parse Gold YAML — authoritative | Best-effort query of `inventory_schema`; may return zero rows | Mismatches are warnings (Gold may not be deployed yet) |
| `deployed_silver` | **Skip YAML entirely** — Silver/Bronze do not have a curated YAML design library | Query `information_schema.columns` for `inventory_schema` (= `silver_schema`) | YAML step skipped; live catalog is the sole source of truth |
| `deployed_bronze` | **Skip YAML entirely** | Query `information_schema.columns` for `inventory_schema` (= `bronze_schema`) | YAML step skipped; live catalog is the sole source of truth |
| `source_csv` | (orchestrator stops earlier — never reaches this step) | — | — |

**Common live-catalog query:**

```sql
SELECT table_name, column_name, full_data_type
FROM {catalog}.information_schema.columns
WHERE table_schema = '{inventory_schema}'
```

**Build the `gold_inventory` dict:**

```python
gold_inventory = {
    "dim_customer": {
        "columns": {"customer_key": "BIGINT", "customer_name": "STRING", ...},
        "primary_key": ["customer_key"],
        "foreign_keys": []
    },
    "fact_sales": {
        "columns": {"sales_key": "BIGINT", "customer_key": "BIGINT", ...},
        "primary_key": ["sales_key"],
        "foreign_keys": [{"columns": ["customer_key"], "references": "dim_customer"}]
    }
}
```

**Gate:** The `gold_inventory` dict MUST be non-empty before proceeding to Phase 1.

- `deployed_gold`: both YAML and live catalog must agree (existing fail-loud behavior).
- `gold_design`: YAML alone may be the source of truth — warn-only when the live catalog is empty. If YAML is ALSO empty/missing, STOP.
- `deployed_silver` / `deployed_bronze`: live catalog must return at least the manifest-declared tables. If the catalog query is empty, STOP — the workshop layer was not actually deployed.

---

### Phase 0.5: Local Pre-Flight (MANDATORY, 10 minutes)

**Why:** Every hour spent in Phases 1–6 without pre-flight has produced an average of 3 deploy cycles in the retrospective. The four checks below run locally in ≤ 10 minutes and collectively catch ~80 % of the issues that cause a failed `bundle deploy`/`bundle run`. Do NOT skip — each of these has fixed a real outage.

**Context setup:** No new skills loaded. Use the Python and SQL you already have from Phase 0.

| # | Check | How | Fail-loud contract |
|---|---|---|---|
| 1 | **Variable enumeration** (dashboards, Metric Views, Genie configs) | `monitoring/02-databricks-aibi-dashboards/scripts/deploy_dashboard.py::enumerate_required_variables` — run against `src/dashboards/*.lvdash.json`, `src/semantic/metric_views/*.yaml`, and `src/genie_spaces/*.json`. | `RuntimeError` if any `${var}` is unresolved by the caller's variables dict. |
| 2 | **DDL smoke test** (Metric Views + TVFs) | Parse each `src/semantic/metric_views/*.yaml` and each TVF CREATE statement; run an `EXPLAIN` against a warehouse. Alternatively use `spark.sql("SELECT * FROM {view} LIMIT 0")` after a dry-run CREATE in a throwaway schema. | `RuntimeError` listing every failing artifact. |
| 3 | **Genie validator** | Run `semantic-layer/04-genie-space-export-import-api`'s `_assert_sql_arrays(space)` over every rendered Genie Space JSON. | `RuntimeError` on first serialized_space invariant violation. |
| 4 | **Live-catalog intersection** | Re-run the Phase 0 gold intersection from `planning/00-project-planning/SKILL.md` Phase 2 Step 6 against the fully-rendered semantic-layer manifest (post-variable-substitution). Catches late-added table/column references that never hit the planning manifest. | `RuntimeError` + regenerate `plans/gold-gap-remediation.md` if gap. |

**Orchestration recipe (paste into a scratch notebook or a `scripts/preflight.py`):**

```python
from pathlib import Path

# Check 1: dashboard + metric view + genie variable enumeration
from scripts.deploy_dashboard import enumerate_required_variables

variables = {"catalog": catalog, "gold_schema": gold_schema,
             "warehouse_id": warehouse_id, "feature_schema": feature_schema}

for pattern in ["src/dashboards/*.lvdash.json",
                "src/semantic/metric_views/*.yaml",
                "src/genie_spaces/*.json"]:
    files = list(Path(".").glob(pattern))
    required = enumerate_required_variables(files)
    missing = {n: fs for n, fs in required.items() if variables.get(n) in (None, "")}
    if missing:
        raise RuntimeError(
            f"[preflight/{pattern}] missing vars: "
            + ", ".join(f"{n} (used by {len(fs)} files)" for n, fs in missing.items())
        )

# Check 2: DDL smoke test — EXPLAIN every Metric View & TVF
#   (skip here — see references/pre-flight-ddl-smoke.md for the templates)

# Check 3: Genie serialized_space invariants
import json
from scripts.deploy_genie_spaces import _assert_sql_arrays, process_json_values
for gf in Path("src/genie_spaces").glob("*.json"):
    raw = json.loads(gf.read_text())
    rendered = process_json_values(raw, variables)
    _assert_sql_arrays(rendered)   # raises on any violation

# Check 4: Live-catalog intersection against the rendered manifest
#   (re-use the block from planning/00-project-planning/SKILL.md
#    Phase 2 Step 6 — do not duplicate it here)

print("✅ Phase 0.5 pre-flight passed — safe to proceed to Phase 1.")
```

**STOP Rule:** Every Phase 0.5 check failure must halt the orchestrator. Do not "run bundle deploy anyway to see what the cluster says" — every minute you spend in that loop is 10x the cost of fixing the pre-flight failure locally.

---

### Phase 1: Metric Views (1-2 hours)

**Context setup:** Read the skills below just-in-time. After this phase, persist the "Metric Views Notes to Carry Forward" and discard the full skill content.

| # | Skill Path | What It Provides |
|---|------------|------------------|
| 1 | `skills/databricks-expert-agent/SKILL.md` | Extract-don't-generate principle |
| 2 | `data_product_accelerator/skills/common/naming-tagging-standards/SKILL.md` | CM-02 dual-purpose COMMENT format for Metric Views |
| 3 | `data_product_accelerator/skills/common/databricks-python-imports/SKILL.md` | sys.path setup for creation script in Asset Bundle |
| 4 | `data_product_accelerator/skills/semantic-layer/01-metric-views-patterns/SKILL.md` | YAML syntax, validation, joins, composability, format types |

**Input:** For each domain in `manifest['domains']`, iterate over `domain['metric_views']`. Each entry defines `name`, `source_table`, `dimensions`, `measures`, and `business_questions`. Do NOT create Metric Views not listed in the manifest.

**Steps:**
1. Read `manifest['domains'][domain]['metric_views']` — this is your complete list of Metric Views per domain
2. For each entry, use the manifest's `source_table`, `dimensions`, and `measures` — cross-reference every column against `gold_inventory` (Phase 0)
3. **Validation gate:** For each YAML, apply ALL three validations:
   - **Column existence:** Verify every `dimensions[].column` and `measures[].column` exists in `gold_inventory[source_table]["columns"]`. Fail with explicit error listing unresolved references.
   - **Transitive join detection:** Inspect all join `on` clauses. If ANY join's `on` references a join alias instead of `source`, flag as transitive join error. Fix (preferred on the workshop runtime, DBR 17.1+ with 1:1 keys): restructure as **nested joins** (snowflake schema); or use denormalized columns (Fix 1). Use the subquery-source pattern only as the fallback for DBR < 17.1 or non-unique intermediate keys (see `01-metric-views-patterns` decision ladder).
   - **Format type validation:** Verify all measure `format.type` values are one of: `byte`, `currency`, `date`, `date_time`, `number`, `percentage`. Common mistakes: `percent` (use `percentage`), `decimal` (use `number`).
4. Create `create_metric_views.py` with sys.path setup from `databricks-python-imports`
5. Test each Metric View with sample queries
6. Track completion: check off each manifest entry as its Metric View is confirmed created

#### Phase 1 Completion Gate (MANDATORY)

**DO NOT proceed to Phase 2 until you have:**
1. Written all Phase 1 artifacts to disk
2. **Run the `create_metric_views` per-task verification row** from the "Per-task verification" table in Phase 5 *against a scratch dev target* — do not wait until the full bundle runs. Verifying now catches ~40 % of the defects that otherwise surface in Phase 5.
3. Presented the user with a summary: artifact names, paths, key design decisions
4. Asked: "Phase 1 is complete. Shall I proceed to Phase 2 (TVFs), or review/modify first?"

Bulk creation without checkpoints causes cascading failures. A 2-minute pause catches issues that take 30 minutes to debug post-deployment.

### Phase 2: Table-Valued Functions (1-2 hours)

**Context setup:** Discard Phase 1 skill content. Keep only `gold_inventory` + Phase 1's "Metric Views Notes to Carry Forward". Read the skills below just-in-time.

| # | Skill Path | What It Provides |
|---|------------|------------------|
| 1 | `skills/databricks-expert-agent/SKILL.md` | Extract TVF names/columns from `gold_inventory` |
| 2 | `data_product_accelerator/skills/common/naming-tagging-standards/SKILL.md` | CM-04 v3.0 structured TVF COMMENTs |
| 3 | `data_product_accelerator/skills/semantic-layer/02-databricks-table-valued-functions/SKILL.md` | STRING params, null safety, Genie compat, notebook_task deployment |

**Input:** For each domain in `manifest['domains']`, iterate over `domain['tvfs']`. Each entry defines `name`, `description`, `parameters` (all STRING), `gold_tables_used`, and `business_questions`. Do NOT create TVFs not listed in the manifest.

**Steps:**
1. Read `manifest['domains'][domain]['tvfs']` — this is your complete list of TVFs per domain
2. For each entry, use the manifest's `parameters` (ALL STRING) and `gold_tables_used` — cross-reference against `gold_inventory`
3. Implement TVFs with null safety and SCD2 handling
4. Add v3.0 bullet-point comments per `naming-tagging-standards` CM-04
5. **Validation gate:** Parse each TVF SQL to extract all table/column references. Verify every reference exists in `gold_inventory`. Fail with explicit error listing hallucinated references.
6. Validate with test queries
7. Track completion: check off each manifest entry as its TVF is confirmed created

#### Phase 2 Completion Gate (MANDATORY)

**DO NOT proceed to Phase 3 until you have:**
1. Written all Phase 2 artifacts to disk
2. **Run the `create_tvfs` per-task verification row** from the "Per-task verification" table in Phase 5 *against a scratch dev target*. Every TVF must return at least one row on a smoke input — silent empty results mean the TVF is broken for Genie.
3. Presented the user with a summary: artifact names, paths, key design decisions
4. Asked: "Phase 2 is complete. Shall I proceed to Phase 3 (Genie Space), or review/modify first?"

Bulk creation without checkpoints causes cascading failures. A 2-minute pause catches issues that take 30 minutes to debug post-deployment.

### Phase 3: Genie Space Setup (1 hour)

**Context setup:** Discard Phase 2 skill content. Keep `gold_inventory` + Phase 1 notes (MV names/paths) + Phase 2's "TVF Notes to Carry Forward" (TVF names/paths). Read the skills below just-in-time. Phase 3 uses TWO worker skills — Genie Space Patterns (for design) and Export/Import API (for JSON config generation).

| # | Skill Path | What It Provides |
|---|------------|------------------|
| 1 | `skills/databricks-expert-agent/SKILL.md` | Extract asset references from `gold_inventory` |
| 2 | `data_product_accelerator/skills/common/naming-tagging-standards/SKILL.md` | Table/column COMMENTs required by Genie |
| 3 | `data_product_accelerator/skills/semantic-layer/03-genie-space-patterns/SKILL.md` | 8-section deliverable, agent instructions, SQL expressions, benchmark questions |
| 4 | `data_product_accelerator/skills/semantic-layer/04-genie-space-export-import-api/SKILL.md` | JSON schema, array sorting, ID generation, idempotent deployment |

**Input:** First check the **top-level** `manifest.unified_genie_space` (singular). If present, build that single cross-domain space and SKIP per-domain `genie_spaces[]` (matches the planning manifest template's `unified_genie_space` precedence rule). Otherwise, for each domain in `manifest['domains']`, iterate over `domain['genie_spaces']`. Each entry defines `name`, `warehouse`, `assets` (metric_views, tvfs, tables), `benchmark_questions_count`, and `benchmark_questions`. Do NOT create Genie Spaces not listed in the manifest.

```python
unified = manifest.get("unified_genie_space")
if unified:
    print(f"Using unified Genie Space: {unified.get('name')} "
          f"(domains_covered={unified.get('domains_covered')}). "
          f"Skipping per-domain genie_spaces[].")
    spaces_to_create = [unified]
else:
    spaces_to_create = [
        {"domain": d, **gs}
        for d, dc in manifest.get("domains", {}).items()
        for gs in dc.get("genie_spaces", [])
    ]
```

**Context from prior phases:** Use Phase 1's MV notes to assign metric views to spaces. Use Phase 2's TVF notes to assign TVFs. Use `gold_inventory` for Gold table assignments.

**Steps:**
1. Verify all Gold tables have column comments (Genie depends on these)
2. Read `manifest['unified_genie_space']` first; otherwise iterate `manifest['domains'][domain]['genie_spaces']` — use the manifest's `assets` to assign data assets (Metric Views, TVFs, Gold Tables) to each space
3. Write General Instructions (≤20 lines)
4. Create benchmark questions — use the manifest's `benchmark_questions` as the baseline; ensure minimum 10 per space with exact SQL answers
5. **Validation gate:** Parse each benchmark question's expected SQL. Verify all table/column references exist in `gold_inventory`. Verify all TVF references match TVFs created in Phase 2. Verify all Metric View references match MVs created in Phase 1. Fail with explicit error listing hallucinated references.
6. Configure Serverless SQL Warehouse (as specified in manifest's `warehouse` field)
7. **Generate API-compatible Genie Space JSON config file** using the `genie-space-export-import-api` JSON schema. Save to `src/{project}_semantic/genie_configs/`. Use template variables (`${catalog}`, `${gold_schema}`) for portability.
8. Track completion: check off each manifest entry as its Genie Space config is confirmed generated

#### Phase 3 Completion Gate (MANDATORY)

**DO NOT proceed to Phase 4 until you have:**
1. Written all Phase 3 artifacts to disk
2. Presented the user with a summary: artifact names, paths, key design decisions
3. Asked: "Phase 3 is complete. Shall I proceed to Phase 4 (Asset Bundle), or review/modify first?"

Bulk creation without checkpoints causes cascading failures. A 2-minute pause catches issues that take 30 minutes to debug post-deployment.

### Phase 4: Asset Bundle Configuration (30 min)

**Context setup:** Discard Phase 3 skill content. Keep `gold_inventory` + Phase 3's "Genie Space Notes to Carry Forward" (space names, JSON paths, space IDs). Read just-in-time:

| # | Skill Path | What It Provides |
|---|------------|------------------|
| 1 | `skills/databricks-asset-bundles/SKILL.md` | Job YAML patterns, serverless config, `notebook_task` vs `sql_task`, `base_parameters` |

**Activities:**
1. Copy `semantic-layer-job-template.yml` from `data_product_accelerator/skills/semantic-layer/00-semantic-layer-setup/assets/templates/` to `resources/semantic/semantic_layer_job.yml` — customize paths and variables
2. Add YAML/JSON sync to `databricks.yml`:
   ```yaml
   sync:
     include:
       - "src/semantic/metric_views/**/*.yaml"
       - "src/semantic/genie_configs/**/*.json"
   ```
3. Add resource reference to `databricks.yml`: `resources/semantic/semantic_layer_job.yml`
4. **Ensure `warehouse_id` variable in `databricks.yml`:**
   ```yaml
   variables:
     warehouse_id:
       description: "SQL Warehouse ID for notebook_task execution"
       default: ""
   ```
   The warehouse ID is required for notebook tasks that execute SQL. Retrieve it from the Databricks workspace SQL Warehouse settings page.
5. **Add per-Genie-Space ID variables** for update-or-create pattern:
   ```yaml
   variables:
     genie_space_id_<space_name>:
       description: "Existing Genie Space ID for <space_name> (empty for initial creation)"
       default: ""
   ```
   These variables enable idempotent deployments: if a space ID is provided, the deploy script PATCHes the existing space instead of creating a duplicate. After first deployment, record the space IDs and set them in variables.

**Combined Job Structure (3 tasks with `depends_on` chains):**
- `create_metric_views` — `notebook_task`, no deps
- `create_table_valued_functions` — `notebook_task`, depends_on: `create_metric_views`
- `deploy_genie_spaces` — `notebook_task`, depends_on: `create_metric_views` + `create_table_valued_functions`

**⚠️ All 3 tasks use `notebook_task`.** `sql_task.parameters` are SQL bind parameters (`:param`) — they cannot substitute identifiers in DDL like `${catalog}.${gold_schema}` in CREATE FUNCTION statements.

**Critical Rules (from `databricks-asset-bundles`):**
- `notebook_task` for Metric Views, TVFs, and Genie (all 3 tasks)
- `base_parameters` dict for all `notebook_task` entries (variable substitution for catalog, schema, etc.)
- `warehouse_id` required for tasks that execute SQL (pass via `base_parameters` to notebooks)
- `environment_version: "4"` with PyYAML + requests dependencies
- YAML/JSON sync is CRITICAL — without it, creation scripts cannot find configs

**Output:** `resources/semantic/semantic_layer_job.yml`, updated `databricks.yml`

See `assets/templates/semantic-layer-job-template.yml` for the starter template.

### Phase 5: Deploy & Run (30 min)

**Context setup:** Keep Phase 4's job YAML path + all accumulated notes. Read just-in-time:

| # | Skill Path | What It Provides |
|---|------------|------------------|
| 1 | `data_product_accelerator/skills/common/databricks-autonomous-operations/SKILL.md` | Deploy → Poll → Diagnose → Fix → Redeploy loop |

**Two commands — platform-enforced ordering:**
1. `databricks bundle deploy -t dev`
2. `databricks bundle run semantic_layer_job -t dev`

Databricks enforces the `depends_on` chain: Metric Views are created first, then TVFs, then Genie Spaces. If any task fails, downstream tasks do not run.

**Per-task verification (MANDATORY — run AFTER each task completes, not at the end of the job).** Do NOT batch verifications at the end of the Phase. A silent success upstream produces wasted downstream work when verification only runs at the end.

| Task | Verification SQL / API | Pass criterion | STOP rule on fail |
|---|---|---|---|
| `create_metric_views` | `SHOW VIEWS IN {catalog}.{semantic_schema}` filtered to expected names; plus `DESCRIBE EXTENDED {catalog}.{semantic_schema}.{mv_name}` returns YAML metric body non-empty. (`semantic_schema` defaults to `gold_schema` for Gold-based runs; in workshop runs it may be a separate schema or fall back to the planning-source schema.) | Every manifest-declared Metric View present; `DESCRIBE EXTENDED` shows `METRICS LANGUAGE YAML`. | STOP — do NOT run TVFs. Re-run `create_metric_views` with the specific failing YAML fixed. |
| `create_tvfs` | `SHOW FUNCTIONS IN {catalog}.{semantic_schema} LIKE '*'` filtered to expected names; plus a sample `SELECT * FROM {catalog}.{semantic_schema}.{tvf}(...) LIMIT 1` for each. | Every manifest-declared TVF present and callable with smoke input. | STOP — do NOT deploy Genie Spaces. |
| `deploy_genie_spaces` | GET `/api/2.0/genie/spaces/{id}?include_serialized_space=true` for every deployed space. | Response non-empty; `data_sources.tables` + `data_sources.metric_views` non-empty; `instructions.sql_functions[*].sql` all `List[str]`. | STOP — do NOT deploy dashboards that query Genie. |
| `deploy_dashboards` | For every dashboard file: after `ws.workspace.import_`, `ws.workspace.get_status(target_path)` returns `object_type=FILE` and size > the pre-upload file size. | Every target path exists and is non-zero bytes. | STOP — re-upload failing files only; do NOT re-run the whole deploy. |
| `databricks bundle run` (overall) | All task statuses = `SUCCESS` AND all per-task verifications above have passed. | No task stuck in `INTERNAL_ERROR` / `FAILED` / `SKIPPED`. | STOP — follow the `databricks-autonomous-operations` diagnose loop for the specific failing task. |

**On failure:** Follow the `databricks-autonomous-operations` diagnose → fix → redeploy loop. **Do NOT** attempt to patch the problem in the workspace and continue — the Asset Bundle workspace copy will be overwritten on the next `bundle deploy`, hiding the fix.

### Phase 6: API Deployment (Recommended, 30 min)

**Context setup:** If Phase 3's "Genie API Notes to Carry Forward" are still available, use them. Otherwise re-read just-in-time:

| # | Skill Path | What It Provides |
|---|------------|------------------|
| 1 | `data_product_accelerator/skills/semantic-layer/04-genie-space-export-import-api/SKILL.md` | REST API, JSON schema, idempotent deployment, array sorting |

**Steps:**
1. Export Genie Space config from dev as JSON (or use the Phase 3 JSON)
2. Parameterize with variable substitution (`${catalog}`, `${gold_schema}`)
3. Import to staging/prod environment via REST API

> This complements the Asset Bundle approach. Phase 5 deploys within a single workspace; Phase 6 enables cross-workspace promotion via the REST API.

---

## Post-Creation Validation

### Manifest Compliance (CRITICAL)
- [ ] `plans/manifests/semantic-layer-manifest.yaml` was read at Phase 0 before any implementation
- [ ] Every Metric View maps 1:1 to a `domains[domain].metric_views[]` entry in the manifest
- [ ] Every TVF maps 1:1 to a `domains[domain].tvfs[]` entry in the manifest
- [ ] Every Genie Space maps 1:1 to a `domains[domain].genie_spaces[]` entry in the manifest, OR the single space matches the top-level `unified_genie_space`
- [ ] When `unified_genie_space` is present, per-domain `genie_spaces[]` were SKIPPED (no duplicate spaces created)
- [ ] No artifacts were created via self-discovery (only manifest-driven)
- [ ] If `planning_mode: workshop`, artifact counts do NOT exceed manifest totals
- [ ] If `selected_layer = source_csv`, the orchestrator stopped at Phase 0 with the planning-contract-only message (no Phase 1+ artifacts created)
- [ ] If `selected_layer in {deployed_silver, deployed_bronze}` (workshop), the orchestrator printed the workshop advisory and proceeded to build artifacts against `inventory_schema` / `semantic_schema`
- [ ] Manifest `summary` counts match actual deployed artifact counts
- [ ] `planning_source.selected_layer` was inspected before building the inventory; the inventory was sourced from the matching schema (Gold YAML for Gold sources; live `information_schema.columns` for Silver/Bronze)

### Anti-Hallucination Compliance
- [ ] `gold_inventory` dict built from YAML + catalog in Phase 0
- [ ] All table/column references in Metric Views validated against `gold_inventory`
- [ ] All table/column references in TVFs validated against `gold_inventory`
- [ ] All benchmark SQL references validated against `gold_inventory` + Phase 1/2 outputs

### Common Skill Compliance
- [ ] Names extracted from `gold_inventory` (not generated) per `databricks-expert-agent`
- [ ] All COMMENTs follow `naming-tagging-standards` dual-purpose format (CM-02)
- [ ] TVF COMMENTs follow v3.0 structured format (CM-04)
- [ ] Asset Bundle YAML follows `databricks-asset-bundles` patterns
- [ ] Python imports follow `databricks-python-imports` sys.path setup

### Semantic Layer Specifics
- [ ] All Metric Views use `WITH METRICS LANGUAGE YAML` syntax
- [ ] All TVFs use STRING parameters only
- [ ] Genie Space has ≤20 line General Instructions
- [ ] Genie Space has ≥10 benchmark questions with exact SQL
- [ ] Genie Space uses Serverless SQL Warehouse
- [ ] All Gold tables have column comments before Genie Space creation
- [ ] API-compatible Genie Space JSON generated in `src/{project}_semantic/genie_configs/`

### Deployment Compliance
- [ ] Combined `semantic_layer_job.yml` with `depends_on` chains created
- [ ] `databricks.yml` updated with sync (YAML + JSON) and resource references
- [ ] All 3 tasks pass in `semantic_layer_job` run

---

## Pipeline Progression

**Previous stage:** `planning/00-project-planning` → Project plan for semantic layer, observability, ML, and GenAI agent phases should be complete

**Next stage:** After completing the semantic layer, proceed to:
- **`monitoring/00-observability-setup`** — Set up Lakehouse Monitoring, AI/BI Dashboards, and SQL Alerts

---

## Related Skills

| Skill | Relationship | Path |
|-------|-------------|------|
| `metric-views-patterns` | **Mandatory** — Metric View YAML | `semantic-layer/01-metric-views-patterns/SKILL.md` |
| `databricks-table-valued-functions` | **Mandatory** — TVF patterns | `semantic-layer/02-databricks-table-valued-functions/SKILL.md` |
| `genie-space-patterns` | **Mandatory** — Genie Space setup | `semantic-layer/03-genie-space-patterns/SKILL.md` |
| `genie-space-export-import-api` | **Mandatory** — JSON config + API deployment | `semantic-layer/04-genie-space-export-import-api/SKILL.md` |
| `databricks-expert-agent` | **Mandatory** — Extraction principle | `skills/databricks-expert-agent/SKILL.md` |
| `databricks-asset-bundles` | **Mandatory** — Deployment | `skills/databricks-asset-bundles/SKILL.md` |
| `databricks-python-imports` | **Mandatory** — Python patterns | `common/databricks-python-imports/SKILL.md` |
| `naming-tagging-standards` | **Mandatory** — COMMENTs, naming, tags | `common/naming-tagging-standards/SKILL.md` |
| `databricks-autonomous-operations` | **Mandatory** — Deploy/diagnose/fix loop | `common/databricks-autonomous-operations/SKILL.md` |

## Post-Completion: Skill Usage Summary (MANDATORY)

**After completing all phases of this orchestrator, output a Skill Usage Summary reflecting what you ACTUALLY did — not a pre-written summary.**

### What to Include

1. Every skill `SKILL.md` or `references/` file you read (via the Read tool), in the order you read them
2. Which phase you were in when you read it
3. Whether it was a **Worker**, **Common**, **Cross-domain**, or **Reference** file
4. A one-line description of what you specifically used it for in this session

### Format

| # | Phase | Skill / Reference Read | Type | What It Was Used For |
|---|-------|----------------------|------|---------------------|
| 1 | Phase N | `path/to/SKILL.md` | Worker / Common / Cross-domain / Reference | One-line description |

### Summary Footer

End with:
- **Totals:** X worker skills, Y common skills, Z reference files read across N phases
- **Skipped:** List any skills from the dependency table above that you did NOT need to read, and why (e.g., "phase not applicable", "user skipped", "no issues encountered")
- **Unplanned:** List any skills you read that were NOT listed in the dependency table (e.g., for troubleshooting, edge cases, or user-requested detours)

---

## Version History

- **v1.2.0** (Feb 2026) — Progressive disclosure protocol: just-in-time skill loading, context handoff between phases, explicit working memory management per AgentSkills.io and Anthropic context engineering best practices
- **v1.1.0** (Feb 2026) — TVF task type corrected to notebook_task; warehouse_id and Genie Space ID variables added; validation gates enhanced with transitive join detection and format type validation

---

## References

- [Metric Views](https://docs.databricks.com/aws/en/metric-views/semantic-metadata)
- [Table-Valued Functions](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-tvf)
- [Genie Spaces](https://docs.databricks.com/aws/en/genie/trusted-assets)
- [Genie Conversation API](https://docs.databricks.com/api/workspace/genie)
