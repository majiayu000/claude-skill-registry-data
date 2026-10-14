---
name: gold-layer-setup
description: End-to-end orchestrator for implementing Gold layer tables, merge scripts, FK constraints, and Asset Bundle jobs from YAML schema definitions. Guides users through Silver contract validation, YAML-driven table creation, Silver-to-Gold MERGE operations (SCD Type 1/2 dimensions, aggregated/transaction facts, accumulating snapshots, factless facts, periodic snapshots, junk dimensions), foreign key constraint application, Asset Bundle job configuration, and post-deployment validation. Orchestrates pipeline-workers (01-yaml-table-setup, 02-merge-patterns, 03-deduplication, 04-grain-validation, 05-schema-validation) and common skills (databricks-asset-bundles, databricks-table-properties, databricks-python-imports, schema-management-patterns, unity-catalog-constraints, databricks-expert-agent). Use when implementing Gold layer from YAML designs, creating table setup scripts, writing merge scripts, deploying Gold layer jobs, or troubleshooting Gold layer implementation errors.
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: jobs
deploy_verb: bundle_deploy
deploy_note: "Gold tables + Silver-to-Gold MERGE jobs + FK constraints deploy via `bundle deploy --target dev` (runDatabricksCli on Genie Code). Strip DEFAULT clauses from DDL (SCD2 cols set in INSERT/MERGE); printSchema() before MERGE. On Genie Code, write generated table/merge scripts under the cloned repo root (`{REPO_ROOT}` = `state_file_root` from `skills/vibecoding-state`, e.g. `src/`), not a bare relative path \u2014 relative paths resolve against the page CWD (see `skills/genie-code-environment` \u00a78)."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "2.0.0"
  domain: gold
  role: orchestrator
  pipeline_stage: 4
  pipeline_stage_name: gold-implementation
  next_stages:
    - project-planning
  workers:
    - pipeline-workers/01-yaml-table-setup
    - pipeline-workers/02-merge-patterns
    - pipeline-workers/03-deduplication
    - pipeline-workers/04-grain-validation
    - pipeline-workers/05-schema-validation
  common_dependencies:
    - databricks-asset-bundles
    - databricks-table-properties
    - databricks-python-imports
    - schema-management-patterns
    - unity-catalog-constraints
    - databricks-expert-agent
    - naming-tagging-standards
    - databricks-autonomous-operations
  dependencies:
    - pipeline-workers/01-yaml-table-setup
    - pipeline-workers/02-merge-patterns
    - pipeline-workers/03-deduplication
    - pipeline-workers/04-grain-validation
    - pipeline-workers/05-schema-validation
    - databricks-asset-bundles
    - databricks-table-properties
    - databricks-python-imports
    - schema-management-patterns
    - unity-catalog-constraints
    - databricks-expert-agent
  last_verified: "2026-02-07"
  volatility: low
  upstream_sources: []  # Internal setup patterns
---

# Gold Layer Implementation Orchestrator

This skill orchestrates the complete Gold layer implementation process, transforming YAML schema designs into production-ready Delta tables with merge scripts, FK constraints, and Asset Bundle jobs. It is the natural successor to the `gold/00-gold-layer-design` skill.

**Predecessor:** `gold/00-gold-layer-design` skill (YAML files must exist before using this skill)

**Core Philosophy:** YAML as Single Source of Truth — Python reads YAML at runtime, DDL is generated dynamically, schema changes require YAML edits only.

## When to Use This Skill

- Implementing Gold layer tables from completed YAML designs
- Creating generic YAML-driven table setup scripts
- Writing Silver-to-Gold MERGE scripts (dimensions and facts)
- Applying FK constraints after table creation
- Configuring Asset Bundle jobs for Gold layer deployment
- Troubleshooting Gold layer implementation errors (duplicate keys, schema mismatches, grain violations)

## Prerequisites

**MANDATORY:** Complete `gold/00-gold-layer-design` skill first. The following must exist:
- [ ] YAML schema files in `gold_layer_design/yaml/{domain}/*.yaml`
- [ ] ERD documentation (`erd_master.md`)
- [ ] Column lineage documentation (`COLUMN_LINEAGE.csv`)

## Critical Dependencies (Read at Indicated Phase)

### Gold-Domain Skills

| Skill | Read At | Purpose |
|-------|---------|---------|
| `pipeline-workers/01-yaml-table-setup` | Phase 1 | YAML-to-DDL patterns, setup script structure |
| `pipeline-workers/02-merge-patterns` | Phase 2 | SCD Type 1/2, fact aggregation, column mapping |
| `pipeline-workers/03-deduplication` | Phase 2 | Deduplication before MERGE (mandatory) |
| `pipeline-workers/04-grain-validation` | Phase 2 | Grain inference from PK, pre-merge validation |
| `pipeline-workers/05-schema-validation` | Phase 2 | DataFrame-to-DDL schema validation |

### Common Skills

| Skill | Read At | Purpose |
|-------|---------|---------|
| `databricks-asset-bundles` | Phase 3 | Job YAML patterns, serverless config, sync |
| `databricks-table-properties` | Phase 1 | Standard TBLPROPERTIES by layer |
| `unity-catalog-constraints` | Phase 1 | PK/FK constraint application patterns |
| `schema-management-patterns` | Phase 1 | CREATE SCHEMA IF NOT EXISTS |
| `databricks-python-imports` | Phase 2 | Pure Python modules, avoid sys.path issues |
| `databricks-expert-agent` | All | Schema extraction over generation principle |
| `databricks-autonomous-operations` | Phase 4+ (if user-triggered) | Deploy → Poll → Diagnose → Fix → Redeploy loop when jobs fail |

### 🔴 Non-Negotiable Defaults (Applied to EVERY Gold Table and Job)

These defaults are ALWAYS applied. There are NO exceptions, NO overrides, NO alternative options.

| Default | Value | Applied Where | NEVER Do This Instead |
|---------|-------|---------------|----------------------|
| **Serverless** | `environments:` block with `environment_key` | Every job YAML | ❌ NEVER define `job_clusters:` or `existing_cluster_id:` |
| **Environments V4** | `environment_version: "4"` | Every job's `environments.spec` | ❌ NEVER omit or use older versions |
| **Auto Liquid Clustering** | `CLUSTER BY AUTO` | Every `CREATE TABLE` in `setup_tables.py` | ❌ NEVER use `CLUSTER BY (col1, col2)` or `PARTITIONED BY` |
| **Change Data Feed** | `'delta.enableChangeDataFeed' = 'true'` | Every table's TBLPROPERTIES | ❌ NEVER omit (required for incremental propagation) |
| **Row Tracking** | `'delta.enableRowTracking' = 'true'` | Every table's TBLPROPERTIES | ❌ NEVER omit (breaks downstream MV refresh) |
| **notebook_task** | `notebook_task:` with `base_parameters:` | Every task in job YAML | ❌ NEVER use `python_task:` or CLI-style `parameters:` |
| **FK graceful failure** | Warn + continue | Every FK in `add_fk_constraints.py` | ❌ NEVER raise/crash if FK constraint fails (serverless cannot apply FKs to non-PK columns) |

See [Setup Script Patterns](references/setup-script-patterns.md) for DDL template and [Asset Bundle Job Patterns](references/asset-bundle-job-patterns.md) for job YAML template.

### 🔴 YAML Extraction Over Generation (Merge Scripts Included)

**EVERY value below MUST be extracted from Gold YAML files or COLUMN_LINEAGE.csv. NEVER generate, guess, or hardcode.** Table names, column names/types, PKs, FKs, business keys, grain types, SCD types, source Silver tables, and column mappings — ALL come from YAML. The ONLY things coded by hand are aggregation expressions and derived column formulas (business logic).

See [Merge Script Patterns](references/merge-script-patterns.md) for the complete extraction helpers: `load_table_metadata()`, `build_inventory()`, `load_column_mappings_from_yaml()`, `build_merge_condition()`, and correct vs. incorrect usage examples.

## Quick Start (3-4 hours)

### What You'll Create

1. `setup_tables.py` — Generic script reads YAML, creates all tables dynamically
2. `add_fk_constraints.py` — Apply FK constraints AFTER all PKs exist
3. `merge_gold_tables.py` — Merge Silver to Gold with explicit column mapping
4. `gold_setup_job.yml` — Asset Bundle job for table setup + FK constraints
5. `gold_merge_job.yml` — Asset Bundle job for periodic MERGE operations

### Deliverables Checklist

**Setup Scripts:**
- [ ] `src/{project}_gold/setup_tables.py` — Generic YAML-driven table creation
- [ ] `src/{project}_gold/add_fk_constraints.py` — FK constraint application
- [ ] (User-triggered) Verify: `databricks bundle run gold_setup_job -t dev`

**Merge Scripts:**
- [ ] `src/{project}_gold/merge_gold_tables.py` — Silver-to-Gold MERGE
- [ ] Dimension merges (SCD Type 1 or 2) with deduplication
- [ ] Fact merges with aggregation and grain validation
- [ ] (User-triggered) Verify: `databricks bundle run gold_merge_job -t dev`

**Asset Bundle Jobs:**
- [ ] `resources/gold/gold_setup_job.yml` — Setup + FK constraints (two tasks)
- [ ] `resources/gold/gold_merge_job.yml` — Periodic merge with schedule
- [ ] YAML files synced in `databricks.yml`

### Deployment Commands (run when ready — NOT auto-executed by this skill)

> **Client note:** IDE runs these in a terminal; Genie Code runs the `databricks bundle …` commands via `runDatabricksCli` (be on the bundle's page; generated files anchor to `{REPO_ROOT}`). See `skills/genie-code-environment`.

```bash
# 1. Deploy setup job (creates tables from YAML)
databricks bundle deploy -t dev
databricks bundle run gold_setup_job -t dev

# 2. Verify tables created
# SHOW TABLES IN {catalog}.{gold_schema}

# 3. Run merge job (Silver to Gold)
databricks bundle run gold_merge_job -t dev
```

---

## Working Memory Management

This orchestrator spans 5+ phases. To maintain coherence without context pollution, follow this note-taking discipline:

**After each phase, persist a brief summary note** (e.g., in a scratch file or conversation notes) capturing:
- **Phase 0 output:** Silver contract pass/fail per table, any YAML fixes made, resolution report location
- **Phase 1 output:** Table inventory dict, YAML base path, count of tables created, any FK failures
- **Phase 2 output:** Merge function inventory (which tables use SCD1 vs SCD2, aggregated vs transaction), any column mapping issues
- **Phase 3 output:** Job YAML file paths, databricks.yml sync status
- **Phase 4 output (if user-triggered):** Deployment results, validation failures to investigate

**What to keep in working memory:** Only the current phase's worker skill, the table inventory dict, and the previous phase's summary note. Discard intermediate tool outputs (DDL strings, full DataFrames, raw validation SQL results) — they are reproducible from YAML.

**What to offload to references:** Each pipeline-worker skill has `Pipeline Notes to Carry Forward` and `Next Step` sections. Read them to know what to pass to the next phase. The worker skills form a chain: `01 → 02 → 03 → 04 → 05`.

---

## Step-by-Step Workflow

### Phase 0: Upstream Contract Validation (15 min)

**MANDATORY: Execute before proceeding to any implementation phase.**

**Reference:** `data_product_accelerator/skills/gold/01-gold-layer-setup/references/design-to-pipeline-bridge.md` — Full validation logic documentation

**Purpose:** Validate that all source column names and types referenced in YAML lineage actually exist in the deployed upstream tables. This catches column name mismatches BEFORE any code is written, eliminating the most common source of iteration.

**Steps:**
1. Execute `scripts/validate_upstream_contracts.py` with the project's `catalog` and `source_schema` widget parameters (or run `run_phase0_validation()` inline from the script)
2. Capture and paste the full printed output — it produces a PASS/FAIL report per Gold table
3. If ANY table shows FAILED, fix YAML lineage `silver_column` values in `gold_layer_design/yaml/` to match actual source columns, then re-run the script

**Gate:** ALL contracts must show PASSED in the script output before proceeding to Phase 1.

**Minimum-viable validation (if scripts unavailable or context-constrained):**
For each Gold table you plan to implement, run `DESCRIBE TABLE {catalog}.{silver_schema}.{silver_table}` and confirm every non-GENERATED `silver_column` in its YAML lineage exists. Output one line per table:
```
dim_destination: 7 lineage columns validated against silver_destinations — PASS
dim_user: 9 lineage columns validated against silver_users — PASS
```
If ANY column is missing, fix the YAML lineage before proceeding.

**Backup guardrail:** The merge template (`scripts/merge_gold_tables_template.py`) also embeds `validate_upstream_contracts()` as a fail-fast check in `main()`. Even if Phase 0 is skipped, the merge job will abort with a clear error before any MERGE executes.

**Output:** Column resolution reports for all Gold tables, confirming source→Gold mappings are correct.

---

### Phase 1: YAML-Driven Table Creation (30 min)

**MANDATORY: Read each skill below using the Read tool BEFORE writing any code for this phase.**

If context-constrained, read AT MINIMUM these two (they prevent the most common errors):
- `data_product_accelerator/skills/common/unity-catalog-constraints/SKILL.md` — prevents FK-to-non-PK errors (the #1 Gold layer failure mode)
- `data_product_accelerator/skills/gold/pipeline-workers/01-yaml-table-setup/SKILL.md` — prevents DDL and YAML discovery errors

Full list:

1. `data_product_accelerator/skills/gold/pipeline-workers/01-yaml-table-setup/SKILL.md` — YAML-to-DDL patterns, `find_yaml_base()`, `build_create_table_ddl()`
2. `data_product_accelerator/skills/common/databricks-table-properties/SKILL.md` — Standard TBLPROPERTIES by layer
4. `data_product_accelerator/skills/common/unity-catalog-constraints/SKILL.md` — PK/FK `ALTER TABLE` patterns, NOT NULL requirements
5. `data_product_accelerator/skills/common/schema-management-patterns/SKILL.md` — `CREATE SCHEMA IF NOT EXISTS` pattern

**Activities:**
1. Create `setup_tables.py` — Single generic script reads ALL YAML files, creates tables
2. Create `add_fk_constraints.py` — Applies FK constraints AFTER all PKs exist
3. Define standard table properties (CDF, row tracking, auto-optimize, layer=gold)
4. Handle schema creation with `CREATE SCHEMA IF NOT EXISTS`
5. Enable Predictive Optimization on Gold schema

**Key Implementation Rules:**
- FK constraints via `ALTER TABLE` AFTER all PKs exist (never inline in CREATE TABLE)
- PK columns must be NOT NULL in YAML
- Use `CREATE OR REPLACE TABLE` for idempotent setup
- Include error handling with try/except for constraint application
- YAML directory discovery pattern (`find_yaml_base()`)
- PyYAML dependency in job environment

**Output:** `src/{project}_gold/setup_tables.py` and `src/{project}_gold/add_fk_constraints.py`

See `references/setup-script-patterns.md` for complete implementation patterns.
See `references/fk-constraint-patterns.md` for FK constraint details.
See `scripts/setup_tables_template.py` for starter template.
See `scripts/add_fk_constraints_template.py` for starter template.

---

### Phase 1b: Advanced Setup Patterns (Optional)

**Read if applicable:** `references/setup-advanced-patterns.md`

These patterns extend Phase 1 based on design decisions from `design-workers/02-dimension-patterns`:

**Role-Playing Dimension Views:** If any dimension has `dimension_pattern: role_playing` in YAML, create alias views after table creation. Example: `dim_date` → `dim_order_date`, `dim_ship_date`, `dim_delivery_date`.

**Unknown Member Row Insertion:** Insert a `-1` key "Unknown" member row in every dimension table AFTER PKs are applied but BEFORE FK constraints. This prevents NULL foreign keys for late-arriving facts.

**Execution Order:**
1. Create tables (Phase 1)
2. Apply PK constraints (Phase 1)
3. Create role-playing views (Phase 1b)
4. Insert unknown member rows (Phase 1b)
5. Apply FK constraints (Phase 1)
6. Run merge scripts (Phase 2)

---

### Phase 2: MERGE Script Implementation (2 hours)

**MANDATORY: Read each skill below using the Read tool BEFORE writing any merge code.**

If context-constrained, read AT MINIMUM these two:
- `data_product_accelerator/skills/gold/pipeline-workers/03-deduplication/SKILL.md` — prevents MERGE duplicate-row errors (the #1 merge failure mode)
- `data_product_accelerator/skills/gold/pipeline-workers/05-schema-validation/SKILL.md` — prevents schema mismatch at runtime

Full list:

1. `data_product_accelerator/skills/gold/pipeline-workers/02-merge-patterns/SKILL.md` — SCD Type 1/2, fact aggregation, column mapping, `spark_sum` alias
2. `data_product_accelerator/skills/gold/pipeline-workers/03-deduplication/SKILL.md` — Deduplication before MERGE (ALWAYS required, prevents `DELTA_MULTIPLE_SOURCE_ROW_MATCHING_TARGET_ROW_IN_MERGE`)
3. `data_product_accelerator/skills/gold/pipeline-workers/04-grain-validation/SKILL.md` — Grain inference from PK, transaction vs aggregated patterns
4. `data_product_accelerator/skills/gold/pipeline-workers/05-schema-validation/SKILL.md` — `validate_merge_schema()`, DataFrame-to-DDL checks
5. `data_product_accelerator/skills/common/databricks-python-imports/SKILL.md` — Pure Python modules, avoid `sys.path` issues in serverless
6. `data_product_accelerator/skills/gold/01-gold-layer-setup/references/advanced-merge-patterns.md` — Accumulating snapshot, factless fact, periodic snapshot, junk dimension patterns
7. `data_product_accelerator/skills/gold/01-gold-layer-setup/references/design-to-pipeline-bridge.md` — Silver contract validation, lineage-driven column builder, scripted column resolution

**Activities:**

**Step 0 — EXTRACTION FIRST (before writing ANY code):**
1. Load ALL Gold YAML files using `load_table_metadata()` (see YAML Extraction section above)
2. Load `COLUMN_LINEAGE.csv` using `load_column_mappings()` for Silver→Gold renames
3. For each table: extract `table_name`, `pk_columns`, `business_key`, `scd_type`, `grain`, `columns`, `lineage`
4. Build a table inventory dict keyed by table name — this drives ALL merge functions
5. Verify source tables exist: `spark.table(source_table)` before coding any merge logic
6. Use `build_column_expressions()` from `references/design-to-pipeline-bridge.md` for DIRECT_COPY/RENAME/CAST/GENERATED columns instead of writing `.withColumn()` calls manually — this automates ~70% of column mappings deterministically from YAML lineage

**Step 1 — Create merge functions using extracted metadata:**
1. Create `merge_gold_tables.py` with separate functions per table (start from `scripts/merge_gold_tables_template.py` which includes embedded `validate_upstream_contracts()` and `validate_merge_schema()` guardrails)
2. Implement dimension merges (SCD Type 1 or Type 2 — read `scd_type` from YAML)
3. Implement fact merges (aggregation to match grain — read `grain` from YAML)
4. Add deduplication before every MERGE (MANDATORY — use `business_key` from YAML)
5. Add explicit column mapping (use `lineage.silver_column` from YAML or `COLUMN_LINEAGE.csv`)
6. Add schema validation before merge (`validate_merge_schema()` is already in the template — keep it)
7. Add grain validation for fact tables (use `pk_columns` from YAML)
8. Merge dimensions FIRST, then facts (dependency order from YAML `foreign_keys`)

**For Each Dimension Table:**

1. **Extract metadata** — `meta = load_table_metadata(yaml_path)` → get `business_key`, `scd_type`, `columns`
2. **Deduplicate** — `.orderBy(col("processed_timestamp").desc()).dropDuplicates(meta["business_key"])` (from YAML)
3. **Map columns** — Loop over `load_column_mappings()` results: `.withColumn(gold_col, col(silver_col))`
4. **Generate surrogate key** — `md5(concat_ws("||", ...))` using columns from YAML `primary_key`
5. **Add SCD columns** — `effective_from`, `effective_to`, `is_current` (only if `scd_type == "scd2"`)
6. **Select explicitly** — `.select(meta["columns"])` — column list FROM YAML, not typed by hand
7. **Validate schema** — Compare DataFrame columns against `meta["columns"]`
8. **Build MERGE condition** — `" AND ".join(f"target.{c} = source.{c}" for c in meta["business_key"])` (from YAML)

**Design Pattern Awareness (Dimensions):** Check YAML `dimension_pattern` for advanced patterns:
- `role_playing` → Views already created in Phase 1b, no special merge logic needed
- `junk` → Use `assets/templates/junk-dimension-populate.py` instead of standard SCD merge
- Standard dimensions → Use SCD Type 1 or 2 merge based on `scd_type`

**For Each Fact Table:**

1. **Extract metadata** — `meta = load_table_metadata(yaml_path)` → get `pk_columns`, `grain`, `columns`
2. **Infer grain** — Read `grain` from YAML (or infer: composite PK = aggregated, single PK = transaction)
3. **Aggregate** — `.groupBy(meta["pk_columns"]).agg(...)` — grain columns FROM YAML
4. **Validate grain** — Verify one row per `meta["pk_columns"]` combination
5. **Map columns** — Loop over `load_column_mappings()` results
6. **Select explicitly** — `.select(meta["columns"])` — column list FROM YAML
7. **Validate schema** — Compare DataFrame columns against `meta["columns"]`
8. **Build MERGE condition** — `" AND ".join(f"target.{c} = source.{c}" for c in meta["pk_columns"])` (from YAML)

**Design Pattern Awareness (Facts):** Check YAML `grain_type` for advanced patterns:
- `accumulating_snapshot` → Use `assets/templates/accumulating-snapshot-merge.py` (milestone progression)
- `factless` → Use `assets/templates/factless-fact-merge.py` (INSERT only, no aggregation)
- `periodic_snapshot` → Use `assets/templates/periodic-snapshot-merge.py` (full period replacement)
- Standard transaction/aggregated → Use standard fact aggregation merge

See `references/advanced-merge-patterns.md` for pattern selection table and details.

**Critical Rules (from dependency skills):**
- ALWAYS deduplicate Silver before MERGE (prevents `DELTA_MULTIPLE_SOURCE_ROW_MATCHING_TARGET_ROW_IN_MERGE`)
- Deduplication key MUST match MERGE condition key
- Use `spark_sum` not `sum` (avoid shadowing Python builtins)
- Never name variables `count`, `sum`, `min`, `max` (shadows PySpark functions)
- Cast `DATE_TRUNC` results to DATE type
- Inline helper functions or use pure Python modules (not notebook imports)

**Output:** `src/{project}_gold/merge_gold_tables.py`

See `references/merge-script-patterns.md` for complete SCD1/SCD2/fact patterns.
See `scripts/merge_gold_tables_template.py` for starter template.

---

### Phase 3: Asset Bundle Configuration (30 min)

**MANDATORY: Read this skill using the Read tool BEFORE creating job YAML files:**

1. `skills/databricks-asset-bundles/SKILL.md` — Job YAML patterns, serverless config, `notebook_task` vs `python_task`, `base_parameters`, sync

**Activities:**
1. Add YAML sync to `databricks.yml` — `gold_layer_design/yaml/**/*.yaml`
2. Create `gold_setup_job.yml` with two tasks (setup tables then add FK constraints)
3. Create `gold_merge_job.yml` with scheduled merge execution
4. Add PyYAML dependency to job environment
5. Configure serverless environment
6. Add tags (environment, layer, job_type)

**Critical Rules (from `databricks-asset-bundles`):**
- Use `notebook_task` not `python_task`
- Use `base_parameters` dict (not CLI-style `parameters`)
- PyYAML dependency: `pyyaml>=6.0` in environment spec
- YAML sync is CRITICAL — without it, `setup_tables.py` cannot find schemas
- FK task depends on setup task (`depends_on`)
- Merge job has optional schedule (PAUSED in dev, enabled in prod)

**Output:** Updated `databricks.yml`, `resources/gold/gold_setup_job.yml`, `resources/gold/gold_merge_job.yml`

See `references/asset-bundle-job-patterns.md` for complete job templates.
See `assets/templates/gold-setup-job-template.yml` and `assets/templates/gold-merge-job-template.yml`.

---

### 🛑 STOP — Artifact Creation Complete

**Phases 0–3 are complete.** All scripts (`setup_tables.py`, `add_fk_constraints.py`, `merge_gold_tables.py`) and job YAMLs have been created. **Do NOT proceed to Phase 4 unless the user explicitly requests deployment.**

Report what was created and ask the user if they want to deploy, run, and validate.

---

### Phase 4: Deployment and Testing (30 min) — USER-TRIGGERED ONLY

> **This phase is executed ONLY when the user explicitly requests deployment.** Do not auto-execute.

**Activities:**
1. Deploy: `databricks bundle deploy -t dev`
2. Run setup job: `databricks bundle run gold_setup_job -t dev`
3. Verify tables created: `SHOW TABLES IN {catalog}.{gold_schema}`
4. Verify PKs: `SHOW CREATE TABLE {catalog}.{gold_schema}.{table}`
5. Verify FKs: `DESCRIBE TABLE EXTENDED {catalog}.{gold_schema}.{table}`
6. Run merge job: `databricks bundle run gold_merge_job -t dev`
7. Verify record counts, grain, FK relationships, SCD Type 2

See `references/validation-queries.md` for complete validation SQL.

---

### Phase 4b: Enable Anomaly Detection on Gold Schema (5 min) — USER-TRIGGERED ONLY

> **This phase is executed ONLY when the user explicitly requests it.** Do not auto-execute.

**MANDATORY: Read this skill using the Read tool:**

1. `data_product_accelerator/skills/monitoring/04-anomaly-detection/SKILL.md` — Schema-level freshness/completeness monitoring

**Why:** Gold tables are the primary consumer-facing layer — stale or incomplete data directly impacts dashboards and Genie Spaces.

**Steps:** Enable schema-level anomaly detection on the Gold schema after all tables are created. No exclusions needed — all Gold tables should be monitored. Read the monitoring skill for the SDK code pattern. This is non-blocking — if it fails, the deployment continues.

---

### Phase 5: Post-Implementation Validation (30 min) — USER-TRIGGERED ONLY

> **This phase is executed ONLY when the user explicitly requests validation.** Do not auto-execute.

**MANDATORY: Read this skill using the Read tool to cross-reference created tables against ERD:**

1. `data_product_accelerator/skills/gold/design-workers/05-erd-diagrams/SKILL.md` — Verify all ERD entities have corresponding tables, all relationships match FK constraints

**Activities:**
1. ERD cross-reference — Compare created tables against `erd_master.md` to confirm nothing was missed
2. Schema validation — DataFrame columns match DDL for all merge functions
3. Grain validation — No duplicate rows at PRIMARY KEY level
4. FK integrity — No orphaned foreign key references
5. SCD Type 2 — Exactly one `is_current = true` per business key
6. Data quality — Record counts, NULL checks, range validations
7. Audit timestamps — `record_created_timestamp` and `record_updated_timestamp` populated
8. Conformance validation — Conformed dimensions have identical schemas across domains (if applicable)
9. Advanced pattern validation — Accumulating snapshot milestones progress, factless facts have no measures, periodic snapshots have one row per entity-period

See `references/validation-queries.md` for complete SQL queries.

---

## File Organization

```
project_root/
├── databricks.yml                              # Bundle config (sync YAMLs!)
├── gold_layer_design/
│   └── yaml/                                   # Source of Truth (from design phase)
│       └── {domain}/
│           └── {table}.yaml
├── src/
│   └── {project}_gold/
│       ├── setup_tables.py                     # Phase 1: Generic YAML-driven setup
│       ├── add_fk_constraints.py               # Phase 1: FK constraint application
│       └── merge_gold_tables.py                # Phase 2: Silver-to-Gold MERGE
└── resources/
    └── gold/
        ├── gold_setup_job.yml                  # Phase 3: Setup + FK job
        └── gold_merge_job.yml                  # Phase 3: Merge job
```

## Key Principles & Troubleshooting

**Core rule:** YAML is the single source of truth — extract everything, generate nothing. Deduplicate always. Validate schema and grain before every merge.

See [Implementation Checklist](references/implementation-checklist.md) for the 8 key principles and phase-by-phase validation checklists.

See [Common Issues](references/common-issues.md) for error diagnosis (YAML not found, duplicate key MERGE, `UNRESOLVED_COLUMN`, grain duplicates, Silver column mismatch, FK failures).

## Validation Checklist

See [Implementation Checklist](references/implementation-checklist.md) for complete phase-by-phase checklists covering Setup, YAML Extraction, Merge, Deployment, Silver Contract Validation, and Advanced Patterns.

## Time Estimates

| Phase | Duration | Activities |
|-------|----------|------------|
| Phase 0: Silver contract | 15 min | Silver introspection, contract validation, resolution reports |
| Phase 1: Setup scripts | 30 min | setup_tables.py + add_fk_constraints.py |
| Phase 1b: Advanced setup | 15 min | Role-playing views, unknown member rows (if applicable) |
| Phase 2: Merge scripts | 2 hours | Dimension + fact merges with validation |
| Phase 3: Asset Bundle | 30 min | Job YAML files + databricks.yml sync |
| Phase 4: Deployment (user-triggered) | 30 min | Deploy, run, verify |
| Phase 5: Validation (user-triggered) | 30 min | Schema, grain, FK, SCD2 checks |
| **Total** | **2.5-3.5 hours** (artifact creation) + **1 hour** (if user-triggered deployment/validation) | For 3-5 tables |

## Next Steps After Implementation

After Gold layer implementation is complete and validated:
1. **Metric Views** — Create semantic metric views from Gold tables
2. **TVFs** — Create Table-Valued Functions for Genie integration
3. **Custom Business Metrics** — Set up Lakehouse Monitoring with AGGREGATE/DERIVED/DRIFT metrics (anomaly detection for baseline freshness/completeness is already enabled in Phase 4b)
4. **Genie Space** — Configure Genie Space with Gold tables, metric views, and TVFs

## Pipeline Progression

**Previous stage:** `silver/00-silver-layer-setup` → Silver tables must exist for Gold merge scripts to read from. Gold YAML designs (from stage 1: `gold/00-gold-layer-design`) must also exist.

**Next stage:** After completing Gold layer implementation, proceed to:
- **`planning/00-project-planning`** — Plan the semantic layer, observability, ML, and GenAI agent phases

## Reference Files

- **[Setup Script Patterns](references/setup-script-patterns.md)** — YAML-driven table creation, `find_yaml_base()`, `build_create_table_ddl()`, PK application
- **[FK Constraint Patterns](references/fk-constraint-patterns.md)** — FK constraint application after PKs, error handling, YAML FK format
- **[Merge Script Patterns](references/merge-script-patterns.md)** — SCD Type 1/2 dimension merges, fact aggregation merges, column mapping, deduplication
- **[Asset Bundle Job Patterns](references/asset-bundle-job-patterns.md)** — gold_setup_job.yml, gold_merge_job.yml, databricks.yml sync
- **[Validation Queries](references/validation-queries.md)** — Schema, grain, FK integrity, SCD Type 2 validation SQL
- **[Common Issues](references/common-issues.md)** — YAML not found, PyYAML missing, duplicate key MERGE, column mismatch, grain duplicates
- **[Advanced Merge Patterns](references/advanced-merge-patterns.md)** — Accumulating snapshot, factless fact, periodic snapshot, junk dimension merge patterns
- **[Advanced Setup Patterns](references/setup-advanced-patterns.md)** — Role-playing dimension views, unknown member row insertion
- **[Design-to-Pipeline Bridge](references/design-to-pipeline-bridge.md)** — Silver contract validation, lineage-driven column builder, type compatibility, resolution reports
- **[Implementation Checklist](references/implementation-checklist.md)** — Key principles, phase-by-phase validation checklists, advanced pattern checks

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

## External References

- [Delta Lake MERGE](https://docs.delta.io/latest/delta-update.html#upsert-into-a-table-using-merge)
- [Unity Catalog Constraints](https://docs.databricks.com/data-governance/unity-catalog/constraints.html)
- [Databricks Asset Bundles](https://docs.databricks.com/dev-tools/bundles/)
- [AgentSkills.io Specification](https://agentskills.io/specification)
