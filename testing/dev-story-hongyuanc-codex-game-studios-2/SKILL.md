---
name: dev-story
description: "Use when an implementation-ready story has been approved for bounded source, test, and evidence work."
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

# Dev Story

This skill bridges planning and code. It reads a story file in full, assembles
all the context a programmer needs, routes to the correct specialist agent, and
drives implementation to completion — including writing the test.

**The loop for every story:**
```
$codex-game-studios:qa-plan sprint           ← define test requirements before sprint begins
$codex-game-studios:story-readiness [path]   ← validate before starting
$codex-game-studios:dev-story [path]         ← implement it  (this skill)
$codex-game-studios:code-review [files]      ← review it
$codex-game-studios:story-done [path]        ← verify and close it
```

**After all sprint stories are done:** run `$codex-game-studios:team-qa sprint` to execute the full QA cycle and get a sign-off verdict before advancing the project stage.

**Output:** Source code + test file in the project's `src/` and `tests/` directories.

---

## Phase 1: Find the Story

**If a path is provided**: read that file directly.

**If no argument**: check `production/session-state/active.md` for the active
story. If found, confirm: "Continuing work on [story title] — is that correct?"
If not found, ask: "Which story are we implementing?" file search
`production/epics/**/*.md` and list stories with Status: Ready.

---

## Phase 2: Load Full Context

**Before loading any context, verify required files exist.** Extract the ADR path from the story's `ADR Governing Implementation` field, then check:

| File | Path | If missing |
|------|------|------------|
| TR registry | `docs/architecture/tr-registry.yaml` | **STOP** — "TR registry not found at `docs/architecture/tr-registry.yaml`. Run `$codex-game-studios:architecture-review` to bootstrap the registry from your GDDs and ADRs." |
| Governing ADR | path from story's ADR field | **STOP** — "ADR file [path] not found. Run `$codex-game-studios:architecture-decision` to create it, or correct the filename in the story's ADR field." |
| Control manifest | `docs/architecture/control-manifest.md` | **WARN and continue** — "Control manifest not found — layer rules cannot be checked. Run `$codex-game-studios:create-control-manifest`." |

If the TR registry or governing ADR is missing, report the story as **BLOCKED** and stop. Do not change the story, sprint status, or session state.

Read all of the following simultaneously — these are independent reads. Do not start implementation until all context is loaded:

### The story file
Extract and hold:
- **Story title, ID, layer, type** (Logic / Integration / Visual/Feel / UI / Config/Data)
- **TR-ID** — the GDD requirement identifier
- **Governing ADR** reference
- **Manifest Version** embedded in story header
- **Acceptance Criteria** — every checkbox item, verbatim
- **Implementation Notes** — the ADR guidance section in the story
- **Out of Scope** boundaries
- **Test Evidence** — the required test file path
- **Dependencies** — what must be DONE before this story

### The TR registry
Read `docs/architecture/tr-registry.yaml`. Look up the story's TR-ID.
Read the current `requirement` text — this is the source of truth for what the
GDD requires now. Do not rely on any inline text in the story file (may be stale).

### The governing ADR
Read `docs/architecture/[adr-file].md`. Extract:
- The full Decision section
- The Implementation Guidelines section (this is what the programmer follows)
- The Engine Compatibility section (post-cutoff APIs, known risks)
- The ADR Dependencies section

### The control manifest
Read `docs/architecture/control-manifest.md`. Extract the rules for this story's layer:
- Required patterns
- Forbidden patterns
- Performance guardrails

Check: does the story's embedded Manifest Version match the current manifest header date?
If they differ, use `request_user_input` before proceeding:
- Prompt: "Story was written against manifest v[story-date]. Current manifest is v[current-date]. New rules may apply. How do you want to proceed?"
- Options:
  - `[A] Update story manifest version and implement with current rules (Recommended)`
  - `[B] Implement with old rules — I accept the risk of non-compliance`
  - `[C] Stop here — I want to review the manifest diff first`

If [A]: use the current rules and include the intended `Manifest Version:` story update in the complete Implementation Preflight. Do not edit yet.
If [B]: record the accepted risk as a planned `Manifest-Note:` in the complete Implementation Preflight. Do not edit yet. Read the current manifest and include any resulting risk in the preflight.
If [C]: stop. Do not spawn any agent. Let the user review and re-run `$codex-game-studios:dev-story`.

### Dependency validation

After extracting the **Dependencies** list from the story file, validate each:

1. file search `production/epics/**/*.md` to find each dependency story file.
2. Read its `Status:` field.
3. If any dependency has Status other than `Complete` or `Done`:
   - Use `request_user_input`:
     - Prompt: "Story '[current story]' depends on '[dependency title]' which is currently [status], not Complete. How do you want to proceed?"
     - Options:
       - `[A] Proceed anyway — I accept the dependency risk`
       - `[B] Stop — I'll complete the dependency first`
       - `[C] The dependency is done but status is stale — verify it through $codex-game-studios:story-done first`
   - If [B]: report the current story as BLOCKED and stop without changing any file.
   - If [C]: stop and route completion through `$codex-game-studios:story-done [dependency path]`; re-run `$codex-game-studios:dev-story` only after that workflow completes.
   - If [A]: include "Implement with incomplete dependency: [dependency title] — [status]" as a risk in the complete Implementation Preflight. Do not write it anywhere yet.

If a dependency file cannot be found: warn "Dependency story not found: [path]. Verify the path or create the story file."

All prerequisite, manifest-mismatch, and dependency choices before the preflight are read-only resolution decisions. No story, dependency, sprint-status, session-state, evidence, or source file may change before approval of the complete Implementation Preflight. Never mark another story Complete in this workflow; route completion through `$codex-game-studios:story-done`.

---

### Engine reference
Read `.codex/docs/technical-preferences.md`:
- `Engine:` value — determines which programmer agents to use
- Naming conventions (class names, file names, signal/event names)
- Performance budgets (frame budget, memory ceiling)
- Forbidden patterns

### Implementation Preflight

Before changing status, delegating implementation, or writing any file, render this complete preflight:

```markdown
## Implementation Preflight
- Story: [path]
- Requirements: [TR-IDs]
- Governing ADRs: [paths]
- Intended files: [complete list]
- Required tests: [complete list]
- Acceptance criteria: [checkbox list]
- Risks or open questions: [none, or explicit items]
```

Replace every bracketed field with values from the selected story and the loaded governing artifacts. The intended-file list must include source, tests, evidence, the story file, `production/sprint-status.yaml`, and `production/session-state/active.md` when they will change. No bracketed placeholder may remain in the preflight shown to the user.

Pause before requesting approval when the story contains a design ambiguity, conflicts with a governing ADR, lacks a required architectural decision, or cannot be implemented inside its stated scope. Do not guess or use approval to bypass those blockers.

Ask whether to approve this one complete story changeset. After approval, state exactly: `Work may proceed within the approved story boundary; do not ask again for each listed file.` Then:

1. Update `production/sprint-status.yaml`, if listed and present: set the matching entry to `status: in_progress` and update the top-level date.
2. Update the story file, if listed: set `Last Updated:` to today's `YYYY-MM-DD` date, adding it after `Status:` when absent.
3. Implement and verify only the listed files and criteria.

Pause and request a revised preflight before touching any file outside the list, materially changing behavior, expanding scope, or departing from a governing ADR. The original approval does not cover those changes.

---

## Phase 3: Route to the Right Programmer

Based on the story's **Layer**, **Type**, and **system name**, determine which
specialist to spawn through Codex custom-agent delegation.

**Config/Data stories — skip agent spawning entirely:**
If the story's Type is `Config/Data`, no programmer agent or engine specialist is needed. Jump directly to Phase 4 (Config/Data note). The implementation is a data file edit — no routing table evaluation, no engine specialist.

### Primary agent routing table

| Story context | Primary agent |
|---|---|
| Foundation layer — any type | `engine-programmer` |
| Any layer — Type: UI | `ui-programmer` |
| Any layer — Type: Visual/Feel | `gameplay-programmer` (implements) |
| Core or Feature — gameplay mechanics | `gameplay-programmer` |
| Core or Feature — AI behaviour, pathfinding | `ai-programmer` |
| Core or Feature — networking, replication | `network-programmer` |
| Config/Data — no code | No agent needed (see Phase 4 Config note) |

### Engine specialist — always spawn as secondary for code stories

Read the `Engine Specialists` section of `.codex/docs/technical-preferences.md`
to get the configured primary specialist. Spawn them alongside the primary agent
when the story involves engine-specific APIs, patterns, or the ADR has HIGH
engine risk.

| Engine | Specialist agents available |
|--------|----------------------------|
| Godot 4 | `godot-specialist`, `godot-gdscript-specialist`, `godot-shader-specialist` |
| Unity | `unity-specialist`, `unity-ui-specialist`, `unity-shader-specialist` |
| Unreal Engine | `unreal-specialist`, `ue-gas-specialist`, `ue-blueprint-specialist`, `ue-umg-specialist`, `ue-replication-specialist` |

**When engine risk is HIGH** (from the ADR or VERSION.md): always spawn the engine
specialist, even for non-engine-facing stories. High risk means the ADR records
assumptions about post-cutoff engine APIs that need expert verification.

---

## Phase 4: Implement

Spawn the chosen programmer agent(s) through Codex custom-agent delegation with the full context package:

Brief the agent with file paths and targeted reading instructions — do not serialize document content into the delegation brief. The agent reads what it needs directly:

1. **Story file**: `[story-path]` — read in full
2. **GDD requirement**: look up TR-ID `[TR-XXX-NNN]` in `docs/architecture/tr-registry.yaml` — use the `requirement` field as source of truth
3. **ADR**: `docs/architecture/[adr-file].md` — read the **Decision** and **Implementation Guidelines** sections only
4. **Control manifest**: `docs/architecture/control-manifest.md` — read rules for the **[layer]** layer only
5. **Engine preferences**: `.codex/docs/technical-preferences.md` — read naming conventions and performance budgets
6. **Test file path**: `[path from story's Test Evidence section]` — this file must be created as part of implementation
7. **Test requirement** (Logic and Integration stories only): The test file MUST be created at `[path from the story's Test Evidence section]`. Write the test alongside the implementation — do not defer it. The story cannot be closed via `$codex-game-studios:story-done` without this file present. Each acceptance criterion must have at least one test function covering it. Test file naming: `[system]_[feature]_test.[ext]`. Function naming: `test_[scenario]_[expected_outcome]`. No random seeds, no time-dependent assertions, no external I/O.
8. **Explicit instruction**: implement this story following the ADR guidelines, respect the manifest rules, stay within the story's Out of Scope boundaries. Write clean, doc-commented public APIs.

The agent should:
- Create or modify files in `src/` following the ADR guidelines
- Respect all Required and Forbidden patterns from the control manifest
- Stay within the story's Out of Scope boundaries (do not touch unrelated files)
- Write clean, doc-commented public APIs

### Config/Data stories (no agent needed)

For Type: Config/Data stories, no programmer agent is required. The implementation
is editing a data file. Read the story's acceptance criteria and make the specified
changes to the data file directly. Note which values were changed and what they
changed from/to.

### Visual/Feel stories

Spawn `gameplay-programmer` to implement the code/animation calls. Note that
Visual/Feel acceptance criteria cannot be auto-verified — the "does it feel right?"
check happens in `$codex-game-studios:story-done` via manual confirmation.

---

## Phase 5: Test Evidence Requirements

The test requirement was included in the Phase 4 programmer agent brief (item 7). This phase summarizes what evidence each story type requires — used when collecting the Phase 6 summary.

| Story Type | Required Evidence | Notes |
|---|---|---|
| **Logic** | Automated unit test at path from story's Test Evidence section | BLOCKING — included in Phase 4 agent brief |
| **Integration** | Integration test OR documented playtest record | BLOCKING — included in Phase 4 agent brief |
| **Visual/Feel** | Evidence doc at `production/qa/evidence/[slug]-evidence.md` | ADVISORY — note in Phase 6 summary |
| **UI** | Manual walkthrough doc or interaction test | ADVISORY — note in Phase 6 summary |
| **Config/Data** | None — smoke check serves as evidence | N/A |

For Visual/Feel and UI stories, include in the Phase 6 summary: "Manual evidence required at `production/qa/evidence/[slug]-evidence.md` before this story can be fully closed."

---

## Phase 6: Collect and Summarise

After the programmer agent(s) complete, collect:

- Files created or modified (with paths)
- Test file created (path and number of test functions written)
- Any deviations from the story's Out of Scope boundary (flag these)
- Any questions or blockers the agent surfaced
- Any engine-specific risks the specialist flagged

Present a concise implementation summary:

```
## Implementation Complete: [Story Title]

**Files changed**:
- `src/[path]` — created / modified ([brief description])
- `tests/[path]` — test file ([N] test functions)

**Acceptance criteria covered**:
- [x] [criterion] — implemented in [file:function]
- [x] [criterion] — covered by test [test_name]
- [ ] [criterion] — DEFERRED: requires playtest (Visual/Feel)

**Deviations from scope**: [None] or [list files touched outside story boundary]
**Engine risks flagged**: [None] or [specialist finding]
**Blockers**: [None] or [describe]

**Before running `$codex-game-studios:story-done`:** run your test suite locally and confirm the tests you wrote pass. `$codex-game-studios:story-done` will re-run them automatically, but a failing test discovered there means returning to implementation context.

Ready for: `$codex-game-studios:code-review [file1] [file2]` then `$codex-game-studios:story-done [story-path]`
```

---

## Phase 7: Update Session State

Append to the already listed and approved `production/session-state/active.md` path:

```
## Session Extract — $codex-game-studios:dev-story [date]
- Story: [story-path] — [story title]
- Files changed: [comma-separated list]
- Test written: [path, or "None — Visual/Feel/Config story"]
- Blockers: [None, or description]
- Next: $codex-game-studios:code-review [files] then $codex-game-studios:story-done [story-path]
```

Create `active.md` if it does not exist. Confirm: "Session state updated."

---

## Error Recovery Protocol

If any spawned agent (through Codex custom-agent delegation) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** via `request_user_input` with choices:
   - Skip this agent and note the gap in the final report
   - Retry with narrower scope
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. Never discard work because one agent blocked.

Common blockers:
- Input file missing (story not found, GDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; run `$codex-game-studios:architecture-decision` first
- Scope too large → split into two stories via `$codex-game-studios:create-stories`
- Conflicting instructions between ADR and story → surface the conflict, do not guess
- Manifest version mismatch → show diff to user, ask whether to proceed with old rules or update story first

## Collaborative Protocol

- **One story-level approval** — implementation may be performed directly or through Codex custom agents, but every worker receives the approved preflight and stays inside it. Workers do not ask again for each listed file.
- **Load before implementing** — do not start coding until all context is loaded
  (story, TR-ID, ADR, manifest, engine prefs). Incomplete context produces code
  that drifts from design.
- **The ADR is the law** — implementation must follow the ADR's Implementation
  Guidelines. If the guidelines conflict with what seems "better," flag it in the
  summary rather than silently deviating.
- **Stay in scope** — the Out of Scope section is a contract. If implementing
  the story requires touching an out-of-scope file, stop and surface it:
  "Implementing [criterion] requires modifying [file], which is out of scope.
  Shall I proceed or create a separate story?"
- **Test is not optional for Logic/Integration** — do not mark implementation
  complete without the test file existing
- **Visual/Feel criteria are deferred, not skipped** — mark them as DEFERRED
  in the summary; they will be manually verified in `$codex-game-studios:story-done`
- **Ask before large structural decisions** — if the story requires an
  architectural pattern not covered by the ADR, surface it before implementing:
  "The ADR doesn't specify how to handle [case]. My plan is [X]. Proceed?"

---

## Recommended Next Steps

- Run `$codex-game-studios:code-review [file1] [file2]` to review the implementation before closing the story
- Run `$codex-game-studios:story-done [story-path]` to verify acceptance criteria and mark the story complete
- After all sprint stories are done: run `$codex-game-studios:team-qa sprint` for the full QA cycle before advancing the project stage
