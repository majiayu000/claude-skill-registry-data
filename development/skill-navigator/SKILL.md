---
name: skill-navigator
description: Intelligent skill navigation system with tiered loading and orchestrator-first routing for context-efficient agent operation. Routes tasks to the correct domain skill based on keyword detection with orchestrator priority. Each skill uses progressive disclosure with references/, scripts/, and assets/ directories. Use this skill as the entry point for any Databricks-related task to determine which specialized skills to load.
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "Routing/navigator meta-skill — selects which domain skills to load; no deployed resource and no deploy verb. Client-agnostic routing. Client-awareness layer present (M06): `client_context` is detected/gated by `skills/vibecoding-state` and `skills/genie-code-environment` is loaded on demand — see the Tier-1-thin note under Context Budget Management."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "3.0"
  domain: meta
  role: navigator
  last_verified: "2026-06-02"
  volatility: low
  upstream_sources: []  # Internal routing
---

# Skill Navigator: Context-Aware Tiered Loading System

## Purpose

This navigation skill implements **tiered context loading** with **orchestrator-first routing** to keep total context under Claude Opus's 200K token limit. After restructuring, ALL SKILL.md files are lightweight (< 2K tokens each). The heavy content lives in `references/` files loaded on demand.

**For detailed domain index summaries, see:** [references/domain-indexes.md](references/domain-indexes.md)

**For visual learners:**
- [Interactive Skill Navigation Guide](../../docs/framework-design/10-skill-navigation-visual-guide.html) — animated browser-based walkthrough
- [Skill Hierarchy Tree](../../docs/framework-design/11-skill-hierarchy-tree.html) — visual organization map

**For orchestrator deep dives:**
- [Gold Design Orchestrator Walkthrough](../../docs/framework-design/13-gold-design-orchestrator-walkthrough.md)
- [Silver Orchestrator Walkthrough](../../docs/framework-design/14-silver-orchestrator-walkthrough.md)
- [Gold Pipeline Orchestrator Walkthrough](../../docs/framework-design/15-gold-pipeline-orchestrator-walkthrough.md)
- [Semantic Layer Orchestrator Walkthrough](../../docs/framework-design/12-semantic-layer-orchestrator-walkthrough.md)
- [Genie Optimization Agent Walkthrough](../../docs/agent-walkthrough.md)

**For efficiency optimization:**
- [Parallel Execution Guide](../../docs/framework-design/09-parallel-execution-guide.md) — run independent stages concurrently

---

## Pipeline Progression Overview (Design-First)

This framework uses a **Design-First** pipeline: design the target Gold model from the customer's schema CSV, then build the data layers (Bronze → Silver) to feed it, then implement.

**Entry point:** Customer provides a source schema CSV in `data_product_accelerator/context/`. Start with Gold Design.

| Stage | Name | Orchestrator Skill | Key Deliverables |
|-------|------|-------------------|-----------------|
| 1 | Gold Design | `gold/00-gold-layer-design` | Read schema CSV → ERDs, YAML schemas, documentation |
| 2 | Bronze | `bronze/00-bronze-layer-setup` | Bronze Delta tables matching source schema + Faker data |
| 3 | Silver | `silver/00-silver-layer-setup` | DLT pipelines with DQ rules |
| 4 | Gold Implementation | `gold/01-gold-layer-setup` | Tables, merge scripts, FK constraints |
| 5 | Planning | `planning/00-project-planning` | Plan semantic, observability, ML, GenAI phases |
| 6 | Semantic Layer | `semantic-layer/00-semantic-layer-setup` | Metric Views, TVFs, Genie Spaces |
| 7 | Observability | `monitoring/00-observability-setup` | Monitors, dashboards, alerts |
| 8 | ML | `ml/00-ml-pipeline-setup` | ML experiments, models, inference |
| 9 | GenAI Agents | `genai-agents/00-course-orchestrator` | Agents, evaluation, deployment |

```
data_product_accelerator/context/*.csv → Gold Design (1) → Bronze (2) → Silver (3) → Gold Impl (4) → Planning (5) → Semantic (6) → Observability (7) → ML (8) → GenAI (9)
```

---

## Plan-as-Contract Pattern

The Planning orchestrator (stage 5) generates **YAML manifest files** that downstream orchestrators (stages 6-9) consume as implementation contracts. This follows the "Extract, Don't Generate" principle for the planning-to-implementation handoff.

```
Gold YAML ─► Planning (stage 5) ─► Manifests ─► Downstream Orchestrators (stages 6-9)
                   │                    │
                emits:              consumes:
                4 manifests         1 manifest each
```

| Manifest | Emitted By | Consumed By |
|---|---|---|
| `plans/manifests/semantic-layer-manifest.yaml` | `planning/00-*` | `semantic-layer/00-*` (stage 6) |
| `plans/manifests/observability-manifest.yaml` | `planning/00-*` | `monitoring/00-*` (stage 7) |
| `plans/manifests/ml-manifest.yaml` | `planning/00-*` | `ml/00-*` (stage 8) |
| `plans/manifests/genai-agents-manifest.yaml` | `planning/00-*` | `genai-agents/00-*` (stage 9) |

Each downstream orchestrator has a **Phase 0: Read Plan** step that reads its manifest. If the manifest doesn't exist (e.g., user skipped Planning), the orchestrator falls back to **self-discovery** from Gold tables.

**Key metadata fields:** `emits` (on Planning), `consumes` + `consumes_fallback` (on downstream orchestrators).

**See also:** [Semantic Layer Orchestrator Walkthrough](../../docs/framework-design/12-semantic-layer-orchestrator-walkthrough.md) for a detailed example of how orchestrators consume manifests and fall back to self-discovery.

---

## Input Convention: `data_product_accelerator/context/` Directory

The `data_product_accelerator/context/` directory is the **standard location** for customer-provided input metadata that drives the entire pipeline:

```
data_product_accelerator/
└── context/
    ├── {ProjectName}_Schema.csv     # MANDATORY: Customer source schema (THE starting input)
    ├── business_requirements.md     # Optional: Business context, use cases, stakeholders
    └── prompts/                     # Legacy prompt templates (reference only)
```

**The schema CSV** (e.g., `data_product_accelerator/context/Wanderbricks_Schema.csv`) contains table and column metadata exported from the customer's source system. Expected columns: `table_catalog`, `table_schema`, `table_name`, `column_name`, `ordinal_position`, `full_data_type`, `data_type`, `is_nullable`, `comment`.

**Who reads it:**
- `gold/00-gold-layer-design` (Phase 0: Schema Intake) — parses into table inventory for dimensional modeling
- `bronze/00-bronze-layer-setup` (Approach A) — creates Bronze DDLs matching source schema

## Output Convention: Generated Artifacts at Repository Root

All generated artifacts are created at the **repository root** (parent of `data_product_accelerator/`), not inside the framework module:

| Artifact | Created By | Path (from repo root) |
|----------|-----------|----------------------|
| Dimensional model YAMLs, ERDs | Gold Design (stage 1) | `gold_layer_design/` |
| Notebooks and scripts | Bronze, Silver, Gold, Semantic, ML skills | `src/` |
| Phase plans and manifests | Planning (stage 5) | `plans/` |
| DAB job/pipeline YAML | Asset Bundle skills | `resources/` |
| Bundle root config | Asset Bundle skills | `databricks.yml` |

This separation keeps the framework (`data_product_accelerator/`) read-only and portable, while generated code lives alongside it at the repo root.

---

## CRITICAL: Skill Structure (Post-Restructuring)

Every skill now follows **progressive disclosure** and **numbered ordering**:

```
domain-folder/
├── 00-orchestrator-skill/       # Orchestrator (manages end-to-end workflow)
│   ├── SKILL.md                 # Overview, critical rules, mandatory deps
│   ├── references/              # Detailed patterns (loaded on demand)
│   ├── scripts/                 # Validation utilities
│   └── assets/templates/        # YAML, SQL, JSON starters
├── 01-worker-skill/             # Worker (specific patterns)
│   ├── SKILL.md
│   └── references/
├── 02-worker-skill/             # Worker (more patterns)
│   └── SKILL.md
└── ...
```

### Numbering Convention
- `00-` = Orchestrator (start here for end-to-end workflows)
- `01-`, `02-`, ... = Workers (specific patterns, loaded by orchestrator or standalone)
- **Gold domain exception:** Workers are organized into `design-workers/` (Stage 1 design phase) and `pipeline-workers/` (Stage 4 implementation phase) subdirectories instead of numbered prefixes

### How to Navigate Within a Skill
1. **Read SKILL.md first** (~1-2K tokens) — Contains overview, critical rules, and links
2. **Read specific references/ files** only when you need detailed patterns
3. **Execute scripts/** as black-box utilities
4. **Copy assets/templates/** as starting points

---

## Routing Algorithm

```
1. User request received
2. Detect domain keywords (see table below)
3. IF keyword matches an ORCHESTRATOR skill → Route to orchestrator
   - Orchestrator will call worker skills via MANDATORY Read pattern
4. IF keyword matches a WORKER skill AND no orchestrator context → Route to worker directly
   - Worker skills have standalone: true and work independently
5. IF keyword matches a WORKER skill AND orchestrator is active → Let orchestrator handle it
```

---

## Context Budget Management

**Claude Opus Context Limit:** 200K tokens
**Target Operating Budget:** 40-60K tokens (for optimal performance)
**Maximum Skill Budget:** 80K tokens (leaves room for code/files)

| Tier | Purpose | Token Budget | Content |
|---|---|---|---|
| **Tier 1: Core** | Always loaded | ~4K tokens | 4 core SKILL.md files |
| **Tier 2: Domain Index** | Loaded on domain detection | ~2K per domain | Domain summaries |
| **Tier 3: SKILL.md** | Loaded on specific task | ~1-2K each | Individual skill overview |
| **Tier 4: References** | Loaded on demand | ~2-8K each | Detailed patterns & guides |

> **Client awareness (Tier-1-thin).** This navigator routes the same way for every client. `skills/vibecoding-state` detects and gates `client_context`; load `skills/genie-code-environment` **on demand** (Tier 4) only when running on the in-workspace agent and a routed skill flags a client caveat (its `deploy_note` / `coverage`). Routed prompts open with a client-specific RULE_0 preamble — follow it. Keep this routing layer thin; behavior detail stays in `genie-code-environment`.

---

## Task Detection & Skill Routing Table

### Bootstrap / New Project Route (start here)

| Task Keywords | Route To |
|---|---|
| "new project", "schema CSV", "customer schema", "bootstrap", "start from scratch", "onboarding", "build data platform" | `gold/00-gold-layer-design` (Stage 1 — reads schema CSV from `data_product_accelerator/context/`) |

### Orchestrator Routes (prefer these for end-to-end workflows)

| Task Keywords | Domain | Route To (Orchestrator) |
|---|---|---|
| "design Gold", "dimensional model", "Gold from scratch", "schema CSV" | Gold | `gold/00-gold-layer-design` (stage 1) |
| "Bronze setup", "Bronze tables", "test data", "demo data" | Bronze | `bronze/00-bronze-layer-setup` (stage 2) |
| "Silver layer", "create Silver", "Bronze to Silver", "Silver pipeline" | Silver | `silver/00-silver-layer-setup` (stage 3) |
| "implement Gold", "Gold tables", "Gold merge scripts" | Gold | `gold/01-gold-layer-setup` (stage 4) |
| "project plan", "architecture planning", "planning_mode: workshop" | Planning | `planning/00-project-planning` (stage 5) |
| "semantic layer", "build Genie", "Metric Views and TVFs" | Semantic | `semantic-layer/00-semantic-layer-setup` (stage 6) |
| "observability", "monitoring setup", "dashboards and alerts" | Monitoring | `monitoring/00-observability-setup` (stage 7) |
| "MLflow", "ML pipeline", "model training" | ML | `ml/00-ml-pipeline-setup` (stage 8) |
| "GenAI agent", "build agent", "ResponsesAgent" | GenAI | `genai-agents/00-course-orchestrator` (stage 9) |

### Worker Routes (for standalone/specific tasks)

| Task Keywords | Domain | Route To (Worker) |
|---|---|---|
| "Faker", "synthetic", "corruption" | Bronze | `bronze/01-faker-data-generation` |
| "DLT", "expectations" | Silver | `silver/01-dlt-expectations-patterns` |
| "DQX", "validation" | Silver | `silver/02-dqx-patterns` |
| "Gold merge", "MERGE" | Gold | `gold/pipeline-workers/02-merge-patterns` |
| "duplicate key" | Gold | `gold/pipeline-workers/03-deduplication` |
| "Gold documentation" | Gold | `gold/design-workers/06-table-documentation` |
| "ERD", "diagram" | Gold | `gold/design-workers/05-erd-diagrams` |
| "dimension pattern", "role-playing", "junk dimension", "hierarchy" | Gold | `gold/design-workers/02-dimension-patterns` |
| "fact pattern", "factless", "accumulating snapshot", "measure additivity" | Gold | `gold/design-workers/03-fact-table-patterns` |
| "conformed dimension", "bus matrix", "drill-across" | Gold | `gold/design-workers/04-conformed-dimensions` |
| "design validation", "validate model" | Gold | `gold/design-workers/07-design-validation` |
| "industry alignment", "industry data model", "Vibe data model", "industry coverage" | Gold | `gold/design-workers/08-industry-alignment` |
| "schema validation" | Gold | `gold/pipeline-workers/05-schema-validation` |
| "fact grain" | Gold | `gold/pipeline-workers/04-grain-validation` |
| "YAML setup" | Gold | `gold/pipeline-workers/01-yaml-table-setup` |
| "metric view", "semantic" | Semantic | `semantic-layer/01-metric-views-patterns` |
| "TVF", "function" | Semantic | `semantic-layer/02-databricks-table-valued-functions` |
| "Genie Space", "Genie setup" | Semantic | `semantic-layer/03-genie-space-patterns` |
| "Genie API", "export/import" | Semantic | `semantic-layer/04-genie-space-export-import-api` |
| "monitoring", "Lakehouse" | Monitor | `monitoring/01-lakehouse-monitoring-comprehensive` |
| "dashboard", "AI/BI" | Monitor | `monitoring/02-databricks-aibi-dashboards` |
| "alert", "SQL alert" | Monitor | `monitoring/03-sql-alerting-patterns` |
| "anomaly detection", "freshness", "completeness", "stale tables", "unhealthy tables" | Monitor | `monitoring/04-anomaly-detection` |
| "deploy", "Asset Bundle" | Infra | `skills/databricks-asset-bundles` |
| "schema", "CREATE SCHEMA" | Infra | `common/schema-management-patterns` |
| "table properties" | Infra | `common/databricks-table-properties` |
| "constraints", "PK/FK" | Infra | `common/unity-catalog-constraints` |
| "Python imports" | Infra | `common/databricks-python-imports` |
| "job failed", "troubleshoot", "self-heal", "redeploy", "diagnose", "deploy failed", "pipeline failed" | Ops | `common/databricks-autonomous-operations` |
| "naming", "snake_case", "COMMENT", "tag", "PII", "cost_center", "dim_", "fact_", "governed tag", "budget policy" | Standards | `common/naming-tagging-standards` |
| "ResponsesAgent", "predict_stream", "AI Playground" | GenAI | `genai-agents/01-responses-agent-patterns` |
| "evaluation", "LLM judge", "scorer" | GenAI | `genai-agents/02-mlflow-genai-evaluation` |
| "Lakebase memory", "CheckpointSaver", "stateful agent" | GenAI | `genai-agents/03-lakebase-memory-patterns` |
| "prompt registry", "prompt versioning" | GenAI | `genai-agents/04-prompt-registry-patterns` |
| "multi-agent", "Genie orchestration", "intent classification" | GenAI | `genai-agents/05-multi-agent-genie-orchestration` |
| "deploy agent", "deployment job" | GenAI | `genai-agents/06-deployment-automation` |
| "production monitoring", "registered scorers" | GenAI | `genai-agents/07-production-monitoring` |
| "MLflow GenAI", "MLflow tracing", "GenAI foundation" | GenAI | `genai-agents/08-mlflow-genai-foundation` |
| "simple agent", "scaffold agent", "MCP agent", "quick agent", "tool calling agent" | GenAI | `genai-agents/09-simple-agent-scaffold` |
| "exploration notebook" | Explore | `exploration/00-adhoc-exploration-notebooks` |
| "create skill", "new skill", "SKILL.md" | Admin | `admin/create-agent-skill` |
| "improve skills" | Admin | `admin/self-improvement` |
| "audit skills", "check freshness", "stale skills", "verify skills", "skill audit", "update check" | Admin | `admin/skill-freshness-audit` |
| "documentation", "organize docs", "file structure", "root cleanup" | Admin | `admin/documentation-organization` |

---

## Progressive Loading Strategy

### Step 1: Initial Detection (~4K tokens)
```
User Request → Tier 1 already loaded (4 core SKILL.md files)
```

### Step 2: Domain Routing (~6K tokens total)
```
Detect domain keywords → Read domain index from references/domain-indexes.md
Example: "metric view" → Semantic Layer index section
```

### Step 3: Load Skill Overview (~7-8K tokens total)
```
Identify task → Read the specific SKILL.md (~1-2K tokens)
If end-to-end → Load orchestrator (00-*) first
If specific task → Load worker directly
```

### Step 4: Deep Dive into References (as needed)
```
Need detailed patterns → Read specific references/ file from the skill
Example: Need dedup SQL → Read references/dedup-patterns.md
```

### Step 5: Execute Scripts or Copy Templates (as needed)
```
Need validation → Run scripts/validate.py
Need starter file → Copy assets/templates/template.yaml
```

### Step 6: Working Memory Between Phases
```
When executing a multi-phase orchestrator, persist a brief summary note after
each phase. Keep only the current phase's worker skill + previous phase's summary
in working memory. Discard intermediate tool outputs. Each worker's
"Notes to Carry Forward" section tells you what to pass to the next phase.
```

---

## Context Budget Monitoring

### Green Zone (0-20K tokens)
- Load multiple SKILL.md files freely
- Load 2-3 reference files

### Yellow Zone (20-50K tokens)
- Continue loading SKILL.md files (they're lightweight)
- Be selective about which references/ to load
- Prefer running scripts/ over reading them

### Red Zone (50K+ tokens)
- Reference skill paths instead of loading
- Execute scripts as black boxes
- Consider splitting task into phases

---

## Complete Skill Directory Map

```
skills/
├── skill-navigator/SKILL.md                                     # This navigator
│
├── admin/
│   ├── create-agent-skill/SKILL.md                              # Agent Skill creation guide [utility]
│   ├── documentation-organization/SKILL.md                      # Documentation structure [utility]
│   ├── self-improvement/SKILL.md                                # Agent learning [utility]
│   └── skill-freshness-audit/SKILL.md                           # Skill currency verification [utility]
│
├── bronze/
│   ├── 00-bronze-layer-setup/SKILL.md                           # ORCHESTRATOR: Bronze setup [stage 2]
│   └── 01-faker-data-generation/SKILL.md                        # Worker: Synthetic data [stage 2]
│
├── common/                                                       # Shared skills (no numbering)
│   ├── databricks-expert-agent/SKILL.md                         # Core SA agent [shared, stages 1-9]
│   ├── databricks-asset-bundles/SKILL.md                        # DAB configuration [shared, stages 1-9]
│   ├── databricks-autonomous-operations/SKILL.md                # Autonomous SRE ops [shared, stages 1-9]
│   ├── naming-tagging-standards/SKILL.md                        # Naming, comments & tags [shared, stages 1-9]
│   ├── databricks-python-imports/SKILL.md                       # Python imports [shared, stages 1-9]
│   ├── databricks-table-properties/SKILL.md                     # Table properties [shared, stages 1-4]
│   ├── schema-management-patterns/SKILL.md                      # Schema management [shared, stages 1-4]
│   └── unity-catalog-constraints/SKILL.md                       # PK/FK constraints [shared, stages 3-4]
│
├── silver/
│   ├── 00-silver-layer-setup/SKILL.md                         # ORCHESTRATOR: Silver DLT [stage 3]
│   ├── 01-dlt-expectations-patterns/SKILL.md                     # Worker: DLT expectations [stage 3]
│   └── 02-dqx-patterns/SKILL.md                                # Worker: DQX framework [stage 3]
│
├── gold/
│   ├── 00-gold-layer-design/SKILL.md                            # ORCHESTRATOR: Gold design [stage 1 — entry point]
│   ├── 01-gold-layer-setup/SKILL.md                      # ORCHESTRATOR: Gold implementation [stage 4]
│   ├── design-workers/
│   │   ├── 01-grain-definition/SKILL.md                          # Worker: Grain definition [stage 1]
│   │   ├── 02-dimension-patterns/SKILL.md                        # Worker: Dimension design patterns [stage 1]
│   │   ├── 03-fact-table-patterns/SKILL.md                       # Worker: Fact table design patterns [stage 1]
│   │   ├── 04-conformed-dimensions/SKILL.md                      # Worker: Enterprise integration [stage 1]
│   │   ├── 05-erd-diagrams/SKILL.md                              # Worker: ERD diagrams [stage 1]
│   │   ├── 06-table-documentation/SKILL.md                       # Worker: Table documentation [stage 1]
│   │   ├── 07-design-validation/SKILL.md                         # Worker: Design validation [stage 1]
│   │   └── 08-industry-alignment/SKILL.md                        # Worker: Industry data model alignment (advisory) [stage 1]
│   └── pipeline-workers/
│       ├── 01-yaml-table-setup/SKILL.md                          # Worker: YAML-driven tables [stage 4]
│       ├── 02-merge-patterns/SKILL.md                            # Worker: MERGE operations [stage 4]
│       ├── 03-deduplication/SKILL.md                             # Worker: Deduplication [stage 4]
│       ├── 04-grain-validation/SKILL.md                            # Worker: Grain validation [stage 4]
│       └── 05-schema-validation/SKILL.md                          # Worker: Schema validation [stage 4]
│
├── planning/
│   └── 00-project-planning/SKILL.md                     # ORCHESTRATOR: Planning [stage 5]
│
├── semantic-layer/
│   ├── 00-semantic-layer-setup/SKILL.md                         # ORCHESTRATOR: Semantic layer [stage 6]
│   ├── 01-metric-views-patterns/SKILL.md                        # Worker: Metric views [stage 6]
│   ├── 02-databricks-table-valued-functions/SKILL.md            # Worker: TVFs for Genie [stage 6]
│   ├── 03-genie-space-patterns/SKILL.md                         # Worker: Genie Space setup [stage 6]
│   └── 04-genie-space-export-import-api/SKILL.md                # Worker: Genie API [stage 6]
│
├── monitoring/
│   ├── 00-observability-setup/SKILL.md                         # ORCHESTRATOR: Observability [stage 7]
│   ├── 01-lakehouse-monitoring-comprehensive/SKILL.md            # Worker: Monitoring [stage 7]
│   ├── 02-databricks-aibi-dashboards/SKILL.md                   # Worker: Dashboards [stage 7]
│   ├── 03-sql-alerting-patterns/SKILL.md                        # Worker: Alerts [stage 7]
│   └── 04-anomaly-detection/SKILL.md                            # Worker: Freshness/completeness [stage 7] (auto-triggered by Silver/Gold setup)
│
├── ml/
│   └── 00-ml-pipeline-setup/SKILL.md                     # ORCHESTRATOR: ML patterns [stage 8]
│
├── genai-agents/
│   ├── 00-course-orchestrator/SKILL.md                   # ORCHESTRATOR: GenAI course router [stage 9]
│   ├── foundation/                                       # Foundation: UC, MLflow, tracing, tools, AI Gateway
│   ├── tracks/                                           # Track A/B/C agent implementations
│   ├── sdlc/                                             # Prompt registry, evaluation, deploy, monitor
│   ├── capstone/                                         # Optional Genie orchestrator capstone
│   └── 09-simple-agent-scaffold/SKILL.md                 # Worker: Minimal MCP tool-calling agent [stage 9]
│
├── exploration/
│   └── 00-adhoc-exploration-notebooks/SKILL.md                  # Utility: Exploration [standalone]
```

---

## Post-Completion: Skill Usage Summary (MANDATORY)

**After completing a routing or orchestration session, output a Skill Usage Summary reflecting what you ACTUALLY did — not a pre-written summary.**

### What to Include

1. Every skill `SKILL.md` or `references/` file you read (via the Read tool), in the order you read them
2. Which routing step or phase you were in when you read it
3. Whether it was an **Orchestrator**, **Worker**, **Common**, **Cross-domain**, or **Reference** file
4. A one-line description of what you specifically used it for in this session

### Format

| # | Step / Phase | Skill / Reference Read | Type | What It Was Used For |
|---|-------------|----------------------|------|---------------------|
| 1 | Routing | `path/to/SKILL.md` | Orchestrator / Worker / Common / Reference | One-line description |

### Summary Footer

End with:
- **Totals:** X orchestrator skills, Y worker skills, Z common skills, W reference files read
- **Routing path:** Which orchestrator(s) were invoked and in what order
- **Skipped:** List any skills from the routing table that were considered but not needed, and why
- **Unplanned:** List any skills read that were outside the normal routing path (e.g., troubleshooting, edge cases)

---

## Maintenance

When adding new skills:
1. Calculate token size (`wc -l SKILL.md` — roughly lines/2.5 = tokens in K)
2. Ensure SKILL.md is under 500 lines; use references/ for detailed content
3. Assign to appropriate domain with correct numbered prefix
4. Add `role`, `pipeline_stage`, and relationship metadata to frontmatter
5. Update [references/domain-indexes.md](references/domain-indexes.md) with the new skill
6. Update the Task Detection & Routing Table above
7. Update the Complete Skill Directory Map above
