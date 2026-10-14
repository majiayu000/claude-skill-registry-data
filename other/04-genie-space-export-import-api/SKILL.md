---
name: genie-space-export-import-api
description: Comprehensive patterns for Databricks Genie Space Export/Import API - JSON schema, serialization format, and programmatic deployment. Use when programmatically creating, exporting, or importing Genie Spaces via REST API, troubleshooting API deployment errors, or implementing CI/CD for Genie Spaces. Includes complete GenieSpaceExport schema, API endpoints (List, Get, Create, Update, Delete), JSON format requirements, ID generation, variable substitution, inventory-driven generation patterns, and production deployment checklists.
clients: [ide_cli, genie_code]
bundle_resource: genie
deploy_verb: bundle_deploy
deploy_note: "RULE_8 tiers: T1 native `genie_spaces` bundle entry (preferred; verify CLI support via `bundle validate`) -> T2 provisioning notebook job (active fallback) -> T3 `createAsset`+PATCH dev-authoring loop (Genie-Code only: create a shell with `createAsset(assetType=genie)`, populate the FULL `serialized_space` via `PATCH /api/2.0/genie/spaces/{id}`, then PERSIST that JSON into the bundle and run T1/T2 once in dev for the version-controlled deploy). T3 is sanctioned for fast dev iteration ONLY when the JSON is persisted in the bundle and a job reproduces it; an orphan space with no persisted JSON is the regression. IDE (ide_cli) stays on T1/T2 (bundle) and never uses `createAsset`. Space name + table_identifiers carry the per-user prefix. semantic_warehouse_id is baked at deploy time, never a runtime --var."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "3.8.0"
  domain: semantic-layer
  role: worker
  pipeline_stage: 6
  pipeline_stage_name: semantic-layer
  called_by:
    - semantic-layer-setup
  standalone: true
  last_verified: "2026-08-30"
  volatility: high
  upstream_sources:
    - name: "databricks-agent-skills"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-genie-agents/SKILL.md"
      relationship: "extended"
      last_synced: "2026-08-30"
      sync_commit: "ca92a6c"
    - name: "databricks-docs-genie-getspace"
      url: "https://docs.databricks.com/api/workspace/genie/getspace"
      relationship: "upstream"
      last_synced: "2026-08-30"
    - name: "databricks-docs-genie-createspace"
      url: "https://docs.databricks.com/api/workspace/genie/createspace"
      relationship: "upstream"
      last_synced: "2026-08-30"
    - name: "databricks-docs-genie-updatespace"
      url: "https://docs.databricks.com/api/workspace/genie/updatespace"
      relationship: "upstream"
      last_synced: "2026-08-30"
    - name: "databricks-docs-genie-conversation-api"
      url: "https://docs.databricks.com/aws/en/genie/conversation-api"
      relationship: "upstream"
      last_synced: "2026-08-30"
---

# Genie Space Export/Import API

## Overview

This skill provides comprehensive patterns for programmatically creating, exporting, and importing Databricks Genie Spaces via the REST API. It covers the complete `GenieSpaceExport` JSON schema, API endpoints, common deployment errors, and production-ready workflows including variable substitution and asset inventory-driven generation.

> **Terminology (2026):** Databricks renamed **Genie Spaces** to **Genie Agents**. The REST endpoints are unchanged (`/api/2.0/genie/spaces`), and this skill uses "Genie Space" and "Genie Agent" interchangeably. The API now also exposes **Agent-mode** endpoints (stream reasoning + SQL + final reports with citations) alongside the Chat-mode and Management APIs covered here. See the [Genie Agents API](https://docs.databricks.com/aws/en/genie/conversation-api).

## When to Use This Skill

Use this skill when you need to:

- **Programmatically deploy Genie Spaces** via REST API (CI/CD pipelines, environment promotion)
- **Export Genie Space configurations** for version control, backup, or migration
- **Troubleshoot API deployment errors** (`BAD_REQUEST`, `INVALID_PARAMETER_VALUE`, `INTERNAL_ERROR`)
- **Implement cross-workspace deployment** with template variable substitution
- **Generate Genie Spaces from asset inventories** to prevent non-existent table errors
- **Validate Genie Space JSON structure** before deployment
- **Understand the complete GenieSpaceExport schema** (config, data_sources, instructions, benchmarks)

## Start From Templates (Mandatory)

**NEVER write the deployment notebook or job YAML from scratch.** Writing these from scratch is the #1 source of deployment failures — copy the template, then customize:

- `assets/templates/deploy_genie_spaces.py` → copy to `src/{project}_semantic/deploy_genie_spaces.py`
- `assets/templates/genie-deployment-job-template.yml` → copy to `resources/semantic/genie_deploy_job.yml`

The templates encode the correct notebook cell separators, `extract_space_config()` (wrapped vs raw format handling), `validate_genie_json_structure()`, array sorting, and `base_parameters` wiring. Hand-written versions routinely miss one of these and fail in deploy cycles 2–9 (see the retrospective in `references/` or the project's retrospectives directory).

## End-to-End Deployment? Use the Orchestrator

If you are deploying **TVFs + Metric Views + Genie Spaces together** (not just a standalone Genie Space), **STOP and read `semantic-layer/00-semantic-layer-setup/SKILL.md` first.** That orchestrator:
- Mandates a Gold schema inventory query before artifact creation (prevents phantom table errors)
- Coordinates skill loading across 6 phases with validation gates
- Provides combined job templates with `depends_on` chains

This skill handles **individual Genie Space API operations.** The orchestrator handles the **end-to-end semantic layer lifecycle.**

## Quick Reference

### API Operations

| Operation | Method | Endpoint | Use Case |
|-----------|--------|----------|----------|
| **List Spaces** | GET | `/api/2.0/genie/spaces` | Discover existing spaces |
| **Get Space** | GET | `/api/2.0/genie/spaces/{space_id}?include_serialized_space=true` | Export config, backup |
| **Create Space** | POST | `/api/2.0/genie/spaces` | New deployment, CI/CD |
| **Update Space** | PATCH | `/api/2.0/genie/spaces/{space_id}` | Modify config, add benchmarks |
| **Delete Space** | DELETE | `/api/2.0/genie/spaces/{space_id}` | Cleanup, teardown |

### API Limits

| Resource | Limit | Enforcement |
|----------|-------|-------------|
| `instructions.sql_functions` | **Max 50** | Truncate in generation script |
| `benchmarks.questions` | **Max 50** | Truncate in generation script |
| `data_sources.tables` | No hard limit | Keep ~25-30 for performance |
| `data_sources.metric_views` | No hard limit | Keep ~5-10 per space |

### Required Root Field

Every Genie Space JSON MUST include an explicit `"version"` at the root of `serialized_space`. The API accepts **versions 1 and 2**; **use version 2** — it is the richer schema that supports `benchmarks`, `data_sources.metric_views`, `example_question_sqls[].parameters`, and `join_specs`:

```json
{"version": 2, "config": {...}, "data_sources": {...}, "instructions": {...}, "benchmarks": {...}}
```

Omitting `version` (or sending `0`) causes silent failures or API rejection (`ExportConverter supports versions 1 and 2, but got 0`). The API does NOT default the version — set it explicitly.

### Required `serialized_space` Invariants (MANDATORY — validate BEFORE every POST / PATCH)

Genie Space creation silently succeeds but produces a broken room when these invariants are violated. The API's validation surface is narrow — once the space exists, the only way to diagnose is inspecting the UI. Always run the validator below *before* calling `POST /api/2.0/genie/spaces` or `PATCH /api/2.0/genie/spaces/{id}`.

| Field path (inside `serialized_space`) | Required type | Non-negotiable invariants |
|---|---|---|
| `version` | `int` | Must be `1` or `2`; prefer `2`. Missing or `0` is rejected. |
| `config.title` | `str` | Non-empty. Mirrors top-level `title` in the POST envelope. |
| `config.description` | `str` | Non-empty. |
| `config.semantic_warehouse_id` | `str` (16+ hex chars) | Must be the **deploy-time** warehouse id (see Action S10). Never a template placeholder. |
| `data_sources.tables` | `list[object]` | Each entry: `{identifier: "catalog.schema.table", description?: List[str], column_configs?: [...] }`. **NO `id` field** (adding one fails with `Cannot find field: id`). **Sorted by `identifier`**; any `column_configs` sorted by `column_name`. |
| `data_sources.metric_views` | `list[object]` | Each entry: `{identifier: "catalog.schema.mv_name", description?: List[str], column_configs?: [...] }`. **NO `id` field**. Sorted by `identifier`; any `column_configs` sorted by `column_name`. |
| `instructions.general_instructions` | `list[str]` | List of plain strings — no nested objects. |
| `instructions.sql_functions` | `list[object]` | Each: `{id: uuid4.hex, identifier: "catalog.schema.fn_name"}`. No other fields. Max 50 entries. |
| `instructions.example_question_sqls` | `list[object]` | Each: `{id: uuid4.hex, question: List[str], sql: List[str]}` plus optional `parameters: [{name, type_hint, description?: List[str], default_value?}]` and `usage_guidance?: List[str]`. **`question` and `sql` MUST be `List[str]`**, never single strings. |
| `instructions.join_specs` | `list[object]` | (v2) Each: `{id: uuid4.hex, left: {identifier, alias}, right: {identifier, alias}, sql: List[str], comment?: List[str], instruction?: List[str]}`. **`sql` MUST contain exactly two elements**: the backtick-quoted join condition AND a relationship annotation `"--rt=FROM_RELATIONSHIP_TYPE_<CARDINALITY>--"`. Sorted by `id`. |
| `benchmarks.questions` | `list[object]` | Each: `{id: uuid4.hex, question: List[str], answer: [{format: "SQL"\|"INSTRUCTIONS", content: List[str]}]}`. SQL lives inside `answer[].content`, never as a top-level `sql` field. Max 50 entries. |
| Every `id` field | `str` (32 hex chars) | `uuid.uuid4().hex` — lowercase, no dashes. Regenerate on every new deploy (never copy/paste IDs across environments). Time-ordered 32-hex UUIDs also work and self-satisfy sort order. |

**The #1 silent-failure mode observed in production:** `example_question_sqls[].sql`, `example_question_sqls[].question`, or `benchmarks.questions[].answer[].content` submitted as a single string instead of `List[str]`. The API accepts it, but the resulting space has empty/broken example queries because Genie serializes only the first character and then errors internally on render. There is no error surfaced on POST.

#### Validator — `_assert_sql_arrays`

Run this against every `serialized_space` dict BEFORE `json.dumps(...)` and BEFORE the POST/PATCH. Failing loud here saves ~10–15 minutes of UI-round-trip debugging per iteration.

```python
import re
import uuid as _uuid_mod
from typing import Any, List

_UUID_HEX_RE = re.compile(r"^[0-9a-f]{32}$")
_WAREHOUSE_ID_RE = re.compile(r"^[0-9a-f]{16,}$")  # Databricks warehouse ids are hex


def _is_uuid_hex(value: Any) -> bool:
    return isinstance(value, str) and bool(_UUID_HEX_RE.match(value))


def _assert_sql_arrays(space: dict) -> None:
    """
    Validate serialized_space invariants before POST / PATCH.
    Raises RuntimeError on the FIRST violation — never returns False / warns.

    Schema reference: https://docs.databricks.com/aws/en/genie/conversation-api
    Enforces:
      - version is 1 or 2 (prefer 2); missing / 0 is rejected.
      - data_sources.tables / metric_views entries use `identifier` only (NO `id`);
        any column_configs are sorted by `column_name`.
      - instructions.sql_functions entries: {id, identifier} only.
      - instructions.example_question_sqls entries: {id, question: List[str], sql: List[str]}
        (optional `parameters` / `usage_guidance` are allowed).
      - instructions.join_specs[].sql has exactly two elements (condition + --rt=...-- annotation).
      - benchmarks.questions[].answer[].content must be List[str] (SQL lives there,
        not as a top-level `sql` field).
    """
    errors: List[str] = []

    if space.get("version") not in (1, 2):
        errors.append(
            "serialized_space.version must be 1 or 2 (prefer 2); got %r" % space.get("version")
        )

    cfg = space.get("config") or {}
    if not isinstance(cfg.get("title"), str) or not cfg.get("title"):
        errors.append("config.title must be a non-empty string")
    if not isinstance(cfg.get("description"), str) or not cfg.get("description"):
        errors.append("config.description must be a non-empty string")

    wh = cfg.get("semantic_warehouse_id")
    if not isinstance(wh, str) or not _WAREHOUSE_ID_RE.match(wh or ""):
        errors.append(
            "config.semantic_warehouse_id must be a concrete warehouse id baked at deploy time; "
            f"got {wh!r}. Template placeholders like '${{warehouse_id}}' are never acceptable."
        )

    # Data sources — sorted by `identifier`, NEVER include `id` on these entries.
    ds = space.get("data_sources") or {}
    for key in ("tables", "metric_views"):
        items = ds.get(key) or []
        if not isinstance(items, list):
            errors.append(f"data_sources.{key} must be a list")
            continue
        idents = [it.get("identifier", "") for it in items]
        if idents != sorted(idents):
            errors.append(f"data_sources.{key} must be sorted by identifier (got {idents})")
        for it in items:
            if "id" in it:
                errors.append(
                    f"data_sources.{key} entry MUST NOT include `id` — the API rejects with "
                    f"`Cannot find field: id`. Use only `identifier` and optional `description`. Got: {it}"
                )
            ident = it.get("identifier")
            if not isinstance(ident, str) or ident.count(".") != 2:
                errors.append(
                    f"data_sources.{key} entry `identifier` must be 'catalog.schema.name': {it}"
                )
            # column_configs (optional) must be sorted by column_name.
            ccs = it.get("column_configs")
            if ccs is not None:
                if not isinstance(ccs, list):
                    errors.append(f"data_sources.{key} entry `column_configs` must be a list: {it}")
                else:
                    names = [c.get("column_name", "") for c in ccs]
                    if names != sorted(names):
                        errors.append(
                            f"data_sources.{key}[{ident}].column_configs must be sorted by column_name (got {names})"
                        )

    instr = space.get("instructions") or {}

    # instructions.sql_functions — {id, identifier} only.
    sqlfns = instr.get("sql_functions") or []
    if not isinstance(sqlfns, list):
        errors.append("instructions.sql_functions must be a list")
    else:
        for idx, it in enumerate(sqlfns):
            if not isinstance(it, dict):
                errors.append(f"instructions.sql_functions[{idx}] must be an object")
                continue
            if not _is_uuid_hex(it.get("id")):
                errors.append(f"instructions.sql_functions[{idx}].id must be uuid4.hex (32 hex chars)")
            ident = it.get("identifier")
            if not isinstance(ident, str) or ident.count(".") != 2:
                errors.append(
                    f"instructions.sql_functions[{idx}].identifier must be 'catalog.schema.fn_name'"
                )

    # instructions.example_question_sqls — {id, question: List[str], sql: List[str]}.
    eqs = instr.get("example_question_sqls") or []
    if not isinstance(eqs, list):
        errors.append("instructions.example_question_sqls must be a list")
    else:
        for idx, it in enumerate(eqs):
            if not isinstance(it, dict):
                errors.append(f"instructions.example_question_sqls[{idx}] must be an object")
                continue
            if not _is_uuid_hex(it.get("id")):
                errors.append(f"instructions.example_question_sqls[{idx}].id must be uuid4.hex")
            for arr_field in ("question", "sql"):
                arr = it.get(arr_field)
                if not isinstance(arr, list) or not all(isinstance(s, str) and s.strip() for s in arr):
                    errors.append(
                        f"instructions.example_question_sqls[{idx}].{arr_field} must be a non-empty "
                        f"List[str] — single strings cause silent breakage. Wrap as [\"...\"]."
                    )

    # instructions.join_specs (v2) — {id, left, right, sql}. sql MUST be exactly two
    # elements: the join condition AND a "--rt=FROM_RELATIONSHIP_TYPE_<CARDINALITY>--" annotation.
    joins = instr.get("join_specs") or []
    if not isinstance(joins, list):
        errors.append("instructions.join_specs must be a list")
    else:
        join_ids = [j.get("id", "") for j in joins if isinstance(j, dict)]
        if join_ids != sorted(join_ids):
            errors.append(f"instructions.join_specs must be sorted by id (got {join_ids})")
        for idx, it in enumerate(joins):
            if not isinstance(it, dict):
                errors.append(f"instructions.join_specs[{idx}] must be an object")
                continue
            if not _is_uuid_hex(it.get("id")):
                errors.append(f"instructions.join_specs[{idx}].id must be uuid4.hex")
            for side in ("left", "right"):
                node = it.get(side)
                if not isinstance(node, dict) or not isinstance(node.get("identifier"), str):
                    errors.append(f"instructions.join_specs[{idx}].{side} must be {{identifier, alias}}")
            sql = it.get("sql")
            if not isinstance(sql, list) or len(sql) != 2:
                errors.append(
                    f"instructions.join_specs[{idx}].sql must be a 2-element List[str]: "
                    f"[join condition, '--rt=FROM_RELATIONSHIP_TYPE_<CARDINALITY>--']"
                )
            elif not str(sql[1]).startswith("--rt=FROM_RELATIONSHIP_TYPE_"):
                errors.append(
                    f"instructions.join_specs[{idx}].sql[1] must be a relationship annotation "
                    f"'--rt=FROM_RELATIONSHIP_TYPE_<CARDINALITY>--'; omitting it is rejected by the API."
                )

    # benchmarks.questions — SQL lives inside answer[].content, NOT a top-level sql field.
    bench = (space.get("benchmarks") or {}).get("questions") or []
    if not isinstance(bench, list):
        errors.append("benchmarks.questions must be a list")
    else:
        for idx, it in enumerate(bench):
            if not isinstance(it, dict):
                errors.append(f"benchmarks.questions[{idx}] must be an object")
                continue
            if not _is_uuid_hex(it.get("id")):
                errors.append(f"benchmarks.questions[{idx}].id must be uuid4.hex")
            q = it.get("question")
            if not isinstance(q, list) or not all(isinstance(s, str) and s.strip() for s in q):
                errors.append(f"benchmarks.questions[{idx}].question must be List[str]")
            answers = it.get("answer") or []
            if not isinstance(answers, list):
                errors.append(f"benchmarks.questions[{idx}].answer must be a list")
                continue
            for aidx, ans in enumerate(answers):
                if not isinstance(ans, dict):
                    errors.append(f"benchmarks.questions[{idx}].answer[{aidx}] must be an object")
                    continue
                if ans.get("format") not in ("SQL", "INSTRUCTIONS"):
                    errors.append(
                        f"benchmarks.questions[{idx}].answer[{aidx}].format must be 'SQL' or 'INSTRUCTIONS'"
                    )
                content = ans.get("content")
                if not isinstance(content, list) or not all(isinstance(s, str) and s.strip() for s in content):
                    errors.append(
                        f"benchmarks.questions[{idx}].answer[{aidx}].content must be List[str] — "
                        f"this is the #1 silent-failure mode for benchmark answers."
                    )

    # Limits
    if len(sqlfns) > 50:
        errors.append("instructions.sql_functions exceeds 50-entry limit — truncate before POST")
    if len(bench) > 50:
        errors.append("benchmarks.questions exceeds 50-entry limit — truncate before POST")

    gi = instr.get("general_instructions")
    if gi is not None:
        if not isinstance(gi, list) or not all(isinstance(x, str) for x in gi):
            errors.append("instructions.general_instructions must be List[str]")

    if errors:
        joined = "\n  - ".join(errors)
        raise RuntimeError(
            f"serialized_space validation failed — refusing to POST/PATCH:\n  - {joined}"
        )


# Usage:
#   _assert_sql_arrays(space_dict)
#   payload = {"title": ..., "warehouse_id": ..., "serialized_space": json.dumps(space_dict)}
#   ws.api_client.do("POST", "/api/2.0/genie/spaces", body=payload)
```

**Where to wire this in:**
- `scripts/import_genie_space.py` — immediately before `json.dumps(space)` in every path (initial POST and incremental PATCH).
- `assets/templates/deploy_genie_spaces.py` — at the top of each per-space loop iteration.
- Local Phase 0.5 pre-flight (see Action S7 in `00-semantic-layer-setup/SKILL.md`) — enumerated against the rendered config BEFORE `bundle validate`.

### `semantic_warehouse_id` MUST be baked at deploy time (NOT a runtime `--var`)

`serialized_space.config.semantic_warehouse_id` is consumed by the Genie runtime when it renders example queries and routes natural-language questions. The id is **embedded in the POSTed JSON body** — once the space exists, the Genie service does not re-read it from the Asset Bundle.

That means it must be a concrete 16+ character hex warehouse id at the moment `deploy_genie_spaces.py` calls `POST /api/2.0/genie/spaces`. Any of the following produces a broken room:

| Value at POST time | Outcome |
|---|---|
| `abc0123def456789` (real id) | ✅ Space works. |
| `${var.warehouse_id}` (unrendered) | ❌ Space created; every query fails with "warehouse not found". |
| `${warehouse_id}` (shell-style placeholder) | ❌ Same failure mode. |
| Empty string / missing field | ❌ API rejects with `INVALID_PARAMETER_VALUE`. |

**Rule:** Resolve `warehouse_id` at `databricks bundle deploy` time (deploy-time baking — see `skills/databricks-asset-bundles/SKILL.md` §Pitfall: `--var` at run time does NOT override deploy-time-baked values) and pass the resolved value into the notebook task via `base_parameters.warehouse_id`. The `deploy_space` helper in `assets/templates/deploy_genie_spaces.py` stamps this value into `serialized_space.config.semantic_warehouse_id` automatically, so you only need to ensure the value reaching the notebook widget is concrete.

**Validation:** `_assert_sql_arrays` enforces a hex-only `semantic_warehouse_id` on every POST/PATCH. If you see `config.semantic_warehouse_id must be a concrete deploy-time warehouse id` in a pre-flight error, the root cause is always that `warehouse_id` reached the notebook as a template placeholder — fix it in the bundle YAML, not in the Genie config.

**Post-deploy rotation:** If the workspace's semantic warehouse id changes (e.g. migration to serverless), the fix is NOT a runtime override. It's a `bundle deploy` with the new id + a PATCH of every existing space via `deploy_genie_spaces.py` (which will now take the update path because the space ids are persisted per Action S9).

### Core Workflow

**Initial Deployment:**
1. List spaces (check if already exists)
2. Load configuration from JSON file
3. Substitute template variables (`${catalog}`, `${gold_schema}`, etc.)
4. Create space with full configuration
5. Get space to verify deployment

**Incremental Updates:**
1. Get current space configuration (capture its `etag`)
2. Modify specific sections (e.g., add benchmarks)
3. Update space with PATCH (partial update), passing the captured `etag`

> **Optimistic concurrency (`etag`):** The GET response includes an `etag`. Pass it back on the PATCH
> (`update_genie_space(..., etag=...)`) and the update fails safely with `409 Conflict` if the space
> was edited by someone else since your GET — preventing a blind overwrite. Omit `etag` for a
> last-writer-wins update. Re-GET to fetch the new `etag` and retry on conflict.

**Migration/Backup:**
1. Get space with `include_serialized_space=true`
2. Save JSON to version control
3. Create space in new environment (with variable substitution)

## Key Patterns

### 1. JSON Structure Requirements

**CRITICAL:** The `serialized_space` field must be a JSON string (escaped), not a nested object:

```python
payload = {
    "title": "My Space",
    "warehouse_id": "abc123",
    "serialized_space": json.dumps(genie_config)  # ✅ String, not dict
}
```

### Section 4: ID Generation

**All IDs MUST be `uuid.uuid4().hex`** — a 32-character lowercase hex string with no dashes.

```python
import uuid

def generate_id() -> str:
    """Generate a Genie Space compatible ID (32 hex chars, no dashes)."""
    return uuid.uuid4().hex  # e.g., "a1b2c3d4e5f6789012345678abcdef01"
```

**Required ID fields** (every one must be a fresh `uuid.uuid4().hex`).

Use the canonical nested-schema field paths below. Any older guidance that listed flat `space.tables[].id` / `space.materialized_views[].id` / `space.sql_functions[].id` / `space.example_question_sqls[].id` as required was for a deprecated flat schema and is superseded by this list:

- `config.sample_questions[].id`
- `instructions.sql_functions[].id`
- `instructions.text_instructions[].id`
- `instructions.example_question_sqls[].id`
- `instructions.join_specs[].id`
- `instructions.sql_snippets.measures[].id`
- `instructions.sql_snippets.filters[].id`
- `instructions.sql_snippets.expressions[].id`
- `benchmarks.questions[].id`

> **Tip:** `uuid.uuid4().hex` is always valid. The Genie docs also suggest a **time-ordered** 32-hex UUID so IDs sort alphabetically in creation order and self-satisfy the sort requirements below.

**❌ Arrays that MUST NOT have an `id`** (adding one causes `Cannot find field: id in message ...` errors — see Common Errors):

- `data_sources.tables[]` — use only `identifier` and optional `description`
- `data_sources.metric_views[]` — use only `identifier` and optional `description`
- `benchmarks.questions[].answer[]` — use only `format` and `content`

This is the single source of truth for ID placement. The no-id list later in this section and in Section 7 intentionally restates it for retrieval during debugging — keep both lists consistent if editing.

**❌ WRONG IDs (will cause import failures):**
```python
"genie_" + uuid.uuid4().hex[:24]    # ❌ Prefixed, wrong length
"aaaa" * 8                           # ❌ Not random
str(uuid.uuid4())                    # ❌ Contains dashes (36 chars)
hashlib.md5(name.encode()).hexdigest()  # ❌ Deterministic, not UUID4
```

**✅ CORRECT: Always use `uuid.uuid4().hex`** — nothing else.

**Arrays that do NOT have `id` fields — NEVER add one:**
- `data_sources.tables[]` — uses `identifier` only
- `data_sources.metric_views[]` — uses `identifier` only
- `benchmarks.questions[].answer[]` — uses `format` + `content` only

A common agent error is applying `regenerate_ids()` universally across all arrays. The function must SKIP `data_sources.tables` and `data_sources.metric_views`.

### Section 5: Array Format Requirements

**ALL string-content fields in the Genie Space JSON MUST be single-element arrays**, not plain strings.

| Field | ❌ Wrong | ✅ Correct |
|-------|---------|-----------|
| `question` | `"What is revenue?"` | `["What is revenue?"]` |
| `content` (in answer) | `"SELECT ..."` | `["SELECT ..."]` |
| `description` (tables) | `"Orders table"` | `["Orders table"]` |
| `description` (MVs) | `"Revenue metrics"` | `["Revenue metrics"]` |
| `description` (TVFs) | `"Date range query"` | `["Date range query"]` |

**Rule:** If a field contains human-readable text or SQL, wrap it in a single-element array `["value"]`.

**Exception:** `format` in answer objects is a plain string: `"SQL"` or `"INSTRUCTIONS"`.

### 4. Template Variable Substitution

**NEVER hardcode schema paths.** Use template variables:

```json
{
  "data_sources": {
    "tables": [
      {"identifier": "${catalog}.${gold_schema}.dim_store"}  // ✅ Template
    ]
  }
}
```

Substitute at runtime:

```python
def substitute_variables(data: dict, variables: dict) -> dict:
    json_str = json.dumps(data)
    json_str = json_str.replace("${catalog}", variables.get('catalog', ''))
    json_str = json_str.replace("${gold_schema}", variables.get('gold_schema', ''))
    return json.loads(json_str)
```

### 5. Asset Inventory-Driven Generation

**Step 0 — Verify assets exist before referencing them:**

The schema(s) to inspect come from the planning manifest, not a hard-coded `gold_schema`. Production spaces inspect Gold; some manifests also expose `semantic_schema` (Metric Views/TVFs may be deployed there). When a manifest provides `unified_genie_space.assets` or `domains[].genie_spaces[].assets`, treat those identifiers as the **allowlist** — only verify schemas that contain those allowlisted assets.

```sql
-- Run this BEFORE creating or editing any Genie Space JSON.
-- {schema} is one of: ${gold_schema}, ${semantic_schema} (from manifest).
SELECT table_name, table_type
FROM {catalog}.information_schema.tables
WHERE table_schema = '{schema}'
ORDER BY table_type, table_name;

SELECT routine_name
FROM {catalog}.information_schema.routines
WHERE routine_schema = '{schema}';
```

**Only include assets that appear in these results AND are listed in the manifest's `assets` allowlist.** A Genie Space that references a non-existent table fails with `Table '...' does not exist` during space creation. This is the #1 cause of deployment failures. Do NOT trust a pre-generated manifest as ground truth — query the live catalog using the schemas declared by `planning_source` (`gold_schema` for production / Gold-based runs, or `silver_schema` / `bronze_schema` for workshop deployments). The semantic-layer orchestrator only stops before this skill runs when `planning_source.selected_layer = source_csv` (no live tables exist).

**NEVER manually edit `data_sources`.** Generate from verified inventory:

```python
# Load inventory
with open('actual_assets_inventory.json') as f:
    inventory = json.load(f)

# Generate data_sources from inventory
genie_config['data_sources']['tables'] = [
    {"identifier": table_id}
    for table_id in inventory['genie_space_mappings']['cost_intelligence']['tables']
]
```

**Benefits:**
- ✅ Prevents "table doesn't exist" errors
- ✅ Enforces API limits automatically
- ✅ Single source of truth for assets

### 6. Column Configs (optional, richer context)

`column_configs` is a first-class, per-column list on `data_sources.tables[]` and `data_sources.metric_views[]` that gives Genie extra retrieval/formatting hints. Supported per-column fields:

| Field | Purpose |
|-------|---------|
| `column_name` | Target column (required within a config entry). |
| `description` | `List[str]` column description. |
| `synonyms` | `List[str]` alternate names for entity matching. |
| `get_example_values` | Sample distinct values so Genie learns the domain. |
| `build_value_dictionary` | Build a value dictionary for high-cardinality categorical filters. |
| `enable_entity_matching` | Match user-mentioned entities to this column. |
| `enable_format_assistance` | Help Genie format values (dates, regions, etc.). |
| `exclude` | Hide the column from Genie. |

```json
{
  "data_sources": {
    "tables": [
      {
        "identifier": "catalog.schema.orders",
        "column_configs": [
          {"column_name": "order_date", "enable_format_assistance": true},
          {"column_name": "region", "enable_entity_matching": true, "build_value_dictionary": true}
        ]
      }
    ]
  }
}
```

**Rules / trade-offs:**
- `column_configs` entries MUST be **sorted by `column_name`** (the API validates this — see Section 8).
- Richer configs add LLM context but increase the risk of `INTERNAL_ERROR` on very complex spaces. If a large space fails to deploy, drop back to `identifier`-only entries first, then reintroduce column_configs incrementally.

### 7. Field Validation Rules

**config.sample_questions:**
- ✅ Array of objects (not strings)
- ✅ Each object: `{id: string, question: string[]}`
- ❌ NO `name`, `description` fields

**data_sources.metric_views:**
- ✅ `identifier` field (full 3-part UC name)
- ✅ Optional: `description`, `column_configs`
- ❌ NO `id`, `name`, `full_name` fields

**instructions.sql_functions:**
- ✅ `id` field (32 hex chars) - REQUIRED
- ✅ `identifier` field (full 3-part function name) - REQUIRED
- ❌ NO other fields (`name`, `signature`, `description`)

### Section 8: Array Sorting Requirements

**CRITICAL: All arrays in the Genie Space JSON MUST be sorted before any PATCH request.** The Genie API uses protobuf serialization which requires deterministic ordering. Unsorted arrays produce: `Invalid export proto: data_sources.tables must be sorted by identifier`.

**Sort keys by array path:**

| Array Path | Sort Key | Direction |
|------------|----------|-----------|
| `data_sources.tables` | `identifier` | Ascending |
| `data_sources.tables[].column_configs` | `column_name` | Ascending |
| `data_sources.metric_views` | `identifier` | Ascending |
| `data_sources.metric_views[].column_configs` | `column_name` | Ascending |
| `instructions.sql_functions` | `(id, identifier)` | Ascending |
| `instructions.text_instructions` | `id` | Ascending |
| `instructions.example_question_sqls` | `id` | Ascending |
| `instructions.join_specs` | `id` | Ascending |
| `instructions.sql_snippets.measures` | `id` | Ascending |
| `instructions.sql_snippets.filters` | `id` | Ascending |
| `instructions.sql_snippets.expressions` | `id` | Ascending |
| `config.sample_questions` | `id` | Ascending |
| `benchmarks.questions` | `id` | Ascending |

**Implementation — `sort_genie_config()`:**
```python
def sort_genie_config(config: dict) -> dict:
    """Sort all arrays in Genie config — API rejects unsorted data."""
    if "data_sources" in config:
        for key in ["tables", "metric_views"]:
            if key in config["data_sources"]:
                config["data_sources"][key] = sorted(
                    config["data_sources"][key],
                    key=lambda x: x.get("identifier", ""),
                )
                # column_configs (if present) must be sorted by column_name.
                for entry in config["data_sources"][key]:
                    if isinstance(entry.get("column_configs"), list):
                        entry["column_configs"] = sorted(
                            entry["column_configs"],
                            key=lambda c: c.get("column_name", ""),
                        )
    if "instructions" in config:
        if "sql_functions" in config["instructions"]:
            config["instructions"]["sql_functions"] = sorted(
                config["instructions"]["sql_functions"],
                key=lambda x: (x.get("id", ""), x.get("identifier", "")),
            )
        for key in ["text_instructions", "example_question_sqls", "join_specs"]:
            if key in config["instructions"]:
                config["instructions"][key] = sorted(
                    config["instructions"][key],
                    key=lambda x: x.get("id", ""),
                )
        if "sql_snippets" in config["instructions"]:
            for key in ["measures", "filters", "expressions"]:
                if key in config["instructions"]["sql_snippets"]:
                    config["instructions"]["sql_snippets"][key] = sorted(
                        config["instructions"]["sql_snippets"][key],
                        key=lambda x: x.get("id", ""),
                    )
    if "config" in config and "sample_questions" in config["config"]:
        config["config"]["sample_questions"] = sorted(
            config["config"]["sample_questions"],
            key=lambda x: x.get("id", ""),
        )
    if "benchmarks" in config and "questions" in config["benchmarks"]:
        config["benchmarks"]["questions"] = sorted(
            config["benchmarks"]["questions"],
            key=lambda x: x.get("id", ""),
        )
    return config
```

**Always call `sort_genie_config()` BEFORE submitting to the API.** The canonical implementation is documented in Section 8 of this skill.

### Section 9: Idempotent Deployment (Update-or-Create)

To prevent duplicate Genie Spaces on re-deployment, implement an update-or-create pattern:

1. **Store space IDs in `databricks.yml` variables:**
```yaml
variables:
  genie_space_id_<space_name>:
    description: "Existing Genie Space ID (empty for first deployment)"
    default: ""
```

2. **Deployment logic:**
```python
space_id = dbutils.widgets.get("genie_space_id_<space_name>")

if space_id:
    # UPDATE existing space (PATCH without title to avoid " (updated)" suffix)
    payload = {"serialized_space": json.dumps(space_json)}
    # Do NOT include "title" in PATCH to avoid title mutation
    response = requests.patch(f"{base_url}/api/2.0/genie/spaces/{space_id}", ...)
else:
    # CREATE new space
    response = requests.post(f"{base_url}/api/2.0/genie/spaces", ...)
    new_space_id = response.json()["space"]["id"]
    print(f"Created new space: {new_space_id}")
    print(f"Set variable: genie_space_id_<space_name> = {new_space_id}")
```

3. **⚠️ PATCH without title:** Including `title` in a PATCH request causes the API to append " (updated)" to the title. Omit `title` from PATCH payload to preserve the original name.

4. **After first deployment:** Record the returned space IDs and set them as `databricks.yml` variable defaults for subsequent deployments.

## Common Errors & Quick Fixes

| Error | Cause | Quick Fix |
|-------|-------|-----------|
| `BAD_REQUEST: Invalid JSON` | sample_questions as strings | Convert to objects with `id` and `question[]` |
| `BAD_REQUEST: Invalid JSON` | metric_views with `full_name` | Use `identifier` instead |
| `INTERNAL_ERROR: Failed to retrieve schema` | Missing `id` in sql_functions | Add `id` field (32 hex chars) |
| `INVALID_PARAMETER_VALUE: Expected array` | `question` is string | Wrap in array: `["question"]` |
| `Exceeded maximum number (50)` | Too many TVFs/benchmarks | Truncate to 50 in generation script |
| `expected_sql` field not recognized | Used `expected_sql` instead of `answer` | Use `answer: [{format: "SQL", content: ["SELECT ..."]}]` |
| `Invalid export proto: data_sources.tables must be sorted by identifier` | Arrays not sorted — sort key is `identifier` (not `table_name`) for tables/metric_views, `id` for all others | Call `sort_genie_config()` before every PATCH (see Section 8) |
| Invalid ID format | ID is not 32-char hex, contains dashes, or is prefixed | Use `uuid.uuid4().hex` exclusively |
| `Cannot find field: id in message ...MetricView` | Added `id` to `data_sources.metric_views[]` | Remove `id` — use only `identifier` and `description` (see Section 4) |
| `Cannot find field: id in message ...BenchmarkAnswer` | Added `id` to `benchmarks.questions[].answer[]` | Remove `id` — use only `format` and `content` |
| `Invalid export proto: ExportConverter supports versions 1 and 2, but got 0` | Missing top-level `version` field in `serialized_space` | Add `"version": 2` at the root before `json.dumps()` (see "Required Root Field" above) |

See [Troubleshooting Guide](references/troubleshooting.md) for detailed fix scripts.

## Reference Files

- **[API Reference](references/api-reference.md)**: Complete API endpoint documentation, request/response schemas, authentication details, Databricks CLI usage
- **[Workflow Patterns](references/workflow-patterns.md)**: Detailed GenieSpaceExport schema (config, data_sources, instructions, benchmarks), ID generation, serialization patterns, variable substitution, asset inventory-driven generation, complete examples
- **[Troubleshooting](references/troubleshooting.md)**: Common production errors with Python fix scripts, validation checklists, deployment checklist, error recovery patterns, field-level format requirements

## Implementation: Start from Templates (MANDATORY)

**NEVER write deployment notebooks or job YAMLs from scratch.** The templates below handle pre-flight JSON validation, correct ID field scoping, `extract_space_config()` for wrapped/raw formats, array sorting (via the canonical `sort_genie_config()`), and `version: 2` injection. Writing from scratch bypasses these safeguards.

**Step 1 — Copy the notebook template into your project:**

```bash
cp data_product_accelerator/skills/semantic-layer/04-genie-space-export-import-api/assets/templates/deploy_genie_spaces.py \
   src/{project}_semantic/deploy_genie_spaces.py
```

**Step 2 — Copy the job YAML template:**

```bash
cp data_product_accelerator/skills/semantic-layer/04-genie-space-export-import-api/assets/templates/genie-deployment-job-template.yml \
   resources/semantic/genie_deploy_job.yml
```

**Step 3 — Customize:**
- In the notebook: populate `GENIE_SPACE_METADATA` with your `{space_name: genie_space_id_<name>}` mapping
- In the job YAML: update `notebook_path` and `base_parameters` to match your bundle layout

**Available templates:**
- **`assets/templates/deploy_genie_spaces.py`** — Databricks notebook for Asset Bundle `notebook_task` deployment (parameters via `dbutils.widgets.get()`)
- **`assets/templates/genie-deployment-job-template.yml`** — Standalone Asset Bundle job YAML (for combined deployment, the orchestrator provides `semantic-layer-job-template.yml`)

> **CLI vs Notebook:** `scripts/import_genie_space.py` is the CLI tool (`argparse`) for local/CI use. The notebook template (`dbutils.widgets.get()`) is for Asset Bundle `notebook_task` deployment.

## Scripts

- **[export_genie_space.py](scripts/export_genie_space.py)**: Export Genie Space configurations
  ```bash
  python scripts/export_genie_space.py --host <workspace> --token <token> --list
  python scripts/export_genie_space.py --host <workspace> --token <token> --space-id <id> --output space.json
  ```

- **[import_genie_space.py](scripts/import_genie_space.py)**: Create/update Genie Spaces from JSON
  ```bash
  python scripts/import_genie_space.py --host <workspace> --token <token> create \
    --config space.json --title "My Space" --description "..." --warehouse-id <id>
  
  python scripts/import_genie_space.py --host <workspace> --token <token> update \
    --space-id <id> --title "Updated Title"
  ```

## Production Deployment Checklist

1. **Validate JSON Structure**
   ```bash
   python scripts/validate_against_reference.py
   ```

2. **Validate SQL Queries** (if benchmarks present)

   > **Client note:** IDE runs this in a terminal; Genie Code runs the `databricks bundle …` command via `runDatabricksCli` (be on the bundle's page). See `skills/genie-code-environment`.

   ```bash
   databricks bundle run -t dev genie_benchmark_validation_job
   ```

3. **Deploy Genie Spaces**
   ```bash
   databricks bundle deploy -t dev
   databricks bundle run -t dev genie_spaces_deployment_job
   ```

4. **Verify in UI**
   - Navigate to Genie Spaces
   - Test sample questions
   - Verify data sources load correctly

## Related Resources

### Official Documentation
- [Create Space API](https://docs.databricks.com/api/workspace/genie/createspace)
- [Update Space API](https://docs.databricks.com/api/workspace/genie/updatespace)
- [List Spaces API](https://docs.databricks.com/api/workspace/genie/listspaces)
- [Genie Overview](https://docs.databricks.com/genie/)

### Related Skills
- `genie-space-patterns` - UI-based Genie Space setup
- `metric-views-patterns` - Metric view YAML creation
- `databricks-table-valued-functions` - TVF patterns for Genie

## Genie API Notes to Carry Forward

After completing Genie Space API deployment, carry these notes to the next worker:
- **Deployed Space IDs:** Map of space name → space ID (32-char hex) for each deployed space
- **Deployment method:** Whether spaces were created (POST) or updated (PATCH)
- **Variable settings for re-deployment:** `genie_space_id_<name>` values to set in `databricks.yml` for idempotent future deployments
- **Validation results:** Benchmark SQL validation pass/fail counts per space
- **Cross-environment status:** Which environments (dev/staging/prod) have been deployed to

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| GET space without `?include_serialized_space=true` | Response contains only top-level metadata (title, description, space_id); `data_assets`, `general_instructions`, and nested config are omitted — space appears empty | Always append `?include_serialized_space=true` to the Get Space endpoint |
| PATCH `/api/2.0/data-rooms/{id}` with a partial payload | **Silently wipes `serialized_space` to `{}`.** `start-conversation` reports "no tables or functions are available"; downstream agents hit misleading `PERMISSION_DENIED: No access to table X` errors | NEVER PATCH `/api/2.0/data-rooms/{id}`. The only supported mutation surface is `PATCH /api/2.0/genie/spaces/{id}` with a full `{"serialized_space": "<full JSON string>"}` payload. See the anti-pattern block below. |

### ❌ Anti-pattern: `PATCH /api/2.0/data-rooms/{id}` is destructive-by-default

`/api/2.0/data-rooms/{id}` is an **internal** API surface that lives adjacent to the supported `/api/2.0/genie/spaces/{id}` endpoint — similar name, very different semantics. Partial PATCH payloads on `/data-rooms/{id}` (for example, attempting to flip `run_as_type`, `display_name`, or `warehouse_id` in isolation) **silently wipe the space's `serialized_space`**.

Symptoms after the wipe:

- `GET /api/2.0/genie/spaces/{id}?include_serialized_space=true` returns `serialized_space = {}`.
- `databricks genie start-conversation $SPACE_ID --content "..."` returns "no tables or functions are available in this Genie space schema".
- Downstream agents (e.g., endpoints deployed via `agents.deploy()`) return `PERMISSION_DENIED: No access to table X` — even though the SP has all the right UC grants. The error is misleading: the real cause is that the space is empty.

The only supported mutation endpoint is:

```
PATCH /api/2.0/genie/spaces/{id}
Body: {"serialized_space": "<full JSON string>"}
```

To recover from an accidental wipe, use the `restore-genie-space.py` helper in `data_product_accelerator/skills/genai-agents/09-simple-agent-scaffold/references/restore-genie-space.py`. It reads your source-of-truth `genie_configs/*.json`, substitutes template vars (`${catalog}`, `${gold_schema}`, `${semantic_warehouse_id}`), sorts the `tables`/`functions` arrays by identifier (required by the API), and PATCHes the correct endpoint. Cross-reference: `09-simple-agent-scaffold/SKILL.md` "Do NOT PATCH `/api/2.0/data-rooms/{id}` with partial payloads" anti-pattern block.

There is no supported public API for flipping `run_as_type` on an existing space — rebuild the space via the Genie UI or re-run this skill's deploy script.

## Next Step

After API deployment is complete:
- **If this is the first deployment:** Record space IDs and set them as `databricks.yml` variable defaults.
- **If deploying to additional environments:** Re-run the deploy notebook with target environment variables.

## Version History

- **v3.8.0** (Aug 30, 2026) — Reconciled with the Genie Agents API (Conversation API doc updated Aug 27, 2026). Added `instructions.join_specs` (schema row + `_assert_sql_arrays` block requiring the 2-element `sql` with a `--rt=FROM_RELATIONSHIP_TYPE_<CARDINALITY>--` annotation + `sort_genie_config()` sorting by `id`). Added `column_configs` sorting by `column_name` (validator + sort function + Section 8 table) and rewrote Section 6 to document the first-class column-config fields (`get_example_values`, `build_value_dictionary`, `enable_entity_matching`, `enable_format_assistance`, `exclude`, `synonyms`). Documented optional `example_question_sqls[].parameters` / `usage_guidance`. Relaxed the version check to accept v1 or v2 (prefer v2) instead of hard-failing non-2. Added Spaces->Agents terminology note and Agent-mode API pointer. Noted time-ordered UUIDs as a self-sorting ID option.
- **v3.7.0** (Apr 27, 2026) — Reconciled `Required serialized_space Invariants` table and `_assert_sql_arrays` validator with the current `getspace`/`createspace`/`updatespace` API: `data_sources.tables`/`metric_views` use `identifier` only and MUST NOT include `id`; `instructions.sql_functions` is `{id, identifier}` (no `sql` array); SQL for benchmarks lives in `answer[].content: List[str]` (not a top-level `sql` field). Replaced legacy `table_full_name`/`metric_view_full_name`/`sample_queries` references with current schema names. Validator now enforces the post-rename surface.
- **v3.6.0** (Feb 22, 2026) — Fixed Section 8 array sorting: corrected sort keys from `table_name`/`materialized_view_name`/`function_name` to `identifier`/`id` (matching actual API protobuf requirements). Replaced `sort_all_arrays()` with `sort_genie_config()` (canonical implementation in applier). Updated Common Errors with specific error message `Invalid export proto: data_sources.tables must be sorted by identifier`. Added missing arrays (`text_instructions`, `sample_questions`, `benchmarks.questions`) to sort table.
- **v2.0** (Feb 2026) — Array sorting requirements (Section 8); idempotent deployment pattern (Section 9); expanded array format table; strengthened ID generation guidance; 3 new common errors; deploy template major rewrite; benchmark SQL validation templates added; Notes to Carry Forward and Next Step for progressive disclosure
- **v3.0** (January 2026) - Inventory-driven programmatic generation, template variables, 100% deployment success
- **v2.0** (January 2026) - Production deployment patterns, format validation, 8 common error fixes
- **v1.0** (January 2026) - Initial schema documentation and API patterns
