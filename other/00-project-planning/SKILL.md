---
name: project-planning
description: >-
  Create multi-phase project plans for Databricks data platform solutions
  with Agent Domain Framework and Agent Layer Architecture. Includes interactive
  Quick Start with key decisions, industry-specific domain patterns, complete
  phase document templates (Use Cases, Agents, Frontend), Genie Space integration
  patterns, deployment order requirements, and worked examples. Supports both
  acceleration mode (plan on a completed Gold layer) and workshop mode
  (`planning_mode: workshop`) that plans from the best available layer with hard
  artifact caps. Use when planning any Databricks solution post-Gold layer —
  observability, analytics, agent-based frameworks, or multi-artifact projects.
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: bundle_deploy
deploy_note: "Design-phase skill: produces multi-phase plans, manifests, and addendums; it has no deployed resource of its own — downstream artifacts deploy later via `bundle deploy --target dev` (runDatabricksCli on Genie Code). B12: the Gold-gap STOP gate writes `plans/gold-gap-remediation.md` and halts before generating plans; workshop mode (`planning_mode: workshop`) applies hard artifact caps. On Genie Code, write all generated plans/manifests under the cloned repo root (`{REPO_ROOT}` = `state_file_root` from `skills/vibecoding-state`, e.g. `plans/`), not a bare relative path — relative paths resolve against the page CWD (see `skills/genie-code-environment` §8)."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "2.0"
  domain: planning
  role: orchestrator
  pipeline_stage: 5
  pipeline_stage_name: planning
  next_stages:
    - semantic-layer-setup
  workers: []
  common_dependencies:
    - databricks-expert-agent
    - naming-tagging-standards
  emits:
    - plans/use-case-catalog.md
    - plans/manifests/semantic-layer-manifest.yaml
    - plans/manifests/observability-manifest.yaml
    - plans/manifests/ml-manifest.yaml
    - plans/manifests/genai-agents-manifest.yaml
    - plans/manifests/gold-dependency-manifest.yaml          # acceleration mode (Gold source)
    - plans/manifests/source-dependency-manifest.yaml         # workshop mode (any source layer; superset of gold-dependency-manifest)
    - plans/gold-gap-remediation.md   # emitted ONLY when live-catalog intersection finds missing tables/columns (acceleration)
    - plans/source-gap-remediation.md # emitted ONLY in workshop mode when the selected planning source has missing tables/columns
  reads:
    # Acceleration mode (default) reads Gold design + deployed Gold:
    - gold_layer_design/yaml/
    - gold_layer_design/erd_master.md
    - gold_layer_design/docs/BUSINESS_ONBOARDING_GUIDE.md
    # Workshop mode may also read these as fallbacks (in priority order):
    - data_product_accelerator/context/*.csv     # source schema CSV (last-resort planning basis)
    # Workshop mode also probes the live catalog for deployed Bronze/Silver/Gold schemas as a planning source.
  supported_modes:
    - acceleration     # Full breadth (DEFAULT) — all domains, all artifacts, full rationalization
    - workshop         # Learning & Enablement — minimal representative sampling with hard artifact caps
  default_mode: acceleration
  last_verified: "2026-02-07"
  volatility: low
  upstream_sources: []  # Internal planning methodology
---

# Project Plan Methodology for Databricks Solutions

## Planning Mode

**Default: Data Product Acceleration** — full breadth, all domains, all artifacts, **Gold layer required as planning basis**. This is the standard behavior described in this entire skill document below.

**Workshop mode** is available for Learning & Enablement scenarios with hard artifact caps **and layer flexibility** — it can plan from the best available source layer (Gold, Gold design YAML, Silver, Bronze, or source CSV). Workshop mode is NEVER activated unless the user includes the **exact phrase** `planning_mode: workshop` in their prompt.

> **Mode vs source layer:** `planning_mode` (acceleration | workshop) controls artifact caps and validation strictness. `planning_source.selected_layer` (gold | gold_design | silver | bronze | source_csv) records which input the plan was derived from and is set automatically by Phase 0 below. Acceleration mode FORCES `selected_layer = gold` (or `gold_design` only if explicitly allowed). Workshop mode picks the best available source via the Phase 0 priority order and stamps it onto every manifest.

### Mode Detection Rules

1. **Default is ALWAYS `acceleration`.** If the user does not explicitly declare workshop mode, use acceleration.
2. **Workshop mode requires EXPLICIT opt-in.** The user must include one of these EXACT phrases:
   - `planning_mode: workshop`
   - `"workshop mode"`
   - `"use workshop mode"`
3. **Do NOT infer workshop mode** from words like "small", "simple", "demo", "limited", "quick", "basic", "training", or "few". These are NOT triggers. A user may want a narrow-scope acceleration plan — that's still acceleration mode with fewer use cases.
4. **When in doubt, ask.** If the user's intent is ambiguous (e.g., "Create a plan for a workshop"), ask: *"Would you like full Data Product Acceleration mode (default) or Workshop mode with limited artifacts? To use workshop mode, include `planning_mode: workshop` in your request."*
5. **Confirm mode at the start.** The first line of any plan output should state the active mode:
   - `**Planning Mode:** Data Product Acceleration (default)`
   - `**Planning Mode:** Workshop (explicit opt-in — artifact caps active)`
6. **When workshop mode is activated,** read `references/workshop-mode-profile.md` for artifact caps, phase scope, and selection criteria. Do NOT read that reference otherwise.
7. **Propagate mode to manifests.** Add `planning_mode: workshop` or `planning_mode: acceleration` to all generated manifest YAML files. Downstream orchestrators seeing `workshop` MUST NOT expand beyond the listed artifacts via self-discovery.

## Overview

Comprehensive methodology for creating multi-phase project plans for Databricks data platform solutions. This skill combines interactive project planning with architectural methodology, including templates, worked examples, and quality standards.

**Key Assumption (mode-aware):**

- **Acceleration mode (default):** Planning starts AFTER Bronze ingestion AND Gold layer design are complete. Gold is the required planning basis. These are prerequisites, not phases. Phase 0 will stop with a remediation message if Gold is missing.
- **Workshop mode (`planning_mode: workshop`):** Planning AND deployment are layer-agnostic. Phase 0 selects the highest-fidelity input present from: deployed Gold, Gold design YAML, deployed Silver, deployed Bronze, or a source schema CSV. The selected layer is stamped onto every manifest as `planning_source.selected_layer`. Workshop manifests built from Silver or Bronze are marked `implementation_readiness: workshop_deployable` — downstream stages (semantic-layer, observability, ml, genai-agents) deploy directly against the selected layer. Workshop manifests built from a source CSV are marked `implementation_readiness: workshop_draft` (planning contract only — no live tables to deploy against). `requires_gold_promotion` is an **advisory** field; it is recommended for production but never blocks deployment.

## When to Use This Skill

Use this skill when:
- Creating architectural plans for Databricks data platform projects
- Building observability, analytics, or monitoring solutions
- Planning multi-artifact solutions (TVFs, Metric Views, Dashboards, Genie Spaces, Alerts, ML Models)
- Developing agent-based frameworks for platform management
- Creating frontend applications for data platform interaction
- Starting a new project after Gold layer is complete

## Idempotency Guard (Run FIRST)

**Before regenerating plans, detect existing artifacts to avoid clobbering work-in-progress.** A common failure mode is regenerating `plans/` wholesale on a re-run and overwriting user edits to manifests, addendums, or the Use Case Catalog.

```python
from pathlib import Path

PLANS_DIR = Path("plans")
if PLANS_DIR.exists() and any(PLANS_DIR.iterdir()):
    existing = sorted(p.relative_to(".") for p in PLANS_DIR.rglob("*") if p.is_file())
    print("Existing plan artifacts detected:")
    for p in existing:
        print(f"  {p}  (mtime={Path(p).stat().st_mtime})")
    print(
        "\nHow would you like to proceed?\n"
        "  - regenerate  (DELETE and rebuild all plan files — destructive)\n"
        "  - incremental (keep existing files, only emit MISSING artifacts)\n"
        "  - skip        (exit this orchestrator — recommended default)\n"
    )
```

**Rules:**
- **Default is `skip`.** If the user is silent or ambiguous, assume `skip` and exit with a summary of existing files.
- `regenerate` must be explicit. Confirm the action ("I will delete N files under `plans/` — proceed?") before doing anything destructive.
- `incremental` is the right choice when downstream orchestrators (semantic-layer, observability, ml, genai-agents) reported a missing manifest — only emit the missing manifest, not the whole tree.

**Escape flag:** Users can set `planning_allow_overwrite: true` in their prompt to skip the idempotency check (equivalent to choosing `regenerate` without interactive confirmation).

---

## Quick Start (5 Minutes)

### Fast Track: Create Your Project Plan

```bash
# 1. Verify prerequisites for your mode:
#    Acceleration (default):
#      - Bronze ingestion ✅
#      - Silver DLT streaming ✅
#      - Gold dimensional model ✅ (REQUIRED)
#    Workshop (planning_mode: workshop):
#      - At least ONE of: deployed Gold, gold_layer_design/yaml/, deployed Silver,
#        deployed Bronze, or data_product_accelerator/context/*.csv
#      - Phase 0 picks the highest-fidelity input automatically.

# 2. Run this prompt with your project info:
"Create a phased project plan for {project_name} with:
- Planning assets: {n} tables (Gold/Silver/Bronze depending on what is available)
- Use cases: {use_case_1, use_case_2, use_case_3, etc.}
- Target audience: {executives, analysts, data scientists}
- Agent domains: {domain1, domain2, domain3, domain4, domain5}"

# 3. Output: Complete plan structure in plans/ folder
#    - Acceleration emits gold-dependency-manifest.yaml.
#    - Workshop emits gold-dependency-manifest.yaml OR source-dependency-manifest.yaml
#      depending on the selected planning source layer.
```

### Key Decisions (Answer These First)

| Decision | Options | Your Choice |
|----------|---------|-------------|
| Agent Domains | Derive from business questions (typically 2-5) | __________ |
| Phase 1 Addendums | TVFs, Metric Views, Dashboards, Monitoring, Genie, Alerts, ML | __________ |
| Phase 2 Scope | AI Agents (optional) or skip | __________ |
| Phase 3 Scope | Frontend App (optional) or skip | __________ |
| Genie Space Count | Based on asset count vs 25-asset limit (see Rationalization) | __________ |
| Agent Architecture | Agents use Genie Spaces (recommended) or Direct SQL | __________ |
| Agent-Genie Mapping | 1:1, consolidated, or unified (based on asset volume) | __________ |

## Working Memory Management

This orchestrator spans 3 phases. To maintain coherence without context pollution:

**After each phase, persist a brief summary note** capturing:
- **Phase 1:** Domain list with Gold table mappings, addendum selections, business questions per domain, artifact count estimates
- **Phase 2:** Plan document file paths, cross-references verified, total artifact counts by type
- **Phase 3:** Manifest file paths (semantic-layer, observability, ml, genai-agents), validation results, summary counts

**What to keep in working memory:** Current phase's template, domain list + artifact inventory, and previous phase's summary. Discard intermediate outputs — they are on disk. Read templates from `assets/templates/` and references just-in-time, not upfront.

---

## Step-by-Step Workflow

### Phase 0: Planning Source Discovery (MANDATORY, runs before Phase 1)

This phase decides WHICH layer the plan will be derived from and stamps the answer onto every emitted manifest as `planning_source`. It runs in **both** modes; the only difference is which selections are allowed.

#### Step 0.1 — Inventory available planning inputs

Detect each potential planning source. Record presence/absence in working memory.

```python
from pathlib import Path
from databricks.sdk import WorkspaceClient

def detect_planning_sources(catalog: str, user_schema_prefix: str) -> dict:
    """Return a dict describing every potential planning source that exists.

    Priority order (highest fidelity first):
      1. deployed_gold     — live tables in <catalog>.<prefix>_gold
      2. gold_design       — gold_layer_design/yaml/*.yaml authored, deployment may or may not be done
      3. deployed_silver   — live tables in <catalog>.<prefix>_silver
      4. deployed_bronze   — live tables in <catalog>.<prefix>_bronze
      5. source_csv        — data_product_accelerator/context/*.csv (last resort)
    """
    w = WorkspaceClient()
    sources = {}
    for layer, schema in (
        ("deployed_gold",   f"{user_schema_prefix}_gold"),
        ("deployed_silver", f"{user_schema_prefix}_silver"),
        ("deployed_bronze", f"{user_schema_prefix}_bronze"),
    ):
        try:
            tables = list(w.tables.list(catalog_name=catalog, schema_name=schema))
            sources[layer] = {"schema": f"{catalog}.{schema}", "table_count": len(tables)} if tables else None
        except Exception:
            sources[layer] = None
    yaml_dir = Path("gold_layer_design/yaml")
    if yaml_dir.exists() and any(yaml_dir.glob("*.yaml")):
        sources["gold_design"] = {"path": str(yaml_dir), "yaml_count": len(list(yaml_dir.glob("*.yaml")))}
    else:
        sources["gold_design"] = None
    csvs = list(Path("data_product_accelerator/context").glob("*.csv"))
    sources["source_csv"] = {"paths": [str(c) for c in csvs]} if csvs else None
    return sources
```

#### Step 0.2 — Select the planning source by mode

| Mode | Allowed `selected_layer` values | Selection rule |
|------|---------------------------------|----------------|
| `acceleration` (default) | `deployed_gold`, `gold_design` | Pick `deployed_gold` if present; else `gold_design` ONLY when explicitly accepted; else **STOP** with a Gold-required remediation message. |
| `workshop` | `deployed_gold`, `gold_design`, `deployed_silver`, `deployed_bronze`, `source_csv` | Pick the highest-priority source present. Never silently fall through to a lower layer when a higher one exists. |

**Acceleration STOP message:**
> Planning in acceleration mode requires the Gold layer. Run the Gold Layer Design and Setup skills first, or re-run with `planning_mode: workshop` to plan from a lower layer.

**Workshop selection log (must be printed):**
```
Phase 0 — Planning source selected: <selected_layer>
  Available: deployed_gold=<bool>, gold_design=<bool>, deployed_silver=<bool>, deployed_bronze=<bool>, source_csv=<bool>
  Reason: highest-fidelity available input under workshop mode
```

#### Step 0.3 — Derive readiness markers

Compute the readiness fields that every emitted manifest must include. `requires_gold_promotion` is **advisory only** — it is a hint for production hardening, never a deployment gate.

```python
def readiness_for(selected_layer: str, mode: str) -> dict:
    if selected_layer == "deployed_gold":
        # Production-deployable from Gold.
        return {"implementation_readiness": "gold_ready",
                "requires_gold_promotion": False}
    if selected_layer == "gold_design":
        # Deployable once the Gold layer is provisioned.
        return {"implementation_readiness": "gold_design_only",
                "requires_gold_promotion": False}
    # Silver, Bronze, source CSV — workshop only.
    if mode != "workshop":
        raise SystemExit("Non-Gold planning sources are only allowed in workshop mode.")
    if selected_layer in {"deployed_silver", "deployed_bronze"}:
        # Workshop builds the semantic layer directly on top of Silver/Bronze.
        # Gold promotion is recommended for production but not required to deploy.
        return {"implementation_readiness": "workshop_deployable",
                "requires_gold_promotion": False}
    if selected_layer == "source_csv":
        # No live tables — planning contract only; downstream stages will not
        # attempt to deploy until at least one live layer exists.
        return {"implementation_readiness": "workshop_draft",
                "requires_gold_promotion": False}
    raise SystemExit(f"Unknown selected_layer={selected_layer!r}")
```

**Readiness state semantics:**

| `implementation_readiness` | When | Downstream behavior |
|---|---|---|
| `gold_ready` | Acceleration or workshop on `deployed_gold` | Full production deploy |
| `gold_design_only` | Acceleration or workshop on `gold_design` (Gold YAML, no live tables yet) | Deploy after Gold provisioning; live-catalog checks advisory |
| `workshop_deployable` | Workshop on `deployed_silver` or `deployed_bronze` | Deploy semantic layer / Genie Spaces directly against the Silver or Bronze schema; Gold promotion is an advisory next step |
| `workshop_draft` | Workshop on `source_csv` only | Planning contract only; downstream stages stop and ask for at least one live layer |

#### Step 0.4 — Stamp `planning_source` onto every manifest

Every manifest emitted by Phases 1–3 (semantic-layer, observability, ml, genai-agents, gold-dependency, source-dependency) MUST carry a top-level block:

```yaml
planning_source:
  selected_layer: deployed_gold | gold_design | deployed_silver | deployed_bronze | source_csv
  schema: "<catalog>.<schema>"            # e.g. main.acme_gold (omit/null for source_csv)
  source_yaml_dir: "gold_layer_design/yaml"   # only when selected_layer = gold_design
  source_csv_paths: ["data_product_accelerator/context/<file>.csv"]  # only for source_csv
  selected_at: "<ISO-8601 UTC>"
implementation_readiness: gold_ready | gold_design_only | workshop_deployable | workshop_draft
requires_gold_promotion: true | false   # advisory only; never a deployment gate
```

Downstream orchestrators (semantic-layer, observability, ml, genai-agents) read these fields:

- `gold_ready` / `gold_design_only` / `workshop_deployable` — proceed with deployment against the layer the manifest declares (`gold_schema` for Gold sources; `silver_schema` / `bronze_schema` for workshop deployments on Silver/Bronze).
- `workshop_draft` (only emitted when `selected_layer = source_csv`) — stop before deployment; the plan is a contract only.
- `requires_gold_promotion` is advisory; it influences messaging, not gating.

#### Step 0.5 — Mode-aware Phase 1 prerequisites table

The `Prerequisites Status` table in Phase 1 must reflect the selected source. Layers above the selected one are still valid; layers below it (or absent) are marked `N/A` or `Planned only`. See the updated `assets/templates/prerequisites-template.md` for the dynamic format.

---

### Phase 1: Requirements Gathering

#### Project Information

| Field | Your Value |
|-------|------------|
| Project Name | {project_name} |
| Business Domain | {hospitality, retail, healthcare, finance, etc.} |
| Primary Use Cases | {use_case_1, use_case_2, use_case_3, etc.} |
| Target Stakeholders | {executives, analysts, data scientists, operations} |

#### Prerequisites Status (filled by Phase 0)

The status of each layer must reflect what Phase 0 detected. Layers above the selected planning source are "✅ Complete"; the selected layer itself is the source the plan was derived from; layers below or absent are `N/A` or `Planned only`. Use the dynamic format from `assets/templates/prerequisites-template.md`.

| Layer | Count | Status (mode-aware) |
|-------|-------|---------------------|
| Bronze Tables | {n} | ✅ Complete / N/A / Planned only |
| Silver Tables | {m} | ✅ Complete / N/A / Planned only |
| Gold Dimensions | {d} | ✅ Complete / Designed only / N/A |
| Gold Facts | {f} | ✅ Complete / Designed only / N/A |
| **Selected planning source** | — | `{planning_source.selected_layer}` (from Phase 0) |

#### Define Agent Domains

Derive domains from your business questions and **planning-source table groupings** (see Artifact Rationalization Framework). Use Gold table groupings when `planning_source.selected_layer` is `deployed_gold` or `gold_design`; otherwise group on the selected source-layer tables (Silver / Bronze / source CSV entities). Do not force a fixed number — let the data model and use cases determine natural boundaries.

##### Required Reads (Before Proceeding)

Before defining domains and use cases, you MUST have read these references. Check each off in your Skill Usage Summary:

- [ ] `references/rationalization-framework.md` — domain sizing rules, TVF creation gate, Genie Space capacity planning, naming conventions
- [ ] `references/worked-example-wanderbricks.md` (if the project is WanderBricks or a hospitality/vacation-rental domain) OR `references/industry-domain-patterns.md` (otherwise) — domain naming, use case card depth, reference SQL patterns

If a worked example matches your project, treat it as the **primary format reference** for use case cards and artifact designs — adapt, don't reinvent. "MANDATORY" means read it; note in the Skill Usage Summary if the reference did not change your decisions, but still read it.

**Workshop mode:** `references/workshop-mode-profile.md` should already be loaded when `planning_mode: workshop` was detected — see its **Document Scope** section, since workshop mode changes artifact counts but NOT which documents to produce.

| Domain | Icon | Focus Area | Key Planning Assets | Est. Business Questions |
|--------|------|------------|---------------------|------------------------|
| {Domain 1} | {emoji} | {focus} | {tables from selected layer} | {count} |
| {Domain 2} | {emoji} | {focus} | {tables from selected layer} | {count} |
| ... | ... | ... | ... | ... |

**Sizing check:** If a domain has < 3 business questions, consider merging it. If two domains share > 70% of their planning assets (Gold/Silver/Bronze tables, depending on `planning_source.selected_layer`), consolidate.

See [Industry Domain Patterns](references/industry-domain-patterns.md) for examples by industry.

#### Phase 1 Addendum Selection

| # | Addendum | Include? | Artifact Count |
|---|----------|----------|----------------|
| 1.1 | ML Models | {Yes/No} | {count} |
| 1.2 | Table-Valued Functions | {Yes/No} | {count} |
| 1.3 | Metric Views | {Yes/No} | {count} |
| 1.4 | Lakehouse Monitoring | {Yes/No} | {count} |
| 1.5 | AI/BI Dashboards | {Yes/No} | {count} |
| 1.6 | Genie Spaces | {Yes/No} | {count} |
| 1.7 | Alerting Framework | {Yes/No} | {count} |

#### Key Business Questions by Domain

List 5-10 key questions per domain that the solution must answer:

**{Domain 1}:**
1. {Question 1}
2. {Question 2}
3. {Question 3}
4. {Question 4}
5. {Question 5}

#### Use Case Catalog

After defining business questions and selecting addendums, consolidate into a **Use Case Catalog** — one entry per distinct analytical or operational problem the solution will address. Each use case ties business questions to the **planning assets** (Gold tables in acceleration; selected-layer tables in workshop) and artifacts that solve them. Use `assets/templates/use-case-catalog-template.md` for the full format.

| UC# | Use Case Name | Domain | Planning Assets | Artifact Types | Example Question |
|-----|--------------|--------|-----------------|---------------|-----------------|
| UC-001 | {Descriptive Name} | {Domain} | `fact_*`, `dim_*`  *(or `silver_*` / `bronze_*` in workshop drafts)* | TVF, MV, Dashboard | "{Natural language question}?" |
| UC-002 | ... | ... | ... | ... | ... |

**Use Case Catalog Rules:**
- Every use case MUST include 3-5 business questions phrased in natural language
- Every business question from the domain sections above MUST map to at least one use case
- Every artifact in the addendum summaries MUST trace back to at least one use case question
- Questions should be phrased as stakeholders would ask them (these become Genie benchmark candidates)
- Group related questions into a single use case when they share the same planning assets (Gold tables in acceleration; selected-layer tables in workshop) and grain

See [Worked Example: Wanderbricks](references/worked-example-wanderbricks.md) for 3 fully worked-out use case cards.

**Stakeholder Checkpoint:** After generating the use case catalog, present the Use Case Summary table to the user for review. Whether to block depends on prompt specificity:

- **If the user's prompt listed explicit output steps** (e.g., "analyze Gold layer, generate use-case plans, produce manifests"): treat as pre-approval. Include the summary table at the top of your response and proceed without blocking. Note: *"Use cases derived from Gold layer analysis — let me know if adjustments are needed before the next pipeline stage."*
- **If the user's prompt was open-ended** (e.g., "create a plan"): pause and ask for confirmation before proceeding to addendum generation.

If the user requests changes after seeing the summary, update the catalog and domain questions before continuing.

### Phase 2: Plan Document Generation

Create plan documents using templates in the following order:

1. **README** — `assets/templates/plans-readme-template.md` (plan index)
2. **Prerequisites** — `assets/templates/prerequisites-template.md` (data layer summary)
3. **Use Case Catalog** — `assets/templates/use-case-catalog-template.md` (consolidated use case definitions)
4. **Phase 1 Master** — `assets/templates/phase1-use-cases-template.md` (analytics artifacts)
5. **Addendums** (selected in Phase 1):
   - TVFs — `assets/templates/phase1-tvfs-template.md`
   - Alerting — `assets/templates/phase1-alerting-template.md`
   - Genie Spaces — `assets/templates/phase1-genie-spaces-template.md`
6. **Phase 2** — `assets/templates/phase2-agent-framework-template.md` (AI agents)
7. **Phase 3** — `assets/templates/phase3-frontend-template.md` (user interface)

#### Phase 2 Completion Gate

Before proceeding to Phase 3 (Manifests), verify that ALL selected plan documents exist on disk.

> **CANONICAL NUMBERING REFERENCE.** Every filename in the table below matches [`assets/addendum-numbering.md`](./assets/addendum-numbering.md) — the single source of truth for Phase 1 addendum numbers. If you are adding a new addendum, extend `addendum-numbering.md` **first**, then use the new name here. Never invent a number (e.g. the stale `phase1-addendum-1.1-dashboards.md` is forbidden — dashboards are `1.5-aibi-dashboards.md`).

| Document | Template | Required? |
|----------|----------|-----------|
| `plans/README.md` | `plans-readme-template.md` | ALWAYS |
| `plans/prerequisites.md` | `prerequisites-template.md` | ALWAYS |
| `plans/use-case-catalog.md` | `use-case-catalog-template.md` | ALWAYS |
| `plans/phase1-use-cases.md` | `phase1-use-cases-template.md` | ALWAYS |
| `plans/phase1-addendum-1.2-tvfs.md` | `phase1-tvfs-template.md` | If TVFs selected |
| `plans/phase1-addendum-1.3-metric-views.md` | (inline) | If Metric Views selected |
| `plans/phase1-addendum-1.6-genie-spaces.md` | `phase1-genie-spaces-template.md` | If Genie Spaces selected |
| `plans/phase1-addendum-1.4-lakehouse-monitoring.md` | (inline) | If Monitoring selected |
| `plans/phase1-addendum-1.5-aibi-dashboards.md` | (inline) | If Dashboards selected |
| `plans/phase1-addendum-1.7-alerting.md` | `phase1-alerting-template.md` | If Alerting selected |
| `plans/phase1-addendum-1.1-ml-models.md` | (inline) | If ML selected |

**If any required document is missing, create it from its template before generating manifests.** Manifests reference these files in `generated_from.plan_addendums` — they must exist on disk. **Workshop mode does not waive this gate**: artifact counts inside each document are capped, but the document set is unchanged.

#### Phase 2 Step 5 — Emit Source Dependency Manifest (MANDATORY, layer-aware)

**Before Phase 3 manifest generation, extract every source-layer table/column referenced across all plan addendums into a single machine-readable manifest.** This becomes the contract validated against the live catalog in the next step.

The manifest filename and shape depend on the Phase 0 selected layer:

| `planning_source.selected_layer` | File path | Top-level key |
|----------------------------------|-----------|---------------|
| `deployed_gold` or `gold_design` | `plans/manifests/gold-dependency-manifest.yaml` | `gold_dependencies:` |
| `deployed_silver`, `deployed_bronze`, `source_csv` (workshop) | `plans/manifests/source-dependency-manifest.yaml` | `source_dependencies:` |

Acceleration mode emits ONLY `gold-dependency-manifest.yaml` (existing behavior). Workshop mode emits whichever file matches its selected layer; when the selected layer is Gold, it emits `gold-dependency-manifest.yaml` for backward compatibility. Both shapes share the same `referenced_by` semantics.

```yaml
# plans/manifests/gold-dependency-manifest.yaml  (acceleration, or workshop with Gold source)
planning_mode: acceleration  # or workshop — mirror the parent manifest's planning_mode
planning_source:
  selected_layer: deployed_gold   # or gold_design
  schema: "<catalog>.<gold_schema>"
implementation_readiness: gold_ready  # or gold_design_only
requires_gold_promotion: false
generated_from:
  plan_addendums:
    - plans/phase1-use-cases.md
    - plans/phase1-addendum-1.2-tvfs.md
    - plans/phase1-addendum-1.3-metric-views.md
    - plans/phase1-addendum-1.5-aibi-dashboards.md
    - plans/phase1-addendum-1.6-genie-spaces.md
gold_dependencies:
  - table: fact_booking_daily
    columns: [booking_key, property_key, booking_date, net_revenue, nights]
    referenced_by:
      - semantic-layer/metric_views/revenue_analytics_metrics.yaml
      - semantic-layer/tvfs/get_revenue_by_property
      - observability/dashboards/revenue_overview.lvdash.json
  - table: dim_property
    columns: [property_key, property_name, destination_id, is_current]
    referenced_by:
      - semantic-layer/metric_views/revenue_analytics_metrics.yaml
summary:
  total_tables: 12
  total_columns: 84
  total_referenced_by: 37
```

```yaml
# plans/manifests/source-dependency-manifest.yaml  (workshop only; Bronze/Silver/source CSV)
planning_mode: workshop
planning_source:
  selected_layer: deployed_silver   # or deployed_bronze, source_csv
  schema: "<catalog>.<silver_schema>"   # null for source_csv
  source_csv_paths: []                  # populated for source_csv
implementation_readiness: workshop_deployable   # workshop_draft only when selected_layer=source_csv
requires_gold_promotion: false                  # advisory only; never gates deployment
generated_from:
  plan_addendums:
    - plans/phase1-use-cases.md
source_dependencies:
  - table: silver_bookings
    columns: [booking_id, property_id, booking_date, gross_amount]
    referenced_by:
      - planning/use_case_cards/revenue_overview.md
summary:
  total_tables: 4
  total_columns: 22
  total_referenced_by: 6
```

**Rules:**
- One entry per **distinct** source table; union all column references from all plan addendums.
- `referenced_by` uses relative artifact paths so downstream fixes can trace artifacts back to the missing column.
- Emit this manifest even when `planning_mode: workshop` — the workshop cap applies to artifact counts, not to manifest accuracy.
- The shape is identical to Gold's: only the filename, top-level key (`source_dependencies` vs `gold_dependencies`), and `planning_source` block change.

#### Phase 2 Step 6 — Live-Catalog Intersection (STOP / WARN Rule, MANDATORY, mode-aware)

**Immediately after emitting the dependency manifest, query the live catalog and cross-reference every table/column reference.** Downstream stages all assume the planning source is consistent with the live catalog — catching gaps HERE saves 5+ deploy cycles later.

The validation behavior depends on `planning_mode` and `planning_source.selected_layer`:

| Mode + selected layer | Behavior | Artifacts |
|------------------------|----------|-----------|
| `acceleration` + `deployed_gold` | **Fail-loud STOP** if any gap | Emit `plans/gold-gap-remediation.md`; raise |
| `acceleration` + `gold_design` (only when explicitly accepted) | **Warn** (Gold may not be deployed yet) | Emit `plans/gold-gap-remediation.md`; do NOT raise |
| `workshop` + `deployed_gold` | **Fail-loud STOP** if any gap (same as acceleration) | Emit `plans/gold-gap-remediation.md`; raise |
| `workshop` + `gold_design` | **Warn** | Emit `plans/gold-gap-remediation.md`; continue |
| `workshop` + `deployed_silver` / `deployed_bronze` | **Warn** | Emit `plans/source-gap-remediation.md`; continue |
| `workshop` + `source_csv` | **Skip live intersection** (no live schema to compare against) | None |

```python
import yaml
from pathlib import Path
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
catalog = "<lakehouse_default_catalog>"

# Choose which manifest to load based on Phase 0 selection.
gold_path   = Path("plans/manifests/gold-dependency-manifest.yaml")
source_path = Path("plans/manifests/source-dependency-manifest.yaml")
manifest_path = gold_path if gold_path.exists() else source_path
manifest = yaml.safe_load(manifest_path.read_text())

planning_mode    = manifest.get("planning_mode", "acceleration")
selected_layer   = manifest.get("planning_source", {}).get("selected_layer", "deployed_gold")
target_schema    = manifest.get("planning_source", {}).get("schema")  # e.g. "<catalog>.<schema>"
deps_key         = "gold_dependencies" if "gold_dependencies" in manifest else "source_dependencies"

# Workshop + source_csv: nothing to intersect against, skip.
if selected_layer == "source_csv":
    print("ℹ Skipping live-catalog intersection — selected_layer=source_csv has no live schema.")
else:
    # Pull every table and column from the live target schema in one shot.
    schema_only = target_schema.split(".")[-1]
    live_cols = (
        spark.sql(f"""
          SELECT table_name, column_name, full_data_type
          FROM {catalog}.information_schema.columns
          WHERE table_schema = '{schema_only}'
        """).collect()
    )
    live_index = {}
    for row in live_cols:
        live_index.setdefault(row.table_name, {})[row.column_name] = row.full_data_type

    missing_tables, missing_columns = [], []
    for dep in manifest[deps_key]:
        tbl = dep["table"]
        if tbl not in live_index:
            missing_tables.append({"table": tbl, "referenced_by": dep["referenced_by"]})
            continue
        for col in dep["columns"]:
            if col not in live_index[tbl]:
                missing_columns.append({"table": tbl, "column": col, "referenced_by": dep["referenced_by"]})

    if missing_tables or missing_columns:
        # Pick remediation filename based on dependency kind.
        remediation_path = Path(
            "plans/gold-gap-remediation.md" if deps_key == "gold_dependencies"
            else "plans/source-gap-remediation.md"
        )
        remediation_path.write_text(
            f"# {('Gold' if deps_key == 'gold_dependencies' else 'Source')} Dependency Gap Remediation\n\n"
            f"The following references in plan addendums do not exist in `{target_schema}`.\n\n"
            "## Missing tables\n\n"
            + "\n".join(f"- **{m['table']}** — referenced by {m['referenced_by']}" for m in missing_tables)
            + "\n\n## Missing columns\n\n"
            + "\n".join(
                f"- **{m['table']}.{m['column']}** — referenced by {m['referenced_by']}"
                for m in missing_columns
            )
            + "\n\n## Next steps\n\n"
            "1. Acceleration / Gold source: add tables to `gold_layer_design/yaml/` and re-run "
            "`gold/01-gold-layer-setup`.\n"
            "2. Workshop / Silver or Bronze: extend the corresponding setup skill (silver/bronze) "
            "and re-run.\n"
            "3. Re-run this Planning skill to regenerate manifests.\n"
        )

        is_strict = (planning_mode == "acceleration" and selected_layer == "deployed_gold") \
                 or (planning_mode == "workshop"     and selected_layer == "deployed_gold")
        msg = (f"{deps_key} gap detected: {len(missing_tables)} missing tables, "
               f"{len(missing_columns)} missing columns. See {remediation_path}.")
        if is_strict:
            raise RuntimeError(msg + " STOP — downstream orchestrators cannot proceed.")
        else:
            print(f"⚠ {msg} Continuing under non-strict mode/layer; downstream manifests "
                  f"will carry implementation_readiness=" + manifest.get("implementation_readiness", ""))
    else:
        print(f"✅ {deps_key} intersected cleanly with live catalog `{target_schema}`.")
```

**Escape flag:** If the user has an out-of-band reason to bypass the gap (e.g., Gold is intentionally incomplete for a phased rollout), they can pass `planning_allow_gold_gap: true` in their prompt. In that case, still emit the remediation file as a warning, but proceed to Phase 3 with a prominent `gold_gap_acknowledged: true` marker in every downstream manifest. This flag does NOT relax mode-specific behavior; non-Gold workshop manifests already carry `implementation_readiness: workshop_deployable` (Silver/Bronze) or `workshop_draft` (source CSV).

### Phase 3: Manifest Generation (Plan-as-Contract)

After creating plan documents, generate **machine-readable YAML manifests** that downstream orchestrators consume as implementation contracts.

**Why manifests?** The "Extract, Don't Generate" principle applies to the planning-to-implementation handoff. Manifests ensure downstream orchestrators implement exactly what was planned — no missed artifacts, no naming inconsistencies.

**MANDATORY: Read the manifest generation guide:**

| # | Reference Path | What It Provides |
|---|----------------|------------------|
| 1 | `references/manifest-generation-guide.md` | Full manifest workflow, validation, consumption pattern |

**Steps:**
1. Review Gold layer YAML schemas in `gold_layer_design/yaml/`
2. For each plan addendum, extract the concrete artifact definitions
3. Generate 4 YAML manifests using templates from `assets/templates/manifests/`:
   - `plans/manifests/semantic-layer-manifest.yaml` — TVFs, Metric Views, Genie Spaces
   - `plans/manifests/observability-manifest.yaml` — Monitors, Dashboards, Alerts
   - `plans/manifests/ml-manifest.yaml` — Feature Tables, Models, Experiments
   - `plans/manifests/genai-agents-manifest.yaml` — Agents, Tools, Eval Datasets
4. For each artifact in a manifest, add `use_case_refs` listing the UC# it implements (from `plans/use-case-catalog.md`)
5. Validate all table/column references exist in Gold YAML
6. Verify summary counts match actual artifact counts
7. Run `python scripts/validate_use_case_coverage.py plans/use-case-catalog.md` to verify coverage
8. Commit manifests alongside plan documents

**Key principle:** Every artifact in a manifest MUST trace back to (a) a Gold layer table and (b) a business question from the plan addendum.

**Output Structure:**
```
plans/
├── use-case-catalog.md                    # Consolidated use case definitions
├── manifests/
│   ├── semantic-layer-manifest.yaml       # → consumed by semantic-layer/00-*
│   ├── observability-manifest.yaml        # → consumed by monitoring/00-*
│   ├── ml-manifest.yaml                   # → consumed by ml/00-*
│   └── genai-agents-manifest.yaml         # → consumed by genai-agents/00-*
```

**Downstream consumption:** Each downstream orchestrator (stages 6-9) has a **Phase 0: Read Plan** step that reads its manifest. If the manifest doesn't exist (e.g., user skipped Planning), the orchestrator falls back to self-discovery from Gold tables.

---

## Plan Structure Framework

### Standard Project Phases

```
plans/
├── README.md                              # Index and overview
├── use-case-catalog.md                    # Consolidated use case definitions
├── prerequisites.md                       # Bronze/Silver/Gold summary (optional)
├── phase1-use-cases.md                    # Analytics artifacts (master)
│   ├── phase1-addendum-1.1-ml-models.md
│   ├── phase1-addendum-1.2-tvfs.md
│   ├── phase1-addendum-1.3-metric-views.md
│   ├── phase1-addendum-1.4-lakehouse-monitoring.md
│   ├── phase1-addendum-1.5-aibi-dashboards.md
│   ├── phase1-addendum-1.6-genie-spaces.md
│   └── phase1-addendum-1.7-alerting.md
├── phase2-agent-framework.md              # AI Agents
├── phase3-frontend-app.md                 # User Interface
└── manifests/                             # Machine-readable contracts
    ├── semantic-layer-manifest.yaml       # → semantic-layer/00-*
    ├── observability-manifest.yaml        # → monitoring/00-*
    ├── ml-manifest.yaml                   # → ml/00-*
    └── genai-agents-manifest.yaml         # → genai-agents/00-*
```

### Phase Dependencies

```
Prerequisites (Bronze → Silver → Gold) → Phase 1 (Use Cases) → Phase 2 (Agents) → Phase 3 (Frontend)
         [COMPLETE]                               ↓
                                           All Addendums
```

## Agent Domain Framework

### Core Principle

**ALL artifacts across ALL phases MUST be organized by Agent Domain.** This ensures:
- Consistent categorization across 100+ artifacts
- Clear ownership by future AI agents
- Easy discoverability for users
- Aligned tooling for each domain

### Agent Domain Application

Every artifact (TVF, Metric View, Dashboard, Alert, ML Model, Monitor, Genie Space) must:
1. Be tagged with its Agent Domain
2. Use the domain's planning assets (Gold tables in acceleration; selected-layer tables in workshop)
3. Answer domain-specific questions
4. Be grouped with related domain artifacts in documentation

**Example Pattern:**
```markdown
## {Domain}: get_{metric}_by_{dimension}

**Agent Domain:** {Domain}
**Planning Assets:** `fact_{entity}`, `dim_{entity}`   # or `silver_{entity}` / `bronze_{entity}` in workshop drafts
**Business Questions:** "What are the top {metric} by {dimension}?"
```

See [Industry Domain Patterns](references/industry-domain-patterns.md) for domain templates by industry.

## Agent Layer Architecture Pattern

### Core Principle: Agents Use Genie Spaces as Query Interface

**AI Agents DO NOT query data assets directly.** Instead, they use Genie Spaces as their natural language query interface. Genie Spaces translate natural language to SQL and route to appropriate tools.

```
USERS (Natural Language)
    ↓
PHASE 2: AI AGENT LAYER (LangChain/LangGraph)
    ├── Orchestrator Agent (intent classification)
    └── Specialized Agents (1 per domain)
            ↓
PHASE 1.6: GENIE SPACES (NL Query Execution)
    ├── {Domain 1} Intelligence Genie Space
    ├── {Domain 2} Intelligence Genie Space
    └── Unified {Project} Monitor
            ↓
PHASE 1: DATA ASSETS (Agent Tools)
    ├── Metric Views (pre-aggregated - use FIRST)
    ├── TVFs (parameterized queries)
    ├── ML Predictions (ML-powered insights)
    └── Lakehouse Monitors (drift detection)
            ↓
PREREQUISITES: GOLD LAYER (Foundation)
```

### Deployment Order (Critical!)

**Genie Spaces MUST be deployed BEFORE agents can use them.**

```
Phase 1.1-1.5 (Data Assets) → Phase 1.6 (Genie Spaces) → Phase 2 (Agents)
         ↓                            ↓                        ↓
   Build foundation          Create NL interface        Consume interface
```

For detailed architecture, design patterns, "Why Genie Spaces" comparison, and testing strategy, see [Agent Layer Architecture](references/agent-layer-architecture.md).

## Artifact Rationalization Framework

**MANDATORY: Read** `references/rationalization-framework.md` for complete sizing guides, decision matrices, and naming conventions.

**Core Principle:** Every artifact must trace to a specific business question. Do not create artifacts to fill quotas.

**Critical constraints (always enforce, even without reading the reference):**
- Genie Spaces: **max 25 assets per space**; 10-25 per space is optimal; <10 = merge spaces
- TVFs: **only** when Metric Views cannot answer the question (requires parameterized multi-table logic)
- Metric Views: one per distinct analytical grain, not per domain
- Domains: emerge from business questions (min 3 questions per domain); merge if >70% planning-asset overlap
- Naming: `get_{domain}_{metric}` for TVFs, `{domain}_analytics_metrics` for Metric Views

## SQL Query Standards

**ALWAYS use Gold layer tables for production deployable artifacts, NEVER `system.*` tables directly.** Reference pattern: `${catalog}.${gold_schema}.table_name`. In workshop deployments built from Silver or Bronze (`implementation_readiness: workshop_deployable`), SQL **does** reference `${catalog}.${silver_schema}.*` or `${catalog}.${bronze_schema}.*` directly — the workshop semantic layer is built on top of those tables. `requires_gold_promotion` is an advisory flag recommending Gold promotion for production hardening; it does not block workshop deployment.

- Date parameters: `STRING` type (Genie compatible), cast at query time: `CAST(start_date AS DATE)`
- SCD Type 2 joins: `LEFT JOIN dim_{entity} d ON f.{entity}_id = d.{entity}_id AND d.is_current = TRUE`

## Documentation Quality Standards

**LLM-Friendly Comments** — All artifacts must include: what it does, when to use it, example questions it answers. Pattern: `COMMENT 'LLM: Returns top N {metric}... Example questions: "What are the top 10...?"'`

**Summary Tables** — Every addendum must include: overview table (all artifacts with domain, dependencies, status), by-domain sections, count summary, and success criteria.

## Common Mistakes to Avoid

| Mistake | Correct Approach |
|---------|-----------------|
| Querying `system.*` tables directly | Always use Gold layer: `${catalog}.${gold_schema}.fact_*` |
| Omitting Agent Domain on artifacts | Every artifact must be tagged: `## {Domain}: get_{metric}` |
| Adding a TVF without cross-addendum check | Also consider: Metric View counterpart? Alert? Dashboard? |
| Using `DATE` type in TVF parameters | Use `STRING COMMENT 'Format: YYYY-MM-DD'` (Genie compatible) |
| Deploying agents before Genie Spaces | Genie Spaces MUST be deployed first — agents consume them |
| Genie Space with 25+ assets | Split by domain cohesion; each space 10-25 assets |
| One Genie Space per domain when assets are thin | Consolidate thin domains (<10 assets) into fewer spaces |
| TVF that duplicates a Metric View | TVFs only when multi-period/multi-table parameterized logic is needed |
| Forcing a fixed domain count | Let business questions determine domains — 2-3 focused > 5-6 thin |
| Counting a Genie Space as artifact coverage for a use-case question | Genie Space is an interface layer, not an implementing artifact. Every question must be answerable by at least one TVF, Metric View, or listed Gold table in the Genie Space's asset list. |
| Inventing new YAML keys when the manifest template doesn't fit | Adapt within the template schema first. If the template is truly insufficient (e.g., unified cross-domain Genie Space), extend the template with a documented key (e.g., `unified_genie_space`) — never ship ad-hoc schema a downstream consumer doesn't know to look for. |

## Reference Files

- **[Phase Details](references/phase-details.md)** — Full phase and addendum descriptions with deliverables
- **[Estimation Guide](references/estimation-guide.md)** — Effort estimation, dependency management, risks
- **[Agent Layer Architecture](references/agent-layer-architecture.md)** — Detailed architecture, "Why Genie Spaces" comparison, design patterns, testing strategy, multi-agent query example
- **[Industry Domain Patterns](references/industry-domain-patterns.md)** — Domain templates for Hospitality, Retail, Healthcare, Finance, SaaS, and Databricks System Tables
- **[Worked Example: Wanderbricks](references/worked-example-wanderbricks.md)** — Complete 101-artifact project example with TVF SQL, Metric View YAML, Alert YAML
- **[Manifest Generation Guide](references/manifest-generation-guide.md)** — Plan-as-contract pattern: how to generate YAML manifests for downstream orchestrators

## Assets

### Plan Templates
- **[Project Plan Template](assets/templates/project-plan-template.md)** — Generic phase template with SQL standards
- **[Prerequisites Template](assets/templates/prerequisites-template.md)** — Data layer summary (Bronze/Silver/Gold)
- **[Use Case Catalog Template](assets/templates/use-case-catalog-template.md)** — Consolidated use case definitions with business questions
- **[Phase 1 Use Cases Template](assets/templates/phase1-use-cases-template.md)** — Master analytics artifacts
- **[Phase 1 TVFs Template](assets/templates/phase1-tvfs-template.md)** — Table-Valued Functions addendum
- **[Phase 1 Alerting Template](assets/templates/phase1-alerting-template.md)** — Alerting framework addendum
- **[Phase 1 Genie Spaces Template](assets/templates/phase1-genie-spaces-template.md)** — Genie Spaces addendum with Agent readiness
- **[Phase 2 Agent Framework Template](assets/templates/phase2-agent-framework-template.md)** — AI agents with Genie integration
- **[Phase 3 Frontend Template](assets/templates/phase3-frontend-template.md)** — User interface
- **[Plans README Template](assets/templates/plans-readme-template.md)** — plans/ folder index

### Manifest Templates (Plan-as-Contract)
- **[Semantic Layer Manifest](assets/templates/manifests/semantic-layer-manifest.yaml)** — TVFs, Metric Views, Genie Spaces contract
- **[Observability Manifest](assets/templates/manifests/observability-manifest.yaml)** — Monitors, Dashboards, Alerts contract
- **[ML Manifest](assets/templates/manifests/ml-manifest.yaml)** — Feature Tables, Models, Experiments contract
- **[GenAI Agents Manifest](assets/templates/manifests/genai-agents-manifest.yaml)** — Agents, Tools, Eval Datasets contract

## Validation Checklist

### Structure
- [ ] Follows standard template
- [ ] Has Overview with Status, Dependencies, Effort
- [ ] Organized by Agent Domain
- [ ] Includes code examples
- [ ] Has Success Criteria table
- [ ] Has References section

### Content Quality
- [ ] All queries reference the planning-source layer (Gold for acceleration; Gold/Silver/Bronze for workshop deployments per `planning_source.selected_layer`); never `system.*` tables directly
- [ ] All artifacts tagged with Agent Domain
- [ ] LLM-friendly comments on all artifacts
- [ ] Examples use `${catalog}.${gold_schema}` variables for Gold sources, or `${silver_schema}` / `${bronze_schema}` for workshop deployments on those layers
- [ ] Summary tables are accurate and complete
- [ ] Every emitted manifest carries `planning_source`, `implementation_readiness`, and `requires_gold_promotion` from Phase 0 (with `requires_gold_promotion` as advisory only)

### Cross-References
- [ ] Main phase document links to addendums
- [ ] Addendums link back to main phase
- [ ] Related artifacts cross-reference each other
- [ ] Dependencies are documented

### Use Case Traceability
- [ ] Use case catalog exists with one entry per distinct business problem
- [ ] Every use case includes 3-5 business questions in natural language
- [ ] Every business question from domain sections maps to at least one use case
- [ ] Every artifact in addendum summaries traces back to at least one use case question
- [ ] Use case catalog cross-references addendum documents

### Completeness
- [ ] Domains derived from business questions (not forced to a fixed count)
- [ ] Every TVF traces to a business question that Metric Views cannot answer
- [ ] Every Metric View covers a distinct analytical grain (no duplicates)
- [ ] Key business questions documented per domain (≥3 per domain)
- [ ] All Phase 1 addendums included
- [ ] User requirements addressed
- [ ] Reference patterns incorporated

### Rationalization (Prevent Bloat)
- [ ] Each Genie Space has ≤ 25 data assets
- [ ] No Genie Space has < 10 assets (merge thin spaces)
- [ ] Genie Space count justified by asset volume (not just domain count)
- [ ] No TVF duplicates a Metric View query
- [ ] No domain has < 3 distinct business questions (merge small domains)
- [ ] Domains with >70% planning-asset overlap (Gold/Silver/Bronze, by selected layer) are consolidated

### Agent Layer Architecture (If Phase 2 Included)
- [ ] Agent-to-Genie Space mapping documented (1:1 recommended)
- [ ] Deployment order specified (Genie Spaces before Agents)
- [ ] Three-level testing strategy defined
- [ ] Orchestrator agent included for multi-domain coordination
- [ ] Genie Space instructions documented (become agent system prompts)
- [ ] Agent tool definitions reference Genie Spaces (not direct SQL)

## Key Learnings

1. **Agent Domain framework** provides consistent organization across all artifacts — every artifact gets a domain tag
2. **Planning-source layer references only** — never query `system.*` tables directly. Acceleration uses `${catalog}.${gold_schema}.*`. Workshop deployments use `${gold_schema}` / `${silver_schema}` / `${bronze_schema}` based on `planning_source.selected_layer`
3. **Cross-addendum updates** — user requirements span multiple addendums; update all affected documents
4. **LLM-friendly comments** are critical for Genie/AI/BI integration — include example questions
5. **Agents use Genie Spaces as abstraction** — agents don't write SQL; Genie handles NL-to-SQL translation, optimization, and guardrails
6. **1:1 Agent-to-Genie mapping** recommended; Orchestrator agent uses Unified Genie Space for intent classification
7. **Deploy Genie Spaces before agents** — three-level testing: assets → Genie → Agents
8. **Genie Space 25-asset hard limit** — plan space count from total asset volume, not domain count; fewer focused spaces > many thin ones
9. **Rationalize before creating** — every artifact must trace to a business question; TVFs only when Metric Views can't answer
10. **Domains emerge from data** — business questions and planning-asset groupings (Gold by default; Silver/Bronze in workshop deployments) determine natural domain boundaries

## References

### Official Documentation
- [Databricks Docs](https://docs.databricks.com/)
- [Unity Catalog](https://docs.databricks.com/unity-catalog/)
- [Delta Live Tables](https://docs.databricks.com/dlt/)
- [Lakehouse Monitoring](https://docs.databricks.com/lakehouse-monitoring/)
- [Metric Views](https://docs.databricks.com/metric-views/)
- [Genie Spaces](https://docs.databricks.com/genie/)
- [Model Serving](https://docs.databricks.com/machine-learning/model-serving/)
- [Foundation Models (DBRX)](https://docs.databricks.com/machine-learning/foundation-models/)
- [Databricks System Tables](https://docs.databricks.com/administration-guide/system-tables/)
- [SQL Alerts](https://docs.databricks.com/sql/user/alerts/)
- [Table-Valued Functions](https://docs.databricks.com/sql/language-manual/sql-ref-syntax-ddl-create-sql-function.html)

### Related Skills
- [databricks-table-valued-functions](../../semantic-layer/02-databricks-table-valued-functions/SKILL.md)
- [metric-views-patterns](../../semantic-layer/01-metric-views-patterns/SKILL.md)
- [lakehouse-monitoring-comprehensive](../../monitoring/01-lakehouse-monitoring-comprehensive/SKILL.md)
- [databricks-aibi-dashboards](../../monitoring/02-databricks-aibi-dashboards/SKILL.md)
- [genie-space-patterns](../../semantic-layer/03-genie-space-patterns/SKILL.md) — Genie Space setup for agents

### Agent Framework Technologies
- [LangChain](https://python.langchain.com/) | [LangGraph](https://langchain-ai.github.io/langgraph/)

## Pipeline Progression

**Previous stage (acceleration):** `gold/01-gold-layer-setup` → Gold layer tables and merge scripts should be complete.

**Previous stage (workshop):** ANY of `bronze/00-bronze-layer-setup`, `silver/00-silver-layer-setup`, `gold/00-gold-layer-design`, or `gold/01-gold-layer-setup`. Phase 0 picks the highest-fidelity input automatically.

**Next stage:** After completing the project plan for remaining phases, proceed to:
- **`semantic-layer/00-semantic-layer-setup`** — Build Metric Views, TVFs, and Genie Spaces on top of the planning source. For Gold sources, deployment runs against `gold_schema` (production path). For workshop manifests with `implementation_readiness: workshop_deployable` (Silver/Bronze), deployment runs directly against the selected layer with a quality advisory; Gold promotion is recommended for production. For `implementation_readiness: workshop_draft` (source CSV), the orchestrator stops because there are no live tables to deploy against.

---

## Post-Completion: Skill Usage Summary (MANDATORY)

**After completing all phases of this orchestrator, output a Skill Usage Summary reflecting what you ACTUALLY did — not a pre-written summary.**

### What to Include

1. Every skill `SKILL.md` or `references/` file you read (via the Read tool), in the order you read them
2. Which phase you were in when you read it
3. Whether it was a **Common**, **Reference**, or **Template** file
4. A one-line description of what you specifically used it for in this session

### Format

| # | Phase | Skill / Reference Read | Type | What It Was Used For |
|---|-------|----------------------|------|---------------------|
| 1 | Phase N | `path/to/SKILL.md` | Common / Reference / Template | One-line description |

### Summary Footer

End with:
- **Totals:** X common skills, Y reference files, Z templates read across N phases
- **Manifests emitted:** List each manifest file generated and its artifact count
- **Skipped:** List any expected references or templates that you did NOT need to read, and why
- **Unplanned:** List any skills you read that were NOT listed in the dependency table (e.g., for troubleshooting, edge cases, or user-requested detours)
