---
name: strm-mapping
description: Use when asked to map, crosswalk, align, compare, or gap-analyze any two cybersecurity frameworks, control catalogs, or regulatory requirements using NIST IR 8477 Set-Theory Relationship Mapping (STRM). Triggers on terms like "map controls", "crosswalk", "framework alignment", "gap analysis", or producing a STRM CSV output file.
license: Apache-2.0
compatibility: Designed for Qoder. Also compatible with any Agent Skills-compatible assistant. Run Qoder from the repository root so relative paths resolve correctly.
metadata:
  author: austinsonger
  version: "2.0.0"
  methodology: NIST IR 8477
  standard: agentskills.io
---

# NIST IR 8477 STRM Mapping — GRC Toolkit Skill

## When to Activate

Activate this skill whenever the user asks to:

- Map, crosswalk, align, or compare any two frameworks, catalogs, or control sets
- Create a STRM CSV output file between any two documents
- Perform a gap analysis between any source and target document
- Extend or verify an existing STRM mapping file

---

## Working Directory

All work **must** be performed inside the `working-directory/` folder at the repository root.
Open Qoder from the repository root so relative paths resolve correctly.

- Read input files from `working-directory/`, `knowledge/`, or `examples/`
- Write all in-progress and output files to `working-directory/`
- Never write output to the repo root or any other location

---

## Saving Completed Mappings

When a mapping is fully complete, create a dated artifact folder:

```
working-directory/mapping-artifacts/YYYY-MM-DD_<FocalFramework>-to-<TargetFramework>/
```

Place the completed CSV inside the dated folder.

---

## Runtime Parameters

Before beginning any work, confirm both parameters with the user:

| Parameter | Description | Example |
|---|---|---|
| **Source (Focal) Document** | The framework being mapped FROM | `FFIEC CAT`, `ISO/IEC 27001:2022` |
| **Target (Reference) Document** | The framework being mapped TO | `CIS Controls v8`, `NIST CSF 2.0` |

---

## Step-by-Step Workflow

### Scripts to Call (by Step)

| Step | Script to call |
|---|---|
| Step 1 (Gather) | `node scripts/bin/strm-check-existing-mapping.mjs --focal "<Focal>" --target "<Target>" --working-dir working-directory` |
| Step 1 (JSON input) | `node scripts/bin/strm-extract-json.mjs <file.json>` |
| Step 4 (Write CSV) | `node scripts/bin/strm-init-mapping.mjs --focal "<Focal>" --target "<Target>" --working-dir working-directory`, then `node scripts/bin/strm-generate-filename.mjs --focal "<Focal>" --target "<Target>" [--bridge "<Bridge>"]` |
| Post-completion (required) | `node scripts/bin/strm-validate-csv.mjs --file "<output.csv>"` |
| Post-completion | `node scripts/bin/strm-gap-report.mjs --file "<output.csv>" --focal "<Focal>" --target "<Target>" --working-dir working-directory` |

### 1. Gather Source Files

Read before generating output:

```
knowledge/ir8477-strm-reference.md                                 ← STRM methodology rules
working-directory/<source-document>.csv/.pdf/.md/.json/.yml/.toml  ← Focal document
working-directory/<target-document>.csv/.pdf/.md/.json/.yml/.toml  ← Reference document
```

Search order: `working-directory/` → repo root → `knowledge/`

When an input is JSON and uses HTML-tagged descriptions, run:

```bash
node scripts/bin/strm-extract-json.mjs <input.json> [output.csv]
```

Default output is `working-directory/<framework>-extracted.csv` with columns:
`controlId,title,family,description`.

Write all intermediate files (extracted control lists, partial drafts) to
`working-directory/scratch/`. Do not use system temp directories.

Check for an existing STRM file for this source→target pair before starting.

### 2. Identify FDE and RDE

- **FDE** (Focal Document Element) = one control from the **source** document
- **RDE** (Reference Document Element) = one control from the **target** document

For each document: record full name, URL/citation, control ID format.

### 3. Assign STRM Attributes per Mapping Row

| Attribute | Allowed Values | Scoring Rule |
|---|---|---|
| `Confidence Levels` | `high`, `medium`, `low` | high=+0, medium=−1, low=−2 |
| `NIST IR-8477 Rational` | `semantic`, `functional`, `syntactic` | syntactic=−1, others=+0 |
| `STRM Relationship` | `equal`, `subset_of`, `superset_of`, `intersects_with`, `not_related` | equal=10, subset/superset=7, intersects=4, not_related=0 |
| `Strength of Relationship` | Integer 1–10 | base + confidence adj + rationale adj, clamped to [1,10] |
| `STRM Rationale` | Free text | Explain both FDE and RDE, then why the relationship holds |
| `Notes` | Free text | Flag scope differences, partial overlaps, or gaps |

#### Strength Score Formula

```
strength = base_score + confidence_adj + rationale_adj
base_score  : equal=10  subset_of=7  superset_of=7  intersects_with=4  not_related=0
confidence  : high=0    medium=-1    low=-2
rationale   : syntactic=-1   semantic=0   functional=0
result      : clamp(strength, 1, 10)
```

#### Calibration Defaults

| Attribute | Default | Override Condition |
|---|---|---|
| `Confidence Levels` | `high` | `medium` for ambiguity; `low` for significant inference |
| `NIST IR-8477 Rational` | `semantic` | `functional` for same outcome via different mechanisms. When mapping across different regulatory domains (for example healthcare → law enforcement, financial → defense), default to `functional` unless control wording and scope are substantially identical. Use `syntactic` only for word-for-word similarity (<1%). |

### 4. Write the Output CSV

#### File Naming Convention

```
Set Theory Relationship Mapping (STRM)_ [(<Focal>-to-<Bridge>)-to-<Target>] - <Focal> to <Target>.csv
```

For direct mappings, repeat the focal name as bridge.

#### CSV Structure

Copy `TEMPLATE_Set Theory Relationship Mapping (STRM).csv` and add data from Row 2:

```
Row 1: FDE#,FDE Name,Focal Document Element (FDE),Confidence Levels,NIST IR-8477 Rational,STRM Rationale,STRM Relationship,Strength of Relationship,<Target> Requirement Title,Target ID #,<Target> Requirement Description,Notes
Row 2+: <data rows>
```

Column definitions:

| Col | Header | Content |
|---|---|---|
| A | `FDE#` | Source control ID |
| B | `FDE Name` | Short label for the source control |
| C | `Focal Document Element (FDE)` | Full source control text |
| D | `Confidence Levels` | `high` / `medium` / `low` |
| E | `NIST IR-8477 Rational` | `semantic` / `functional` / `syntactic` |
| F | `STRM Rationale` | Narrative explaining both controls and the relationship |
| G | `STRM Relationship` | `equal` / `subset_of` / `superset_of` / `intersects_with` / `not_related` |
| H | `Strength of Relationship` | Integer 1–10 (computed) |
| I | `<Target> Requirement Title` | Target document short title (replace `<Target>` with actual target name) |
| J | `Target ID #` | Target control ID |
| K | `<Target> Requirement Description` | First sentence of target control text (replace `<Target>` with actual target name) |
| L | `Notes` | Scope differences, gaps, or caveats |

### 5. Rationale Writing Pattern

```
<Source> <FDE#> requires <what FDE requires>. <Target> <Target ID#> requires <what RDE requires>. Both <shared objective>.
```

For `intersects_with`: append "Both address <overlap>. <Source> additionally covers <A>; <Target> additionally covers <B>."

---

## Transitivity Rules

| A→B | B→C | Derived A→C |
|---|---|---|
| equal | equal | equal |
| equal | X | X |
| X | equal | X |
| subset_of | subset_of | subset_of |
| superset_of | superset_of | superset_of |
| not_related | anything | not_related |
| intersects_with | anything | indeterminate — flag for manual review |

---

## Inverse Relationships

| Forward | Inverse |
|---|---|
| equal | equal |
| subset_of | superset_of |
| superset_of | subset_of |
| intersects_with | intersects_with |
| not_related | not_related |

---

## Quality Rules

1. **Never leave Rationale (Column F) empty** — every row needs a narrative.
2. **Strength score must match the formula** — compute explicitly, do not guess.
3. **One FDE can map to multiple target controls** — one row per target control.
4. **`not_related` is rare** — only when there is genuinely zero overlap.
5. **Do not invent target control IDs** — every Target ID# must come from the actual target document.
6. **Confidence defaults to `high`** — lower only when ambiguity or inference is required.
7. **Focus on Baseline maturity first** — prioritize baseline/foundational controls.
8. **Adapt column header labels** — replace `<Target>` in columns I and K with the actual target document name (e.g., `ISO 27001 Requirement Title`, `ISO 27001 Requirement Description`).
9. **Run a relationship distribution self-check after all rows are complete**:
   - If `subset_of + superset_of = 0%`, review `equal` rows; many may actually be `subset_of`.
   - If `equal > 50%`, review each `equal` row and confirm neither control explicitly requires more than the other.
   - If one control says "SHALL" and the other says "SHOULD", this is typically `subset_of`, not `equal`.

---

## Optional: Risk and Threat-Enriched Mappings

Load these files **only** when explicitly requested by the user:

| File | Contents |
|---|---|
| `knowledge/library/risks.json` | SCF 2025.4 risk catalog |
| `knowledge/library/threats.json` | Threat catalog |

Trigger phrases: "include risk data", "add threat context", "risk-to-control mapping",
"threat-to-control", "use the risk library".

Chain: **Threat → Risk → Control** — apply transitivity rules when traversing.

---

## Key Resources

| Resource | Purpose |
|---|---|
| `TEMPLATE_Set Theory Relationship Mapping (STRM).csv` | Blank template — copy, never modify |
| `knowledge/ir8477-strm-reference.md` | Full NIST IR 8477 methodology |
| `examples/` | Worked examples for each mapping type |
| `knowledge/library/risks.json` | Risk catalog (opt-in only) |
| `knowledge/library/threats.json` | Threat catalog (opt-in only) |
