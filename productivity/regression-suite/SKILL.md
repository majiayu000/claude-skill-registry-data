---
name: regression-suite
description: "Map test coverage to CDD critical paths, identify fixed bugs without regression tests, flag coverage drift from new features, and maintain tests/regression-suite.md. Run after implementing a bug fix or before a release gate."
argument-hint: "[update | audit | report]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit
---

## QA policy, facts and authority

Apply `standards/evidence-lifecycle.md`, `standards/notes-adr-sync.md` and existing
collaboration authority. Read actual `workflow/workflow-catalog.yaml`, domain,
current transition and established project QA scope, including initialized
`memory_bank/t1_axioms/qa_context.md` or the existing owning Story/plan/decision.
QA orchestration is optional by default; strict obligations need explicit source,
authority and exact checks/scope. Review mode does not select strict QA. Absent
optional Memory Bank/QA Context with no actual strict selection uses the catalog's
default optional orchestration; disclose absence without requiring initialization.
Unknown applies to unresolved actual required applicability or conflicting policy,
not optional context absence. Resolve that affected scope before dependent claims;
Honor actual user-specified per-effect approval conditions when determining coverage;
do not invent strict obligations or passing results.
Optional orchestration never waives required Story AC, governing DoD, decisions,
evidence or required review. Type tables are starting points; actual owners decide
requirements. Each required check retains PASS/FAIL/NotRun/Blocked/Pending; N/A
needs a governing applicability reason and cannot erase a failure.

Separate sufficiency, actual execution, independence, acceptance and completion.
Files/keywords/counts, planning cases and self-checks prove none of the other facts.
Read relied-on bodies and minimum required direct/indirect dependency closure;
retain full SHA-256/byte sizes, recoverable originals and original-path witnesses.
Disclose reading omissions. Exact bound historical results may be reused only
where selected workflow permits, labeled historical with original runtime/observer,
inputs and scope; never call them this run's execution. Missing required originals
or observations leave affected checks incomplete. Risk acceptance is a separate
scoped record; it cannot change FAIL/NotRun/Blocked/Pending to PASS or completion.

Reuse named paths/effects authority across roles/retries; before new authority show
draft and complete effect set, asking only for material new scope. Review-only
invokes no write entrypoint. Report-only writes its new report, excluding inputs,
indexes, session/sprint/stage state and closure. Existing report paths require a
new revision with prior evidence preserved; index effects need their own covered
scope and historical links. Optional Memory Bank absence uses Story/report/
conversation fallback without initialization, publication or activation.

## User Guide

- When to use: Map test coverage to CDD critical paths, identify fixed bugs without regression tests, flag coverage drift from new features, and maintain tests/regression-suite.md. Run after implementing a bug fix or before a release gate.
- Inputs: Command arguments: `/regression-suite [update | audit | report]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Routing

Resolve actual domain from substantive concept bodies, configured fields and
explicit project decisions under `standards/technical-preferences.md` before
mapping coverage. Populated legacy Product configuration can establish Product
without a concept; filenames/placeholders alone cannot. Conflicts or absent actual
evidence leave the affected route Unknown while neutral checks continue.

For the resolved domain:
- `design/cdd/game-concept.md` -> **[Game]** map regression tests to game critical paths, CDD acceptance criteria, save/load, levels, combat, UI/HUD, and playtest-derived bugs.
- `design/cdd/product-concept.md` -> **[Product]** map regression tests to API contracts, CLI commands, workflows, migrations, auth/permissions, configuration, data integrity, deployment smoke checks, and user-facing UI paths.
- If still unresolved after reading those owners, ask whether coverage should be
  organized around game critical paths or product workflows/contracts.

Keep game regression examples. Product regression mapping is added beside them.

## Dual-Domain Parity Contract

| Area | Game branch | Product branch |
|------|-------------|----------------|
| Context reads | Game Concept, module index, CDD acceptance/formulas/edge cases, closed bugs, unit/integration tests, playtest-derived issues | Product Concept, module index, CDD acceptance/contracts/data/edge cases, closed bugs, unit/integration/contract/CLI/migration tests, deployment smoke records |
| Steps | Map mechanics, save/load, combat, levels, UI/HUD, formulas, and known bugs to regression coverage | Map endpoints, commands, workflows, migrations, auth/permissions, config, data integrity, deployment smoke, and known bugs to regression coverage |
| Outputs | `tests/regression-suite.md` entries for critical game paths and fixed bugs | `tests/regression-suite.md` entries for product contracts/workflows/ops paths and fixed bugs |
| Next steps | Add missing tests, update `/qa-plan`, run `/smoke-check` | Add missing contract/CLI/migration/permission/deployment tests, update `/qa-plan`, run `/smoke-check` |

# Regression Suite

This skill ensures that every bug fix is backed by a test that would have
caught the original bug — and that the regression suite stays current as the
game evolves. It also detects when new features have been added without
corresponding regression coverage.

A regression suite is not a new test category — it is a **curated list of**
tests already in `tests/`** that collectively cover the game's critical paths**
and known failure points. This skill maintains that list.

**Output:** `tests/regression-suite.md`

**When to run:**
- After fixing a bug (confirm a regression test was written or identify gap)
- Before relevant release verification under actual catalog/current phase/selected regression scope
- As part of sprint close to detect coverage drift

---

## 1. Parse Arguments

**Modes:**
- `/regression-suite update` — scan new bug fixes this sprint and check
  for regression test presence; add new tests to the suite manifest
- `/regression-suite audit` — full audit of all CDD critical paths vs.
  existing test coverage; flag paths with no regression test
- `/regression-suite report` — read-only status report (no writes); suitable
  for sprint reviews
- No argument — run `update` if a sprint is active, else `audit`

---

## 2. Load Context

### Step 2a — Load existing regression suite

Read `tests/regression-suite.md` if it exists. Extract:
- Total registered regression tests
- Last updated date
- Any tests flagged as `STALE` or `QUARANTINED`

If absent disclose it; report mode never creates it. Update/audit may draft a manifest for covered writes.

### Step 2b — Load test inventory

Glob all test files:
```
tests/unit/**/*_test.*
tests/integration/**/*_test.*
tests/regression/**/*
```

For each file, note the system (from directory path) and file name.
Discovery is inventory only. Read relied-on test bodies/helpers/fixtures and required results before assigning coverage. Include actual configured Product API/CLI/migration/auth/smoke/E2E paths; filenames prove no behavior or execution.

### Step 2c — Load CDD critical paths

For `audit` mode: read `design/cdd/module-index.md` to get all systems.
For each MVP-tier system, read its CDD and extract:
- Acceptance Criteria (these define the critical paths)
- Formulas section (formulas must have regression tests)
- Edge Cases section (known edge cases should have regression tests)

For `update` mode: skip full CDD scan. Instead read the current sprint plan
and story files to find stories with Status: Complete this sprint.

### Step 2d — Load closed bugs

Glob `production/qa/bugs/*.md` for candidate Closed/Fixed records, then read each relied-on complete original Bug/fix and required attachments. Verify failure scenario, fix scope, test input identity and unresolved actions. Status/keywords/last-line quotes do not prove full reading or resolution; disclose unavailable originals/omissions. Note:
- Which story or system the bug was in
- Whether a regression test was mentioned in the fix description

---

## 3. Map Coverage — Critical Paths

For `audit` mode only:

For each CDD acceptance criterion, determine whether a test exists:

1. Grep `tests/unit/[system]/` and `tests/integration/[system]/` for file names
   and function names related to the criterion's key noun/verb
2. Assign coverage:

| Status | Meaning |
|--------|---------|
| **COVERED** | Actual read behavioral oracle addresses AC and required cases; execution separate |
| **PARTIAL** | A test exists but doesn't cover all cases (e.g. happy path only) |
| **MISSING** | No test found for this critical path |
| **EXEMPT** | Justified automation N/A only; required manual/visual evidence still applies |

3. Elevate MISSING items that correspond to formulas or state machines to
   **HIGH PRIORITY** gap — these are the most likely regression sources.

---

## 4. Map Coverage — Fixed Bugs

For each closed bug:

1. Extract the system slug from the bug's metadata
2. Grep `tests/unit/[system]/` and `tests/integration/[system]/` for a test
   that references the bug ID or the specific failure scenario
3. Read actual regression behavior against the complete original Bug scenario;
   verify setup/stimulus/oracle would catch the original failure. Record static
   coverage separately from actual pre-fix/post-fix execution (NotRun if absent):
   - **HAS REGRESSION TEST** — semantic coverage bound to actual failure scenario
   - **MISSING REGRESSION TEST** — no adequate guard for the known scenario
   - **INCOMPLETE** — required Bug/test/dependency input unavailable or scope unknown

For MISSING REGRESSION TEST items:
- Flag them as regression gaps
- Suggest the test file path: `tests/unit/[system]/[bug-slug]_regression_test.[ext]`
- Note: "Without this test, this bug can silently return in a future sprint."

---

## 5. Detect Coverage Drift

Coverage drift occurs when the game grows but the regression suite doesn't.

Check for drift indicators:
- Stories completed this sprint with no corresponding test files in `tests/`
- New systems added to `module-index.md` since the last regression-suite update
- CDD sections added or revised since the regression suite was last updated
  (use Grep on CDD file modification hints if available, or ask the user)
- `tests/regression-suite.md` last-updated date vs. current date — if gap >
  2 sprints, flag as likely stale

---

## 6. Generate Report and Suite Manifest

### Report format (in conversation)

```
## Regression Suite Status

**Mode**: [update | audit | report]
**Existing registered tests**: [N]
**Test files scanned**: [N]

### Critical Path Coverage (audit mode only)
| System | Total ACs | Covered | Partial | Missing | Exempt |
|--------|-----------|---------|---------|---------|--------|
| [name] | [N] | [N] | [N] | [N] | [N] |

**Coverage rate (non-exempt)**: [N]%

### Bug Regression Coverage
| Bug ID | System | Severity | Has Regression Test? |
|--------|--------|----------|----------------------|
| BUG-NNN | [system] | S[N] | YES / NO ⚠ |

**Bugs without regression tests**: [N]

### Coverage Drift Indicators
[List new systems or stories with no test coverage, or "None detected."]

### Recommended New Regression Tests
| Priority | System | Suggested Test File | Covers |
|----------|--------|---------------------|--------|
| HIGH | [system] | `tests/unit/[system]/[slug]_regression_test.[ext]` | BUG-NNN / AC-[N] |
| MEDIUM | [system] | `tests/unit/[system]/[slug]_test.[ext]` | [criterion] |
```

### Suite manifest format (`tests/regression-suite.md`)

The manifest is a curated index — not the tests themselves, but a registry
of which tests should always pass before a release:

```markdown
# Regression Suite Manifest

> Last Updated: [date]
> Total registered tests: [N]
> Coverage: [N]% of CDD critical paths

## How to run

[Engine-specific command to run all regression tests]

## Registered Regression Tests

### [System Name]

| Test File | Test Function (if known) | Covers | Added |
|-----------|--------------------------|--------|-------|
| `tests/unit/[system]/[file]_test.[ext]` | `test_[scenario]` | AC-N / BUG-NNN | [date] |

## Known Gaps

Tests that should exist but don't yet:

| Priority | System | Suggested Path | Covers | Reason Not Yet Written |
|----------|--------|----------------|--------|------------------------|
| HIGH | [system] | `tests/unit/[system]/[path]` | BUG-NNN | Bug fixed without test |

## Quarantined Tests

Tests that are flaky or disabled (do not run in CI):

| Test File | Function | Reason | Quarantined Since |
|-----------|----------|--------|-------------------|
| (none) | | | |
```

---

## 7. Write Output

Reuse existing named authorization for this manifest create/update effect. Only if missing or materially new ask: "May I write/update `tests/regression-suite.md` with the current
regression suite manifest?"

For `update` mode: append new entries; never remove existing entries
(use `Edit` with targeted insertions).
For `audit` mode: update covered entries/facts, preserving tests, quarantines, unique rationale and historical evidence. Whole-manifest replacement/removal needs separate explicit scope.
For `report` mode: do not write anything.

After writing (if approved):

- For each HIGH priority gap: "Consider creating the missing regression test
  before the next sprint. Run `/test-helpers` to scaffold the test file."
- If bug regression gaps > 0: "These bugs can silently return without regression
  tests. The next sprint should include a story to write the missing tests."
- If coverage drift detected: "Regression suite may be drifting. Consider
  running `/regression-suite audit` at the next sprint boundary."

Manifest operation COMPLETE only after its authorized update. Report mode reports without writing. Coverage/execution gaps remain actual MISSING/INCOMPLETE/FAIL/NotRun; no Story or release completion is implied. Declined writes leave the draft unwritten.

---

## Collaborative Protocol

- **Never remove existing regression tests from the manifest** without
  explicit user approval — removing a test that was deliberately written is a
  regression risk itself
- **Required gaps block dependent claims** — selected required AC/regression evidence precedes affected closure; optional coverage is advisory with owner/due phase. Follow actual catalog/current phase; do not invent a universal regression artifact gate.
- **Quarantine is not deletion** — tests with intermittent failures should be
  quarantined (noted in manifest) but not removed; they should be fixed by
  `/test-flakiness`
- **Resolve manifest-write authority**: reuse covered named path/effect authorization; only missing authority or materially new scope needs confirmation before creating/updating the manifest.
