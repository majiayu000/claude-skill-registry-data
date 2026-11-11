---
name: pair-capability-checkpoint
description: "Writes and resumes a self-contained progress checkpoint (story, branch, tasks done, decisions, remaining todos) so work survives a context reset. Invoke directly to save or resume progress ('save our progress on #313', 'resume story #256'); composed by a future closing phase of /pair-process-implement and consumed by /pair-capability-publish-pr (via $mode=resume)."
version: 0.4.1
author: Foomakers
---

# /pair-capability-checkpoint — Resumable Progress State

Write and resume a self-contained progress checkpoint so a fresh session (or a subagent) can continue a story exactly where the previous one stopped. Follows the [checkpoint template](../../../.pair/knowledge/guidelines/collaboration/templates/checkpoint-template.md) (resolve override-first — [template resolution](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/template-resolution.md)) — five sections: story, branch, tasks done, key decisions, remaining todos.

## Arguments

| Argument   | Required | Description                                                                                                                                                          |
| ---------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$mode`    | Yes      | `write` — persist/return current state. `resume` — locate and parse the existing checkpoint for a story.                                                              |
| `$story`   | No       | Story ID. If omitted, detected from session context or the current branch (`feature/#<id>-*`). If it cannot be detected → **HALT**.                                   |
| `$persist` | No       | Write mode only. `true` (default) — write/update the file at the default location. `false` — write-free: synthesize and return the checkpoint text without touching the filesystem; the composer decides where it lands. |

## Core Rules

- **One file per story:** default location `.pair/working/checkpoints/<story-id>.md`. Write mode always updates it in place — never a second file for the same story. The file is the source of truth; an optional issue-body mirror must be explicitly marked as a copy.
- **Task-scoped:** a downstream handoff consumed only by a session or subagent resuming or continuing _that_ story — NEVER loaded as ambient context into unrelated activity.
- **Write freely, clean up on completion:** writing — including automatically, e.g. between tasks — is fine; the constraint is on _consumption scope_, not write timing. When the story is Done (closing phase or PR merge), the checkpoint is removed so finished-story state never lingers.

## Algorithm

### Step 1: Resolve Story Context

1. **Check**: Is `$story` provided?
2. **Skip**: If yes, proceed to Step 2.
3. **Act**: Attempt detection, in order:
   - Active story already loaded in the current session.
   - Current branch name matching `feature/#<id>-*` (`git branch --show-current`).
   - Resume mode only: a single checkpoint file present under `.pair/working/checkpoints/`.
4. **Verify**: Story ID resolved. If not → **HALT**: "Cannot detect story context — pass `$story` explicitly."

### Step 2: Route by Mode

- `$mode = write` → Step 3.
- `$mode = resume` → Step 6.

### Step 3: Gather State (write mode)

1. **Check**: Is the full state (story, branch, tasks done/pending, decisions) already known from the current session context?
2. **Skip**: If yes, use it directly. Proceed to Step 4.
3. **Act**: If not (e.g., invoked by a subagent with no prior context), reconstruct from artifacts:
   - **Branch**: `git branch --show-current`.
   - **Tasks done/pending**: read the story's Task Breakdown checklist (per [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md)), cross-referenced with commits on the branch — the same technique `/pair-process-implement` uses for idempotent resume.
   - **Decisions**: scan [adoption/tech/adr/](../../../.pair/adoption/tech/adr) and [adoption/decision-log/](../../../.pair/adoption/decision-log) for files touched since the branch diverged from main.
4. **Verify**: All five state elements resolved. Anything that cannot be reconstructed confidently is marked `[unknown — needs confirmation]` — never guessed.

### Step 4: Detect Existing Checkpoint

1. **Check**: Does `.pair/working/checkpoints/<story-id>.md` already exist?
2. **Skip**: If not, proceed to Step 5 to create it.
3. **Act**: If it exists, read its current content — the new state overwrites it in place (Core Rule).
4. **Check**: Do other checkpoint files also resolve to this story ID (e.g. a stray duplicate from a prior manual copy)?
5. **Act**: If duplicates are found, use the most recently modified one as the base and flag the others to the caller as duplicates to remove.

### Step 5: Write / Return Checkpoint

1. **Act**: Render the checkpoint following the [checkpoint template](../../../.pair/knowledge/guidelines/collaboration/templates/checkpoint-template.md), filling all five sections.
2. **Check**: Is `$persist` `false`?
3. **Skip**: If `$persist` is `true` (default) — create `.pair/working/checkpoints/` if missing, write the rendered content to `<story-id>.md` (overwrite in place, per Core Rule).
4. **Act**: If `$persist` is `false` — do not touch the filesystem. Synthesize the text only.
5. **Verify**: Regardless of `$persist`, the full rendered checkpoint text is returned to the caller (Output Format). If an issue-body mirror is requested, mark it explicitly: "Mirror of `.pair/working/checkpoints/<story-id>.md` — file is the source of truth."

### Step 6: Locate Checkpoint (resume mode)

1. **Check**: Does exactly one `.pair/working/checkpoints/<story-id>.md` exist?
2. **Skip**: If exactly one, proceed to Step 7.
3. **Act**: If none exists → **HALT**: "No checkpoint found for #`$story` — start fresh, or provide checkpoint text directly."
4. **Act**: If more than one candidate resolves to the same story (edge case), use the most recently modified file and flag the others as duplicates to the caller.

### Step 7: Parse Checkpoint

1. **Act**: Parse the five sections in order: Story, Branch, Tasks Done, Key Decisions, Remaining Todos. Ignore a trailing "Template Notes" (or any 6th) section if one is present — it is authoring guidance, not checkpoint state.
2. **Check**: Are all five sections present and structurally well-formed?
3. **Skip**: If yes, proceed to Step 8 with full confidence.
4. **Act**: If any section is missing, empty, or malformed — report exactly what WAS parsed, list what's missing or ambiguous, and ask the caller to confirm before proceeding. Never fill gaps by guessing.

### Step 8: Report Parsed State

1. **Act**: Present the parsed state to the caller (Output Format) — story, branch, tasks done, tasks pending, key decisions.
2. **Verify**: All five sections from Step 7 (or their explicit gap markers) appear in the presented state — the caller can identify the next pending task without re-deriving Tasks Done.

## Output Format

Write mode:

```text
CHECKPOINT WRITTEN:
├── Story:    [#ID: Title]
├── Branch:   [feature/#ID-description]
├── Path:     [.pair/working/checkpoints/<story-id>.md | write-free — not persisted]
├── Mode:     [Created | Updated in place]
└── Tasks:    [N done / M total]
```

Followed by the full rendered checkpoint text (per the template) — always returned, regardless of `$persist`.

Resume mode:

```text
CHECKPOINT RESUMED:
├── Story:      [#ID: Title]
├── Branch:     [feature/#ID-description]
├── Tasks done: [list T-N]
├── Tasks left: [list T-N]
├── Decisions:  [N recorded | None yet]
└── Confidence: [High — all sections parsed cleanly | Needs confirmation — see gaps below]
```

## Example: Write Mode Mid-Story

Input — invoked with `$mode: write` from a session with story #313 loaded, 2 of 5 tasks done, no explicit `$story`:

```text
$mode: write
```

(Story detected from branch `chore/#313-t6-completion-criteria`; state gathered from Step 3: Task Breakdown checklist shows T1-T2 checked, an ADL was recorded for the shared-reference naming convention.)

Output — `.pair/working/checkpoints/313.md` is created with:

```markdown
# Checkpoint: #313 — Skill corpus effectiveness pass

**Last updated:** 2026-07-16 14:30
**Written by:** implement session

## 1. Story
**ID:** #313
**Title:** Skill corpus effectiveness: trigger descriptions, shared references, ...
**Goal:** Optimize the 35-skill corpus for LLM-executor effectiveness.
**Source:** github.com/foomakers/pair/issues/313

## 2. Branch
**Branch:** `chore/#313-t6-completion-criteria`
**Commit strategy:** commit-per-task
**Commits so far:** 2 — "sharpen soft Verify beats across assess-* skills"

## 3. Tasks Done
- [x] T1 — Router/catalog + correctness fixes — PR #325
- [x] T2 — Authoring effectiveness standard — PR #319

## 4. Key Decisions
- Shared-reference naming: `skill-conventions/<topic>.md` — see 2026-07-13-shared-reference-naming.md

## 5. Remaining Todos
- [ ] T6 — Completion criteria + steering pass
**Next immediate action:** finish the negation sweep on record-decision, then run the T2 checklist on 4-5 sampled skills.
```

Followed by the `CHECKPOINT WRITTEN` summary block (Output Format above).

## Composition Interface

When composed by a future closing phase of `/pair-process-implement`:

- **Input**: `/pair-process-implement` would invoke `/pair-capability-checkpoint` with `$mode=write` between tasks (or on developer request) to persist progress, `$mode=resume` at Phase 0 when re-invoked on a story that may have been interrupted, and remove the checkpoint on story completion (cleanup).
- **Output**: Write mode's returned text becomes the session's record of state. Resume mode's parsed state lets `/pair-process-implement` skip re-analysis and jump straight to the first pending task.

When composed by `/pair-capability-publish-pr` (the companion capability from the same epic split, wired in #256):

- **Input**: `/pair-capability-publish-pr` invokes `/pair-capability-checkpoint` with `$mode=resume` to read the story's handoff (branch, tasks done, decisions) before composing the PR — it is a **read-only consumer**. It never calls `$mode=write`; when no checkpoint exists, `/pair-capability-publish-pr` gathers state directly from the branch + story instead.
- **Output**: Resume mode's parsed state feeds the PR body. `/pair-capability-publish-pr` owns none of the checkpoint's lifecycle (no write, no cleanup).

When invoked **independently**:

- Full interactive flow. The developer or a subagent passes `$mode` and, if needed, `$story` explicitly.

## Edge Cases

- **No story context detectable**: **HALT** and ask the caller to pass `$story` explicitly (Step 1).
- **Corrupted or incomplete checkpoint on resume**: report exactly what was parsed, list what's missing/ambiguous, and ask for confirmation before the caller proceeds (Step 7).
- **Multiple checkpoints found for one story**: use the most recently modified file; flag the duplicates to the caller for cleanup (Steps 4 and 6).

## Graceful Degradation

See [graceful degradation](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/graceful-degradation.md) (guideline/template missing → use a minimal structure directly; PM tool not accessible during state reconstruction, Step 3 → ask the developer to confirm tasks done/pending directly) for the standard scenarios. Additional cases:

- If the [checkpoint template](../../../.pair/knowledge/guidelines/collaboration/templates/checkpoint-template.md) is not found, use the minimal five-section structure directly: Story, Branch, Tasks Done, Key Decisions, Remaining Todos.
- If `.pair/working/` does not exist yet, create it (and `checkpoints/` under it) on first write.
- If git is not available or the branch cannot be determined, mark the Branch section `[unknown — needs confirmation]` rather than guessing.

## Notes

- This skill **writes at most one file** — `.pair/working/checkpoints/<story-id>.md` — and only in write mode with `$persist=true` (default).
- **Idempotent** — see [idempotency convention](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/idempotency.md). This skill's check: write mode updates the same file in place (never duplicates); resume mode is read-only and safe to repeat.
- `.pair/working/` holds operational, per-project runtime state — never touched by install or update (D14). It is not part of the distributed KB defaults.
- Checkpoints complement, not replace, git/PM-tool state. Even when state is reliably reconstructible from git and the PM tool (as `/pair-process-implement` does today), a checkpoint adds an explicit, fast-to-read summary — most valuable across context resets and subagent handoffs, where reconstruction from scratch is expensive or impossible.
- The write-free (`$persist=false`) option serves composers that own their own persistence (e.g., embedding the handoff directly into a PR body) rather than writing a separate file.
