---
name: team-qa
description: "Use when a sprint or feature needs a coordinated QA strategy, test cases, execution, and sign-off package."
---

<!-- codex-studio-delegation: governed -->
Resolve every role through `../../../.codex/docs/plugin-agent-delegation.md`;
do not require a repository-local `.codex/agents/` or `.codex/agent-packs/` tree.
Before default delegation, run `python3 ../../../tools/codex_studio/agent_delegation.py resolve --project-root <project-root> --role <role>` and use only its returned role contract.

# Team Qa

## Codex Interaction Contract

- Ask one decision question per turn and wait for the answer before asking another.
- Use `request_user_input` for structured choices when it is available; otherwise ask the same concise question directly.
- Use Codex custom agents by role and profile when delegation is useful.
- Treat any approved write as one complete proposed changeset. Before writing, present every target path and material edit together; do not add unlisted files or behavior.
- A new path, expanded scope, or material change requires a revised complete proposed changeset and fresh approval.

## Invocation

Usage: `$codex-game-studios:team-qa [sprint | feature: system-name] [--review full|lean|solo]`. If the required objective cannot be inferred safely, ask for that single missing decision and wait; do not delegate yet.

## Review Mode

Read `.codex/studio.toml` as the only persistent review-mode source. Map `review_mode = "phase-gated"` to lean optional-review depth; mandatory director gates still run. A `--review` argument applies only to the current run. Use `../../../.codex/docs/director-gates.md` and `.codex/docs/technical-preferences.md` for native gate and engine context.

## Team Roster

- `qa-lead`
- `qa-tester`

## Delegation Plan

- Delegate only tasks that are independent and bounded.
- Name the Codex custom-agent role and the exact artifact or evidence it must return.
- Team members must not spawn additional agents (`agents.max_depth = 1`).
- The parent agent synthesizes all results, resolves overlap, and communicates with the user.
- No subagent commits, publishes, or expands scope.
- Parallel delegation is read-only or draft-only until the parent presents a consolidated result.
- Any multi-file implementation requires one complete changeset approval before work begins.
- If a delegated task blocks, surface the evidence and stop dependent work while preserving independent results.

## Pipeline

Every phase before `## Parent Changeset Gate` is read-only or draft-only. Phase 1 loads context only; QA plans, cases, bug reports, and sign-off reports remain in memory until the parent gate.

### Phase 1: Load Context

Before doing anything else, gather the full scope:

1. Detect the current sprint or feature scope from the argument:
   - If argument is a sprint identifier (e.g., `sprint-03`): File search `production/sprints/` for files matching `*[sprint-identifier]*.md`. Read the matched file. If multiple match, use the most recently modified.
   - If argument is `feature: [system-name]`: file search story files tagged for that system
   - If no argument: read `production/session-state/active.md` and `production/sprint-status.yaml` (if present) to infer the active sprint

2. Read `production/stage.txt` to confirm the current project phase.

3. Count stories found and report to the user:
   > "QA cycle starting for [sprint/feature]. Found [N] stories. Current stage: [stage]. Ready to begin QA strategy?"

Ask that single readiness question and wait for the answer. If the answer is not an explicit yes, do not continue to Phase 2.

### Phase 2: QA Strategy (qa-lead)

Delegate to `qa-lead` through Codex custom-agent delegation to review all in-scope stories and produce a QA strategy.

Prompt the qa-lead to:
- Read each story file
- Classify each story by type: **Logic** / **Integration** / **Visual/Feel** / **UI** / **Config/Data**
- Identify which stories require automated test evidence vs. manual QA
- Flag any stories with missing acceptance criteria or missing test evidence that would block QA
- Estimate manual QA effort (number of test sessions needed)
- **Before assessing smoke status, check for an existing smoke check report**: File search `production/qa/smoke-*.md` and read the most recently modified file (if found). If a report exists, use its verdict and findings directly — do not re-interview the user. If no report exists, note: "No prior smoke check report found — run `$codex-game-studios:smoke-check sprint` before proceeding." and set smoke check status to UNKNOWN (treat as PASS WITH WARNINGS for the purpose of continuing). Produce a smoke check verdict: **PASS** / **PASS WITH WARNINGS [list]** / **FAIL [list of failures]** / **UNKNOWN (no report found)**
- Produce a strategy summary table and smoke check result:

  | Story | Type | Automated Required | Manual Required | Blocker? |
  |-------|------|--------------------|-----------------|----------|

  **Smoke Check**: [PASS / PASS WITH WARNINGS / FAIL / UNKNOWN] — [source: `production/qa/smoke-[date].md` or "no report found"] — [details if not PASS]

If the smoke check result is **FAIL**, the qa-lead must list the failures prominently. QA cannot proceed past the strategy phase with a failed smoke check.

Present the qa-lead's full strategy to the user, then use `request_user_input`:

```
question: "QA Strategy Review"
options:
  - "Looks good — proceed to test plan"
  - "Revise strategy or remove blocked stories"
  - "Stop — resolve blockers or smoke failures first"
```

If smoke check **FAIL**: do not proceed to Phase 3. Surface the failures from the smoke check report and stop. The user must fix them, re-run `$codex-game-studios:smoke-check sprint`, and then re-run `$codex-game-studios:team-qa`.
If smoke check **UNKNOWN**: surface a warning — "No smoke check report found. Recommend running `$codex-game-studios:smoke-check sprint` before QA. Proceeding with caution."
If smoke check **PASS WITH WARNINGS**: note the warnings for the sign-off report and continue.
If blockers are present: list them explicitly. The user may choose to skip blocked stories or cancel the cycle.

### Phase 3: Test Plan Generation

Using the strategy from Phase 2, produce a structured test plan document.

The test plan should cover:
- **Scope**: sprint/feature name, story count, dates
- **Story Classification Table**: from Phase 2 strategy
- **Automated Test Requirements**: which stories need test files, expected paths in `tests/`
- **Manual QA Scope**: which stories need manual walkthrough and what to validate
- **Out of Scope**: what is explicitly not being tested this cycle and why
- **Entry Criteria**: what must be true before QA can begin. Always include: (1) Smoke check PASS or PASS WITH WARNINGS report exists at `production/qa/smoke-*.md`, (2) build is stable (no crashes on launch), (3) all Must Have stories have Status: in-progress or done in `production/sprint-status.yaml`. Add any sprint-specific criteria beyond these.
- **Exit Criteria**: what constitutes a completed QA cycle (all stories PASS or FAIL with bugs filed)

Return the QA-plan draft and `production/qa/qa-plan-[sprint]-[date].md` to the parent for inclusion in the one consolidated complete changeset approval. Do not write from the delegated task.

### Phase 4: Test Case Writing (qa-tester)

> **Smoke check** is performed as part of Phase 2 (QA Strategy). If the smoke check returned FAIL in Phase 2, the cycle was stopped there. This phase only runs when the Phase 2 smoke check was PASS, PASS WITH WARNINGS, or UNKNOWN.

For each story requiring manual QA (Visual/Feel, UI, Integration without automated tests):

Delegate to `qa-tester` through Codex custom-agent delegation for each story (run in parallel where possible), providing:
- The story file path
- The relevant section of the QA plan for that story
- The GDD acceptance criteria for the system being tested (if available)
- Instructions to draft detailed test cases covering all acceptance criteria

Each test case set should include:
- **Preconditions**: game state required before testing begins
- **Steps**: numbered, unambiguous actions
- **Expected Result**: what should happen
- **Actual Result**: field left blank for the tester to fill in
- **Pass/Fail**: field left blank

Present the test cases to the user for review before execution, one story per turn.

Use `request_user_input` for one story, wait for the answer, then continue to the next story:

```
question: "Test cases ready for [Story]. Review before manual QA begins?"
options:
  - "Approved — begin manual QA for this story"
  - "Revise this story's test cases"
  - "Skip this story — not ready"
```

### Phase 5: Manual QA Execution

Walk through each story in the approved manual QA list, one story per turn.

Use `request_user_input` for the current story and wait before moving to another:

```
question: "Manual QA — [Story Title]\n[brief description of what to test]"
options:
  - "PASS — all acceptance criteria verified"
  - "FAIL — criteria not met (describe after)"
  - "BLOCKED — cannot test yet (reason)"
```

After PASS, ask separately whether there are non-blocking notes and wait for that answer before the next story.

After each FAIL result: use `request_user_input` to collect the failure description, then delegate to `qa-tester` to return a formal bug-report draft plus its exact intended path in `production/qa/bugs/`. Do not write it yet.

Bug report naming: `BUG-[NNN]-[short-slug].md` (increment NNN from existing bugs in the directory).

After collecting all results, summarize:
- Stories PASS: [count]
- Stories PASS WITH NOTES: [count]
- Stories FAIL: [count] — bugs filed: [IDs]
- Stories BLOCKED: [count]

### Phase 6: QA Sign-Off Report

Delegate to `qa-lead` through Codex custom-agent delegation to produce the sign-off report using all results from Phases 4–6.

The sign-off report format:

```markdown
## QA Sign-Off Report: [Sprint/Feature]
**Date**: [date]

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
- **APPROVED**: All stories PASS or PASS WITH NOTES; no S1/S2 bugs open
- **APPROVED WITH CONDITIONS**: S3/S4 bugs open, or PASS WITH NOTES issues documented; no S1/S2 bugs
- **NOT APPROVED**: Any S1/S2 bugs open; or stories FAIL without documented workaround

Next step guidance by verdict:
- APPROVED: "Build is ready for the next phase. Run `$codex-game-studios:gate-check` to validate advancement."
- APPROVED WITH CONDITIONS: "Resolve conditions before advancing. S3/S4 bugs may be deferred to polish."
- NOT APPROVED: "Resolve S1/S2 bugs and re-run `$codex-game-studios:team-qa` or targeted manual QA before advancing."

Return the sign-off draft and `production/qa/qa-signoff-[sprint]-[date].md` to the parent for inclusion in the one consolidated complete changeset approval. Do not write from the delegated task.

## Parent Changeset Gate

The parent synthesizes the QA plan, test cases, bug-report drafts, sign-off report, and session update before any file mutation. Present one complete proposal containing exact file paths, exact diffs, tests and evidence, and all session-state, report, and milestone writes (use `None` where no such write exists). Obtain approval for the whole changeset; a new bug path, report path, or material change requires a revised proposal.

## Approved Execution

Only after approval may the parent write or delegate the exact approved QA artifacts and session update. No subagent commits, publishes, or expands scope. Every delegate receives only its approved paths and content; manual QA evidence remains attributable to the parent run.

## Error Recovery Protocol

If any delegated agent (through Codex custom-agent delegation) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** via request_user_input with choices:
   - Skip this agent and note the gap in the final report
   - Retry with narrower scope
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. Never discard work because one agent blocked.

Common blockers:
- Input file missing (story not found, GDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; run `$codex-game-studios:architecture-decision` first
- Scope too large → split into two stories via `$codex-game-studios:create-stories`
- Conflicting instructions between ADR and story → surface the conflict, do not guess

## Output

A summary covering: stories in scope, smoke check result, manual QA results, bugs filed (with IDs and severities), and the final APPROVED / APPROVED WITH CONDITIONS / NOT APPROVED verdict.

Verdict: **COMPLETE** — QA cycle finished.
Verdict: **BLOCKED** — smoke check failed or critical blocker prevented cycle completion; partial report produced.

## Session State Update

Only when `production/session-state/active.md` and this exact comment were listed in the approved changeset, the parent appends after the sign-off report is saved. Never append silently, and do not change session state for a draft-only or unapproved BLOCKED result.

```
<!-- QA RUN: [date] | Sprint: [sprint identifier or "ad-hoc"] | Verdict: [PASS/FAIL/CONCERNS] | Report: production/qa/qa-signoff-[sprint]-[date].md -->
```
