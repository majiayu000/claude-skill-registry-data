---
name: qa-plan
description: "Use when a sprint, feature, or story needs test scope, evidence requirements, manual cases, smoke coverage, and QA ownership before implementation."
---

<!-- codex-studio-delegation: governed -->
Resolve every role through `../../../.codex/docs/plugin-agent-delegation.md`;
do not require a repository-local `.codex/agents/` or `.codex/agent-packs/` tree.
Before default delegation, run `python3 ../../../tools/codex_studio/agent_delegation.py resolve --project-root <project-root> --role <role>` and use only its returned role contract.

## Codex Interaction Contract

- Ask one decision question per turn and wait for the answer before asking another.
- Use `request_user_input` for structured choices when it is available; otherwise ask the same concise question directly.
- Use Codex custom agents by role and profile when delegation is useful.
- Treat any approved write as one complete proposed changeset. Do not add unlisted files or behavior; pause and request a new approval if scope expands.

# QA Plan

This skill generates a structured QA plan for a sprint, feature, or individual
story. It reads all in-scope story files and their referenced GDDs, classifies
each story by test type, and produces a plan that tells developers exactly what
to automate, what to verify manually, what the smoke test scope is, and when
to bring in a playtester.

Run this before a sprint begins so the team knows upfront what testing work
is required. A test plan written after implementation is a post-mortem, not a
plan.

**Output:** `production/qa/qa-plan-[sprint-slug]-[date].md`

---

## Phase 1: Parse Scope

**Argument:** use the invocation text supplied with the skill (blank = ask the user).

Determine scope from the argument:

- **`sprint-draft`** — consume the current in-memory sprint draft and story scope supplied directly by `$codex-game-studios:sprint-plan`. Treat that draft as authoritative for this run; never select the most recent persisted sprint. Return the QA plan draft to the caller without writing or requesting a separate approval.
- **`sprint: [explicit-path]`** — read only the explicitly named current sprint file. A bare `sprint` invocation must ask for the intended path; it must not guess from modification time.
- **`feature: [system-name]`** — glob `production/epics/*/story-*.md`, filter
  to stories whose file path or title contains the system name. Also check the
  epic index file (`EPIC.md`) in that system's directory.
- **`story: [path]`** — validate that the path exists and load that single file.
- **No argument** — use `request_user_input`:
  - "What is the scope for this QA plan?"
  - Options: "Current sprint", "Specific feature or epic (enter name)",
    "Specific story (enter path)"

After resolving scope, report: "Building QA plan for [N] stories in [scope]."

If a story file path is referenced but the file does not exist, note it as
MISSING and continue with the remaining stories. Do not fail the entire plan
for one missing file.

---

## Phase 2: Load Inputs

For each in-scope story file, read the full file and extract:

- **Story title** and story ID (from filename or header)
- **Story Type** field (if present in the file header — e.g., `Type: Logic`)
- **Acceptance criteria** — the complete numbered/bulleted list
- **Implementation files** — listed under "Files to Create / Modify" or similar
- **Engine notes** — any engine API warnings or version-specific notes
- **GDD reference** — the GDD path(s) cited
- **ADR reference** — the ADR(s) cited
- **Estimate** — hours or story points if present
- **Dependencies** — other stories this one depends on

After reading stories, load supporting context once (not per story):

- `design/gdd/systems-index.md` — to understand system priorities and which
  GDDs are approved
- For each unique GDD referenced across all stories: read the
  **Acceptance Criteria**, **Formulas**, and **Edge Cases** sections. Do not load
  the full GDD text. These three sections contain the testable requirements, the math
  to verify, and the boundary conditions that tests must cover. If an Edge Cases
  section is absent from the GDD, note it per GDD: "No Edge Cases section found — edge
  case coverage will be inferred from acceptance criteria only."
- `docs/architecture/control-manifest.md` — scan for forbidden patterns that
  automated tests should guard against (if the file exists)

If no GDD is referenced in a story, note it as a gap but do not block the plan.
The story will be classified using acceptance criteria alone.

---

## Phase 3: Classify Each Story

For each story, assign a Story Type:

- **If the story already has a `Type:` field in its header**: accept it as-is. Do NOT re-classify or validate against the criteria below — the Type was set by lead-programmer at story creation and is authoritative. Record it as-is.
- **If the `Type:` field is missing**: infer the type from the acceptance criteria using the table below, and note in the report that the type was inferred (not declared). Flag this as a gap — the story should have its Type declared explicitly before implementation begins.

| Story Type | Classification Indicators |
|---|---|
| **Logic** | Acceptance criteria reference calculations, formulas, numerical thresholds, state transitions, AI decisions, data validation, buff/debuff stacking, economy transactions, or any testable computation |
| **Integration** | Criteria involve two or more systems interacting, signals or events propagating across system boundaries, save/load round-trips, network sync, or persistence |
| **Visual/Feel** | Criteria reference animation behaviour, VFX, shader output, "feels responsive", perceived timing, screen shake, particle effects, audio sync, or visual feedback quality |
| **UI** | Criteria reference menus, HUD elements, buttons, screens, dialogue boxes, inventory panels, tooltips, or any player-facing interface element |
| **Config/Data** | Changes are limited to balance tuning values, data files, or configuration — no new code logic is involved |

**Mixed stories** (e.g., a story that adds both a formula and a UI display):
assign the primary type based on which acceptance criteria carry the highest
implementation risk, and note the secondary type. Mixed Logic+Integration or
Visual+UI combinations are the most common.

After classifying all stories, produce a classification summary table in
conversation before proceeding to Phase 4. This gives the user visibility into
how tests will be allocated.

---

## Phase 4: Generate Test Plan

Assemble the full QA plan document. Use this structure:

````markdown
# QA Plan: [Sprint/Feature Name]
**Date**: [date]
**Generated by**: $codex-game-studios:qa-plan
**Scope**: [N stories across [N systems]]
**Engine**: [engine name from .codex/docs/technical-preferences.md, or "Not configured"]
**Sprint File**: [path to sprint plan if applicable]

---

## Test Summary

| Story | Type | Automated Test Required | Manual Verification Required |
|-------|------|------------------------|------------------------------|
| [story title] | Logic | Unit test — `tests/unit/[system]/` | None |
| [story title] | Integration | Integration test — `tests/integration/[system]/` | Smoke check |
| [story title] | Visual/Feel | None (not automatable) | Screenshot + lead sign-off |
| [story title] | UI | Interaction walkthrough | Manual step-through |
| [story title] | Config/Data | Data validation test | Spot-check in-game values |

---

## Automated Tests Required

### [Story Title] — [Type]
**Test file path**: `tests/[unit|integration]/[system]/[story-slug]_test.[ext]`
**What to test**:
- [Specific formula or rule from the GDD Formulas section]
- [Each named state transition or decision branch]
- [Each side effect that should or should not occur]

**Edge cases to cover**:
- Zero/minimum input values (e.g., 0 damage, empty inventory)
- Maximum/boundary input values (e.g., max level, stat cap)
- Invalid or null input (e.g., missing target, dead entity)
- [Any edge case explicitly called out in the GDD Edge Cases section]

**Estimated test count**: ~[N] unit tests

[If no GDD formula reference was found for this story, note:]
*No formula found in referenced GDD — test cases must be derived from acceptance
criteria directly. Review the GDD Formulas section before writing tests.*

---

## Manual QA Checklist

### [Story Title] — [Type]
**Verification method**: [Screenshot + designer sign-off | Playtest session |
Manual step-through | Comparison against reference footage]
**Who must sign off**: [designer / lead-programmer / qa-lead / art-lead]
**Evidence to capture**: [screenshot of X | video clip of Y | written playtest
notes | side-by-side comparison]

Checklist:
- [ ] [Specific observable condition — concrete and falsifiable]
- [ ] [Another condition]
- [ ] [Every acceptance criterion translated into a manual check item]

*If any criterion uses subjective language ("feels", "looks", "seems"), it must
be supplemented with a specific benchmark or a playtest protocol note.*

---

## Smoke Test Scope

Critical paths to verify before any QA hand-off for this sprint:

1. Game launches to main menu without crash
2. New game / new session can be started
3. [Primary mechanic introduced or changed this sprint]
4. [Any system with a regression risk from this sprint's changes]
5. Save / load cycle completes without data loss (if save system exists)
6. Performance is within budget on target hardware (no new frame spikes)

*Smoke tests are verified by the developer via `$codex-game-studios:smoke-check`. Reference this
list when running that skill.*

---

## Playtest Requirements

| Story | Playtest Goal | Min Sessions | Target Player Type |
|-------|--------------|--------------|-------------------|
| [story] | [What question must the session answer?] | [N] | [new player / experienced] |

**Sign-off requirement**: Playtest notes must be written to
`production/session-logs/playtest-[sprint]-[story-slug].md` and reviewed by
the [designer / qa-lead] before the story can be marked COMPLETE.

If no stories require playtest validation: *No playtest sessions required for
this sprint.*

---

## Definition of Done — This Sprint

A story is DONE when ALL of the following are true:

- [ ] All acceptance criteria verified — via automated test result OR documented
      manual evidence (screenshot, video, or playtest notes with sign-off)
- [ ] Test file exists at the specified path for all Logic and Integration stories
- [ ] Manual evidence document exists for all Visual/Feel and UI stories
- [ ] Smoke check passes (run `$codex-game-studios:smoke-check sprint` before QA hand-off)
- [ ] No regressions introduced
- [ ] Code reviewed (via `$codex-game-studios:code-review` or documented peer review)
- [ ] Story file updated to `Status: Complete` (via `$codex-game-studios:story-done`)
````

When generating content, use the actual story titles, GDD formula text, and
acceptance criteria extracted in Phase 2. Do not use placeholder text — every
test entry should reflect the real requirements of these specific stories.

---

## Phase 5: Write Output

**Embedded `sprint-draft` mode:** return the complete QA plan draft and its exact
`production/qa/qa-plan-sprint-[N]-[date].md` target to `$codex-game-studios:sprint-plan`. Do not
write, update session state, backfill stories, or request approval. `$codex-game-studios:sprint-plan`
owns the combined complete changeset approval.

Show the complete plan in conversation (or a summary if it is very long). First ask one decision question: whether the proposed changeset should contain only the QA plan and session-state record, or also the listed story backfills. Wait for the answer.

Then show one complete proposed changeset containing:

- `production/qa/qa-plan-[sprint-slug]-[date].md`
- `production/session-state/active.md`
- every story file selected for backfill, when that option was chosen

Ask one approval question for that exact list. If approved, write the plan exactly as generated and apply only the listed backfills. For each listed Logic or Integration story, replace `## QA Test Cases` with the Phase 4 specs, or append it before `## Test Evidence` when absent. For listed Visual/Feel and UI stories, write the manual verification steps. Do not touch unlisted stories.

After writing:

"QA plan written to `production/qa/qa-plan-[sprint-slug]-[date].md`.

Next steps:
- Share this plan with the team before sprint implementation begins
- Once all sprint stories are implemented, run `$codex-game-studios:smoke-check sprint` to gate QA hand-off — not yet, only after implementation is complete
- For Logic/Integration stories, create the test files at the listed paths
  before marking stories done — `$codex-game-studios:story-done` checks for them"

Append the following to the already approved `production/session-state/active.md` path (create it if needed):

```
<!-- QA-PLAN: [date] | System: [system/sprint identifier] | Plan written: production/qa/qa-plan-[identifier]-[date].md -->
```

---

## Collaborative Protocol

- **Never write the plan without asking** — Phase 5 requires explicit approval.
- **Classify conservatively**: when a story is ambiguous between Logic and
  Integration, classify it as Integration — it requires both unit and
  integration tests.
- **Do not invent test cases** beyond what acceptance criteria and GDD formulas
  support. If a formula is absent from the GDD, flag it rather than guessing.
- **Playtest requirements are advisory**: the user decides whether a playtest
  is warranted for borderline Visual/Feel stories. Flag the case; do not mandate.
- Use `request_user_input` for scope selection when no argument is provided.
  Keep all other phases non-interactive — present findings, then ask once to
  approve the write.
