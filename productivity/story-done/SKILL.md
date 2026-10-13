---
name: story-done
description: "End-of-story completion review. Reads the story file, verifies each acceptance criterion against the implementation, checks for CDD/ADR deviations, prompts code review, updates story status to Complete, and surfaces the next ready story from the sprint."
argument-hint: "[story-file-path] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, AskUserQuestion, Task
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

- When to use: End-of-story completion review. Reads the story file, verifies each acceptance criterion against the implementation, checks for CDD/ADR deviations, prompts code review, updates story status to Complete, and surfaces the next ready story from the sprint.
- Inputs: Command arguments: `/story-done [story-file-path] [--review full|lean|solo]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: Only when Memory Bank is initialized and each named write effect is covered: `memory_bank/t3_archive/sprint_snapshots/story-closure-index.md`.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

# Story Done

This skill closes the loop between design and implementation. Run it at the end
of implementing any story. It ensures every acceptance criterion is verified
before the story is marked done, CDD and ADR deviations are explicitly
documented rather than silently introduced, code review is prompted rather than
forgotten, and the story file reflects actual completion status.

**Output:** Completion report; eligible scoped Story/state writes and next eligible story.

---

## Phase 1: Find the Story

Resolve the review mode (once, store for all gate spawns this run):
1. If `--review` is present, require its nonempty value to be exactly
   `full`, `lean` or `solo`; use the valid explicit value.
2. Otherwise, if `production/review-mode.txt` exists, read and trim its value;
   require exactly `full`, `lean` or `solo`, then use that valid global value.
3. Only when both override and global file are absent default to `lean`.

Resolve once and reuse the same valid mode for all applicable director spawns.
Empty/invalid explicit values or an existing empty/invalid global file stop mode
resolution before any director spawn, gate-skip verdict or status/closure write.
Report the actual invalid source/value and request correction; do not silently
fall back to lean or invent a completed gate. Preserve existing legal CLI/modes.

See `standards/director-gates.md` for the full check pattern.

**If a file path is provided** (e.g., `/story-done production/epics/core/story-damage-calculator.md`):
read that file directly.

**If no argument is provided:**

1. Read `production/session-state/active.md`, if present, for its explicit active
   Story path and sprint reference; verify these against the actual Story body.
2. Read `production/sprint-status.yaml`, if present, and the sprint plans whose
   bodies reference that Story/sprint. Use real IDs, paths and ownership, not file
   modification time. An `in-progress` YAML entry or equivalent documented Story
   state may identify a candidate only when its scope and owner agree.
3. For multiple candidates or conflicting active/status/plan references, use the
   runtime's available question mechanism to list the real paths and scope
   differences and resolve which Story/sprint is intended. Do not pick the newest
   file or silently override a contradictory owner.
4. If no Story or owning sprint can be established, request the missing path/scope.
   Continue independent checks, leaving dependent closure and next-Story selection
   unresolved; do not create or repair state as a discovery step.

Retain the resolved owning sprint and references for Phase 8. A provided Story path
also requires this ownership reconciliation before making sprint-specific claims.

---

## Phase 2: Read the Story

Read the full story file. Extract and hold in context:

- **Story name and ID**
- **CDD Requirement TR-ID(s)** referenced (e.g., `TR-combat-001`)
- **Manifest Version**, full raw-byte SHA-256/size, original path/collection time and retained snapshot; date-only identity is LegacyRecheck
- **ADR reference(s)** referenced
- **Acceptance Criteria** — the complete list (every checkbox item)
- **Implementation files** — files listed under "files to create/modify"
- **Story Type** — the `Type:` field from the story header.
  - Game types: Logic / Integration / Visual/Feel / UI / Config/Data
  - Product types: API / CLI / Data/Migration / Auth/Permission / Workflow / UI / Integration / Ops/Deployment / Config
- **Technology notes** — any technology-specific constraints noted (engine compatibility for game, stack compatibility for product)
- **Definition of Done** — if present, the story-level DoD
- **Estimated vs actual scope** — if an estimate was noted

Also read actual disposition and required inputs:
- Governing CDD substantive rules/ACs, required attachments and dependencies;
  current TR registry for assigned IDs. Missing required owners are incomplete;
  do not manufacture TR-IDs or treat quoted Story text as current authority.
- Exact Accepted ADR revision/section/scope for `covered`; justified `cdd-layer`/
  `no-adr` uses its substantive named CDD/local owner/reason instead. Reconcile
  actual Notes/code choices under `standards/notes-adr-sync.md`; unresolved required
  decisions/conflicts/documentation updates block affected closure.
- Complete current control-manifest bytes and applicable rules. Bind full SHA-256,
  byte size, original path, timezone-qualified CollectedAt and recoverable snapshot,
  with commit plus uncommitted/ignored identities. Historical approval needs exact
  input/scope/authority match. Disclose an absent optional manifest/Memory Bank;
  missing required owners block affected checks.

---

## Phase 3: Verify Acceptance Criteria

For each acceptance criterion in the story, attempt verification using one of
three methods:

### Automatic verification (run without asking)

- **File existence check**: `Glob` for files the story said would be created.
- **Test pass check**: if a test file path is mentioned, run it via `Bash`.
- **No hardcoded values check**: `Grep` for numeric literals in implementation code
  paths that should be in config files.
- **No hardcoded strings check**: `Grep` for user-facing strings in `src/`
  that should be in localization files.
- **Dependency check**: if a criterion says "depends on X", check that X exists.

### Manual verification with confirmation (use `AskUserQuestion`)

- Criteria about subjective qualities ("feels responsive", "animations play correctly")
- Criteria about gameplay behaviour ("player takes damage when...", "enemy responds to...")
- Criteria about product workflow behaviour ("user can approve invoice", "CLI prints the expected table")
- Performance criteria ("completes within Xms") — require measured output, method, budget and exact target runtime/hardware/input identity; absent measurement is NotRun

Batch up to 4 manual verification questions into a single `AskUserQuestion` call:

```
question: "Does [criterion]?"
options: "Yes — passes", "No — fails", "Not tested yet"
```

### Unexecuted or unavailable verification

- Game playtest, Product user/workflow sessions, deployment and full-build checks
  need actual observations. Record NotRun for unexecuted checks, Blocked for missing
  prerequisites and Pending for required confirmation. Every required incomplete
  item prevents both completion levels; optional follow-up needs owner/due phase.

### Test-Criterion Traceability

After completing the pass/fail/deferred check above, map each acceptance
criterion to the test that covers it:

For each acceptance criterion in the story:

1. Read the Story's exact Test Evidence paths and the actual test configuration
   first, including configured roots outside `tests/` and runner discovery rules.
   Ask whether a unit, integration or confirmed manual test directly verifies
   this criterion:
   - **Unit test**: read the exact named file first, then search the configured
     unit-test roots/discovered paths for candidates (`tests/unit/` is a
     conventional example; `Glob`/`Grep` locate candidates only).
   - **Integration test**: use the exact named file and configured integration
     roots/discovered paths similarly (`tests/integration/` is an example).
   - **Manual confirmation**: if the criterion was verified via `AskUserQuestion`
     above with a "Yes — passes" answer, count that as a manual test

2. Produce a traceability table:

```
| Criterion | Test | Status |
|-----------|------|--------|
| AC-1: [criterion text] | tests/unit/test_foo.gd::test_bar | COVERED |
| AC-2: [criterion text] | Manual playtest/user-test confirmation | COVERED |
| AC-3: [criterion text] | — | UNTESTED |
```

3. Resolve each required AC to actual test setup/stimulus/behavioral assertion and
   result, or documented manual observation. Candidate filenames/keywords locate
   evidence only. Coverage is not execution. A bare "Yes" without observer, actual
   steps, exact build/input identity, time and result is Pending confirmation.
4. Any required AC lacking adequate actual PASS evidence blocks closure regardless
   of percentage covered. Keep FAIL/NotRun/Blocked/Pending; only optional additional
   checks may remain advisory with owner/due phase.

### Test Evidence Requirement

Based on the Story Type extracted in Phase 2, check for required evidence:

First determine the project domain from the story's CDD path or nearby concept
document (`game-concept.md` vs `product-concept.md`). Use the game table for game
stories and the product table for product stories. If domain is unknown and the
type exists in both domains (`UI`, `Integration`), resolve actual governing owner/
surface or ask. Keywords cannot determine required applicability; unresolved scope
remains Unknown.

**[游戏专用]** Game evidence table:
| Story Type | Required Evidence | Gate Level |
|---|---|---|
| **Logic** | Automated unit test in `tests/unit/[system]/` — must exist and pass | BLOCKING |
| **Integration** | Integration test in `tests/integration/[system]/` OR playtest/session log doc | BLOCKING |
| **Visual/Feel** | Screenshot + sign-off in `production/qa/evidence/` | ADVISORY |
| **UI** | Manual walkthrough doc OR interaction test in `production/qa/evidence/` | ADVISORY |
| **Config/Data** | Smoke check pass report in `production/qa/smoke-*.md` | ADVISORY |

**[通用产品]** Product evidence table:

Resolve automated evidence from the Story's exact paths and actual configured test
roots, naming and runner discovery, including tests outside `tests/`. Read required
originals and verify matching actual PASS results for the named ACs and inputs.
Conventional directories are discovery examples, not prerequisites. A missing
required original remains visible; fallback discovery does not waive it or erase
a failure. Where the owning workflow permits an alternate location, reconcile
that exact path with its owner before closure and verify the same required checks.

| Story Type | Required Evidence | Gate Level |
|---|---|---|
| **API** | Contract test at the exact Story-bound configured path — must exist and pass | BLOCKING |
| **CLI** | Smoke command output in `production/qa/evidence/smoke/` — `--help` + core command | ADVISORY |
| **Data/Migration** | Migration test against fresh instance at the exact Story-bound configured path — must exist and pass | BLOCKING |
| **Auth/Permission** | Permission test at the exact Story-bound configured path — must exist and pass | BLOCKING |
| **Workflow** | Integration test at the exact Story-bound configured path — must exist and pass | BLOCKING |
| **UI** | Walkthrough doc OR screenshot in `production/qa/evidence/` | ADVISORY |
| **Integration** | Integration test OR API contract test | BLOCKING |
| **Ops/Deployment** | Deployment smoke in `production/qa/smoke-*.md` | BLOCKING |
| **Config** | Config validation test OR smoke check | ADVISORY |

**Product evidence checks:**

- **API**: read the Story's exact Test Evidence path first, then search actual
  configured roots/discovered paths for contract tests covering its endpoint,
  schema and TR-ID (`tests/api/` is an example). Verify actual matching PASS;
  missing required evidence or incomplete required checks are **BLOCKING**.
- **CLI**: check `production/qa/evidence/smoke/`, `production/qa/evidence/manual/`, or
  `production/qa/smoke-*.md` for command output covering `--help` and the core
  command path. If none found, flag **ADVISORY**.
- **Data/Migration**: read the exact Test Evidence path first, then search
  actual configured roots/discovered paths for migration or fresh-instance tests
  (`tests/integration/` is an example). Verify actual matching PASS; missing
  required evidence or incomplete required checks are **BLOCKING**.
- **Auth/Permission**: first read the Story's exact Test Evidence files and
  actual test configuration. Verify the configured runner discovers those files,
  that their behavioral assertions cover the required role, token and access
  boundaries (including required allow/deny and invalid/expired cases), and that
  matching actual execution passes. Search actual configured roots/discovered
  paths for additional candidates only as needed; `tests/unit/auth/` and
  `tests/api/` are conventional examples. Missing required evidence, failed tests
  or incomplete required boundary coverage/execution remain **BLOCKING**.
- **Workflow**: read the exact Test Evidence path first, then search actual
  configured roots/discovered paths for required workflow coverage
  (`tests/integration/[module]/` is an example). Verify actual matching PASS;
  missing required evidence or incomplete required checks are **BLOCKING**.
- **UI**: check `production/qa/evidence/` for walkthrough or screenshot evidence,
  or an interaction test named in the story. If none found, flag **ADVISORY**.
- **Integration**: read the exact Test Evidence path first, then search actual
  configured roots/discovered paths for required service, webhook, queue or
  contract coverage (`tests/integration/` and `tests/api/` are examples). Verify
  actual matching PASS; missing required evidence or incomplete required checks
  are **BLOCKING**.
For Ops/Deployment, resolve the actual conventional smoke report, confirmed CI evidence or exact Story-named deployment artifact used by this review. Read its original source and verify the required matching PASS deployment evidence; no route bypasses that requirement. Unresolved source selection remains Unknown.

- **Ops/Deployment**: check for `production/qa/smoke-*.md`, CI evidence, or a
  deployment smoke artifact named in the story. If none found, flag **BLOCKING**.
- **Config**: check for a config validation test, smoke report, or evidence doc
  covering the changed environment variable, feature flag, or setting. If none
  found, flag **ADVISORY**.

**For game Logic stories**: first read the story's **Test Evidence** section to extract the
exact required file path. Use `Glob` to check that exact path. If the exact path is not
found, also search `tests/unit/[system]/` broadly (the file may have been placed at a
slightly different location). If no test file is found at either location:
- Flag as **BLOCKING**: "Logic story has no unit test file. Story requires it at
  `[exact-path-from-Test-Evidence-section]`. Create and run the test before marking
  this story Complete."

**For game Integration stories**: read the story's **Test Evidence** section for the exact
required path. Use `Glob` to check that exact path first, then search
`tests/integration/[system]/` broadly, then check `production/session-logs/`,
`production/qa/evidence/playtests/`, and `production/qa/evidence/` for a playtest or session
log record referencing this story.
If none found: flag as **BLOCKING** (same rule as Logic).

**For game Visual/Feel and game UI stories**: glob `production/qa/evidence/` for a file
referencing this story. If none: flag as **ADVISORY** —
"No manual test evidence found. Create `production/qa/evidence/[story-slug]-evidence.md`
using the test-evidence template and obtain sign-off before final closure."

**For game Config/Data stories**: check for any `production/qa/smoke-*.md` file.
If none: flag as **ADVISORY** — "No smoke check report found. Run `/smoke-check`."

**If no Story Type is set**: flag as **ADVISORY** —
"Story Type not declared. Add one domain-appropriate value: Game
`Logic|Integration|Visual/Feel|UI|Config/Data`, or Product
`API|CLI|Data/Migration|Auth/Permission|Workflow|UI|Integration|Ops/Deployment|Config`."

Any required gap prevents both COMPLETE and COMPLETE WITH NOTES. ADVISORY type-table rows mean only additional evidence not required by the actual Story/DoD; each required AC still needs actual PASS evidence. File existence alone cannot prove passing tests or sign-off.

---

## Phase 4: Check for Deviations

Compare the implementation against the design documents.

Run these checks automatically:

1. **CDD rules check**: Using the current requirement text from `tr-registry.yaml`
   (looked up by the story's TR-ID), check that the implementation reflects what
   the CDD actually requires now — not what it required when the story was written.
    Search locates paths; read actual implementation behavior and bound results
    against substantive rules. Matching identifiers establish no behavioral PASS.

2. **Manifest identity/freshness check**: compare full raw-byte SHA-256/size,
   original path/CollectedAt and retained snapshot with actual current manifest.
   Date-only legacy references are LegacyRecheck; date equality is not PASS.
   Reconcile actual affected rules, decisions, dependencies and verification.
   Mismatched/unknown required scope blocks closure until checked. Disclose an
   absent optional manifest; never silently skip required inputs.

3. **ADR constraints check**: Apply the actual disposition's Accepted ADR/CDD/local owner and required Notes synchronization. Check
   for forbidden patterns from `docs/architecture/control-manifest.md` (if it
   exists). `Grep` for patterns explicitly forbidden in the ADR.

4. **Hardcoded values check**: `Grep` the implemented files for numeric literals
   in module logic that should be in data files.

5. **Scope check**: Did the implementation touch files outside the story's stated
   scope? (files not listed in "files to create/modify")

For each deviation found, categorize:

- **BLOCKING** — implementation contradicts the CDD or ADR (must fix before
  marking complete)
- **ADVISORY** — implementation drifts slightly from spec but is functionally
  equivalent (document, user decides)
- **OUT OF SCOPE** — additional files were touched beyond the story's stated
  boundary (flag for awareness — may be valid or scope creep)

---

## Phase 4b: QA Coverage Gate

**Review mode check** — apply before spawning QL-TEST-COVERAGE:
- `solo` → skip. Note: "QL-TEST-COVERAGE skipped — Solo mode." Proceed to Phase 5.
- `lean` → skip (not a PHASE-GATE). Note: "QL-TEST-COVERAGE skipped — Lean mode." Proceed to Phase 5.
- `full` → spawn as normal.

After completing the deviation checks in Phase 4, spawn `qa-lead` via Task using gate **QL-TEST-COVERAGE** (`standards/director-gates.md`).

Pass:
- The story file path and story type
- Test file paths found during Phase 3 (exact paths, or "none found")
- The story's `## QA Test Cases` section (the pre-written test specs from story creation)
- The story's `## Acceptance Criteria` list

The qa-lead reviews whether the tests actually cover what was specified — not just whether files exist.

Apply the verdict:
- **ADEQUATE** → proceed to Phase 5
- **GAPS** → classify actual required AC/DoD gaps as blocking; only optional extra coverage remains advisory with owner/due phase.
- **INADEQUATE** → flag as **BLOCKING**: "QA lead: critical logic is untested. Verdict cannot be COMPLETE until coverage improves. Specific gaps: [list]."

Skip this phase for advisory-only evidence story types when no code test is
required by the story: Game Config/Data; Product CLI / UI / Config. Do not skip
for Product API, Data/Migration, Auth/Permission, Workflow, Integration, or
Ops/Deployment stories.

---

## Phase 5: Lead Programmer Code Review Gate

**Review mode check** — apply before spawning LP-CODE-REVIEW:
- `solo` → skip. Note: "LP-CODE-REVIEW skipped — Solo mode." Proceed to Phase 6 (completion report).
- `lean` → skip (not a PHASE-GATE). Note: "LP-CODE-REVIEW skipped — Lean mode." Proceed to Phase 6 (completion report).
- `full` → spawn as normal.

Spawn `lead-programmer` via Task using gate **LP-CODE-REVIEW** (`standards/director-gates.md`).

Pass: implementation file paths, story file path, relevant CDD section, governing ADR.

Present the verdict to the user. If CONCERNS, surface them via `AskUserQuestion`:
- Options: `Revise flagged issues` / `Accept and proceed` / `Discuss further`
If REJECT, do not proceed to Phase 6 verdict until the issues are resolved.

No files requires actual applicability: a documented non-code Story may be N/A; missing required implementation/review is Blocked/NotRun. Mode skips establish no independence/approval and cannot waive an explicitly required independent review.

---

## Phase 6: Present the Completion Report

Before updating any files, present the full report:

```markdown
## Story Done: [Story Name]
**Story**: [file path]
**Date**: [today]

### Acceptance Criteria: [X/Y passing]
- [x] [Criterion 1] — auto-verified (test passes)
- [x] [Criterion 2] — confirmed
- [ ] [Criterion 3] — FAILS: [reason]
- [?] [Criterion 4] — DEFERRED: requires playtest/user test/deployment session

### Test-Criterion Traceability
| Criterion | Test | Status |
|-----------|------|--------|
| AC-1: [text] | [test file::test name] | COVERED |
| AC-2: [text] | Manual confirmation | COVERED |
| AC-3: [text] | — | UNTESTED |

### Test Evidence
**Story Type**: [Game: Logic | Integration | Visual/Feel | UI | Config/Data] OR [Product: API | CLI | Data/Migration | Auth/Permission | Workflow | UI | Integration | Ops/Deployment | Config] OR [Not declared]
**Required evidence**: [domain-specific required evidence from the game/product table]
**Evidence found**: [YES — `[path]` | NO — BLOCKING | NO — ADVISORY]

### Deviations
[NONE] OR:
- BLOCKING: [description] — [CDD/ADR reference]
- ADVISORY: [description] — user accepted / flagged for tech debt

### Scope
[All changes within stated scope] OR:
- Extra files touched: [list] — [note whether valid or scope creep]

### Verdict: COMPLETE / COMPLETE WITH NOTES / BLOCKED
```

**Verdict definitions:**
- **COMPLETE**: every required AC/check has adequate actual PASS evidence; required
  decisions/reviews and relevant completion authority are satisfied, no blocking deviations.
- **COMPLETE WITH NOTES**: the same required conditions pass, with only permitted
  advisory actions and owner/due phase.
- **BLOCKED**: any required FAIL/NotRun/Blocked/Pending/Unknown or missing required
  decision/review/authority; unresolved required deviations must be resolved.

Legacy `COMPLETE WITH RISKS` aliases COMPLETE WITH NOTES only after verifying those
same required facts. Preserve the original historical record. Otherwise project
BLOCKED with actual findings, never normalize risk acceptance into completion.

If the verdict is **BLOCKED**: do not proceed to Phase 7. List what must be
fixed. Offer to help fix the blocking items.

---

## Phase 7: Authorized Closure Changeset

Establish eligible COMPLETE/COMPLETE WITH NOTES first. Present exact closure
revision/input manifest, findings and all proposed paths/effects. Reuse existing
covered authority; otherwise ask "May I write this named closure changeset?"
List each intended effect separately:

1. `[story path]`: `Status: Complete` and Completion Notes with canonical verdict,
   required outcomes, exact evidence/decision/review inputs, actual observer/runtime/
   time, historical/current execution, independence, completion authority and remaining
   advisory action/owner/due phase.
2. `production/sprint-status.yaml`, if selected/present: matching Story `status: done`
   only from that exact eligible closure revision; retain source/completed date and
   change top-level timestamp only when listed. Never infer done from risk/label.
3. `production/session-state/active.md`, only in covered scope: append actual verdict,
   Story/closure/evidence source and next recommendation. Creation also needs authority.
4. `docs/tech-debt-register.md`, if listed/authorized: permitted advisory action rows;
   no entry changes test facts, required acceptance or completion.
5. Initialized `memory_bank/t3_archive/sprint_snapshots/story-closure-index.md`, only
   with its covered pointer effect. Completion Verdict: COMPLETE,
   COMPLETE WITH NOTES, or BLOCKED. Use `Story Path` as the dedupe key for authorized
   current pointers; retain historical closure links. Legacy RISKS follows Phase 6.

Story-write approval authorizes none of the other paths/effects. Report-only cannot
set Complete/done or alter any input/index/state. With partial authority perform
only covered effects and disclose pending projections. Freshly verify inputs before
dependent writes; stop affected effects on mismatch/failure and preserve evidence.
Immutable closure publication requires its own explicit authority; checks/reports/
adapter writes are not publication. Without Memory Bank use Story/report fallback,
disclosing absent optional index without initialization.

---

## Phase 8: Surface the Next Story

After completion, help the developer keep momentum:

1. Read the owning sprint resolved in Phase 1 and its referenced Story bodies;
   reconcile matching entries in `production/sprint-status.yaml` when present.
2. Use the actual storage vocabulary, without adding serialized status values:
   - Markdown `Ready` and YAML `ready-for-dev` identify ready candidates.
   - Markdown `Draft` and YAML `backlog` identify candidates needing
     `/story-readiness`; do not present them as already ready for development.
   - Exclude `Blocked` / `blocked`, `Complete` / `done`, and stories already
     `in-progress` or `review` from the next ready list.
   - Require no blocking incomplete dependency and Must Have / Should Have priority
     (YAML `must-have` / `should-have`). A Ready label alone does not prove readiness.
3. If Story and YAML states conflict, or sprint ownership is still ambiguous,
   list the actual paths/states for resolution; do not invent READY/NOT STARTED
   storage values, fix statuses or choose a sprint by mtime.

Present:

```
### Next Up
The following stories are ready to pick up:
1. [Story name] — [1-line description] — Est: [X hrs]
2. [Story name] — [1-line description] — Est: [X hrs]

Run `/story-readiness [path]` to confirm a story is implementation-ready
before starting.
```

List Draft/backlog candidates separately as "Needs readiness review" with their
actual paths and unresolved requirements. Surfacing recommendations writes no
Story, sprint or session state.

If every in-scope Must Have has an exact eligible closure (not merely a Complete
label), surface current selected QA follow-up:

```
### Sprint Close-Out Sequence
Every required Must Have closure condition passes.
1. `/smoke-check sprint` — recommended critical-path evidence collection
2. `/team-qa sprint` — optional default orchestration when useful
3. `/gate-check` — assess actual transition, no automatic advancement
```

Explicitly selected strict obligations remain required for their named scope;
NotRun/Blocked/Pending cannot be represented as passing. Optional orchestration
waives no required AC/evidence. A Blocked Must Have prevents "all complete";
list its actual unresolved checks and continue independent work.

If there are Should Have stories still unstarted, surface them alongside the close-out sequence so the user can choose: close the sprint now, or pull in more work first.

If no more stories are ready but Must Have stories are still In Progress (not Complete):
"No more stories ready to start — [N] Must Have stories still in progress. Continue implementing those before sprint close-out."

---

## Collaborative Protocol

- Completion requires actual required PASS evidence, decisions/reviews and relevant
  scope/authority. Reuse continuing authority without repeated per-role/file prompts.
- Authorized remediation is a separate writer action with fresh required review.
  Risk acceptance records its own exact authority/scope and cannot alter test facts.
- Governance exceptions/actions preserve required failures/unexecuted facts and
  actual BLOCKED closure. File-write approval cannot mark an untested Story Complete.
- Manual confirmation identifies actual observations; skips/self-checks do not
  satisfy required independent review.

---

## Recommended Next Steps

- Run `/story-readiness [next-story-path]` to validate the next story before starting implementation
- After all exact Must Have closures are eligible: consider optional `/smoke-check` and `/team-qa`; apply actual strict obligations, then assess `/gate-check`
- If tech debt was logged: track it via `/tech-debt` to keep the register current
