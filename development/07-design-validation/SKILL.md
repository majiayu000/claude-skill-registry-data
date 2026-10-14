---
name: 07-design-validation
description: Cross-validation of Gold layer design artifacts during the design phase. Use when validating that YAML schemas, ERDs, lineage CSVs, and PK/FK references are internally consistent before handing off to implementation. Catches design-time inconsistencies (e.g., column in ERD but not in YAML, FK referencing non-existent table) that would otherwise surface as runtime bugs.
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: bundle_deploy
deploy_note: "Design-phase pattern; output feeds the Gold design/setup artifacts deployed downstream via `bundle deploy --target dev`. No standalone resource."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "1.0.0"
  domain: gold
  role: worker
  pipeline_stage: 1
  pipeline_stage_name: gold-design
  called_by:
    - gold-layer-design
  standalone: true
  last_verified: "2026-04-17"
  volatility: low
  upstream_sources: []
---

# Design Consistency Validation

## Overview

Gold layer design produces multiple interconnected artifacts — YAML schemas, Mermaid ERDs, column lineage CSVs, and PK/FK constraint definitions. These artifacts are created across different phases and can drift out of sync. This skill provides **cross-validation patterns to catch inconsistencies during the design phase**, before they propagate into implementation bugs.

**Key Principle:** Catch design inconsistencies early. A column missing from a YAML schema but present in an ERD is cheap to fix in design; it's a `UNRESOLVED_COLUMN` runtime error in implementation.

**Companion skill:** For runtime DataFrame-vs-DDL schema validation during implementation, see `pipeline-workers/05-schema-validation/SKILL.md`.

## When to Use This Skill

- Completing Phase 8 (Design Validation) of the Gold Layer Design workflow
- Cross-checking YAML schemas against ERD diagrams
- Validating that all YAML columns have lineage metadata
- Ensuring PK/FK references point to valid tables and columns
- Running pre-handoff validation before implementation begins

## Core Problem: Design Artifact Drift

Gold layer design involves multiple interconnected artifacts:

| Artifact | Location | Contains |
|----------|----------|----------|
| **YAML Schemas** | `gold_layer_design/yaml/{domain}/` | Column names, types, PKs, FKs, descriptions |
| **ERD Diagrams** | `gold_layer_design/erd_master.md` | Entity names, column names, relationships |
| **Lineage CSV** | `gold_layer_design/COLUMN_LINEAGE.csv` | Source → target column mappings |
| **Source Mapping** | `gold_layer_design/SOURCE_TABLE_MAPPING.csv` | Table-level source → Gold mapping |

**Problem:** These are authored at different phases (ERD at Phase 3, YAML at Phase 4, Lineage at Phase 5). Changes in one may not be reflected in others.

## Validation 1: YAML ↔ ERD Consistency

### What to Check

Every column in the ERD must exist in the corresponding YAML schema, and vice versa.

### Validation Pattern

```python
import yaml
import re
from pathlib import Path

def validate_yaml_erd_consistency(yaml_dir: Path, erd_path: Path) -> dict:
    """Cross-check YAML schemas against ERD diagram."""
    
    # Parse YAML schemas
    yaml_tables = {}
    for yaml_file in yaml_dir.rglob("*.yaml"):
        with open(yaml_file) as f:
            spec = yaml.safe_load(f)
        table_name = spec.get("table_name", yaml_file.stem)
        yaml_tables[table_name] = {
            col["name"] for col in spec.get("columns", [])
        }
    
    # Parse ERD (extract entity names and columns from Mermaid syntax)
    erd_tables = {}
    with open(erd_path) as f:
        erd_content = f.read()
    
    # Match Mermaid ERD entity blocks: table_name { ... }
    entity_pattern = re.compile(
        r'(\w+)\s*\{([^}]*)\}', re.MULTILINE | re.DOTALL
    )
    for match in entity_pattern.finditer(erd_content):
        table_name = match.group(1)
        columns_block = match.group(2)
        columns = set()
        for line in columns_block.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('%%'):
                parts = line.split()
                if len(parts) >= 2:
                    columns.add(parts[1])  # type column_name
        erd_tables[table_name] = columns
    
    # Cross-check
    issues = []
    
    # Tables in YAML but not in ERD
    for table in yaml_tables:
        if table not in erd_tables:
            issues.append(f"YAML table '{table}' missing from ERD")
    
    # Tables in ERD but not in YAML
    for table in erd_tables:
        if table not in yaml_tables:
            issues.append(f"ERD table '{table}' missing from YAML")
    
    # Column-level comparison for common tables
    for table in set(yaml_tables) & set(erd_tables):
        yaml_cols = yaml_tables[table]
        erd_cols = erd_tables[table]
        
        for col in yaml_cols - erd_cols:
            issues.append(f"YAML column '{table}.{col}' missing from ERD")
        for col in erd_cols - yaml_cols:
            issues.append(f"ERD column '{table}.{col}' missing from YAML")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "yaml_table_count": len(yaml_tables),
        "erd_table_count": len(erd_tables)
    }
```

### Common Mismatches

| Mismatch | Cause | Fix |
|----------|-------|-----|
| Column in ERD, missing in YAML | ERD updated after YAML was generated | Add column to YAML schema |
| Column in YAML, missing in ERD | YAML updated without ERD refresh | Add column to ERD or regenerate ERD |
| Table name differs | Rename in one artifact but not the other | Align names across all artifacts |

## Validation 2: YAML ↔ Lineage CSV Consistency

### What to Check

Every Gold column in the YAML must have a corresponding entry in `COLUMN_LINEAGE.csv`.

### Validation Pattern

```python
import csv

def validate_yaml_lineage_consistency(yaml_dir: Path, lineage_csv_path: Path) -> dict:
    """Cross-check YAML columns against lineage CSV entries."""
    
    # Parse YAML schemas
    yaml_columns = set()
    for yaml_file in yaml_dir.rglob("*.yaml"):
        with open(yaml_file) as f:
            spec = yaml.safe_load(f)
        table_name = spec.get("table_name", yaml_file.stem)
        for col in spec.get("columns", []):
            yaml_columns.add(f"{table_name}.{col['name']}")
    
    # Parse lineage CSV
    lineage_columns = set()
    with open(lineage_csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            gold_table = row.get("gold_table", "")
            gold_column = row.get("gold_column", "")
            if gold_table and gold_column:
                lineage_columns.add(f"{gold_table}.{gold_column}")
    
    # Cross-check
    missing_lineage = yaml_columns - lineage_columns
    extra_lineage = lineage_columns - yaml_columns
    
    return {
        "valid": len(missing_lineage) == 0,
        "missing_lineage": sorted(missing_lineage),
        "extra_lineage": sorted(extra_lineage),
        "yaml_column_count": len(yaml_columns),
        "lineage_column_count": len(lineage_columns)
    }
```

### Why This Matters

Columns without lineage entries become implementation ambiguity — the merge script author won't know where the data comes from, leading to guesses and bugs. **33% of implementation bugs** trace back to incomplete lineage documentation.

## Validation 3: PK/FK Reference Consistency

### What to Check

Every FOREIGN KEY in a YAML schema must reference a valid PRIMARY KEY column in the referenced table's YAML schema.

### Validation Pattern

```python
def validate_pk_fk_consistency(yaml_dir: Path) -> dict:
    """Validate PK/FK references across all YAML schemas."""
    
    # Parse all YAML schemas
    tables = {}
    for yaml_file in yaml_dir.rglob("*.yaml"):
        with open(yaml_file) as f:
            spec = yaml.safe_load(f)
        table_name = spec.get("table_name", yaml_file.stem)
        
        pk_columns = []
        if "primary_key" in spec:
            pk_columns = spec["primary_key"].get("columns", [])
        
        fk_constraints = spec.get("foreign_keys", [])
        
        tables[table_name] = {
            "pk_columns": set(pk_columns),
            "fk_constraints": fk_constraints,
            "all_columns": {col["name"] for col in spec.get("columns", [])}
        }
    
    issues = []
    
    for table_name, info in tables.items():
        for fk in info["fk_constraints"]:
            ref_table = fk.get("references_table", "")
            ref_column = fk.get("references_column", "")
            fk_column = fk.get("column", "")
            
            # Check FK column exists in this table
            if fk_column not in info["all_columns"]:
                issues.append(
                    f"FK column '{table_name}.{fk_column}' not found in table columns"
                )
            
            # Check referenced table exists
            if ref_table not in tables:
                issues.append(
                    f"FK in '{table_name}' references non-existent table '{ref_table}'"
                )
                continue
            
            # Check referenced column is a PK in the target table
            if ref_column not in tables[ref_table]["pk_columns"]:
                issues.append(
                    f"FK '{table_name}.{fk_column}' → '{ref_table}.{ref_column}' "
                    f"but '{ref_column}' is not a PK in '{ref_table}'"
                )
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "table_count": len(tables),
        "total_fk_count": sum(len(t["fk_constraints"]) for t in tables.values())
    }
```

### Common FK Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| FK references non-existent table | Table renamed or not yet designed | Add missing table or fix reference |
| FK column not a PK in target | Wrong column referenced | Update FK to reference correct PK |
| FK column missing from source table | Column removed during design iteration | Add column back or remove FK |

## Validation 4: YAML Mandatory Fields

### What to Check

Every YAML schema must include the non-negotiable defaults from the design orchestrator.

### Validation Pattern

```python
def validate_yaml_mandatory_fields(yaml_dir: Path) -> dict:
    """Validate all YAML schemas include mandatory fields."""
    
    MANDATORY_TABLE_PROPERTIES = {
        "delta.enableChangeDataFeed": "true",
        "delta.enableRowTracking": "true",
        "delta.autoOptimize.optimizeWrite": "true",
        "delta.autoOptimize.autoCompact": "true",
        "layer": "gold"
    }
    
    issues = []
    
    for yaml_file in yaml_dir.rglob("*.yaml"):
        with open(yaml_file) as f:
            spec = yaml.safe_load(f)
        table_name = spec.get("table_name", yaml_file.stem)
        
        # Check clustering
        if spec.get("clustering") != "auto":
            issues.append(f"{table_name}: missing 'clustering: auto'")
        
        # Check table properties
        props = spec.get("table_properties", {})
        for prop, expected_value in MANDATORY_TABLE_PROPERTIES.items():
            if props.get(prop) != expected_value:
                issues.append(
                    f"{table_name}: missing or wrong table property "
                    f"'{prop}' (expected '{expected_value}', "
                    f"got '{props.get(prop, 'MISSING')}')"
                )
        
        # Check PK columns are NOT NULL
        pk_columns = set()
        if "primary_key" in spec:
            pk_columns = set(spec["primary_key"].get("columns", []))
        
        for col in spec.get("columns", []):
            if col["name"] in pk_columns and col.get("nullable", True):
                issues.append(
                    f"{table_name}.{col['name']}: PK column is nullable "
                    f"(must be 'nullable: false')"
                )
    
    return {
        "valid": len(issues) == 0,
        "issues": issues
    }
```

## Validation 5: Cross-Worker Semantic Rule Compliance

### What to Check

Structural validations 1-4 only confirm that fields exist and references resolve. They pass even when the design has used the wrong transformation type, paraphrased the FK shape, left `true`/`false` in business dimensions, or forgot an unknown-member row. Validation 5 closes this gap by enforcing the semantic rules shared across the design-worker skills.

### Rule Table

| # | Rule | Authoritative source | How to detect a violation |
|---|------|---------------------|---------------------------|
| 1 | No `BOOLEAN` columns in business-sourced dimensions | `design-workers/02-dimension-patterns` Rule 3 | `col.type == "BOOLEAN"` in any `dim_*.yaml` except `dim_date` / `dim_time` whitelist |
| 2 | Every dimension referenced by a `nullable: true` FK declares `unknown_member:` | `references/yaml-schema-patterns.md` Unknown Member section | Scan fact YAMLs for `nullable: true` FKs, then check target dim has an `unknown_member` block |
| 3 | Every `lineage.transformation` value is in the 15-item enum | `00-gold-layer-design/SKILL.md` Phase 4 | `transformation not in STANDARD_TRANSFORMATIONS` |
| 4 | Every `foreign_keys:` entry uses `{columns, references, nullable}` shape | `DESIGN_DECISIONS.md` FK contract | Missing any of the three keys, or extra keys |
| 5 | No literal `[`, `]`, `<`, or `>` characters inside `description:` strings | `common/naming-tagging-standards` description pattern | `re.search(r"[\[\]<>]", description)` matches |
| 6 | Mandatory top-level YAML keys present (`table_name`, `domain`, `description`, `table_properties`, `clustering`, `columns`, `primary_key`) | `DESIGN_DECISIONS.md` top-level key contract | Any mandatory key missing |
| 7 | Fact measures declare `additivity: additive | semi_additive | non_additive` | `design-workers/03-fact-patterns` | `measures` entry missing `additivity` |

### Validation Pattern

```python
import re
import yaml
from pathlib import Path

# Authoritative constants (copy-paste into the validation subagent)
STANDARD_TRANSFORMATIONS = {
    "DIRECT_COPY", "RENAME", "CAST",
    "AGGREGATE_SUM", "AGGREGATE_SUM_CONDITIONAL",
    "AGGREGATE_COUNT", "AGGREGATE_AVG",
    "DERIVED_CALCULATION", "DERIVED_CONDITIONAL",
    "HASH_MD5", "HASH_SHA256",
    "COALESCE", "DATE_TRUNC", "GENERATED", "LOOKUP",
}

MANDATORY_FK_KEYS = {"columns", "references", "nullable"}

# Description must NOT contain placeholder-bracket characters as literals
DESC_FORBIDDEN_CHARS = re.compile(r"[\[\]<>]")

BOOLEAN_DIM_WHITELIST = {"dim_date", "dim_time"}


def validate_semantic_rules(yaml_dir: Path) -> dict:
    """Cross-worker semantic rule compliance (Validation 5)."""
    issues = []
    dim_unknown_members = {}  # dim_name -> bool (has unknown_member?)
    fact_nullable_fks = []    # list of (fact_name, target_dim)

    # Pass 1: scan every YAML
    for yaml_file in yaml_dir.rglob("*.yaml"):
        with open(yaml_file) as f:
            spec = yaml.safe_load(f)
        table_name = spec.get("table_name", yaml_file.stem)
        is_dim = table_name.startswith("dim_")
        is_fact = table_name.startswith("fact_")

        # Rule 6: top-level key presence
        for key in ("table_name", "domain", "description", "table_properties", "clustering", "columns", "primary_key"):
            if key not in spec:
                issues.append(f"{table_name}: missing mandatory top-level key '{key}'")

        # Rule 1: no BOOLEAN in business dims
        if is_dim and table_name not in BOOLEAN_DIM_WHITELIST:
            for col in spec.get("columns", []):
                if col.get("type") == "BOOLEAN":
                    issues.append(
                        f"{table_name}.{col['name']}: BOOLEAN not allowed in business dimension "
                        f"(convert to STRING per 02-dimension-patterns Rule 3)"
                    )

        # Rule 2 prep: track unknown_member presence
        if is_dim:
            dim_unknown_members[table_name] = "unknown_member" in spec

        # Rule 4: FK shape
        for fk in spec.get("foreign_keys", []):
            keys = set(fk.keys())
            missing = MANDATORY_FK_KEYS - keys
            if missing:
                issues.append(
                    f"{table_name}: foreign_keys entry missing keys {sorted(missing)} "
                    f"(got {sorted(keys)})"
                )
            if is_fact and fk.get("nullable") is True:
                # Resolve target dim name from 'references: dim_X(col)'
                ref = fk.get("references", "")
                target = ref.split("(")[0].strip()
                if target:
                    fact_nullable_fks.append((table_name, target))

        # Rules 3 and 5 per column
        for col in spec.get("columns", []):
            desc = col.get("description", "")
            if DESC_FORBIDDEN_CHARS.search(desc):
                issues.append(
                    f"{table_name}.{col['name']}: description contains literal bracket/angle char "
                    f"(placeholders are not literal per naming-tagging-standards)"
                )
            lineage = col.get("lineage") or {}
            tfm = lineage.get("transformation")
            if tfm and tfm not in STANDARD_TRANSFORMATIONS:
                issues.append(
                    f"{table_name}.{col['name']}: transformation '{tfm}' not in 15-type enum "
                    f"(see 00-gold-layer-design Phase 4 edge-case mapping)"
                )

        # Rule 7: fact measures must declare additivity
        if is_fact:
            for m in spec.get("measures", []):
                if "additivity" not in m:
                    issues.append(
                        f"{table_name}: measure '{m.get('name', '?')}' missing 'additivity' "
                        f"(additive | semi_additive | non_additive)"
                    )

    # Rule 2 resolve: every dim referenced by nullable FK must have unknown_member
    for fact_name, target_dim in fact_nullable_fks:
        if target_dim in dim_unknown_members and not dim_unknown_members[target_dim]:
            issues.append(
                f"{target_dim}: referenced by {fact_name} with nullable: true FK, "
                f"but dimension does not declare 'unknown_member:' block"
            )

    return {"valid": len(issues) == 0, "issues": issues}
```

### Wiring Into the Full Workflow

Add Validation 5 alongside the existing four in `run_design_validation`:

```python
# Validation 5: Cross-Worker Semantic Rule Compliance
results["semantic_rules"] = validate_semantic_rules(yaml_dir)
```

## Validation 6: Industry Data Model Alignment (ADVISORY)

### What to Check

Benchmark the Gold design against a **Databricks Industry Vibe Data Model** (or any canonical industry reference) for **entity coverage, terminology, and sensitivity alignment**. Unlike Validations 1–5 — self-referential consistency checks that MUST pass — Validation 6 is **advisory**: it produces a coverage scorecard and gap list but NEVER flips the overall `all_valid` result.

**Read first:** `design-workers/08-industry-alignment/references/industry-data-model-alignment.md` — the Silver-vs-Gold nuance, the manifest, the crosswalk states, and the scoring rubric. This is semantic coverage, NOT structural equivalence.

### Single Source of Matching

Matching is owned by `design-workers/08-industry-alignment` (Phase 0/2), which writes `gold_layer_design/INDUSTRY_CROSSWALK.csv`. Validation 6 **loads** that crosswalk — it does NOT re-match — then verifies it against the current YAML and scores it. This avoids two divergent matchers.

### Preconditions

- If `INDUSTRY_CROSSWALK.csv` is absent, `industry_reference_source: none` (or the worker was skipped). Record "Industry alignment: N/A" and return `{"valid": True, "applicable": False}` — never a failure.

### Rule Table

| # | Rule | Severity | How detected |
|---|------|----------|--------------|
| 1 | Every `core` reference entity is `Covered`, `Absorbed`, `Waived`, or `Planned` | advisory-high | Crosswalk row in `Gap` state with `importance: core` |
| 2 | `Covered`/`Absorbed` `gold_tables` still exist in the current YAML | advisory-high | Named Gold table not found among YAML `table_name`s (drift after Phase 2) |
| 3 | Every `PII` entity's covering Gold table carries a `PII` tag | advisory-med | Covering table missing `table_properties.PII` |
| 4 | Every `Waived`/`Planned`/`Gap` row has a rationale | advisory-low | Empty `rationale` cell |

### Validation Pattern

```python
import csv
import yaml
from pathlib import Path

# Reuse the authoritative constants from the worker's overlay script.
IMPORTANCE_WEIGHT = {"core": 3, "extended": 2, "optional": 1}


def _load_gold_tables(yaml_dir: Path) -> dict:
    tables = {}
    for yaml_file in yaml_dir.rglob("*.yaml"):
        with open(yaml_file) as f:
            spec = yaml.safe_load(f) or {}
        name = spec.get("table_name", yaml_file.stem)
        props = spec.get("table_properties", {}) or {}
        tables[name] = {"has_pii": str(props.get("PII", "")).lower() in {"true", "yes", "pii"}}
    return tables


def validate_industry_alignment(yaml_dir: Path, crosswalk_csv: Path) -> dict:
    """Validation 6 — advisory. Loads the worker's crosswalk, verifies it against the
    current YAML, and scores coverage / terminology / PII. `valid` is always True."""
    if not crosswalk_csv or not Path(crosswalk_csv).exists():
        return {"valid": True, "applicable": False,
                "note": "INDUSTRY_CROSSWALK.csv absent — industry alignment N/A."}

    gold = _load_gold_tables(yaml_dir)
    rows = list(csv.DictReader(open(crosswalk_csv)))
    issues = []
    covered_w = applicable_w = 0
    pii_hits = pii_total = 0

    for r in rows:
        state = r["state"].strip()
        importance = r.get("importance", "optional").strip()
        weight = IMPORTANCE_WEIGHT.get(importance, 1)
        gold_tables = [t for t in (r.get("gold_tables", "") or "").split("|") if t]
        sensitive = r.get("sensitivity", "none").strip().upper() == "PII"

        # Scoring: Waived/Planned removed from denominator (not penalized)
        if state not in {"Waived", "Planned"}:
            applicable_w += weight
            if state in {"Covered", "Absorbed"}:
                covered_w += weight

        # Rule 1: unresolved core gaps
        if state == "Gap" and importance in {"core", "extended"}:
            issues.append(f"[gap] {importance} entity '{r['entity']}' not covered/waived/planned")

        # Rule 2: crosswalk drift vs current YAML
        for t in gold_tables:
            if t not in gold:
                issues.append(f"[drift] '{r['entity']}' maps to '{t}' which is not in the current YAML")

        # Rule 3: PII alignment
        if sensitive and state in {"Covered", "Absorbed"}:
            pii_total += 1
            if any(gold.get(t, {}).get("has_pii") for t in gold_tables):
                pii_hits += 1
            else:
                issues.append(f"[pii] '{r['entity']}' is PII but covering table(s) {gold_tables} lack a PII tag")

        # Rule 4: rationale required for non-modeled states
        if state in {"Waived", "Planned", "Gap"} and not (r.get("rationale", "") or "").strip():
            issues.append(f"[rationale] '{r['entity']}' is {state} but has no rationale")

    def pct(a, b):
        return round(100 * a / b) if b else 100

    return {
        "valid": True,              # advisory — never blocks
        "applicable": True,
        "scorecard": {
            "entity_coverage_pct": pct(covered_w, applicable_w),
            "pii_alignment_pct": pct(pii_hits, pii_total),
        },
        "issues": issues,
    }
```

### Emit the Report

From the returned dict, emit `gold_layer_design/INDUSTRY_ALIGNMENT.md` using the report template in `08-industry-alignment/references/industry-data-model-alignment.md`. Record the scorecard line in the validation report; if `applicable` is False, print "Industry alignment: N/A (no reference model provided)".

### Why Advisory, Not a Gate

The reference is external, volatile, and models a *different layer* (Silver business model vs. Gold dimensional). A hard gate would produce false failures whenever the customer's legitimate scope differs from the industry archetype — contradicting Vibe's own "shaped entirely by YOUR context" philosophy. The value is a documented coverage %, a gap list for Phase 9 stakeholder review, and a terminology/PII sanity check — not a pass/fail wall.

## Complete Design Validation Workflow

Run all validations as a comprehensive pre-handoff check (Validations 1–5 are must-pass; Validation 6 is advisory and excluded from `all_valid`):

```python
def run_design_validation(project_dir: Path) -> dict:
    """Run complete design consistency validation suite."""
    yaml_dir = project_dir / "gold_layer_design" / "yaml"
    erd_path = project_dir / "gold_layer_design" / "erd_master.md"
    lineage_csv = project_dir / "gold_layer_design" / "COLUMN_LINEAGE.csv"
    
    results = {}
    
    # Validation 1: YAML ↔ ERD
    if erd_path.exists():
        results["yaml_erd"] = validate_yaml_erd_consistency(yaml_dir, erd_path)
    else:
        results["yaml_erd"] = {"valid": False, "issues": ["ERD file not found"]}
    
    # Validation 2: YAML ↔ Lineage
    if lineage_csv.exists():
        results["yaml_lineage"] = validate_yaml_lineage_consistency(yaml_dir, lineage_csv)
    else:
        results["yaml_lineage"] = {"valid": False, "issues": ["Lineage CSV not found"]}
    
    # Validation 3: PK/FK References
    results["pk_fk"] = validate_pk_fk_consistency(yaml_dir)
    
    # Validation 4: Mandatory Fields
    results["mandatory_fields"] = validate_yaml_mandatory_fields(yaml_dir)

    # Validation 5: Cross-Worker Semantic Rule Compliance
    results["semantic_rules"] = validate_semantic_rules(yaml_dir)

    # Validation 6: Industry Data Model Alignment (ADVISORY — excluded from all_valid)
    crosswalk_csv = project_dir / "gold_layer_design" / "INDUSTRY_CROSSWALK.csv"
    results["industry_alignment"] = validate_industry_alignment(yaml_dir, crosswalk_csv)

    # Summary — compute all_valid over the MUST-PASS checks only (1–5); Validation 6 is advisory
    must_pass = {k: v for k, v in results.items() if k != "industry_alignment"}
    all_valid = all(r.get("valid", False) for r in must_pass.values())
    total_issues = sum(len(r.get("issues", [])) for r in results.values())
    
    print(f"\n{'='*60}")
    print(f"Design Consistency Validation Report")
    print(f"{'='*60}")
    for name, result in results.items():
        status = "✅ PASS" if result.get("valid") else "❌ FAIL"
        issue_count = len(result.get("issues", []))
        print(f"  {name}: {status} ({issue_count} issues)")
        for issue in result.get("issues", [])[:5]:
            print(f"    - {issue}")
        if issue_count > 5:
            print(f"    ... and {issue_count - 5} more")
    print(f"\nOverall: {'✅ ALL PASS' if all_valid else '❌ ISSUES FOUND'}")
    print(f"Total issues: {total_issues}")
    
    return {"all_valid": all_valid, "total_issues": total_issues, "details": results}
```

## Validation Checklist (Design Phase)

Before handing off to implementation:

- [ ] **YAML ↔ ERD:** All tables and columns match between YAML schemas and ERD diagrams
- [ ] **YAML ↔ Lineage:** Every YAML column has a lineage entry in `COLUMN_LINEAGE.csv`
- [ ] **PK/FK References:** All FK constraints reference valid PKs in target tables
- [ ] **Mandatory Fields:** All YAML schemas include `clustering: auto`, CDF, row tracking, auto-optimize, layer tag
- [ ] **PK NOT NULL:** All PRIMARY KEY columns have `nullable: false`
- [ ] **Grain Documented:** All fact tables have explicit `grain` and `grain_type` in YAML
- [ ] **Semantic rule compliance:** Transformation enum, FK format, description format, booleans, unknown_member — all pass (Validation 5)
- [ ] **Industry alignment (advisory):** If a reference model was provided, `INDUSTRY_ALIGNMENT.md` emitted with a coverage scorecard; unresolved core/extended gaps reviewed (Validation 6 — never blocks handoff)

## Reference Files

- **[Design Validation Patterns](references/design-validation-patterns.md)** — Extended validation examples and edge cases

## Related Skills

- **Merge Schema Validation (Implementation):** `pipeline-workers/05-schema-validation/SKILL.md` — Runtime DataFrame-vs-DDL validation
- **YAML-Driven Gold Setup:** `pipeline-workers/01-yaml-table-setup/SKILL.md` — YAML schema structure and format
- **Mermaid ERD Patterns:** `design-workers/05-erd-diagrams/SKILL.md` — ERD syntax and organization

## References

- [AgentSkills.io Specification](https://agentskills.io/specification)

## Inputs

- **From `06-table-documentation`:** Complete YAML schema files with descriptions, TBLPROPERTIES, and lineage metadata
- **From `05-erd-diagrams`:** ERD diagrams (master, domain, summary) with all tables and relationships
- **From orchestrator Phase 5:** COLUMN_LINEAGE.csv with Bronze → Silver → Gold mappings

## Outputs

- Validation report (pass/fail per category: YAML↔ERD, YAML↔Lineage, PK/FK, mandatory fields)
- List of inconsistencies to fix before implementation handoff
- Completed design sign-off checklist

## Design Notes to Carry Forward

After completing this skill, note:
- [ ] All validation checks passed (or list any known exceptions with justification)
- [ ] Design is ready for implementation handoff to `01-gold-layer-setup`
- [ ] Any deferred items flagged for future iteration

## Next Step

Design phase is complete. Return to the orchestrator (`00-gold-layer-design`) for Phase 9 (Stakeholder Review), then proceed to implementation via `gold/01-gold-layer-setup/SKILL.md`.

---

**Pattern Origin:** Phase 8 of Gold Layer Design workflow, implicit validation patterns made explicit
**Key Lesson:** Design artifacts drift across phases. Cross-validate before implementation.
**Impact:** Prevents 33% of implementation bugs caused by incomplete lineage and design inconsistencies
