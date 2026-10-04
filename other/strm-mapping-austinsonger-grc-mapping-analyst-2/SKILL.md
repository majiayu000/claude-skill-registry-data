---
name: strm-mapping
description: Use when asked to map, crosswalk, align, compare, or gap-analyze any two cybersecurity frameworks, control catalogs, or regulatory requirements using NIST IR 8477 Set-Theory Relationship Mapping (STRM). Triggers on terms like "map controls", "crosswalk", "framework alignment", "gap analysis", or producing a STRM CSV output file.
license: Apache-2.0
compatibility: Compatible with any Agent Skills-compatible assistant (Claude Code, OpenAI Codex, Cursor, Gemini CLI, GitHub Copilot, and others). Run your AI assistant from the repository root so relative paths resolve correctly.
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
Start your AI assistant from the repository root so relative paths resolve correctly.

```
working-directory/
```

- Read input files from this directory or from `knowledge/` and `examples/` in the repo root.
- Write all in-progress and output files here.
- Never write output to the repo root or any other location.

---

## Saving Completed Mappings

When a mapping is fully complete, create a dated artifact folder inside:

```
working-directory/mapping-artifacts/
```

### Artifact Folder Naming Convention

```
YYYY-MM-DD_<FocalFramework>-to-<TargetFramework>
```

Use the same short framework names as the CSV file naming convention. Examples:

| Mapping | Folder Name |
|---|---|
| NIST CSF 2.0 → ISO 27001:2022 | `2025-06-01_NIST-CSF-2.0-to-ISO-27001-2022` |
| FFIEC CAT → NIST SP 800-53 | `2025-06-01_FFIEC-CAT-to-NIST-SP-800-53` |
| ISO 27017:2015 → CIS Controls v8 | `2025-06-01_ISO-27017-2015-to-CIS-Controls-v8` |
| CMMC 2.0 → NIST SP 800-171 | `2025-06-01_CMMC-2.0-to-NIST-SP-800-171` |
| PCI DSS v4.0 → SOC 2 TSC | `2025-06-01_PCI-DSS-v4.0-to-SOC2-TSC` |

Use today's date (YYYY-MM-DD) at the time the mapping is completed.

### Artifact Folder Contents

Place the following inside the dated folder:

| File | Description |
|---|---|
| `<csv-filename>.csv` | The completed STRM CSV output (renamed per file naming convention) |
| Any supporting notes or working files | Optional |

---

## Runtime Parameters

Before beginning any work, confirm both parameters with the user if they were not
already specified in the request:

| Parameter | Description | Example |
|---|---|---|
| **Source (Focal) Document** | The framework or catalog being mapped **FROM** | `FFIEC CAT`, `ISO/IEC 27001:2022`, `NIST SP 800-53 Rev 5` |
| **Target (Reference) Document** | The framework or catalog being mapped **TO** | `ISO/IEC 27001:2022`, `CIS Controls v8`, `NIST CSF 2.0` |

> If the user provides only one document, ask which document it should be mapped **to**.
> Either document can be a proprietary catalog, a regulatory framework, an audit
> questionnaire, or any structured list of controls or requirements.

---

## Step-by-Step Workflow

### Scripts to Call (by Step)

| Step | Script to call |
|---|---|
| Step 1 (Gather) | `node scripts/bin/strm-check-existing-mapping.mjs --focal "<Focal>" --target "<Target>" --working-dir working-directory` |
| Step 1 (JSON input) | `node scripts/bin/strm-extract-json.mjs <file.json>` |
| Workflow automation (optional) | `node scripts/bin/strm-run-workflow.mjs --focal "<Focal>" --target "<Target>" --focal-input "<path>" --target-input "<path>" [--manual-qa-done]` |
| Step 3 (Map rows) | `node scripts/bin/strm-map-extracted.mjs --focal "<Focal>" --target "<Target>" --focal-csv "<focal-extracted.csv>" --target-csv "<target-extracted.csv>" --output "<output.csv>" [--top-k 1] [--review-flags]` |
| Step 4 (Write CSV) | `node scripts/bin/strm-init-mapping.mjs --focal "<Focal>" --target "<Target>" --working-dir working-directory` (creates canonical filename + artifact path) |
| Step 5 (Manual QA, required) | `node scripts/bin/strm-init-review-log.mjs --focal "<Focal>" --target "<Target>" --csv "<output.csv>"` (optional scaffold), then review every row and correct relationship/confidence/rationale/notes before validation. |
| Post-completion (required) | `node scripts/bin/strm-validate-csv.mjs --file "<output.csv>"` |
| Post-completion | `node scripts/bin/strm-gap-report.mjs --file "<output.csv>" --focal "<Focal>" --target "<Target>" --working-dir working-directory` — then **expand the gap report** per the Gap Analysis Content Standard below |

### 1. Gather Source Files

Locate and read the relevant input files before generating any output:

```
knowledge/ir8477-strm-reference.md                    ← STRM methodology rules
working-directory/<source-document>.csv/.pdf/.md/.json/.yml/.toml      ← Focal document
working-directory/<target-document>.csv/.pdf/.md/.json/.yml/.toml      ← Reference document
```

Search for input files in this order:
1. `working-directory/` — primary location for user-supplied inputs
2. Project root — for catalog CSVs or PDFs placed there
3. `knowledge/` — for structured control definitions

When an input is JSON and uses HTML-tagged descriptions, run:

```bash
node scripts/bin/strm-extract-json.mjs <input.json> [output.csv]
```

Default output is `working-directory/<framework>-extracted.csv` with columns:
`controlId,title,family,description`.

Write all intermediate files (extracted control lists, partial drafts) to
`working-directory/scratch/`. Do not use system temp directories.

If a prior STRM file already exists for this source→target pair, read it first to
avoid duplicates and maintain consistency.

### 2. Identify the Focal Document Element (FDE) and Reference Document Element (RDE)

- **FDE** = a single control or requirement from the **source** document
- **RDE** = a single control or requirement from the **target** document

Determine for each document:
- Full name and URL (or citation)
- Control ID format (e.g., `D1.G.Ov.B.1`, `A.5.1`, `PR.AC-1`, `AC-2`)
- Maturity or tier structure, if any
- The column or field that contains the control text

### 3. Assign STRM Attributes per Mapping Row

For each FDE → RDE mapping, assign all six STRM attributes:

| Attribute | Allowed Values | Scoring Rule |
|---|---|---|
| `Confidence Levels` | `high`, `medium`, `low` | high = +0, medium = −1, low = −2 |
| `NIST IR-8477 Rational` | `semantic`, `functional`, `syntactic` | syntactic = −1, others = +0 |
| `STRM Relationship` | `equal`, `subset_of`, `superset_of`, `intersects_with`, `not_related` | equal=10, subset/superset=7, intersects=4, not_related=0 |
| `Strength of Relationship` | Integer 1–10 | Base + confidence adj + rationale adj, clamped to [1,10] |
| `STRM Rationale` | Free text | Explain both FDE and RDE, then why the relationship holds |
| `Notes` | Free text | Flag scope differences, partial overlaps, or gaps |

#### Strength Score Calculator

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
| `Confidence Levels` | `high` | `medium` when interpretation or jurisdictional ambiguity exists; `low` when significant inference is required |
| `NIST IR-8477 Rational` | `semantic` | `functional` when controls achieve the same outcome through different mechanisms. When mapping across different regulatory domains (for example healthcare → law enforcement, financial → defense), default to `functional` unless control wording and scope are substantially identical. Use `syntactic` only when word-for-word similarity is the *primary* justification (rare). |

#### Observed Distribution Reference (calibration only)

| Relationship | Approx % |
|---|---|
| `equal` | 43 % |
| `intersects_with` | 39 % |
| `subset_of` | 17 % |
| `superset_of` | 1 % |

| Rationale | Approx % |
|---|---|
| `semantic` | 63 % |
| `functional` | 37 % |
| `syntactic` | < 1 % |

### 4. Write the Output CSV

#### File Naming Convention

```
Set Theory Relationship Mapping (STRM)_ [(<FocalFramework>-to-<BridgeFramework>)-to-<TargetFramework>] - <FocalFramework> to <TargetFramework>.csv
```

- When the focal and bridge frameworks are the same (direct mapping), repeat the focal name in both slots: `(NIST_CSF-to-NIST_CSF)`.
- Substitute actual framework names for `<FocalFramework>`, `<BridgeFramework>`, and `<TargetFramework>`.

Examples:
- `Set Theory Relationship Mapping (STRM)_ [(NIST_CSF_2.0-to-NIST_CSF_2.0)-to-ISO_IEC_27001_2022] - NIST CSF 2.0 to ISO_IEC 27001 2022.csv`
- `Set Theory Relationship Mapping (STRM)_ [(FFIEC-to-FFIEC)-to-NIST_SP_800-53] - FFIEC to NIST SP 800-53.csv`
- `Set Theory Relationship Mapping (STRM)_ [(ISO_IEC_27017_2015-to-ISO_IEC_27001_2022)-to-CIS_Controls_v8] - ISO_IEC 27017 to CIS Controls v8.csv`

#### Required CSV Structure (12 columns)

```
Row 1: FDE#,FDE Name,Focal Document Element (FDE),Confidence Levels,NIST IR-8477 Rational,STRM Rationale,STRM Relationship,Strength of Relationship,<Target> Requirement Title,Target ID #,<Target> Requirement Description,Notes
Row 2+: <data rows>
```

Column definitions:

| Col | Header | Content |
|---|---|---|
| A | `FDE#` | Source control ID |
| B | `FDE Name` | Short human-readable label for the source control |
| C | `Focal Document Element (FDE)` | Full control text or requirement from the source document |
| D | `Confidence Levels` | `high` / `medium` / `low` |
| E | `NIST IR-8477 Rational` | `semantic` / `functional` / `syntactic` |
| F | `STRM Rationale` | Narrative explaining both controls and why the relationship holds |
| G | `STRM Relationship` | `equal` / `subset_of` / `superset_of` / `intersects_with` / `not_related` |
| H | `Strength of Relationship` | Integer 1–10 |
| I | `<Target> Requirement Title` | Target document short title (replace `<Target>` with actual target name) |
| J | `Target ID #` | Target document control ID |
| K | `<Target> Requirement Description` | First sentence of target control text (replace `<Target>` with actual target name) |
| L | `Notes` | Scope differences, gaps, or caveats |

### 5. Rationale Writing Pattern

The `STRM Rationale` field (Column F) must follow this structure:

```
<Source Framework> <FDE#> requires <what the FDE requires>. <Target Framework> <Target ID#> requires <what the target control requires>. Both <shared objective>.
```

Example (FFIEC → NIST SP 800-53):
> FFIEC D3.PC.Am.B.4 requires periodic user access reviews for all systems. NIST SP 800-53 AC-2 requires managing information system accounts including periodic review of account authorizations. Both address periodic access review requirements.

For `intersects_with` mappings, conclude with the divergence:
> Both address <overlap>. <Source Framework> additionally covers <FDE-specific scope>; <Target Framework> additionally covers <RDE-specific scope>.

### 6. Manual Adjudication Pass (Required Before Declaring Done)

Script-generated rows are a starting point only. Before validation and completion:

1. Review every mapping row manually.
2. Confirm `STRM Relationship` is defensible for the pair.
3. Re-check `equal` rows first:
   - If scope/mechanism differs materially, downgrade to `intersects_with` or `subset_of`/`superset_of`.
4. Re-check `intersects_with` rows:
   - If wording and scope are substantially identical, promote to `equal`.
5. Re-check `subset_of`/`superset_of` rows:
   - Verify containment direction is correct.
6. Ensure Notes explain *why* the grading was chosen for that row (no placeholder boilerplate).
7. Recompute strength using the formula after any relationship/confidence/rationale-type changes.
8. Save a manual-review log in the artifact folder:
   - `Manual_Review_<Focal>-to-<Target>.md`
   - Include at minimum: rows reviewed, rows changed, and the list of changed FDE IDs.
   - For every changed row, include a one-line rationale explaining *why* the relationship/confidence/rationale-type was changed.
   - Required per-row log format:
     - `Row <n>: <FDE#> -> <Target ID #> (<old> => <new>) | Reason: <justification>`

---

## Transitivity Rules

When deriving indirect mappings (A→C via A→B and B→C):

| A→B | B→C | Derived A→C |
|---|---|---|
| equal | equal | equal |
| equal | X | X |
| X | equal | X |
| subset_of | subset_of | subset_of |
| superset_of | superset_of | superset_of |
| not_related | anything | not_related |
| anything | not_related | not_related |
| intersects_with | anything | indeterminate |

**Indeterminate** = do not create a derived row; flag for manual review.

---

## Inverse Relationships

When generating reverse mappings (Target → Source):

| Forward | Inverse |
|---|---|
| equal | equal |
| subset_of | superset_of |
| superset_of | subset_of |
| intersects_with | intersects_with |
| not_related | not_related |

---

## Gap Analysis Content Standard

The script `strm-gap-report.mjs` generates a minimal stub. After running it, **always overwrite** the generated file with a fully expanded gap analysis. The expanded report must contain all of the following sections:

### Required Sections

#### 1. Header metadata
```
- Source (Focal): <full framework name>
- Target (Reference): <full framework name>
- Generated: <YYYY-MM-DD>
- Regulations/Controls evaluated: <N>
- Input CSV: <relative path to the STRM CSV>
```

#### 2. Coverage Summary table
A 4-row table with these exact tiers:

| Tier | Count | % | Meaning |
|---|---|---|---|
| ✅ Full Coverage | N | % | Target control fully satisfies the source requirement (`equal` or `subset_of`) |
| 🟡 Partial Coverage | N | % | Some overlap; supplemental controls likely needed (`intersects_with`) |
| 🟠 Source Exceeds Target Scope | N | % | Source requirement is broader; target only partially addresses it (`superset_of`) |
| 🔴 No Coverage | N | % | No meaningful target control found (`not_related`) |

> Replace "Source" and "Target" labels with the actual focal and reference framework names.

#### 3. Relationship Distribution table
Counts and percentages for all five STRM relationship types.

#### 4. Per-tier regulation/control tables

For each of the four tiers, include a table listing every FDE in that tier with:
- FDE ID and title
- Mapped target control ID and title
- STRM relationship
- Strength of Relationship score

For the **No Coverage** tier, add a `Notes` column explaining why no control exists or what kind of supplemental evidence would be needed.

#### 5. Recommended Actions section

Prioritized by tier:
- **Priority 1** — Address No Coverage gaps: list each FDE with a concrete recommended action (new control, policy, or evidence artifact)
- **Priority 2** — Strengthen Partial / Exceeds Scope: list specific FDEs with strength ≤ 4 and suggest supplemental controls or documentation

### Classification Logic

Classify each FDE by its **best** relationship across all its mapped rows:

| Best relationship present | Tier |
|---|---|
| `equal` or `subset_of` | ✅ Full Coverage |
| `intersects_with` (no equal/subset_of) | 🟡 Partial Coverage |
| `superset_of` (no equal/subset_of/intersects_with) | 🟠 Source Exceeds Target Scope |
| only `not_related` | 🔴 No Coverage |

---

## Quality Rules

1. **Never leave Column F (Rationale) empty** — every row needs a narrative.
2. **Strength score must match the formula** — do not guess; compute explicitly.
3. **One FDE can map to multiple target controls** — create one row per target control.
4. **`not_related` rows are rare** — only use when there is genuinely zero overlap.
5. **Do not invent target control IDs** — every `Target ID #` must come from the actual target document provided.
6. **Confidence defaults to `high`** — use `medium` only when interpretation or jurisdictional ambiguity exists; use `low` only when the mapping requires significant inference.
7. **Focus on Baseline maturity first** — when a framework has maturity tiers, prioritize baseline/foundational controls before advanced ones.
8. **Adapt column header labels** — replace `<Target>` in columns I and K with the actual target document name (e.g., `ISO 27001 Requirement Title`, `ISO 27001 Requirement Description`).
9. **Run a relationship distribution self-check after all rows are complete**:
   - If `subset_of + superset_of = 0%`, review `equal` rows; many may actually be `subset_of`.
   - If `equal > 50%`, review each `equal` row and confirm neither control explicitly requires more than the other.
   - If one control says "SHALL" and the other says "SHOULD", this is typically `subset_of`, not `equal`.
10. **Manual QA is mandatory** — never declare completion from script output alone.
11. **Validation and gap report run after manual QA only** — do not run post-completion checks in parallel with row generation.
12. **Gap analysis must be fully expanded** — the stub produced by `strm-gap-report.mjs` is not the final output. Always replace it with the full expanded report per the Gap Analysis Content Standard above, including per-regulation tables for all four coverage tiers and a Recommended Actions section.

---

## Optional: Risk and Threat-Enriched Mappings

> **These inputs are ONLY used when the user explicitly requests risk or threat data.**
> Do not load, reference, or incorporate these files in any standard framework-to-framework
> or control-to-control mapping unless the user specifically asks for it.

### When to Activate

Activate this section only when the user says something like:
- "include risk data", "add threat context", "risk-to-control mapping"
- "threat-to-risk", "threat-to-control", "comprehensive mapping with risks/threats"
- "use the risk library", "use the threat library"

### Source Files

| File | Contents |
|---|---|
| `knowledge/library/risks.json` | SCF 2025.4 risk catalog — `risk_id`, `title`, `description`, `likelihood`, `impact`, `mapped_controls`, `set_theory_relationships`, `threat_ids` |
| `knowledge/library/threats.json` | Threat catalog — `threat_id`, `threat_grouping`, `title`, `description`, `mapped_risk_ids` |

### Relationship Chain

```
Threat → Risk → Control
```

- Each risk (`risk_id`) links to controls via `mapped_controls` and to threats via `threat_ids`
- Each threat (`threat_id`) links to risks via `mapped_risk_ids`
- Risks already carry embedded STRM `set_theory_relationships` — use these when available

### Specialized Mapping Types

#### Risk-to-Control

Use when the user wants to map risks from the library to framework controls.

- **FDE** = risk entry from `risks.json` (`risk_id` as FDE#, `title` as FDE Name, `description` as FDE text)
- **RDE** = target framework control
- Use the embedded `set_theory_relationships[].relation` and `confidence_alignment` from the risk record as starting points; override with independent analysis if needed
- Include `likelihood` and `impact` scores in the Notes column

#### Threat-to-Risk

Use when the user wants to map threats to risks.

- **FDE** = threat entry from `threats.json` (`threat_id` as FDE#, `title` as FDE Name, `description` as FDE text)
- **RDE** = risk entry from `risks.json`
- Derive the STRM relationship from the threat's materiality and the risk's scope
- Note `threat_grouping` (Natural, Manmade, Technical) in the Notes column

#### Threat-to-Control

Use when the user wants to map threats directly to framework controls (skipping the intermediate risk layer).

- **FDE** = threat entry from `threats.json`
- **RDE** = target framework control
- Traverse `threat → risk → control` chain to derive the relationship
- Apply transitivity rules — if any intermediate relationship is `intersects_with`, mark derived as indeterminate and flag for review

### Output Naming for Risk/Threat Mappings

Follow the same artifact folder convention but reflect the mapping type:

| Mapping Type | Folder Name Example |
|---|---|
| Risk-to-Control | `2025-06-01_SCF-Risks-to-NIST-SP-800-53` |
| Threat-to-Risk | `2025-06-01_SCF-Threats-to-SCF-Risks` |
| Threat-to-Control | `2025-06-01_SCF-Threats-to-CIS-Controls-v8` |

### Quality Rules (Risk/Threat specific)

- **Never auto-include** risk or threat files — wait for explicit user request
- **Respect embedded STRM data** in `risks.json` — do not contradict without justification
- **Flag unmapped threats** (`mapped_risk_ids: []`) in Notes — they require manual risk derivation
- **Materiality fields** in threats (`pre_tax_income_5_percent`, etc.) are informational — include relevant values in Notes if present

---

## Existing Mappings in This Repository

Before starting a new mapping, search for existing files to avoid duplication.
Run a glob across the project root and `working-directory/` for any CSV whose name
contains `Set Theory Relationship Mapping` or `STRM`. The file name pattern
encodes both source and target, so it is the fastest way to check for prior work.

---

## Template Reference

A blank STRM template lives at:

```
TEMPLATE_Set Theory Relationship Mapping (STRM).csv
```

Copy (do not modify) that file as the starting point, then rename the copy
according to the file naming convention above.

---

## Related Resources

| Resource | Purpose |
|---|---|
| `TEMPLATE_Set Theory Relationship Mapping (STRM).csv` | Blank STRM template to copy for new mappings |
| `knowledge/ir8477-strm-reference.md` | Full NIST IR 8477 methodology reference |
| `examples/example-control-to-control.md` | ISO 27001 → SOC 2 worked example |
| `examples/example-control-to-evidence.md` | Control-to-evidence mapping example |
| `examples/example-framework-to-control.md` | Framework-to-control mapping example |
| `examples/example-framework-to-policy.md` | Framework-to-policy mapping example |
| `examples/example-framework-to-regulation.md` | Framework-to-regulation mapping example |
| `examples/example-framework-to-risk.md` | Framework-to-risk mapping example |
| `examples/example-regulation-to-control.md` | Regulation-to-control mapping example |
| `knowledge/controls.schema.json` | JSON Schema for control data |
| `knowledge/mappings.schema.json` | JSON Schema for mapping data validation |
| `knowledge/risks.schema.json` | JSON Schema for risk data validation |
| `knowledge/threats.schema.json` | JSON Schema for threat data validation |
| `knowledge/library/risks.json` | SCF 2025.4 risk catalog (optional — explicit request only) |
| `knowledge/library/threats.json` | Threat catalog (optional — explicit request only) |
