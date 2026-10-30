---
name: architecture-traceability
description: Use this skill for requirements deviation checks, requirements traceability, and PO Spec coverage analysis. Compares PO Spec use cases against architecture documentation to detect coverage gaps. Generates a markdown traceability report (TRACEABILITY_REPORT.md) showing Covered, Partial, or Not Covered status per requirement. Invoke when checking for requirements deviations, running a requirements coverage check, verifying PO Spec coverage, generating a traceability matrix, or checking if architecture covers all business requirements.
triggers:
  - traceability
  - traceability report
  - traceability matrix
  - requirements deviation
  - requirements deviation check
  - requirements coverage
  - requirements coverage check
  - PO spec coverage
  - PO spec deviation
  - PO spec vs architecture
  - check PO spec
  - check requirements coverage
  - coverage matrix
  - requirements traceability
---

# Architecture Traceability Skill

## Purpose

This skill compares **PO Spec use cases** against **architecture documentation** to produce a portable markdown traceability report. It answers: "Did the architecture team cover everything the PO asked for?"

**Output**: `TRACEABILITY_REPORT.md` at the project root — a markdown file designed for tickets, emails, Confluence, GitHub issues, and external platforms.

This skill ships in the **sa-analysis** plugin (`sa-skills` depends on it and installs it). `[plugin_dir]` is sa-analysis'
install: `bun ~/.claude/plugins/marketplaces/shadowx4fox-solution-architect-marketplace/scripts/plugin-root.ts --plugin sa-analysis`.
The script reads the architecture through sa-skills' explorer, judge and PO Spec parser and finds sa-skills on its own
(`--sa-skills <dir>`, `SA_SKILLS_DIR`, the repo layout, the install registry).

---

## Documentation Language

Resolve the project's documentation language **before writing anything**, using the protocol in
`skills/architecture-docs/references/LANGUAGE_POLICY.md` §3:

```bash
rg -m1 '<!-- DOC_LANGUAGE:' ARCHITECTURE.md || rg -m1 '<!-- LANGUAGE:' ARCHITECTURE.md
```

`DOC_LANGUAGE` → use it. Legacy `LANGUAGE` → use it and rewrite the marker as `DOC_LANGUAGE`.
Neither → infer from headings (§5.5), ask the user to confirm **once**, stamp `DOC_LANGUAGE` into
`ARCHITECTURE.md`, and never infer again. Messages this skill displays to the user stay English
in every case; only authored file content follows `doc_language`.

**In this skill**: `TRACEABILITY_REPORT.md` headings, narrative and gap descriptions are authored in `doc_language`. The coverage status values `Covered` / `Partial` / `Not Covered`, the use-case identifiers (`UC1`, `UC2`, …), requirement ids, the report filename and the matrix column headers stay English — downstream consumers match them literally.

Structural headings this skill writes carry their English anchor comment in both languages
(`## Heading <!-- SECTION: English Name -->`). The full do-not-localize registry — codes, status
enum values, table column headers, filenames, marker names, `EXPLORER_HEADER` field keys — is
`LANGUAGE_POLICY.md` §4.

---

## When to Invoke This Skill

- User asks to "check requirements coverage", "verify traceability", or "check PO spec coverage"
- User asks for a "requirements deviation check" or "requirements traceability"
- User asks if the architecture covers all business requirements
- User wants to detect requirements deviations or PO Spec deviations
- User needs a traceability matrix or coverage report
- User uses `/skill architecture-traceability`

**Do NOT invoke for:**
- Creating or editing the PO Spec → use `architecture-readiness` skill
- Creating or editing ARCHITECTURE.md → use `architecture-docs` skill
- Compliance contract generation → use `architecture-compliance` skill

---

## Files in This Skill

| File | Purpose |
|------|---------|
| `SKILL.md` | This file — entry point and workflow |
| `scripts/traceability-prepare.js` | **Steps 3–6 as code** (2026-09-21): `bun [plugin_dir]/skills/architecture-traceability/scripts/traceability-prepare.js <project_root> [--spec PRODUCT_OWNER_SPEC.md] [--judge agent\|typesafe\|claude] [--out TRACEABILITY_REPORT.md] [--json] [--dry-run]` parses the use cases and their fields (either language), yields the requirements by the Step 3 table, cuts the evidence per requirement with the explorer over the whole surface (never an EXPLORER_HEADER; the Step 4 routing table weights the file), and classifies each one with the plugin's judge (`scripts/judge.js`): one Score whose three levels are Covered / Partial / Not Covered, plus one yes/no per flow step for "pure UI navigation" (not traced). A requirement the judge has not scored (the default `agent` engine's worksheet still pending, an engine error, an unanswered item) is **❔ Undecided** — never classified by term overlap — and listed under *Undecided (not judged)* with the worksheet to answer and re-run; an unanswered flow step stays traced; `--judge typesafe` (or `SA_JUDGE`) asks Jev, ~5 s for 120 requirements. The report is Step 6's format with the largest-remainder percentages; a Partial's *gap* text is `[NOT DOCUMENTED …]` — the script never composes it, the session states it after reading the evidence. `--json` prints every requirement with its candidates, score, confidence and evidence for the session to refine. On the reference (2026-09-21, architecture 7.0.0) Jev classified 72 / 47 / 1 of 120 where the 2026-09-08 in-session run had 91 / 14 / 10 of 115 against architecture 2.1.0: the judge reads six excerpts per requirement, the session read the documents — the excerpts are what to improve, and every row prints them. Warns when `adr/.institutional-catalog.json` names an edition other than `DOC_LANGUAGE` — evidence in another language than the requirement is the state the judge separates worst on |

---

## Workflow

### Step 1 — Locate PO Spec File

Search for the Product Owner Specification:

```
Search order:
1. PRODUCT_OWNER_SPEC.md at project root
2. PO_SPEC.md at project root
3. Glob **/PRODUCT_OWNER_SPEC.md, **/PO_SPEC.md
4. Glob **/po-spec*, **/product-owner*
5. Ask user for path
```

If no PO Spec found, abort with: *"No Product Owner Specification found. Use `/skill architecture-readiness` to create one first."*

---

### Step 2 — Locate Architecture Documentation

Search for `ARCHITECTURE.md` at the project root. Detect multi-file vs monolithic structure.

Build the `arch_files` list:
- `ARCHITECTURE.md` (navigation index or monolithic)
- `docs/01-system-overview.md` (S1+S2)
- `docs/03-architecture-layers.md` (S4)
- `docs/components/*.md` or `docs/components/*/*.md` (S5)
- `docs/04-data-flow-patterns.md` (S6)
- `docs/05-integration-points.md` (S7)
- `docs/06-technology-stack.md` (S8)
- `docs/07-security-architecture.md` (S9)
- `docs/08-scalability-and-performance.md` (S10)
- `docs/09-operational-considerations.md` (S11)

Only include files that exist. If no `ARCHITECTURE.md` found, abort with: *"No ARCHITECTURE.md found. Use `/skill architecture-docs` to create one first."*

**Also extract the Architecture Version** from `ARCHITECTURE.md`:
- Look for `<!-- ARCHITECTURE_VERSION: X.Y.Z -->` comment at the top of the file
- If present, use that value for the report header
- If absent (architecture predates versioning), use literal `unversioned`

---

### Step 3 — Parse Use Cases from PO Spec

Read the PO Spec file. Locate the Use Cases section by searching for heading patterns:
- `## N. Use Cases` (e.g., `## 4. Use Cases`, `## 3. Use Cases`)
- `## Use Cases`

For each use case found (identified by `### UC-NNN:`, `### N.N UC-NNN:`, `### Use Case N:`, or `### N.N` sub-headings), extract:

| Field | Pattern | Required |
|-------|---------|----------|
| `id` | Parse from heading (e.g., `UC-01`) or generate sequentially | Yes |
| `name` | Text after the colon in the heading | Yes |
| `actor` | `**Actor:**` or `**Actors:**` field | No |
| `description` | `**Description:**` field or first paragraph after heading | No |
| `primaryFlow` | `**Primary Flow:**` numbered steps | No |
| `alternativeFlows` | `**Alternative Flows:**` sub-items | No |
| `edgeCases` | `**Edge Cases:**` items | No |
| `preconditions` | `**Preconditions:**` items | No |
| `postconditions` | `**Postconditions:**` items | No |
| `successMetrics` | `**Success Metrics:**` items | No |

**Phase detection**: Search the PO Spec for phase references:
- Look for `**Phase N:**` sections in Section 8 (Next Steps / Roadmap)
- Cross-reference use case names or keywords with phase deliverables
- If no phase structure found, all UCs default to `Phase 1`

**Requirement extraction**: Each use case yields N traceable requirements:

| Requirement Source | What becomes a requirement |
|--------------------|---------------------------|
| Primary Flow | Each step that implies system behavior (skip pure UI navigation) |
| Alternative Flows | Each alternative scenario |
| Edge Cases | Each edge case with its handling |
| Preconditions | Authentication, role, or system state requirements |
| Postconditions | System state changes that must be supported |
| Success Metrics | Performance, quality, or UX targets |

For **simplified PO Specs** (bullet-point format without formal UC structure), each bullet under the Use Cases section becomes one requirement.

**Extraction filter — strip "how" from PO Spec requirements**: When the PO Spec mentions specific technologies, integration paths, or implementation details (e.g., "integrate with Push Notification Gateway via FCM"), extract only the business capability ("push notification delivery with status tracking") as the traceable requirement. The architecture team decides the "how" — the traceability check validates the "what."

---

### Step 4 — Search Architecture Docs for Coverage

For each requirement from Step 3, search the architecture files for coverage evidence. Map requirement types to architecture sections:

| Requirement Type | Primary Search Targets |
|-----------------|----------------------|
| Functional behavior (flow steps) | S1+S2 (`docs/01-system-overview.md`), S5 (`docs/components/*.md`) |
| Data operations (CRUD, storage) | S6 (`docs/04-data-flow-patterns.md`), S5 |
| External integrations | S7 (`docs/05-integration-points.md`) |
| Authentication / authorization | S9 (`docs/07-security-architecture.md`) |
| Performance / latency targets | S10 (`docs/08-scalability-and-performance.md`) |
| Error handling / edge cases | S5, S11 (`docs/09-operational-considerations.md`) |
| Monitoring / operations | S11 (`docs/09-operational-considerations.md`) |

**Coverage classification**:

- **✅ Covered**: Architecture docs explicitly address this requirement. Evidence includes section reference + brief quote (max 100 chars).
- **⚠️ Partial**: Architecture docs mention related concepts but don't fully address the requirement. Evidence shows what's present; gap describes what's missing.
- **❌ Not Covered**: No evidence found in any architecture doc. Suggest which architecture section should document this.

**Important**: Coverage matching is **semantic, not lexical**. The PO Spec may say "User configures schedule" while the architecture says "Cron-based scheduling." Use architectural understanding to determine coverage — rg is a locating hint, classification is judgment.

**PO Spec Scope Rule — "What" vs "How"**:

The PO Spec defines **what** the business needs (capabilities, outcomes, constraints). It does **not** define **how** the architecture implements those needs (technology choices, integration paths, component decomposition). When evaluating coverage:

- **Evaluate the business capability**, not the implementation path. If the PO Spec says "Push Notification Gateway integration" but the architecture delegates push delivery to a different component that achieves the same outcome, the requirement is **✅ Covered** — the business need (push notifications) is satisfied.
- **Never flag a gap** because the architecture uses a different integration path, technology, or component structure than the PO Spec imagined. The PO owns the "what"; the architecture team owns the "how."
- **Do flag a gap** when the business capability itself is missing — e.g., the PO Spec requires push notifications but no component in the architecture handles push delivery at all.
- When the architecture satisfies the requirement through a different path than the PO Spec expected, note this in the evidence column: `"Covered via [component/path] (differs from PO Spec's expected [path])"`

---

### Step 5 — Compute Summary Statistics

Before generating the report, compute:
- Total requirements count (all UCs combined)
- Covered / Partial / Not Covered counts and percentages
- Per-use-case coverage percentages
- Per-phase coverage breakdown — the phase is the use case's **delivery increment** when `docs/01` declares Delivery Increments (8.143.0: `Increment N · <target>` in the table's order, `Not assigned` for a use case no increment carries; `Incremento` / `Sin asignar` under `es`), read from the facts ledger by the script; otherwise `Phase 1`

**Percentage rounding rule (largest-remainder / Hamilton method)** — apply to any table where multiple integer percentages must sum to 100% (e.g., the global Summary table's Covered / Partial / Not Covered rows, or any per-UC / per-phase / per-source breakdown rendered as integer percents):

1. Compute each row's exact percentage `pᵢ = 100 × countᵢ / total`.
2. Floor each: `fᵢ = floor(pᵢ)`. Track each remainder `rᵢ = pᵢ − fᵢ`.
3. Compute deficit `D = 100 − Σ fᵢ` (an integer in `0..N`, where `N` is the number of rows).
4. Sort rows by `rᵢ` descending; add `+1` to the top `D` rows.
5. Tie-break (`rᵢ` equal): larger `countᵢ` first, then row order in the table (Covered → Partial → Not Covered).
6. Before writing, verify `Covered + Partial + NotCovered == Total` in every breakdown; a count mismatch is a classification bug, never something to fix by forcing percentages. Never ship a table whose integer-% rows sum to 99% or 101%.

For **single-value cells** (per-phase `Coverage` column, per-UC `N/N (X%)` cell, any standalone percentage), use plain `round()` — there is no sum constraint.

**Per-UC / per-phase integer-% breakdowns** — if the report decomposes a single UC, phase, or source into integer percentages across Covered / Partial / Not Covered (e.g., `UC-03 — 73% / 18% / 9%`), apply the largest-remainder rule **per row**, not just to the global Summary. Each such row is its own 100%-budget.

---

### Step 6 — Generate Markdown Report

Write `TRACEABILITY_REPORT.md` at the project root using this format:

```markdown
# PO Spec Use Cases vs Architecture Coverage

**PO Spec**: [filename]
**Architecture**: ARCHITECTURE.md
**Architecture Version**: [ARCHITECTURE_VERSION from `<!-- ARCHITECTURE_VERSION: -->` comment, or "unversioned"]
**Date**: YYYY-MM-DD

## Summary

| Metric | Count | % |
|--------|-------|---|
| Total Requirements | N | — |
| ✅ Covered | N | N% |
| ⚠️ Partial | N | N% |
| ❌ Not Covered | N | N% |

### Coverage by Phase

| Phase | Requirements | Covered | Partial | Gaps | Coverage |
|-------|-------------|---------|---------|------|----------|
| Phase 1 | N | N | N | N | N% |
| Phase 2 | N | N | N | N | N% |

---

## UC-01: [Name] — [Phase]

**Actor**: [actor]
**Coverage**: N/N requirements (N%)

| PO Spec Requirement | Architecture Coverage | Status |
|---------------------|----------------------|--------|
| [requirement text] | [evidence: section + quote] | ✅ Covered |
| [requirement text] | [evidence] | ⚠️ Partial |
| [requirement text] | — | ❌ Not Covered |

(repeat for each use case)

---

## Gap Report

Requirements that need architecture documentation attention:

### ❌ Not Covered

| UC | Requirement | Source | Suggested Section |
|----|-------------|--------|-------------------|
| [UC-id] | [text] | [Primary Flow / Alt Flow / Edge Case / etc.] | [S-number (section name)] |

### ⚠️ Partial

| UC | Requirement | Evidence | Gap |
|----|-------------|----------|-----|
| [UC-id] | [text] | [what's documented] | [what's missing] |
```

**Overwrite policy**: `TRACEABILITY_REPORT.md` is regenerated fresh on each run (not date-stamped).

---

### Step 7 — Report to User

Show summary to the user:

```
Traceability report generated.

PO Spec: [filename] → Architecture: ARCHITECTURE.md v[ARCHITECTURE_VERSION]
Coverage: N% (N/N requirements covered)
  ✅ N covered · ⚠️ N partial · ❌ N gaps

Report: TRACEABILITY_REPORT.md

Copy the Gap Report section to address coverage gaps using /skill architecture-docs.
```

---

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `architecture-readiness` | Prerequisite: PO Spec must exist. If not found, direct user to create one. |
| `architecture-docs` | Prerequisite: ARCHITECTURE.md + docs/ must exist. Gap Report output guides users to update architecture using this skill. |
| `architecture-compliance` | Complementary: compliance validates organizational standards; traceability validates PO Spec coverage. |

---

## Example Invocations

```
/skill architecture-traceability
→ Locates PO Spec and architecture docs, generates coverage report

"Requirements deviation check"
→ Compares PO Spec requirements against architecture, generates traceability report

"Check requirements coverage"
→ Same as above

"Generate a traceability matrix"
→ Same as above

"PO spec coverage check"
→ Generates report highlighting gaps and partial coverage
```

---

## Success Criteria

A successful traceability report produces:

- [ ] All use cases from the PO Spec are listed with their requirements
- [ ] Every requirement has a coverage status (Covered / Partial / Not Covered)
- [ ] Covered requirements include evidence citations (section + quote)
- [ ] Gap Report lists all Not Covered and Partial items with suggested sections
- [ ] Summary statistics are accurate
- [ ] `TRACEABILITY_REPORT.md` renders correctly in GitHub/external platforms
