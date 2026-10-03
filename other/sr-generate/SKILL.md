---
name: sr-generate
description: >
  Phase 6 of the SRS workflow. Reads approved plan files and generates a complete
  IEEE 830-compliant SRS — one file per section, no word limit.
  A full SRS may span 300+ pages across all files.
---

# sr-generate

Goal: produce a complete, publication-ready IEEE 830 SRS.
No word limit. Each section file must be fully written — no placeholders,
no summaries, no "see plan for details."

---

## Step 0 — Identify Project & Gate

```
Ask the user: "Which project should I generate the SRS for? (slug)"
```

Read all files in `projects/{slug}/plan/`.
If plan files don't exist or are incomplete: tell user to run `$sr-plan` first.

Run the readiness gate before writing anything:
```bash
python .codex/scripts/plan_validator.py --dir projects/{slug}/plan/
```

- **BLOCKED** (ERRORs found, e.g. missing file, FR numbering gap, missing "shall"
  clause, bad priority tag): stop here. List the ERRORs and tell the user to fix
  them via `$sr-plan` before retrying `$sr-generate`.
- **READY WITH WARNINGS** (e.g. unresolved `[NEEDS USER INPUT]` not yet logged in
  appendix-b-open-issues.md): show the warnings and ask the user to confirm
  proceeding anyway, or go back to `$sr-plan` to resolve them.
- **READY**: proceed to Step 1.

Load `.codex/skills/srs-generator/references/srs-template.md`.

---

## Step 1 — Generate Section Files

Create files under `projects/{slug}/srs/`. Write each file completely before
moving to the next. Follow `srs-template.md` formatting for each section.

**File order:**

```
srs/
  01-introduction.md
  02-overall-description.md
  03-01-external-interfaces.md
  03-02-functional-requirements.md
  03-03-performance.md
  03-04-database.md
  03-05-design-constraints.md
  03-06-system-attributes.md
  03-07-other-requirements.md
  appendix-a-glossary.md
  appendix-b-open-issues.md
```

---

## FR Format (mandatory for every FR in 03-02)

```markdown
#### FR-NN [Essential|Conditional|Optional]

**Requirement:** The system shall {precise verb} {object} when {condition}.

| Field | Value |
|-------|-------|
| Actor | {who triggers this} |
| Precondition | {system state before} |
| Trigger | {what causes it} |
| Source | {brainstorm round / business rule / regulatory} |

**Acceptance Criteria (GWT):**
- **Given** {system state}
- **When** {actor action or event}
- **Then** {expected system response — measurable}
- **And** {additional assertions if needed}
```

Rules:
- FR-IDs continue sequentially across the entire file — no resets
- Every FR must have: shall clause + all table fields + full GWT
- No "TBD" in Requirement lines — if a requirement is unclear, it should not be in
  the SRS yet (surface it in appendix-b-open-issues.md instead)

---

## NFR Format (mandatory for every NFR in 03-03 and 03-06)

ISO/IEC 25023 Quality Attribute Scenario format:

```markdown
#### NFR-NN — {ISO 25010 Characteristic}: {Sub-characteristic}

| Field | Value |
|-------|-------|
| Source of Stimulus | {who/what triggers the scenario} |
| Stimulus | {the event} |
| Environment | {system state at time of event} |
| Artifact | {which part of the system} |
| Response | {what the system does} |
| Response Measure | {numeric threshold — e.g., ≤ 500ms at 95th percentile} |
```

**Rule:** Response Measure must be numeric. No adjectives ("fast", "good", "acceptable").
If genuinely unknown: `[TBD: {what data is needed} | owner: {role} | resolve-by: {milestone}]`

---

## Step 2 — Generate Master Index

Write `projects/{slug}/srs/00-master-index.md`:

```markdown
# SRS Master Index — {Project Name}
Version: 1.0   Date: {date}   Status: DRAFT

## Document Map
| File | Section | Description | Word count (est.) |
|------|---------|-------------|-----------------|
...

## FR Summary
Total FRs: {n}
- Essential: {n}
- Conditional: {n}
- Optional: {n}

## NFR Summary
Total NFRs: {n} ({n} confirmed / {n} [TBD])

## Open Items
{count} items in appendix-b-open-issues.md requiring resolution before FINAL status.
```

---

## Step 3 — Handoff

Run `python .codex/scripts/srs_validator.py --dir projects/{slug}/srs/ --stats` and use its
counts below (don't recount a 300+ page document by hand).

Output:
```
SRS generation complete.

Location: projects/{slug}/srs/
Files: 11 section files + 00-master-index.md
FRs:  {total} ({Essential}/{Conditional}/{Optional})
NFRs: {total} ({confirmed} confirmed / {TBD} [TBD])

Next: $sr-validate → validates SRS against IEEE 830-1998
```
