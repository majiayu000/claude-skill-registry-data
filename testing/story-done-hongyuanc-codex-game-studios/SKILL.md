---
name: story-done
description: "Use when an implemented story needs evidence-backed acceptance, deviation, test, review, and completion gating."
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

### Native readiness gate for `$codex-game-studios:team-qa`

Before invoking or routing to `$codex-game-studios:team-qa`, confirm that `team-qa` is present in the current task's available skill catalog. If unavailable, report
`Staged dependency: $codex-game-studios:team-qa is not available`, defer the handoff, do not invoke `$codex-game-studios:team-qa`, do not route to `$codex-game-studios:team-qa`, and do not search for or copy a repository-local skill file.

# Story Done

This skill closes the loop between design and implementation. Run it at the end
of implementing any story. It ensures every acceptance criterion is verified
before the story is marked done, GDD and ADR deviations are explicitly
documented rather than silently introduced, code review is prompted rather than
forgotten, and the story file reflects actual completion status.

**Output:** Updated story file (Status: Complete) + surfaced next story.

---

## Phase 1: Find the Story

Resolve the review mode (once, store for all gate spawns this run):
1. If `--review [full|lean|solo]` was passed → use that
2. Else read `.codex/studio.toml` and use its `review_mode` value
3. Map `review_mode = "phase-gated"` to lean optional-review depth; mandatory director gates still run. Never use a competing persistent setting

See `../../../.codex/docs/director-gates.md` for the full check pattern.

**If a file path is provided** (e.g., `$codex-game-studios:story-done production/epics/core/story-damage-calculator.md`):
read that file directly.

**If no argument is provided:**

1. Check `production/session-state/active.md` for the currently active story.
2. If not found there, read the most recent file in `production/sprints/` and
   look for stories marked IN PROGRESS.
3. If multiple in-progress stories are found, use `request_user_input`:
   - "Which story are we completing?"
   - Options: list the in-progress story file names.
4. If no story can be found, ask the user to provide the path.

---

## Phase 2: Read the Story

Read the full story file. Extract and hold in context:

- **Story name and ID**
- **GDD Requirement TR-ID(s)** referenced (e.g., `TR-combat-001`)
- **Manifest Version** embedded in the story header (e.g., `2026-03-10`)
- **ADR reference(s)** referenced
- **Acceptance Criteria** — the complete list (every checkbox item)
- **Implementation files** — files listed under "files to create/modify"
- **Story Type** — the `Type:` field from the story header (Logic / Integration / Visual/Feel / UI / Config/Data)
- **Engine notes** — any engine-specific constraints noted
- **Definition of Done** — if present, the story-level DoD
- **Estimated vs actual scope** — if an estimate was noted

Also read:
- `docs/architecture/tr-registry.yaml` — look up each TR-ID in the story.
  Read the *current* `requirement` text from the registry entry. This is the
  source of truth for what the GDD required — do not use any requirement text
  that may be quoted inline in the story (it may be stale).
- The referenced GDD section — just the acceptance criteria and key rules, not
  the full document. Use this to cross-check the registry text is still accurate.
- The referenced ADR(s) — just the Decision and Consequences sections
- `docs/architecture/control-manifest.md` header — extract the current
  `Manifest Version:` date (used in Phase 4 staleness check)

---

## Pre-Verification Criterion-ID Backfill

Before evidence verification, inspect every acceptance criterion for a stable ID.
No evidence verification may begin while any criterion lacks one.

For legacy criteria without IDs, draft a separately authorized complete changeset
that:

- assigns stable criterion IDs in story order without renumbering existing IDs;
- updates the story's exact evidence references to include those IDs when needed;
- updates only the exact existing evidence files whose criterion attribution must
  be backfilled; and
- lists the story and every evidence path before requesting approval.

Show the ID mapping and file-level edits, then request one approval. If approved,
apply only that metadata/evidence backfill and restart verification from Phase 2
using the updated files. If declined, report BLOCKED and stop. This backfill happens
before any COMPLETE verdict and is never a circular write after completion.

---

## Phase 3: Verify Acceptance Criteria

For each acceptance criterion in the story, attempt verification using one of
three methods:

### Automatic verification (run without asking)

- **File existence check**: `file search` for files the story said would be created.
- **Test pass check**: if a test file path is mentioned, run it via `the shell`.
- **No hardcoded values check**: `repository search` for numeric literals in gameplay code
  paths that should be in config files.
- **No hardcoded strings check**: `repository search` for player-facing strings in `src/`
  that should be in localization files.
- **Dependency check**: if a criterion says "depends on X", check that X exists.

### Manual verification with confirmation (use `request_user_input`)

- Criteria about subjective qualities ("feels responsive", "animations play correctly")
- Criteria about gameplay behaviour ("player takes damage when...", "enemy responds to...")
- Performance criteria ("completes within Xms") — require profiler or benchmark evidence at the story's declared evidence path; never accept performance as assumed

Ask about one manual criterion at a time. Wait for the answer before asking about the next criterion:

```
question: "Does [criterion]?"
options: "Yes — passes", "No — fails", "Not tested yet"
```

### Unverifiable (blocking until evidence exists)

- Criteria that require a full game build to test (end-to-end gameplay scenarios)
- Mark as: `DEFERRED — requires playtest session`. A deferred criterion remains unverified and blocks completion.

### Test-Criterion Traceability

After completing the pass/fail/deferred check above, map each acceptance
criterion to the test that covers it:

For each acceptance criterion in the story:

1. Ask: is there a test — unit, integration, or confirmed manual playtest — that
   directly verifies this criterion?
   - **Unit or integration test**: use only the exact path declared by the story and map the criterion ID to a passing test function or assertion.
   - **Manual evidence**: a conversational confirmation is not durable test evidence. Require the exact canonical evidence file declared by the story, with the criterion ID and passing verdict recorded.

2. Produce a traceability table:

```
| Criterion | Test | Status |
|-----------|------|--------|
| AC-1: [criterion text] | tests/unit/test_foo.gd::test_bar | COVERED |
| AC-2: [criterion text] | production/qa/evidence/[slug]-evidence.md#AC-2 | COVERED |
| AC-3: [criterion text] | — | UNTESTED |
```

3. Apply these escalation rules:

   - If **>50% of criteria are UNTESTED**: escalate to **BLOCKING** — test
     coverage is insufficient to confirm the story is actually done. The verdict
     in Phase 6 cannot be COMPLETE until coverage improves.
   - If **any criteria are UNTESTED**: mark the story BLOCKED until the required
     evidence exists. Include every missing item in the report.
   - If **all criteria are COVERED**: no action needed beyond including the
     table in the report.

### Test Evidence Requirement

Based on the Story Type extracted in Phase 2, check for required evidence:

Evidence is valid only when all of these checks pass:

1. **Exact location and type**: use the exact required evidence path and evidence type declared in the story. A nearby file or a different evidence type does not substitute.
2. **Attribution**: the evidence names the story ID and every covered criterion ID; mention-only matches do not count. For older criteria without IDs, assign stable criterion IDs before closure.
3. **Required schema**: automated evidence maps criterion IDs to named tests and current results; manual evidence records story ID, criterion IDs, build/engine, steps, observed result, date, verdict, and required sign-off rows.
4. **Freshness**: the test run or evidence date must be at or after the story's `Last Updated:` date and cover the current implementation. Missing or stale freshness metadata is BLOCKING.
5. **Passing verdict**: automated commands must exit successfully and manual, smoke, or playtest evidence must state PASS or APPROVED. Existence alone is never enough.

| Story Type | Required Evidence | Gate Level |
|---|---|---|
| **Logic** | Automated unit test in `tests/unit/[system]/` — must exist and pass | BLOCKING |
| **Integration** | Integration test in `tests/integration/[system]/` OR playtest evidence in `production/qa/evidence/` | BLOCKING |
| **Visual/Feel** | Screenshot + sign-off in `production/qa/evidence/` | BLOCKING |
| **UI** | Manual walkthrough doc OR interaction test in `production/qa/evidence/` | BLOCKING |
| **Config/Data** | Exact per-story smoke evidence at `production/qa/evidence/[story-id]-smoke-evidence.md` | BLOCKING |

**For Logic stories**: read the story's **Test Evidence** section to extract the
exact required file path. Require that file, run its current test command, and map every
criterion ID to a passing named test. If the exact file is absent or any mapping/run fails:
- Flag as **BLOCKING**: "Logic story has no unit test file. Story requires it at
  `[exact-path-from-Test-Evidence-section]`. Create and run the test before marking
  this story Complete."

**For Integration stories**: read the story's **Test Evidence** section for its exact
required path and evidence type. Require that exact integration test or exact canonical
playtest evidence file. Validate story/criterion attribution, required schema, freshness,
and passing verdict. Missing or invalid evidence is BLOCKING.

**For Visual/Feel and UI stories**: extract the exact canonical
`production/qa/evidence/[story-slug]-evidence.md` path from the story. Require that
exact file, not another file that merely references the story. Validate the story ID,
all covered criterion IDs, required schema, freshness, passing verdict, and every required
sign-off row. Any missing field, stale result, unchecked required sign-off, or non-passing
verdict is BLOCKING. For solo developers, one person may fill multiple required roles,
but each required row must still be signed.

**For Config/Data stories**: extract the exact `production/qa/evidence/[story-id]-smoke-evidence.md` path declared in the story.
Require that exact evidence file to name the story ID and criterion IDs, satisfy the smoke-evidence
schema, be fresh for the current implementation, and contain a PASS verdict. Otherwise
flag it as BLOCKING and run `$codex-game-studios:smoke-check` to produce the declared evidence.

**If no Story Type is set**: flag as **BLOCKING** —
"Story Type not declared. Add `Type: [Logic|Integration|Visual/Feel|UI|Config/Data]`
to the story header to enable test evidence gate enforcement in future stories."

Any test evidence gap prevents the COMPLETE verdict in Phase 6.

---

## Phase 4: Check for Deviations

Compare the implementation against the design documents.

Run these checks automatically:

1. **GDD rules check**: Using the current requirement text from `tr-registry.yaml`
   (looked up by the story's TR-ID), check that the implementation reflects what
   the GDD actually requires now — not what it required when the story was written.
   `repository search` the implemented files for key function names, data structures, or class
   names mentioned in the current GDD section.

2. **Manifest version staleness check**: Compare the `Manifest Version:` date
   embedded in the story header against the `Manifest Version:` date in the
   current `docs/architecture/control-manifest.md` header.
   - If they match → pass silently.
   - If the story's version is older → flag as ADVISORY:
     `ADVISORY: Story was written against manifest v[story-date]; current manifest
     is v[current-date]. New rules may apply. Run $codex-game-studios:story-readiness to check.`
   - If control-manifest.md does not exist → skip this check.

3. **ADR constraints check**: Read the referenced ADR's Decision section. Check
   for forbidden patterns from `docs/architecture/control-manifest.md` (if it
   exists). `repository search` for patterns explicitly forbidden in the ADR.

4. **Hardcoded values check**: `repository search` the implemented files for numeric literals
   in gameplay logic that should be in data files.

5. **Scope check**: Did the implementation touch files outside the story's stated
   scope? (files not listed in "files to create/modify")

For each deviation found, categorize:

- **BLOCKING** — implementation contradicts the GDD or ADR (must fix before
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

After completing the deviation checks in Phase 4, spawn `qa-lead` through Codex custom-agent delegation using gate **QL-TEST-COVERAGE** (`../../../.codex/docs/director-gates.md`).

Pass:
- The story file path and story type
- Test file paths found during Phase 3 (exact paths, or "none found")
- The story's `## QA Test Cases` section (the pre-written test specs from story creation)
- The story's `## Acceptance Criteria` list

The qa-lead reviews whether the tests actually cover what was specified — not just whether files exist.

Apply the verdict:
- **ADEQUATE** → proceed to Phase 5
- **GAPS** → flag as **BLOCKING** when any required criterion lacks coverage; list the exact missing evidence.
- **INADEQUATE** → flag as **BLOCKING**: "QA lead: critical logic is untested. Verdict cannot be COMPLETE until coverage improves. Specific gaps: [list]."

Skip this phase for Config/Data stories (no code tests required).

---

## Phase 5: Lead Programmer Code Review Gate

**Review mode check** — apply before spawning LP-CODE-REVIEW:
- `solo` → skip. Note: "LP-CODE-REVIEW skipped — Solo mode." Proceed to Phase 6 (completion report).
- `lean` → use `request_user_input` before proceeding:
  - Prompt: "Code review is skipped in lean mode. Did you run `$codex-game-studios:code-review` on the implemented files?"
  - Options:
    - `Yes — $codex-game-studios:code-review passed or was approved with suggestions`
    - `No — skipping code review for this story`
    - `No — I'll run $codex-game-studios:code-review before the sprint close-out`
  - Record the answer in the completion notes (Phase 7). All three options proceed to Phase 6.
- `full` → spawn as normal.

Spawn `lead-programmer` through Codex custom-agent delegation using gate **LP-CODE-REVIEW** (`../../../.codex/docs/director-gates.md`).

Pass: implementation file paths, story file path, relevant GDD section, governing ADR.

Present the verdict to the user. If CONCERNS, surface them via `request_user_input`:
- Options: `Revise flagged issues` / `Accept and proceed` / `Discuss further`
If REJECT, do not proceed to Phase 6 verdict until the issues are resolved.

If the story has no implementation files yet (verdict is being run before coding is done), skip this phase and note: "LP-CODE-REVIEW skipped — no implementation files found. Run after implementation is complete."

---

## Phase 6: Present the Completion Report

Before updating any files, present the full report:

```markdown
## Story Done: [Story Name]
**Story**: [file path]
**Date**: [today]

### Acceptance Criteria: [X/Y passing]
- [x] [Criterion 1] — auto-verified (test passes)
- [x] [Criterion 2] — validated by `[exact evidence path]#[criterion ID]`
- [ ] [Criterion 3] — FAILS: [reason]
- [?] [Criterion 4] — DEFERRED: requires playtest

### Test-Criterion Traceability
| Criterion | Test | Status |
|-----------|------|--------|
| AC-1: [text] | [test file::test name] | COVERED |
| AC-2: [text] | production/qa/evidence/[slug]-evidence.md#AC-2 | COVERED |
| AC-3: [text] | — | UNTESTED |

### Test Evidence
**Story Type**: [Logic | Integration | Visual/Feel | UI | Config/Data | Not declared]
**Required evidence**: [unit test file | integration test or playtest | screenshot + sign-off | walkthrough doc | smoke check pass]
**Evidence found**: [VALID — `[exact path]`, fresh, attributable, PASS | BLOCKING — reason]

### Deviations
[NONE] OR:
- BLOCKING: [description] — [GDD/ADR reference]
- ADVISORY: [description] — user accepted / flagged for tech debt

### Scope
[All changes within stated scope] OR:
- Extra files touched: [list] — [note whether valid or scope creep]

### Verdict: COMPLETE / COMPLETE WITH NOTES / BLOCKED
```

**Verdict definitions:**
- **COMPLETE**: all criteria pass, every required test passes, all required evidence exists, and no blocking deviations remain
- **COMPLETE WITH NOTES**: the COMPLETE conditions hold and advisory deviations are documented
- **BLOCKED**: any criterion is unverified, any required test fails, required evidence is missing, or a blocking deviation remains

Never mark the story Complete while any acceptance criterion is unverified, any required test is failing, or required test evidence is missing.

If the verdict is **BLOCKED**: do not proceed to Phase 7. List what must be
fixed. Offer to help fix the blocking items.

---

## Phase 7: Update Story Status

Do not enter this phase unless the verdict satisfies the COMPLETE conditions above.

First ask one decision: whether to close the verified story or stop without changes. Wait for the answer. If the user chooses closure and advisory deviations exist, ask a second decision on a later turn: whether to include `docs/tech-debt-register.md` in the closure changeset.

Before writing, show one complete proposed changeset containing the story file, `production/sprint-status.yaml` when present, `production/session-state/active.md`, and the tech-debt register only when selected. Request one approval for that list. Do not add files after approval.

1. Update the status field: `Status: Complete`
2. Update the `Last Updated:` field in the story header to today's date (format: `YYYY-MM-DD`). If the field does not exist, add it after the `Status:` line.
3. Add a `## Completion Notes` section at the bottom:

```markdown
## Completion Notes
**Completed**: [date]
**Criteria**: [X/Y passing] ([any deferred items listed])
**Deviations**: [None] or [list of advisory deviations]
**Test Evidence**: [exact validated path, evidence type, freshness date, and passing verdict]
**Code Review**: [Pending / Complete / Skipped]
```

4. If the user chose "Close and log tech debt": append each advisory deviation to `docs/tech-debt-register.md` in this format:
   ```
   - **[date]** ([story title]): [deviation description] — tracked from [story file path]
   ```
   Create the file with a `# Tech Debt Register` heading if it does not exist.

5. **Update `production/sprint-status.yaml`** (if it exists):
   - Find the entry matching this story's file path or ID
   - Set `status: done` and `completed: [today's date]`
   - Update the top-level `updated` field
   - This is a silent update — no extra approval needed (already approved in step above)

6. **Suggest a git commit**: Output a ready-to-use commit command covering the implementation files from the dev-story summary and the updated story file:

```
Suggested commit:
git add [src/ and tests/ files changed during implementation] [story-file-path]
git commit -m "feat: [story title] ([TR-ID])"
```

The `validate-commit.sh` hook will verify design doc references and check for hardcoded values automatically.

### Session State Update

After updating the story file, append to the already listed and approved
`production/session-state/active.md` path:

    ## Session Extract — $codex-game-studios:story-done [date]
    - Verdict: [COMPLETE / COMPLETE WITH NOTES / BLOCKED]
    - Story: [story file path] — [story title]
    - Tech debt logged: [N items, or "None"]
    - Next recommended: [next ready story title and path, or "None identified"]

If `active.md` does not exist, create it with this block as the initial content.
Confirm in conversation: "Session state updated."

---

## Phase 8: Surface the Next Story

After completion, help the developer keep momentum:

1. Read the current sprint plan from `production/sprints/`.
2. Find stories that are:
   - Status: READY or NOT STARTED
   - Not blocked by other incomplete stories
   - In the Must Have or Should Have tier

Present:

```
### Next Up
The following stories are ready to pick up:
1. [Story name] — [1-line description] — Est: [X hrs]
2. [Story name] — [1-line description] — Est: [X hrs]

Run `$codex-game-studios:story-readiness [path]` to confirm a story is implementation-ready
before starting.
```

If no more Must Have stories remain in this sprint (all are Complete or Blocked):

```
### Sprint Close-Out Sequence

All Must Have stories are complete. QA sign-off is required before advancing.
Run these in order:

1. `$codex-game-studios:smoke-check sprint` — verify the critical path still works end-to-end
2. `$codex-game-studios:team-qa sprint` — full QA cycle: test case execution, bug triage, sign-off report
3. `$codex-game-studios:retrospective` — capture what went well, what didn't, and action items for the next sprint
4. `$codex-game-studios:gate-check` — advance to the next phase once QA approves (only if advancing a phase)
5. `$codex-game-studios:sprint-plan new` — plan the next sprint, incorporating velocity data and retrospective action items

Do not run `$codex-game-studios:gate-check` until `$codex-game-studios:team-qa` returns APPROVED or APPROVED WITH CONDITIONS.
```

If there are Should Have stories still unstarted, surface them alongside the close-out sequence so the user can choose: close the sprint now, or pull in more work first.

If no more stories are ready but Must Have stories are still In Progress (not Complete):
"No more stories ready to start — [N] Must Have stories still in progress. Continue implementing those before sprint close-out."

---

## Collaborative Protocol

- **Never mark a story complete without user approval** — Phase 7 requires an
  explicit "yes" before any file is edited.
- **Never auto-fix failing criteria** — report them and ask what to do.
- **Deviations are facts, not judgments** — present them neutrally; the user
  decides if they are acceptable.
- **BLOCKED cannot be overridden into Complete** — resolve or explicitly revise the governing story/design first.
- Use `request_user_input` for the code review prompt and ask manual criteria one at a time.

---

## Recommended Next Steps

- Run `$codex-game-studios:story-readiness [next-story-path]` to validate the next story before starting implementation
- If all Must Have stories are complete: run `$codex-game-studios:smoke-check sprint` → `$codex-game-studios:team-qa sprint` → `$codex-game-studios:gate-check`
- If tech debt was logged: track it via `$codex-game-studios:tech-debt` to keep the register current
