---
name: observability-setup
description: >
  End-to-end orchestrator for setting up Databricks observability including Lakehouse Monitoring,
  Anomaly Detection, AI/BI Dashboards, and SQL Alerts. Guides users through monitor creation for
  Gold tables, schema-level anomaly detection for freshness/completeness, dashboard design with
  monitoring widgets, and config-driven alerting. Orchestrates mandatory dependencies on monitoring
  skills (lakehouse-monitoring-comprehensive, anomaly-detection, databricks-aibi-dashboards,
  sql-alerting-patterns) and common skills (databricks-asset-bundles, databricks-expert-agent,
  databricks-python-imports).
  Use when setting up observability end-to-end, creating Lakehouse Monitors, enabling anomaly
  detection, building dashboards, or configuring SQL alerts.
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: monitors
deploy_verb: bundle_deploy
deploy_note: "Orchestrates Lakehouse monitors + anomaly detection + AI/BI dashboards + SQL-alert jobs, all deployed via `bundle deploy --target dev` (runDatabricksCli on Genie Code). On Genie Code, write generated monitor/alert configs and dashboard JSON under the cloned repo root (`{REPO_ROOT}` = `state_file_root` from `skills/vibecoding-state`), not a bare relative path \u2014 relative paths resolve against the page CWD (see `skills/genie-code-environment` \u00a78)."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "1.0.0"
  domain: monitoring
  role: orchestrator
  pipeline_stage: 7
  pipeline_stage_name: observability
  next_stages:
    - ml-pipeline-setup
  workers:
    - lakehouse-monitoring-comprehensive
    - anomaly-detection
    - databricks-aibi-dashboards
    - sql-alerting-patterns
  common_dependencies:
    - databricks-asset-bundles
    - databricks-expert-agent
    - databricks-python-imports
    - naming-tagging-standards
    - databricks-autonomous-operations
  consumes:
    - plans/manifests/observability-manifest.yaml
  consumes_policy: required  # STOP if manifest is missing — no self-discovery fallback
  dependencies:
    - lakehouse-monitoring-comprehensive
    - anomaly-detection
    - databricks-aibi-dashboards
    - sql-alerting-patterns
    - databricks-asset-bundles
    - databricks-expert-agent
    - databricks-python-imports
  last_verified: "2026-08-30"
  volatility: medium
  upstream_sources: []  # Internal orchestrator
---

# Observability Setup Orchestrator

End-to-end workflow for setting up Databricks observability — Lakehouse Monitoring, Anomaly Detection, AI/BI Dashboards, and SQL Alerts — on top of a completed Gold layer and semantic layer.

**Predecessor:** `semantic-layer-setup` skill (Semantic layer should be complete, but Gold tables are the minimum requirement)

**Time Estimate:** 3-5 hours for initial setup, 30 min per additional table/dashboard

**What You'll Create:**
1. Lakehouse Monitors — data quality, drift, and custom business KPIs for Gold tables
2. Anomaly Detection — schema-level freshness and completeness monitoring via the Data Quality API
3. AI/BI Dashboards — Lakeview dashboards with monitoring widgets and business metrics
4. SQL Alerts — config-driven alerting with severity-based routing

---

## Decision Tree

| Question | Action |
|----------|--------|
| Setting up observability end-to-end? | **Use this skill** — it orchestrates everything |
| Only need Lakehouse Monitoring? | Read `monitoring/01-lakehouse-monitoring-comprehensive/SKILL.md` directly |
| Only need Anomaly Detection? | Read `monitoring/04-anomaly-detection/SKILL.md` directly |
| Only need AI/BI Dashboards? | Read `monitoring/02-databricks-aibi-dashboards/SKILL.md` directly. **Still load common skills first:** `databricks-expert-agent`, `naming-tagging-standards` |
| Only need SQL Alerts? | Read `monitoring/03-sql-alerting-patterns/SKILL.md` directly |

---

## Mandatory Skill Dependencies

**CRITICAL: Before generating ANY code for observability, you MUST read and follow the patterns in these common skills. Do NOT generate these patterns from memory.**

| Phase | MUST Read Skill (use Read tool on SKILL.md) | What It Provides |
|-------|---------------------------------------------|------------------|
| All phases | `skills/databricks-expert-agent` | Core extraction principle: extract names from source, never hardcode |
| Monitor scripts | `common/databricks-python-imports` | Pure Python module patterns for helpers |
| Job deployment | `skills/databricks-asset-bundles` | Job YAML, deployment patterns |
| Troubleshooting | `common/databricks-autonomous-operations` | Deploy → Poll → Diagnose → Fix → Redeploy loop when jobs fail |

### Monitoring-Domain Dependencies

| Skill | Requirement | What It Provides |
|-------|-------------|------------------|
| `monitoring/01-lakehouse-monitoring-comprehensive` | **MUST read** at Phase 1 | Monitor setup, custom metrics, graceful degradation |
| `monitoring/04-anomaly-detection` | **MUST read** at Phase 2 | Schema-level freshness/completeness via Data Quality API |
| `monitoring/02-databricks-aibi-dashboards` | **MUST read** at Phase 3 | Dashboard JSON, widget patterns, deployment |
| `monitoring/03-sql-alerting-patterns` | **MUST read** at Phase 4 | Config-driven alerts, SDK deployment, severity routing |

---

## 🔴 Non-Negotiable Defaults

| Default | Value | Applied Where | NEVER Do This Instead |
|---------|-------|---------------|----------------------|
| **Manifest required** | `plans/manifests/observability-manifest.yaml` | Phase 0 — before any implementation | ❌ NEVER create artifacts via self-discovery; STOP if manifest is missing |
| **Monitor type** | `MonitorTimeSeries` or `MonitorSnapshot` | Every Lakehouse Monitor | ❌ NEVER skip monitor type selection |
| **Custom metrics** | `input_columns=[":table"]` for table-level KPIs | Every custom business metric | ❌ NEVER use column-level when table-level is needed |
| **Anomaly detection ID** | Schema UUID from `w.schemas.get()` | Every `create_monitor()` call | ❌ NEVER pass three-level name as `object_id` |
| **Anomaly detection object** | Wrap in `Monitor(object_type="schema", ...)` | Every `create_monitor()` call | ❌ NEVER pass keyword args directly |
| **Dashboard deployment** | Lakeview JSON with `dataset_catalog`/`dataset_schema` | Every dashboard | ❌ NEVER hardcode catalog/schema in dashboard queries |
| **Alert queries** | Fully qualified table names (no parameters) | Every SQL alert query | ❌ NEVER use parameterized table names in alerts |
| **Serverless** | `environments:` block with `environment_key` | Every monitoring job | ❌ NEVER define `job_clusters:` |

---

## Working Memory Management

This orchestrator spans 5 phases (Phase 0-4). To maintain coherence without context pollution:

**After each phase, persist a brief summary note** capturing:
- **Phase 0 output:** Manifest loaded, planning_mode (acceleration/workshop), artifact counts (monitors, anomaly detection schemas, dashboards, alerts), validation passed
- **Phase 1 output:** Monitor names and IDs, tables monitored, custom metrics config, any creation failures
- **Phase 2 output:** Anomaly detection enabled (yes/no per schema), schema UUIDs, excluded tables, any permission errors
- **Phase 3 output:** Dashboard names and IDs, Lakeview JSON paths, dataset_catalog/dataset_schema settings
- **Phase 4 output:** Alert names and configurations, notification destinations, query SQL paths

**What to keep in working memory:** Only the current phase's worker skill, the artifact inventory (from Phase 0), and the previous phase's summary note. Discard intermediate outputs (full JSON payloads, raw monitoring metrics) — they are on disk and reproducible.

---

## Phased Implementation Workflow

### Phase 0: Read Plan — MANDATORY (5 minutes)

**The observability manifest is REQUIRED. Do NOT proceed without it.**

This orchestrator implements exactly what the project plan defined — no more, no less. The manifest `plans/manifests/observability-manifest.yaml` is generated by the `planning/00-project-planning` skill (stage 5) and serves as the implementation contract.

**🔴 If the manifest does not exist, STOP and tell the user:**
> *"The observability manifest (`plans/manifests/observability-manifest.yaml`) is missing. This orchestrator requires a project plan to define which monitors, dashboards, alerts, and anomaly detection schemas to create. Please run the `planning/00-project-planning` skill first (stage 5), then return here."*

```python
import yaml
from pathlib import Path

manifest_path = Path("plans/manifests/observability-manifest.yaml")

if not manifest_path.exists():
    raise FileNotFoundError(
        "REQUIRED: plans/manifests/observability-manifest.yaml not found. "
        "Run planning/00-project-planning (stage 5) first to generate the "
        "observability manifest, then re-run this orchestrator."
    )

with open(manifest_path) as f:
    manifest = yaml.safe_load(f)

# Respect planning mode — workshop mode means strict artifact caps
planning_mode = manifest.get('planning_mode', 'acceleration')
if planning_mode == 'workshop':
    print("⚠️  Workshop mode active — creating ONLY the artifacts listed in the manifest")

# Extract implementation checklist from manifest
monitors = manifest.get('lakehouse_monitors', [])
anomaly_detection = manifest.get('anomaly_detection', {})
dashboards = manifest.get('dashboards', [])
alerts = manifest.get('alerts', [])

print(f"Plan: {len(monitors)} monitors, "
      f"{len(anomaly_detection.get('schemas', []))} anomaly detection schemas, "
      f"{len(dashboards)} dashboards, {len(alerts)} alerts")

# Validate summary counts match actual artifact counts
summary = manifest.get('summary', {})
assert len(monitors) == int(summary.get('total_monitors', len(monitors))), \
    f"Monitor count mismatch: {len(monitors)} actual vs {summary.get('total_monitors')} in summary"
assert len(dashboards) == int(summary.get('total_dashboards', len(dashboards))), \
    f"Dashboard count mismatch: {len(dashboards)} actual vs {summary.get('total_dashboards')} in summary"
assert len(alerts) == int(summary.get('total_alerts', len(alerts))), \
    f"Alert count mismatch: {len(alerts)} actual vs {summary.get('total_alerts')} in summary"
```

**What the manifest provides:**
- `lakehouse_monitors[]` — table name, monitor type, custom metrics, slicing expressions
- `anomaly_detection` — schemas to enable, tables to exclude per schema
- `dashboards[]` — name, domain, pages, widgets with query sources
- `alerts[]` — alert ID, severity, query SQL, threshold, schedule, notification destination
- `summary` — expected artifact counts for validation
- `planning_mode` — `acceleration` (full) or `workshop` (capped artifacts; do NOT expand via self-discovery)

**Key principle:** Create ONLY the artifacts listed in the manifest. Do NOT add monitors, dashboards, or alerts beyond what the plan specified. If the plan missed something, update the plan first — then re-run this orchestrator.

---

### Phase 1: Lakehouse Monitoring (1-2 hours)

**MANDATORY: Read each skill below using the Read tool BEFORE writing any code for this phase:**

| # | Skill Path | What It Provides |
|---|------------|------------------|
| 1 | `skills/databricks-expert-agent/SKILL.md` | Extract-don't-generate principle |
| 2 | `data_product_accelerator/skills/monitoring/01-lakehouse-monitoring-comprehensive/SKILL.md` | Monitor setup, custom metrics |

**Input:** `manifest['lakehouse_monitors']` — iterate over the manifest's monitor list. Each entry defines `table_name`, `monitor_type`, `custom_metrics`, and `slicing_exprs`. Do NOT add monitors for tables not listed in the manifest.

**Steps:**
1. Read `manifest['lakehouse_monitors']` — this is your complete list of tables to monitor
2. For each entry, use the manifest's `monitor_type` (TimeSeries or Snapshot) — do not override
3. Define custom business metrics from the manifest's `custom_metrics` array using `input_columns=[":table"]` for table-level KPIs
4. Create monitor setup script with graceful degradation (delete-then-create pattern)
5. Deploy monitors and verify metric tables are populated
6. Track completion: check off each manifest entry as its monitor is confirmed active

### Phase 2: Anomaly Detection (15-30 minutes)

**MANDATORY: Read each skill below using the Read tool BEFORE writing any code for this phase:**

| # | Skill Path | What It Provides |
|---|------------|------------------|
| 1 | `data_product_accelerator/skills/monitoring/04-anomaly-detection/SKILL.md` | Schema-level freshness/completeness via Data Quality API |

**Input:** `manifest['anomaly_detection']` — the manifest defines which schemas to enable and which tables to exclude per schema. If the manifest's `anomaly_detection` section is empty or absent, skip this phase entirely.

**Why Phase 2 (right after Lakehouse Monitors):** Enable anomaly detection early so ML models start training on historical commit and row-count patterns. By the time you finish Phases 3-4, the first scan results will be available for dashboards and alerts.

**Steps:**
1. Read `manifest['anomaly_detection']['schemas']` — this is your complete list of schemas to enable
2. For each schema entry, retrieve the schema UUID via `w.schemas.get(full_name=f"{catalog}.{schema}")`
3. Enable anomaly detection using `w.data_quality.create_monitor()` with a `Monitor` object:
   ```python
   from databricks.sdk.service.dataquality import Monitor, AnomalyDetectionConfig

   schema_info = w.schemas.get(full_name=f"{catalog}.{schema}")
   w.data_quality.create_monitor(
       monitor=Monitor(
           object_type="schema",
           object_id=schema_info.schema_id,
           anomaly_detection_config=AnomalyDetectionConfig(
               excluded_table_full_names=[
                   f"{catalog}.{schema}.staging_table",  # Optional: skip staging/temp tables
               ]
           )
       )
   )
   ```
4. Exclude tables listed in the manifest entry's `excluded_tables` via `excluded_table_full_names`
5. Handle idempotency — if already enabled, catch `"already exists"` and skip gracefully
6. Verify enablement via Catalog Explorer (schema Details tab) or `w.data_quality.get_monitor()`
7. Track completion: check off each manifest schema entry as its anomaly detection is confirmed active
8. Note: first scan takes 15-30 minutes; results appear in `system.data_quality_monitoring.table_results`

### Phase 3: AI/BI Dashboards (1-2 hours)

**MANDATORY: Read each skill below using the Read tool BEFORE writing any code for this phase:**

| # | Skill Path | What It Provides |
|---|------------|------------------|
| 1 | `data_product_accelerator/skills/monitoring/02-databricks-aibi-dashboards/SKILL.md` | Dashboard JSON, widget patterns |

**Input:** `manifest['dashboards']` — iterate over the manifest's dashboard list. Each entry defines `name`, `domain`, `pages`, and `widgets`. Do NOT create dashboards not listed in the manifest.

**Steps:**
1. Read `manifest['dashboards']` — this is your complete list of dashboards to create
2. For each dashboard, use the manifest's page layout and widget definitions to design the Lakeview JSON
3. Create queries using monitoring profile/drift tables as specified in widget `query_source`
4. Build widget configurations with proper number formatting
5. Set `dataset_catalog` and `dataset_schema` for environment portability
6. Deploy dashboard via Asset Bundle or API
7. Track completion: check off each manifest entry as its dashboard is confirmed deployed

### Phase 4: SQL Alerts (1 hour)

**MANDATORY: Read each skill below using the Read tool BEFORE writing any code for this phase:**

| # | Skill Path | What It Provides |
|---|------------|------------------|
| 1 | `data_product_accelerator/skills/monitoring/03-sql-alerting-patterns/SKILL.md` | Config-driven alerts, SDK deployment |
| 2 | `skills/databricks-asset-bundles/SKILL.md` | Job YAML for alert deployment |

**Input:** `manifest['alerts']` — iterate over the manifest's alert list. Each entry defines `alert_id`, `severity`, `query`, `threshold`, `schedule`, and `notification_destination`. Do NOT create alerts not listed in the manifest.

**Steps:**
1. Read `manifest['alerts']` — this is your complete list of alerts to create
2. Create alert configuration table (Delta table-based, severity-driven) using the manifest's alert definitions
3. Use each alert's `query` SQL, `threshold`, `operator`, and `schedule` exactly as specified in the manifest
4. Deploy alerts via Databricks SDK (V2 dict-based or typed classes)
5. Configure notification destinations per the manifest's `notification_destination` and `severity` fields
6. Set up Quartz cron schedules from the manifest's `schedule` field
7. Track completion: check off each manifest `alert_id` as its alert is confirmed deployed

---

## Post-Creation Validation

### Manifest Compliance (CRITICAL)
- [ ] `plans/manifests/observability-manifest.yaml` was read at Phase 0 before any implementation
- [ ] Every Lakehouse Monitor maps 1:1 to a `lakehouse_monitors[]` entry in the manifest
- [ ] Every anomaly detection schema maps 1:1 to an `anomaly_detection.schemas[]` entry in the manifest
- [ ] Every dashboard maps 1:1 to a `dashboards[]` entry in the manifest
- [ ] Every alert maps 1:1 to an `alerts[]` entry in the manifest
- [ ] No artifacts were created via self-discovery (only manifest-driven)
- [ ] If `planning_mode: workshop`, artifact counts do NOT exceed manifest totals
- [ ] Manifest `summary` counts match actual deployed artifact counts

### Common Skill Compliance
- [ ] Names extracted from Gold YAML (not generated) per `databricks-expert-agent`
- [ ] Asset Bundle YAML follows `databricks-asset-bundles` patterns
- [ ] Python imports follow `databricks-python-imports` patterns

### Observability Specifics
- [ ] Lakehouse Monitors created for all critical Gold tables
- [ ] Custom business metrics use `input_columns=[":table"]` syntax
- [ ] Monitor setup uses graceful degradation (delete-then-create)
- [ ] Anomaly detection enabled on all Gold schemas (and Silver schemas if applicable)
- [ ] Anomaly detection uses schema UUID (not three-level name) as `object_id`
- [ ] Anomaly detection `create_monitor()` wrapped in `Monitor` object
- [ ] Staging/temp tables excluded via `excluded_table_full_names`
- [ ] Anomaly detection enable is idempotent (handles "already exists" gracefully)
- [ ] Dashboard uses `dataset_catalog`/`dataset_schema` for portability
- [ ] Dashboard widgets align with query columns
- [ ] Alert queries use fully qualified table names (no parameters)
- [ ] Alert severity routing configured (critical → PagerDuty, warning → email)
- [ ] All monitoring jobs use serverless compute

---

## Pipeline Progression

**Previous stage:** `semantic-layer-setup` → Metric Views, TVFs, and Genie Spaces should exist

**Next stage:** After completing observability, proceed to:
- **`ml/00-ml-pipeline-setup`** — Set up ML models, experiments, and batch inference

---

## Related Skills

| Skill | Relationship | Path |
|-------|-------------|------|
| `lakehouse-monitoring-comprehensive` | **Mandatory** — Monitor setup | `monitoring/01-lakehouse-monitoring-comprehensive/SKILL.md` |
| `anomaly-detection` | **Mandatory** — Schema-level freshness/completeness | `monitoring/04-anomaly-detection/SKILL.md` |
| `databricks-aibi-dashboards` | **Mandatory** — Dashboard patterns | `monitoring/02-databricks-aibi-dashboards/SKILL.md` |
| `sql-alerting-patterns` | **Mandatory** — Alert framework | `monitoring/03-sql-alerting-patterns/SKILL.md` |
| `databricks-expert-agent` | **Mandatory** — Extraction principle | `skills/databricks-expert-agent/SKILL.md` |
| `databricks-asset-bundles` | **Mandatory** — Deployment | `skills/databricks-asset-bundles/SKILL.md` |
| `databricks-python-imports` | **Mandatory** — Python patterns | `common/databricks-python-imports/SKILL.md` |

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

- [Lakehouse Monitoring](https://learn.microsoft.com/en-us/azure/databricks/lakehouse-monitoring/create-monitor-api)
- [Anomaly Detection](https://learn.microsoft.com/en-us/azure/databricks/data-quality-monitoring/anomaly-detection/)
- [AI/BI Dashboards](https://docs.databricks.com/aws/en/dashboards/)
- [SQL Alerts](https://docs.databricks.com/api/workspace/alerts)
