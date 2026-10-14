---
name: silver-layer-setup
description: End-to-end orchestrator for creating Silver layer pipelines using Spark Declarative Pipelines (SDP, formerly DLT) with Delta table-based data quality rules, quarantine patterns, and monitoring views. Orchestrates mandatory dependencies on common skills (databricks-table-properties, databricks-python-imports, databricks-asset-bundles, schema-management-patterns, unity-catalog-constraints, databricks-expert-agent) and Silver-domain skills (dlt-expectations-patterns, dqx-patterns). Use when creating a Silver layer from scratch, setting up Bronze-to-Silver pipelines, or implementing Silver SDP/DLT with streaming ingestion and runtime-updateable DQ rules.
clients: [ide_cli, genie_code]
bundle_resource: pipelines
deploy_verb: bundle_deploy
deploy_note: "Silver SDP/DLT pipeline + DQ-rules setup job deploy via `bundle deploy --target dev` (runDatabricksCli on Genie Code) — the bundle is the execution mechanism; NEVER create Silver schemas/tables or load data directly via executeCode/spark.sql, they are the pipeline/job body. The DQ-rules job runs before the pipeline; DLT updates use full_refresh=True; no DEFAULT clauses in serverless table DDL. Write the generated bundle (databricks.yml, src/, resources/) under `dp_bundle_root` (= `<artifact_root>/<use_case_slug>_dab` from `skills/vibecoding-state`) — a self-contained DAB project dir shared across the DP pipeline, NOT the bare clone root. On Genie Code `dp_bundle_root` is also the `bundle deploy` page-context root: be on that folder's page to deploy (see `skills/genie-code-environment` \u00a78)."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "2.0"
  domain: silver
  role: orchestrator
  pipeline_stage: 3
  pipeline_stage_name: silver
  next_stages:
    - gold-layer-setup
  workers:
    - dlt-expectations-patterns
    - dqx-patterns
  common_dependencies:
    - databricks-asset-bundles
    - databricks-expert-agent
    - databricks-python-imports
    - databricks-table-properties
    - schema-management-patterns
    - unity-catalog-constraints
    - naming-tagging-standards
    - databricks-autonomous-operations
  source: context/prompts/02-silver-layer-prompt.md
  last_verified: "2026-08-30"
  volatility: medium
  upstream_sources:
    - name: "databricks-agent-skills"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-pipelines/SKILL.md"
      relationship: "extended"
      last_synced: "2026-08-30"
      sync_commit: "ca92a6c"
---

# Silver Layer Setup - Orchestrator Skill

End-to-end workflow for creating production-grade Silver layer pipelines using Spark Declarative Pipelines (SDP, formerly Delta Live Tables/DLT) with Delta table-based data quality rules, quarantine patterns, streaming ingestion, and monitoring views.

> **Naming:** Databricks rebranded DLT to **Spark Declarative Pipelines (SDP)** / **Lakeflow Declarative Pipelines (LDP)**. The modern Python API is `from pyspark import pipelines as dp`, and Databricks now **recommends `dp`** over `import dlt`. Expectations **are available** in `dp` (e.g. `dp.expect_all_or_drop(...)`, `dp.expect_all(...)`) — the [Lakeflow pipelines Python reference](https://docs.databricks.com/aws/en/ldp/developer/python-ref) maps each `@dlt.expect*` decorator to a `dp` equivalent. This skill still standardizes on `import dlt` for the existing DQ-rules framework (`dlt-expectations-patterns`) because that framework's decorators are written against `dlt`; the two APIs are behaviorally equivalent, so a `dp` migration is straightforward (swap the import and decorator prefix). New projects may use `databricks pipelines init` to scaffold an SDP Asset Bundle project.

**Time Estimate:** 3-4 hours for initial setup, 1 hour per additional table

**What You'll Create:**
1. `dq_rules` Delta table - Centralized rules repository in Unity Catalog
2. `dq_rules_loader.py` - Pure Python module to load rules at runtime
3. `silver_*.py` - SDP/DLT notebooks with expectations loaded from Delta table
4. `silver_pipeline.yml` - Serverless SDP pipeline configuration
5. DQ monitoring views - Per-table metrics and referential integrity checks

---

## Decision Tree

| Question | Action |
|----------|--------|
| Creating a Silver layer from scratch? | **Use this skill** - it orchestrates everything |
| Only need DLT expectations patterns? | Read `silver/01-dlt-expectations-patterns/SKILL.md` directly |
| Need advanced DQX validation? | Read `silver/02-dqx-patterns/SKILL.md` directly |
| Need Asset Bundle configuration? | Read `skills/databricks-asset-bundles/SKILL.md` directly |
| Need table properties reference? | Read `common/databricks-table-properties/SKILL.md` directly |
| Need pure Python import patterns? | Read `common/databricks-python-imports/SKILL.md` directly |

---

## Mandatory Skill Dependencies

**CRITICAL: Before generating ANY code for the Silver layer, you MUST read and follow the patterns in these common skills. Do NOT generate these patterns from memory.**

| Phase | MUST Read Skill (use Read tool on SKILL.md) | What It Provides |
|-------|---------------------------------------------|------------------|
| All phases | `skills/databricks-expert-agent` | Core extraction principle: extract names from source, never hardcode |
| Schema setup | `common/schema-management-patterns` | CREATE SCHEMA DDL with governance metadata |
| DQ rules table | `common/databricks-table-properties` | TBLPROPERTIES for the dq_rules metadata table |
| DQ rules table | `common/unity-catalog-constraints` | PRIMARY KEY constraint syntax |
| Rules loader | `common/databricks-python-imports` | Pure Python module patterns (NO notebook header) |
| DLT notebooks | `common/databricks-table-properties` | Silver-layer TBLPROPERTIES (CDF, row tracking, auto-optimize) |
| Pipeline config | `skills/databricks-asset-bundles` | DLT pipeline YAML, job YAML, serverless config, multi-user `user_prefix` pattern |
| Pipeline config | `common/naming-tagging-standards` | Enterprise naming, COMMENTs, tags, PII classifications for every DDL and resource |
| Deployment (if user-triggered) | `common/databricks-autonomous-operations` | Deploy → Poll → Diagnose → Fix → Redeploy loop when jobs/pipelines fail |

**NEVER do these without FIRST reading the corresponding skill:**
- NEVER write `table_properties={...}` without reading `databricks-table-properties`
- NEVER write Python import patterns without reading `databricks-python-imports`
- NEVER write Asset Bundle YAML without reading `databricks-asset-bundles`
- NEVER write `CREATE SCHEMA` without reading `schema-management-patterns`
- NEVER define PK/FK constraints without reading `unity-catalog-constraints`
- NEVER skip a `references/*.md` file when the SKILL.md links to it with `See: references/...`
- NEVER skip the requirements template in Phase 1 — it forces structured design decisions

> **🔴 CRITICAL — Follow `See: references/...` links.**
> When a SKILL.md (or this orchestrator) says `See: references/xxx.md for complete pattern`,
> you MUST Read that reference file. The SKILL.md is a **summary**; the `references/*.md`
> file contains the complete, production-ready pattern. Skipping references means generating
> from memory rather than from the specification.
>
> For Silver specifically, these are the references most often skipped — read ALL of them
> during their relevant phase:
>
> | Reference | Phase | Why |
> |-----------|-------|-----|
> | `silver/00-silver-layer-setup/assets/templates/requirements-template.md` | Phase 1 | Forces Bronze→Silver mapping, DQ strategy, quarantine decisions before any code |
> | `silver/01-dlt-expectations-patterns/references/expectation-patterns.md` | Phase 2/4 | Complete DQ rules table DDL, loader implementation, population examples |
> | `silver/01-dlt-expectations-patterns/references/quarantine-patterns.md` | Phase 4 | Complete quarantine table implementation with diagnostic columns |
> | `silver/00-silver-layer-setup/references/silver-table-patterns.md` | Phase 4 | DLT table templates, `get_bronze_table()` helper, derived-field patterns |
> | `silver/00-silver-layer-setup/references/monitoring-patterns.md` | Phase 5 | DQ monitoring views, referential integrity, data freshness |
> | `silver/00-silver-layer-setup/references/pipeline-configuration.md` | Phase 6 | Silver-specific DLT pipeline YAML + DQ setup job YAML |

### 🔴 Non-Negotiable Defaults (Applied to EVERY Silver Table and Pipeline)

These defaults are ALWAYS applied. There are NO exceptions, NO overrides, NO alternative options.

| Default | Value | Applied Where | NEVER Do This Instead |
|---------|-------|---------------|----------------------|
| **Serverless** | `serverless: true` | Pipeline YAML | ❌ NEVER set `serverless: false` or define `clusters:` |
| **Auto Liquid Clustering** | `cluster_by_auto=True` | Every `@dlt.table()` | ❌ NEVER use `cluster_by=["col1", "col2"]` or `partition_cols=` |
| **Edition** | `edition: ADVANCED` | Pipeline YAML | ❌ NEVER use `CORE` or `PRO` (expectations require ADVANCED) |
| **Photon** | `photon: true` | Pipeline YAML | ❌ NEVER set `photon: false` |
| **Row Tracking** | `"delta.enableRowTracking": "true"` | Every table's `table_properties` | ❌ NEVER omit (breaks downstream MV refresh) |
| **Change Data Feed** | `"delta.enableChangeDataFeed": "true"` | Every table's `table_properties` | ❌ NEVER omit (required for incremental propagation) |

```python
# ✅ CORRECT: Every @dlt.table() MUST include these
@dlt.table(
    name="silver_anything",
    table_properties={
        "delta.enableChangeDataFeed": "true",
        "delta.enableRowTracking": "true",
        # ... other properties from databricks-table-properties
    },
    cluster_by_auto=True  # 🔴 MANDATORY on every table, including monitoring views
)
```

```yaml
# ✅ CORRECT: Pipeline YAML MUST include these
serverless: true      # 🔴 MANDATORY - no classic clusters
photon: true          # 🔴 MANDATORY - vectorized execution
edition: ADVANCED     # 🔴 MANDATORY - required for expectations
```

### Silver-Domain Dependencies

| Skill | Requirement | What It Provides |
|-------|-------------|------------------|
| `silver/01-dlt-expectations-patterns` | **MUST read** | DQ rules table DDL, rules loader cache pattern, DLT decorators, quarantine generation, runtime rule updates |
| `silver/02-dqx-patterns` | **Optional** | Read only when user needs richer diagnostics than DLT expectations, or pre-merge validation |

---

## Core Philosophy: Schema Cloning

**The Silver layer should essentially clone the source Bronze schema with minimal transformations:**

- **Same column names** as Bronze (no complex renaming)
- **Same data types** (minimal type conversions)
- **Same grain** (no aggregation - that's for Gold)
- **Add data quality rules** (the main value-add)
- **Add derived flags** (business indicators like `is_return`, `is_out_of_stock`)
- **Add business keys** (SHA256 hashes for tracking)
- **Add timestamps** (`processed_timestamp`)

**What NOT to do in Silver:**
- No major schema restructuring
- No aggregations (save for Gold)
- No complex business logic (simple flags only)
- No joining across tables (dimension lookups in Gold)

**Why:** Silver is the validated copy of source data. Gold handles complex transformations. This keeps Silver focused on data quality and makes troubleshooting easier (column names match source).

### Python API: this skill standardizes on `import dlt` (`dp` is the recommended forward path)

Databricks **recommends the modern `dp` API** (`from pyspark import pipelines as dp`) and it **fully supports expectations**. This skill and its DQ-rules framework (`dlt-expectations-patterns`) are currently written against `import dlt`, so **use `import dlt` here to stay consistent with the framework's decorators.** The `dp` equivalents are drop-in — migrating is a mechanical swap of the import and decorator prefix.

```python
# ✅ CURRENT STANDARD for this skill: legacy `dlt` API (matches the DQ-rules framework)
import dlt
from dq_rules_loader import get_critical_rules_for_table

@dlt.table(name="silver_transactions", cluster_by_auto=True)
@dlt.expect_all_or_drop(get_critical_rules_for_table("silver_transactions"))
def silver_transactions():
    return dlt.read_stream(get_bronze_table("bronze_transactions"))
```

```python
# ✅ RECOMMENDED forward path: modern `dp` API (expectations supported — dp.expect_all_or_drop)
from pyspark import pipelines as dp
from dq_rules_loader import get_critical_rules_for_table

@dp.table(name="silver_transactions", cluster_by_auto=True)
@dp.expect_all_or_drop(get_critical_rules_for_table("silver_transactions"))
def silver_transactions():
    return spark.readStream.table("bronze_transactions")
```

**Which to use?** Databricks documents `dp` as the recommended API and both `@dp.expect_all_or_drop()` and `@dp.expect_all()` exist. We keep `import dlt` as this skill's standard only so the rules loader and decorators stay uniform across the framework — **not** because `dp` lacks expectations. To migrate: change `import dlt` → `from pyspark import pipelines as dp`, `@dlt.` → `@dp.`, and `dlt.read_stream(x)` → `spark.readStream.table(x)`. See the [Lakeflow pipelines Python reference](https://docs.databricks.com/aws/en/ldp/developer/python-ref) for the full decorator mapping.

---

## File Structure

```
src/{project}_silver/
├── setup_dq_rules_table.py        # Databricks notebook: Create and populate DQ rules Delta table
├── dq_rules_loader.py             # Pure Python (NO notebook header): Load rules from Delta table
├── silver_dimensions.py           # DLT notebook: Dimension tables (stores, products, etc.)
├── silver_transactions.py         # DLT notebook: Fact table with quarantine
├── silver_inventory.py            # DLT notebook: Additional fact tables (if applicable)
└── data_quality_monitoring.py     # DLT notebook: DQ monitoring views
```

**Critical Files:**
- `dq_rules_loader.py` must be **pure Python** (NO `# Databricks notebook source` header)
- Run `silver_dq_setup_job` BEFORE deploying DLT pipeline

---

## Working Memory Management

This orchestrator spans 6 phases (deployment and Phase 7 are user-triggered). To maintain coherence without context pollution:

**After each phase, persist a brief summary note** capturing:
- **Phase 1 output:** Schema names (catalog, silver_schema), table list, DQ rules strategy decision
- **Phase 2 output:** DQ rules table path, count of rules defined, rule severity distribution
- **Phase 3 output:** `dq_rules_loader.py` path, confirmation it is pure Python (no notebook header)
- **Phase 4 output:** DLT notebook paths per table, expectation counts, SCD handling decisions
- **Phase 5 output:** Monitoring view paths, metric definitions
- **Phase 6 output:** Pipeline YAML path, job YAML path, `databricks.yml` sync status
- **Phase 7 output (if user-triggered):** Anomaly detection config, schema monitoring status

**What to keep in working memory:** Only the current phase's context, the table list from Phase 1, and the previous phase's summary note. Discard intermediate outputs (full DDL strings, DQ rule DataFrames, raw DLT notebook contents) — they are on disk and reproducible.

**Critical file note:** `dq_rules_loader.py` must be **pure Python** (NO `# Databricks notebook source` header). Carry this constraint through all phases.

---

## Phased Implementation Workflow

### Phase 1: Requirements & Schema Setup (30 min)

**Pre-Condition - MUST read these skills first:**
1. Read `skills/databricks-expert-agent/SKILL.md` - Apply extraction principle throughout
2. Read `common/schema-management-patterns/SKILL.md` - Use for Silver schema DDL

**Steps:**
1. **MUST Read AND fill** `assets/templates/requirements-template.md` before writing any code:
   - Map Bronze tables to Silver tables
   - Define DQ rules per entity (critical vs warning)
   - Identify quarantine candidates
   - Skipping this step consistently leads to incomplete DQ coverage and ad-hoc quarantine patterns
2. Create Silver schema using pattern from `schema-management-patterns`
3. Verify Bronze tables exist AND pin each table's column inventory — run SQL, do NOT infer from local files:
   ```bash
   databricks api post /api/2.0/sql/statements -p $PROFILE --json '{
     "warehouse_id": "<WAREHOUSE_ID>",
     "catalog": "<CATALOG>",
     "statement": "SHOW TABLES IN <CATALOG>.<BRONZE_SCHEMA>",
     "wait_timeout": "30s"
   }'
   ```
   If the Bronze schema doesn't exist or has zero tables, STOP and report — the Bronze layer must be completed first. Reading a clone script or inferring from the schema CSV is NOT runtime verification.

   Then, for EVERY Bronze table you will read, run `DESCRIBE TABLE <CATALOG>.<BRONZE_SCHEMA>.<table>` and capture the column names into a `{table: [columns]}` map held in working memory (the **pinned column inventory**). Every DQ rule's `constraint_sql`, every Silver column reference, and every `get_bronze_table()` column authored in Phases 2-4 MUST use a name from this pinned inventory — a reference to a column absent from the live `DESCRIBE` is a hard error, not a "close enough" guess. PRD/CSV names (e.g. `price`, `latitude`) routinely differ from live prefixed names (e.g. `base_price`, `property_latitude`); pinning the inventory first prevents authoring rules against names that do not exist.

---

### Phase 2: DQ Rules Table Setup (30 min)

**Pre-Condition - MUST read these skills first:**
1. Read `silver/01-dlt-expectations-patterns/SKILL.md` - Use for DQ rules table DDL and population
2. Read `common/databricks-table-properties/SKILL.md` - Apply metadata table TBLPROPERTIES
3. Read `common/unity-catalog-constraints/SKILL.md` - Apply PK constraint on (table_name, rule_name)

**Steps:**
1. Create `setup_dq_rules_table.py` notebook
2. Define DQ rules table DDL (schema from `dlt-expectations-patterns`)
3. Apply TBLPROPERTIES from `databricks-table-properties`
4. Apply PK constraint: `CONSTRAINT pk_dq_rules PRIMARY KEY (table_name, rule_name) NOT ENFORCED`
5. Populate rules using the requirements from Phase 1
6. Verify file created: `setup_dq_rules_table.py` is ready for deployment (deployment is user-triggered)

---

### Phase 3: Rules Loader Module (15 min)

**Pre-Condition - MUST read these skills first:**
1. Read `common/databricks-python-imports/SKILL.md` - CRITICAL: loader must be pure Python
2. Read `silver/01-dlt-expectations-patterns/SKILL.md` - Use cache pattern with `toPandas()`

**Steps:**
1. Create `dq_rules_loader.py` as pure Python file (NO notebook header!)
2. Implement functions: `get_critical_rules_for_table()`, `get_warning_rules_for_table()`, `get_quarantine_condition()`
3. Use module-level cache pattern with `toPandas()` (NOT `.collect()`) from `dlt-expectations-patterns`
4. Test import: `from dq_rules_loader import get_critical_rules_for_table`

---

### Phase 4: DLT Notebooks - Silver Tables (1-2 hours)

**Pre-Condition - MUST read these skills first:**
1. Read `common/databricks-table-properties/SKILL.md` - Extract Silver TBLPROPERTIES
2. Read `silver/01-dlt-expectations-patterns/SKILL.md` - Use decorator patterns
3. (Optional) Read `silver/02-dqx-patterns/SKILL.md` - Only if user needs hybrid DQX+DLT

**Steps:**
1. Create DLT notebooks using patterns from `references/silver-table-patterns.md`
2. Include `get_bronze_table()` helper in every notebook (see references/)
3. For each table:
   - Apply Silver TBLPROPERTIES from `databricks-table-properties`
   - Apply `@dlt.expect_all_or_drop(get_critical_rules_for_table(...))` decorator
   - Apply `@dlt.expect_all(get_warning_rules_for_table(...))` decorator
   - Clone Bronze schema with minimal transformations
   - Add derived flags, business keys, `processed_timestamp`
   - Set `cluster_by_auto=True` (NEVER specify columns manually)
4. For high-volume fact tables: create quarantine table using `get_quarantine_condition()`

**See:** `references/silver-table-patterns.md` for complete templates

---

### Phase 5: Monitoring Views (30 min)

**No external skill dependencies** - use `references/monitoring-patterns.md`

**Steps:**
1. Create `data_quality_monitoring.py` DLT notebook
2. Add per-table DQ metrics views (record counts, pass/fail rates)
3. Add referential integrity checks (orphaned records between fact and dimension)
4. Add data freshness monitoring

**See:** `references/monitoring-patterns.md` for complete patterns

---

### Phase 6: Pipeline & Job Configuration (15 min)

**Pre-Condition - MUST read these skills first:**
1. Read `skills/databricks-asset-bundles/SKILL.md` - DLT pipeline YAML, job YAML patterns

**Steps:**
1. Create `resources/silver_dlt_pipeline.yml` using patterns from `databricks-asset-bundles`
2. Create `resources/silver_dq_setup_job.yml` for the DQ rules setup job
3. Set DLT Direct Publishing Mode: `catalog` + `schema` fields (NOT `target`)
4. Pass configuration: `catalog`, `bronze_schema`, `silver_schema`
5. Set: `serverless: true`, `edition: ADVANCED`, `photon: true`
6. **Multi-user safety:** In shared workspaces, include `${var.user_prefix}` in every pipeline/job `name:` field. See `skills/databricks-asset-bundles` → "Shared Workspace Naming" section for the exact pattern. Without it, the second user to deploy hits a `pipeline name is already used` error — and `--force` does NOT fix it (see `skills/databricks-asset-bundles/references/common-errors.md` Error 17).

**See:** `references/pipeline-configuration.md` for Silver-specific examples

---

### 🛑 STOP — Artifact Creation Complete

**Phases 1–6 are complete.** All files (DQ rules table script, rules loader, DLT notebooks, monitoring views, pipeline/job YAMLs) have been created. **Do NOT proceed to deployment or Phase 7 unless the user explicitly requests it.**

**Contract test before any deploy (read-only).** Before reporting completion, validate the authored files against the live schema so column/DDL bugs surface now, not in a failed job run: (1) dry-import `dq_rules_loader.py` — it must import cleanly and stay pure Python (no notebook header); (2) for every rule, run its `constraint_sql` read-only as `SELECT <constraint_sql> FROM <catalog>.<bronze_schema>.<table> LIMIT 1` and confirm each referenced column is in the Phase 1 pinned column inventory — an `UNRESOLVED_COLUMN`/parse error here is the exact failure that otherwise only appears as a failed DQ-setup/pipeline run; (3) confirm the loader's expected `dq_rules` row shape matches `setup_dq_rules_table.py`'s INSERT columns, and that no DDL uses a `DEFAULT` clause or an invented column. Fix and re-run until clean before deploying.

Report what was created and ask the user if they want to deploy and run.

---

**Deployment Order (USER-TRIGGERED ONLY — do not auto-execute):**

> **Client note:** IDE runs these in a terminal; Genie Code runs the `databricks bundle …` commands via `runDatabricksCli`. Generated bundle files anchor to `dp_bundle_root` (= `<artifact_root>/<use_case_slug>_dab`), and on Genie Code that folder is also the `bundle deploy` page-context root — **be on the `dp_bundle_root` page to deploy.** The pipeline/job is the only mechanism that creates Silver tables; never run the DDL/ingest directly. See `skills/genie-code-environment`.

```bash
# 1. Deploy everything
databricks bundle deploy -t dev

# 2. Run DQ rules setup FIRST (creates dq_rules table)
databricks bundle run silver_dq_setup_job -t dev

# 3. Verify rules table exists (NOTE: raw `databricks api` calls do NOT inherit
#    the profile from databricks.yml — pass `-p <profile>` explicitly. See
#    common/databricks-autonomous-operations/SKILL.md "Profile & Workspace Resolution".)
# SELECT * FROM {catalog}.{silver_schema}.dq_rules

# 4. THEN run DLT pipeline (loads rules from table)
databricks pipelines start-update --pipeline-name "[${bundle.target} ${var.user_prefix}] Silver Layer Pipeline"
```

---

### Post-Run Verification (after pipeline completes)

After the DLT pipeline finishes, verify expectations were applied using the DLT system `event_log()` TVF. **Do NOT use `databricks pipelines list-pipeline-events`** — it returns lifecycle events but lacks per-expectation pass/fail counts.

```sql
SELECT
  event_type,
  details:flow_progress.data_quality.dropped_records AS dropped,
  details:flow_progress.data_quality.expectations     AS expectations
FROM event_log("<PIPELINE_ID>")
WHERE details:flow_progress.data_quality IS NOT NULL
ORDER BY timestamp DESC
LIMIT 10;
```

**See:** `silver/01-dlt-expectations-patterns/SKILL.md` (Pattern 5) for the Silver-table-scoped variant, and `common/databricks-autonomous-operations/references/dlt-pipeline-troubleshooting.md` for the full DLT verification playbook.

---

### Phase 7: Enable Anomaly Detection on Silver Schema (5 min) — USER-TRIGGERED ONLY

> **This phase is executed ONLY when the user explicitly requests it.** Do not auto-execute.

**Pre-Condition - MUST read this skill first:**
1. Read `monitoring/04-anomaly-detection/SKILL.md` — Schema-level freshness/completeness monitoring

**Why:** Every Silver schema should have anomaly detection enabled from day one. It builds freshness and completeness ML baselines immediately, catching stale/incomplete tables before downstream consumers notice.

**Steps:**
1. Enable anomaly detection on the Silver schema (uses `enable_anomaly_detection_on_schema()` from the anomaly-detection skill)
2. Exclude metadata tables that are not data pipeline outputs (e.g., `dq_rules`)
3. Verify enablement via Catalog Explorer or SDK

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.dataquality import Monitor, AnomalyDetectionConfig

w = WorkspaceClient()

# Get Silver schema UUID
schema_info = w.schemas.get(full_name=f"{catalog}.{silver_schema}")
schema_id = schema_info.schema_id

# Enable anomaly detection (exclude metadata tables)
try:
    w.data_quality.create_monitor(
        monitor=Monitor(
            object_type="schema",
            object_id=schema_id,
            anomaly_detection_config=AnomalyDetectionConfig(
                excluded_table_full_names=[
                    f"{catalog}.{silver_schema}.dq_rules",  # Metadata, not pipeline output
                ]
            )
        )
    )
    print(f"✓ Anomaly detection enabled on {catalog}.{silver_schema}")
except Exception as e:
    if "already exists" in str(e).lower():
        print(f"✓ Already enabled (skipping)")
    else:
        print(f"⚠️ Non-blocking: {e}")
```

**Note:** This is non-blocking — if anomaly detection fails to enable (permissions, preview limitations), the Silver layer setup continues. Retry later via `monitoring/04-anomaly-detection/scripts/enable_anomaly_detection.py`.

---

## Common Mistakes (Silver-Specific)

### Mistake 1: Deploying DLT Before DQ Setup Job
```
Pipeline Error: Table or view not found: dq_rules
```
**Fix:** Run `silver_dq_setup_job` BEFORE deploying/running DLT pipeline.

### Mistake 2: Notebook Header in Loader File
```python
# dq_rules_loader.py
# Databricks notebook source  # <-- Makes it a notebook, breaks imports!
```
**Fix:** Remove `# Databricks notebook source` line. Read `databricks-python-imports` for correct pattern.

### Mistake 3: Aggregation in Silver
```python
# WRONG: Aggregation belongs in Gold
def silver_sales_daily():
    return dlt.read_stream(...).groupBy("store", "date").agg(sum("revenue"))
```
**Fix:** Keep Silver at transaction grain. Aggregate in Gold.

### Mistake 4: Manual Clustering Columns
```python
# WRONG
@dlt.table(cluster_by=["store_number", "transaction_date"])
```
**Fix:** Always use `cluster_by_auto=True`. Never specify columns.

### Mistake 5: Using expect_or_fail
```python
# WRONG: Pipeline fails on bad data
@dlt.expect_or_fail("valid_id", "id IS NOT NULL")
```
**Fix:** Use `@dlt.expect_all_or_drop()` for critical rules. Pipeline continues, bad records quarantined.

### Mistake 6: Hardcoding Table Names
```python
# WRONG: Hardcoded table reference
dlt.read_stream("my_catalog.bronze.transactions")
```
**Fix:** Use `get_bronze_table()` helper with DLT configuration. See `references/silver-table-patterns.md`.

### Mistake 7: Schema Evolution Without Full Refresh
```
Error: Incompatible schema change detected on streaming table
```
**Fix:** Streaming tables require a **full refresh** for incompatible schema changes (adding NOT NULL columns, changing types). Trigger with: `databricks pipelines start-update --pipeline-name "..." --full-refresh`

### Mistake 8: Missing Row Tracking (Breaks Downstream MVs)
```python
# ❌ WRONG: Missing delta.enableRowTracking
table_properties={
    "delta.enableChangeDataFeed": "true",
    # Row tracking missing!
}
```
**Fix:** ALWAYS include `"delta.enableRowTracking": "true"` in Silver table properties. Without it, downstream Gold materialized views cannot use incremental refresh and will do expensive full recomputation.

### Mistake 9: Mixing `dlt` and `dp` decorators in the same table definition
```python
# ❌ WRONG: mixing APIs — @dp.table with a @dlt.* decorator
from pyspark import pipelines as dp
@dp.table(name="silver_transactions")
@dlt.expect_all_or_drop(get_critical_rules_for_table(...))  # Mixes APIs!
```
**Fix:** Pick one API and use it consistently. Both support expectations — `dp` is Databricks' recommended API (`@dp.table` + `@dp.expect_all_or_drop`), while this skill's DQ-rules framework standardizes on `import dlt` (`@dlt.table` + `@dlt.expect_all_or_drop`). Don't combine `@dp.*` and `@dlt.*` on the same function. See "Python API" section above.

---

## Post-Creation Validation

Before considering the Silver layer complete, verify each item and confirm its source:

### Common Skill Compliance
- [ ] Table properties match `databricks-table-properties` Silver layer spec (not generated from memory)
- [ ] Python imports follow `databricks-python-imports` patterns (loader has NO notebook header)
- [ ] Asset Bundle YAML follows `databricks-asset-bundles` patterns (notebook_task, base_parameters)
- [ ] Schema DDL follows `schema-management-patterns` (IF NOT EXISTS, governance metadata)
- [ ] PK constraint follows `unity-catalog-constraints` syntax (NOT ENFORCED keyword)
- [ ] Names extracted from source files per `databricks-expert-agent` (not hardcoded)

### Silver-Domain Skill Compliance
- [ ] DQ rules table follows `dlt-expectations-patterns` DDL
- [ ] Rules loader uses cache pattern from `dlt-expectations-patterns` (toPandas, not collect)
- [ ] DLT decorators follow `dlt-expectations-patterns` (expect_all_or_drop, expect_all)
- [ ] Quarantine condition uses `dlt-expectations-patterns` generation pattern

### Silver Layer Specifics
- [ ] Schema cloning: Silver columns match Bronze (no aggregation, no joins)
- [ ] `get_bronze_table()` helper used for all source table references
- [ ] `cluster_by_auto=True` on every table (NEVER manual cluster keys)
- [ ] `delta.enableRowTracking` = `true` on every Silver table (required for downstream MV incremental refresh)
- [ ] Quarantine tables created for high-volume fact tables
- [ ] DQ monitoring views created (including data freshness)
- [ ] (User-triggered) Deployment order documented: DQ setup job runs BEFORE DLT pipeline
- [ ] One pipelines API used consistently — `import dlt` is this skill's current standard; `dp` is the recommended forward path (don't mix `@dlt.*` and `@dp.*`)
- [ ] `serverless: true` in pipeline YAML (NEVER classic clusters)
- [ ] `photon: true` in pipeline YAML
- [ ] `edition: ADVANCED` set in pipeline YAML (required for expectations/CDC)
- [ ] No `clusters:` block in pipeline YAML (serverless manages compute)
- [ ] Deduplication applied where Bronze may have duplicate records
- [ ] `processed_timestamp` added to every Silver table
- [ ] Event timestamps preserved from Bronze (not replaced by processing time)
- [ ] (User-triggered) Anomaly detection enabled on Silver schema (Phase 7)
- [ ] (User-triggered) Metadata tables (e.g., `dq_rules`) excluded from anomaly detection

---

## Reference Files

### Silver Table Patterns
- **`references/silver-table-patterns.md`** - Complete DLT table templates: standard pattern, dimension example, fact example with quarantine, `get_bronze_table()` helper, derived field patterns

### Monitoring Patterns
- **`references/monitoring-patterns.md`** - DQ monitoring views: per-table metrics, referential integrity checks, data freshness monitoring

### Pipeline Configuration
- **`references/pipeline-configuration.md`** - Silver-specific DLT pipeline YAML and DQ setup job YAML examples (supplements `databricks-asset-bundles`)

## Templates

### Requirements Template
- **`assets/templates/requirements-template.md`** - Fill-in-first requirements gathering: project context, Bronze-to-Silver table mapping, DQ rules per entity, quarantine strategy

## Related Skills

| Skill | Relationship | Path |
|-------|-------------|------|
| `dlt-expectations-patterns` | **Mandatory** - DQ rules, loader, decorators | `silver/01-dlt-expectations-patterns/SKILL.md` |
| `dqx-patterns` | **Optional** - Advanced validation | `silver/02-dqx-patterns/SKILL.md` |
| `anomaly-detection` | **Mandatory** - Schema freshness/completeness monitoring | `monitoring/04-anomaly-detection/SKILL.md` |
| `databricks-expert-agent` | **Mandatory** - Extraction principle | `skills/databricks-expert-agent/SKILL.md` |
| `databricks-table-properties` | **Mandatory** - Silver TBLPROPERTIES | `common/databricks-table-properties/SKILL.md` |
| `databricks-python-imports` | **Mandatory** - Pure Python loader | `common/databricks-python-imports/SKILL.md` |
| `databricks-asset-bundles` | **Mandatory** - Pipeline/job YAML | `skills/databricks-asset-bundles/SKILL.md` |
| `schema-management-patterns` | **Mandatory** - Schema DDL | `common/schema-management-patterns/SKILL.md` |
| `unity-catalog-constraints` | **Mandatory** - PK constraint | `common/unity-catalog-constraints/SKILL.md` |

## Pipeline Progression

**Previous stage:** `bronze/00-bronze-layer-setup` → Bronze tables must exist before creating Silver

**Next stage:** After completing the Silver layer, proceed to:
- **`gold/01-gold-layer-setup`** — Implement Gold layer tables, merge scripts, and FK constraints from the YAML designs created in stage 1

---

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

## References

### Official Databricks Documentation
- [DLT Expectations](https://docs.databricks.com/aws/en/dlt/expectations)
- [Portable and Reusable Expectations](https://docs.databricks.com/aws/en/ldp/expectation-patterns#portable-and-reusable-expectations)
- [Share Code Between Notebooks](https://docs.databricks.com/aws/en/notebooks/share-code)
- [Automatic Clustering](https://docs.databricks.com/aws/en/delta/clustering#enable-or-disable-automatic-liquid-clustering)
- [Lakeflow Declarative Pipelines (SDP)](https://docs.databricks.com/aws/en/ldp/) - Modern pipeline framework overview
- [Python API: `pyspark.pipelines`](https://docs.databricks.com/aws/en/ldp/developer/python-ref) - Modern Python API reference (future migration target)
- [Row Tracking](https://docs.databricks.com/aws/en/delta/row-tracking) - Required for incremental MV refresh
- [Schema Evolution in Streaming Tables](https://docs.databricks.com/aws/en/ldp/develop#schema-evolution) - Full refresh requirements
- [Pipeline Edition Comparison](https://docs.databricks.com/aws/en/ldp/configure-pipeline#editions) - ADVANCED required for expectations/CDC

---

## See Also

- Authoritative upstream (alternate registry): [databricks-agent-skills / `databricks-pipelines`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-pipelines) — canonical DLT / Spark Declarative Pipelines guidance.

## Version History

- **2026-08-30** — Reconciled the `dlt`-vs-`dp` premise: expectations **are** available in the modern `dp` API (`dp.expect_all_or_drop`), which Databricks recommends. Corrected the "not yet available in `dp`" wording, added a `dp` equivalent snippet, reframed Mistake 9 (mixing `dlt`/`dp` decorators) and the checklist item, and kept `import dlt` as this skill's standard with a mechanical migration note. Bumped `last_verified`.

