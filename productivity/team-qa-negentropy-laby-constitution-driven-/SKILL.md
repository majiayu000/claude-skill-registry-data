---
name: team-qa
description: "Orchestrate the QA team through a full testing cycle. Coordinates qa-lead (strategy + test plan) and qa-tester (test case writing + bug reporting) to produce a complete QA package for a sprint or feature. Covers: test plan generation, test case writing, smoke check gate, manual QA execution, and sign-off report."
argument-hint: "[sprint | feature: system-name]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Task, AskUserQuestion
agent: qa-lead
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

- When to use: Orchestrate the QA team through a full testing cycle. Coordinates qa-lead (strategy + test plan) and qa-tester (test case writing + bug reporting) to produce a complete QA package for a sprint or feature. Covers: test plan generation, test case writing, smoke check gate, manual QA execution, and sign-off report.
- Inputs: Command arguments: `/team-qa [sprint | feature: system-name]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: Only when Memory Bank is initialized and each named write effect is covered: `memory_bank/t3_archive/qa_evidence_index.md`.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Routing

Detect the project domain before QA orchestration:
- `design/cdd/game-concept.md` -> **[Game]** keep game QA coordination: test plan, playtest checklist, smoke check, regression paths, platform/input coverage, and sign-off.
- `design/cdd/product-concept.md` -> **[Product]** coordinate product QA: contract tests, integration tests, CLI smoke, migration tests, permission tests, data integrity checks, deployment smoke, user testing, and sign-off evidence.
- If unclear, ask whether QA should follow game playtest gates or product test evidence gates.

Game QA workflow remains intact. Product QA orchestration is added beside it.

## Dual-Domain Parity Contract

| Area | Game branch | Product branch |
|------|-------------|----------------|
| Context reads | Game Concept, sprint/story files, game CDDs, QA plan, smoke tests, playtest reports, platform/input requirements | Product Concept, sprint/story files, product CDDs, QA plan, API/CLI/workflow/migration/auth evidence, deployment smoke, user-test reports |
| Steps | Strategy, test plan, game test cases, smoke gate, manual QA/playtest execution, bug reporting, sign-off | Strategy, test plan, contract/CLI/migration/permission/workflow test cases, smoke gate, manual/user-test/deployment evidence, bug reporting, sign-off |
| Outputs | QA package under `production/qa/`, playtest/evidence entries, bug reports, sign-off verdict | QA package under `production/qa/`, product evidence entries, contract/migration/deployment/user-test gaps, bug reports, sign-off verdict |
| Next steps | Fix blockers, rerun `/smoke-check`, run `/test-evidence-review`, proceed to `/gate-check` or `/team-polish` | Fix blockers, rerun `/smoke-check`, run `/test-evidence-review`, proceed to `/gate-check`, `/team-polish`, or `/release-checklist` |

When this skill is invoked, orchestrate the QA team through a structured testing cycle.

**Decision Points:** Present substantive findings and resolve material choices/new effects with `AskUserQuestion`; continue phases within existing scoped authority without repeated per-role/phase approval. Pass original paths/effects/limits, exact inputs and required independent-review roles to each agent.

## Team Composition

- **qa-lead** — QA strategy, test plan generation, story classification, sign-off report
- **qa-tester** — Test case writing, bug report writing, manual QA documentation

## How to Delegate

Use the Task tool to spawn each team member as a subagent:
- `subagent_type: qa-lead` — Strategy, planning, classification, sign-off
- `subagent_type: qa-tester` — Test case writing and bug report writing

Always provide full context in each agent's prompt (story file paths, QA plan path, scope constraints). Launch independent qa-tester tasks in parallel where possible (e.g., multiple independent Story test-case drafts in Phase 4 can be prepared simultaneously).

## Pipeline

### Phase 1: Load Context

Before doing anything else, gather the full scope:

1. Detect the current sprint or feature scope from the argument:
   - If argument is a sprint identifier (e.g., `sprint-03`): read all story files in `production/sprints/[sprint]/`
   - If argument is `feature: [system-name]`: glob story files tagged for that system
   - If no argument: read `production/session-state/active.md` and `production/sprint-status.yaml` (if present) to infer the active sprint

2. Read `production/stage.txt` to confirm the current project phase.

3. Count stories found and report to the user:
   > "QA cycle starting for [sprint/feature]. Found [N] stories. Current stage: [stage]. Ready to begin QA strategy?"

### Phase 2: QA Strategy (qa-lead)

Spawn `qa-lead` via Task to review all in-scope stories and produce a QA strategy.

Prompt the qa-lead to:
- Read each story file
- Classify actual Game types or Product API/CLI/Data-Migration/Auth-Permission/Workflow/UI/Integration/Ops-Deployment/Config; bind each required AC/evidence/check
- Identify which stories require automated test evidence vs. manual QA
- Flag any stories with missing acceptance criteria or missing test evidence that would block QA
- Estimate manual QA effort (number of test sessions needed)
- Read actual smoke scenarios and bound execution evidence, or route an authorized `/smoke-check` run. Strategy/scenario review is not execution. Required checks retain PASS/FAIL/NotRun/Blocked/Pending; smoke PASS/PASS WITH WARNINGS/FAIL/INCOMPLETE follows actual results, not test-list existence.
- Produce a strategy summary table and smoke check result:

  | Story | Type | Automated Required | Manual Required | Blocker? |
  |-------|------|--------------------|-----------------|----------|

  **Smoke Check**: [PASS / PASS WITH WARNINGS / FAIL / INCOMPLETE] — [details if not PASS]

If smoke checks actually FAIL, list failures prominently; if required execution
or evidence remains NotRun/Blocked/Pending, record INCOMPLETE with the dependency.
Do not claim required entry criteria met or authorize dependent qualification.
Independent plan/case drafting may continue only with sufficient actual inputs and covered delegation/write authority; it creates no execution or qualification facts.

Present the qa-lead's full strategy to the user, then use `AskUserQuestion`:

```
question: "QA Strategy Review"
options:
  - "Looks good — proceed to test plan"
  - "Adjust story types before proceeding"
  - "Skip blocked stories and proceed with the rest"
  - "Smoke check failed — fix issues and re-run /team-qa"
  - "Cancel — resolve blockers first"
```

If smoke check **FAIL**: surface actual failures and stop execution/qualification
that depends on passing those checks. Independently useful Phase 3 plan or Phase 4
case drafts may continue only with sufficient actual inputs and covered authority,
clearly labeled draft with smoke FAIL retained. The affected original scope remains
incomplete and cannot receive an APPROVED sign-off; fix and re-run the dependent
smoke checks before dependent QA execution or qualification.
If **PASS WITH WARNINGS**, all required smoke checks pass; carry optional warnings. If **INCOMPLETE**, surface required gaps and stop dependent qualification/execution while continuing independent planning/evidence work. A skipped/blocked subset narrows scope and cannot approve the original full scope.
If blockers are present: list them explicitly. The user may choose to skip blocked stories or cancel the cycle.

### Phase 3: Test Plan Generation

Using the strategy from Phase 2, produce a structured test plan document.

The test plan should cover:
- **Scope**: sprint/feature name, story count, dates
- **Story Classification Table**: from Phase 2 strategy
- **Automated Test Requirements**: required checks and exact planned paths from the actual test configuration/runner discovery, including valid roots outside `tests/`
- **Manual QA Scope**: which stories need manual walkthrough and what to validate
- **Out of Scope**: what is explicitly not being tested this cycle and why
- **Entry Criteria**: what must be true before QA can begin (smoke check pass, build stable)
- **Exit Criteria**: all required checks have recorded actual states; distinguish finished report work from approved build/Story closure. Bug filing never changes FAIL to PASS.

Reuse covered named QA-plan write authority. Only if missing or materially new ask: "May I write the QA plan to `production/qa/qa-plan-[sprint]-[date].md`?"

Write when that exact named path/effect is covered by existing or newly obtained authorization; do not re-ask for the same scope.

### Phase 4: Test Case Writing (qa-tester)

> **Smoke check** occurs in Phase 2. Actual required FAIL or INCOMPLETE blocks
> dependent execution/qualification, while independent Phase 4 case drafts may
> proceed with sufficient actual Story/AC/plan inputs and covered authority. Keep
> Actual Result/Pass-Fail blank until observed; case-writing is not smoke PASS.
> Preserve smoke FAIL/NotRun/Blocked/Pending and the original incomplete scope;
> drafts or subset work cannot grant its APPROVED sign-off.

For each story requiring manual QA (Visual/Feel, UI, Integration without automated tests):

Spawn `qa-tester` via Task for each story (run in parallel where possible), providing:
- The story file path
- The relevant section of the QA plan for that story
- The CDD acceptance criteria for the system being tested (if available)
- Instructions to draft detailed cases for all required ACs; file/test-evidence/Bug creation needs explicitly delegated named paths/effects

Each test case set should include:
- **Preconditions**: game state required before testing begins
- **Steps**: numbered, unambiguous actions
- **Expected Result**: what should happen
- **Actual Result**: field left blank for the tester to fill in
- **Pass/Fail**: field left blank

Present the test cases to the user for review before execution. Group by story.
Begin dependent manual QA only when its actual required entry checks qualify;
reviewed drafts alone do not waive failed/unexecuted required smoke checks.

Use `AskUserQuestion` per story group (batched 3-4 at a time):

```
question: "Test cases ready for [Story Group]. Review before manual QA begins?"
options:
  - "Approved — begin manual QA for these stories"
  - "Revise test cases for [story name]"
  - "Skip manual QA for [story name] — not ready"
```

### Phase 6: Manual QA Execution

Walk through each story in the approved manual QA list.

Batch stories into groups of 3-4 and use `AskUserQuestion` for each:

```
question: "Manual QA — [Story Title]\n[brief description of what to test]"
options:
  - "PASS — all acceptance criteria verified"
  - "PASS WITH NOTES — minor issues found (describe after)"
  - "FAIL — criteria not met (describe after)"
  - "BLOCKED — cannot test yet (reason)"
```

Collect actual observer/build/input identity, steps/time/result for every required manual check; unobserved results remain NotRun/Pending. After FAIL collect the observed description and delegate `qa-tester` to draft the Bug. Write under `production/qa/bugs/` only with covered creation path/effect; otherwise present the draft for new scope. Bug filing grants no resolution/approval.

Bug report naming: `BUG-[NNN]-[short-slug].md` (increment NNN from existing bugs in the directory).

After collecting all results, summarize:
- Stories PASS: [count]
- Stories PASS WITH NOTES: [count]
- Stories FAIL: [count] — bugs filed: [IDs]
- Stories BLOCKED: [count]
- Stories NotRun: [count] — actual missing execution/capability
- Stories Pending: [count] — awaiting bound results/reviews

### Phase 7: QA Sign-Off Report

Spawn `qa-lead` with actual results from the defined phases (2 smoke/strategy, 3 plan, 4 cases, 6 manual). Read each required test/evidence body and exact bound automated result; collect all parallel outputs and selected independent reviews before dependent sign-off. Case-writing/sufficiency/self-review is not runtime. Automation without matching results remains NotRun/Pending; unavailable required reviewer remains incomplete.

The sign-off report format:

```markdown
## QA Sign-Off Report: [Sprint/Feature]
**Date**: [date]
**QA Lead sign-off**: [pending]

### Test Coverage Summary
| Story | Type | Auto Test | Manual QA | Result |
|-------|------|-----------|-----------|--------|
| [title] | Logic | PASS | — | PASS |
| [title] | Visual | — | PASS | PASS |

### Bugs Found
| ID | Story | Severity | Status |
|----|-------|----------|--------|
| BUG-001 | [story] | S2 | Open |

### Verdict: APPROVED / APPROVED WITH CONDITIONS / NOT APPROVED

**Conditions** (if any): [list what must be fixed before the build advances]

### Next Step
[guidance based on verdict]
```

Verdict rules:
- **APPROVED**: every required AC/check in the entire declared scope has adequate
  actual PASS evidence, required decisions/review/sign-off authority satisfied and
  no required gap/open blocking finding.
- **APPROVED WITH CONDITIONS**: those same required conditions pass; only permitted
  advisory actions/risks remain with owner/due phase and separate acceptance as needed.
- **NOT APPROVED**: any required FAIL/NotRun/Blocked/Pending/Unknown, missing required
  independence/authority, S1/S2 blocker or unresolved required finding. A workaround/
  accepted risk cannot change actual test truth. Authorized requirement changes or
  valid scoped exceptions change only their exact applicability, preserving facts.

Actual qa-lead sign-off binds actor/outcome/exact inputs/scope/authority; template
`[pending]` is not approval. A narrowed partial scope cannot approve excluded
required Stories or the original full scope.

Next step guidance by verdict:
- APPROVED: "Build is ready for the next phase. Run `/gate-check` to validate advancement."
- APPROVED WITH CONDITIONS: "Resolve conditions before advancing. S3/S4 bugs may be deferred to polish."
- NOT APPROVED: "Resolve S1/S2 bugs and re-run `/team-qa` or targeted manual QA before advancing."

Reuse covered named sign-off report write authority. Only if missing or materially new ask: "May I write this QA sign-off report to `production/qa/qa-signoff-[sprint]-[date].md`?"

Write when that exact named path/effect is covered by existing or newly obtained authorization; do not re-ask for the same scope.

Update the Memory Bank index only when this run enters its separately named, authorized effect after saving the actual report. Initialized Memory Bank alone is insufficient; read-only and report-only scopes exclude indexing. If the intended effect or initialization is unresolved, retain Unknown. Before indexing, read the saved immutable report and exact input/evidence identities; a proposed output or INFO is insufficient. This effect does not initialize Memory Bank.

When initialized and the separate named index effect is covered, update
`memory_bank/t3_archive/qa_evidence_index.md`:
- Type: `qa-signoff`
- Evidence path: `production/qa/qa-signoff-[sprint]-[date].md` (new revision on collision)
- Verdict: APPROVED / APPROVED WITH CONDITIONS / NOT APPROVED plus actual check states
- Dedupe by evidence path for an authorized current pointer retaining historical
  revisions/input links. Report approval alone excludes the index effect.
- Without Memory Bank use report/Story/conversation fallback, disclose optional
  absence and do not initialize it as a side effect.

## Error Recovery Protocol

If any spawned agent (via Task) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** via AskUserQuestion with choices:
   - Skip this agent and note the gap in the final report
   - Retry with narrower scope
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. Never discard work because one agent blocked.

Common blockers:
- Input file missing (story not found, CDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; run `/architecture-decision` first
- Scope too large → split into two stories via `/create-stories`
- Conflicting instructions between ADR and story → surface the conflict, do not guess

## Output

A summary covering: stories in scope, smoke check result, manual QA results, bugs filed (with IDs and severities), and the final APPROVED / APPROVED WITH CONDITIONS / NOT APPROVED verdict.

Report operation: **COMPLETE** only when its authorized output finished. Keep sign-off/runtime separate; a finished NOT APPROVED report completes no Story/build/stage.
Verdict: **BLOCKED** — smoke check failed or critical blocker prevented cycle completion; partial report produced.
