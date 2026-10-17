---
name: data-fixture-auditor
description: "Data fixture auditor: scans test fixture files for coverage gaps, stale data shapes, and missing edge cases. Audits JSON, YAML, and SQL fixtures for cardinality, null ratio, and schema drift. Read-only. Audience: Senior. Trigger: /fixture-audit"
trigger: /fixture-audit
sprint: 83
cluster: data
---

# Data Fixture Auditor

Test fixtures silently rot: happy-path only, stale shapes, zero error-scenario
coverage. This skill scans fixture files, parses entities, measures field coverage,
and generates a quality report.

## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## Usage

```
/fixture-audit <project-directory>
```

Loade das Skill, dann:

```
/fixture-audit $ProjectDir\tests\fixtures\smoke\src
```

## What You Must Do When Invoked

### Step 1

Run `/fixture-audit <project-directory>` against the target project.

### Step 2

Review the fixture quality report for coverage gaps identified by the scan.

### Step 3

Document recommendations to improve fixture coverage.

## Pipeline

1. **Collect** - `fixture-scan.ps1` scannt nach Fixture-Dateien (JSON, YAML, SQL INSERT,
   Factory-Definitions) anhand Namenskonvention (`*fixture*`, `*seed*`, `*test-data*`).
2. **Parse** - Extrahiert Entities und Feldwerte aus jeder Datei.
3. **Measure** - Pro Entity: Cardinality, Konstante-Felder, Null-Ratio, Coverage.
4. **Validate** - Vergleich gegen Companion-Schema (DDL oder JSON Schema).
5. **Report** - `fixture-quality-report.md` mit LLM-bewerteter Coverage-Analyse.

## Quality Dimensions

| Dimension | Bedeutung |
|-----------|-----------|
| Field coverage | Welche Columns sind populated vs. immer null vs. fehlen |
| Cardinality | Verschiedene Werte pro Feld (niedrig = Testlücke) |
| Constant fields | Gleicher Wert in jedem Record |
| Schema drift | Felder im Schema aber nie in Fixtures |

During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).