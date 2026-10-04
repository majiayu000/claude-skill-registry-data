---
name: Qcompact
user_invocable: true
description: Context preservation and session handoff. Use when the user wants to save state, handoff, save context, end session, or continue later.
invocation_trigger: When the context window is full or under pressure (Orange/Red zone).
recommendedModel: haiku
---

> **`.qe` reads → DB:** `.qe/` content is stored in the SQLite store (`qe_files`), so a path may have **no file on disk**. Read `.qe/` content with `node scripts/qe-cat.mjs <path>` (or `--ls`/`--exists`) and structured state with `node scripts/qe-query.mjs …` — do not assume the raw file exists. See `QE_CONVENTIONS.md`.


# Qcompact — Context Preservation & Handoff

## Role
A skill that automatically preserves context under context window pressure, and generates detailed handoff documents on user request.

## Per-Session Layout (Auto-Named)
Multiple terminals on the same project save into separate `sessions/{sid}/` directories so they never clobber each other. The 8-char `sid` is auto-derived from the Claude session id by the SessionStart hook and surfaced as `[Session] sid:XXXXXXXX` in additionalContext — there is no manual `--name` flag. When no sid is available the `_unknown` bucket is used; pre-partition flat files were one-shot migrated into `_legacy`.

SessionStart may also surface `[Session State] ...` with the active plan,
resume source, and Codex background job status. Treat that line as an advisory
shortcut only; the resolver functions below remain the source of truth.

## Operating Modes

### Automatic Mode (Background Call)
Ecompact-executor detects context pressure and runs automatically in the background.
- Saves quietly without notifying the user
- Triggered when entering the `CONTEXT_BUDGET.md` warning zone (70%+ of the active context window by default)
- Saves current state to `.qe/context/sessions/{sid}/snapshot.md`
- Accumulates decisions in `.qe/context/sessions/{sid}/decisions.md`

### Manual Mode (User Invocation)
Calling `{adapter.commandPrefix}Qcompact` directly generates a detailed handoff document.
- Delegates `mode=handoff` to Ecompact-executor
- Creates `.qe/handoffs/sessions/{sid}/HANDOFF_{date}_{time}.md`
- Displays saved context + handoff summary to the user

---

## Automatic Mode Details

### Save Location
`.qe/context/sessions/{sid}/` (auto-named per Claude session)

### Saved Content

#### `snapshot.md` — Context Snapshot
Overwritten on each save (only the latest state is retained):

```markdown
# Context Snapshot
> Saved at: 2026-03-14 10:30

## Current Task
- In-progress task UUID and title
- Checklist progress (completed/total)
- Checklist item currently being worked on

## Key Decisions
- Major decisions made this session
- Directions explicitly instructed by the user

## Changed Files
- Files created/modified/deleted this session

## Pending Items
- Work not yet finished
- What to do next

## Notes
- Constraints or requirements to remember specifically
```

#### `decisions.md` — Accumulated Decision History
Accumulated per session (reverse order, newest first):

```markdown
## [2026-03-14] Session
- Decided to separate framework data into .qe/ folder
- Changed agent prefix from A → E
- Branded as QE framework (Query Executor)
```

---

## Manual Mode Details

### CREATE Workflow

#### Step 1: Delegate to Ecompact-executor
Call Ecompact-executor with a complete delegation packet and `mode=handoff`.
- Create `.qe/handoffs/` directory (if not present)
- Create `HANDOFF_{date}_{time}.md` file
- Auto-collect current task state, git changes, and decisions

#### Step 2: Write Handoff Document
1. **Current status summary** — what the situation is right now
2. **Important context** — key information the next agent must know
3. **Immediate next steps** — clear, actionable first step
4. **Decisions** — choices that include not just the outcome but the reason

#### Step 3: Verify
- No `[TODO: ...]` placeholders remain
- Required sections exist and are filled in
- No potentially confidential information (API keys, passwords, tokens)
- Referenced files exist
- Rebuild the derived index once — `node scripts/lib/doc-index.mjs` (single scan-based rebuild; never append to `.qe/index.md`). See `core/DOC_CONVENTIONS.md`.

#### Step 4: Report to User
- Handoff file location
- Summary of captured context
- First action item for the next session

### RESUME Workflow

#### Step 1: Look Up Handoff
Use the shared resolver — `resolveResumeContext(projectRoot, overrideSid)` in `hooks/scripts/lib/session-resolver.mjs` — the **same function `{adapter.commandPrefix}Qresume` uses**, so handoff lookup here and restore there cannot diverge. It scans the active sid across both `.qe/context/` and `.qe/handoffs/` first, and when the active sid is empty in both, falls back to the newest other bucket (durable handoffs are unioned in, so a handoff saved under a prior sid is reachable). Read `latestHandoff` from the returned descriptor; when `source: 'fallback'`, tell the user which bucket was loaded.

On Codex, render the same workflow as `$Qresume` / `$Qresume --from {sid}` in
handoffs. Do not emit Claude-only slash commands in Codex-facing text.

#### Step 2: Check Freshness
| Level | Meaning |
|-------|---------|
| FRESH | Safe to resume — minimal changes |
| SLIGHTLY_STALE | Review changes before resuming |
| STALE | Carefully verify context |
| VERY_STALE | Consider creating a new handoff |

#### Step 3: Load Handoff and Start Work
- Read the handoff document and start from item #1 of "Immediate next steps"
- If there are chained handoffs, also reference previous ones

### Handoff Chaining
In long-running projects, link handoffs to each other to maintain context lineage:
```
HANDOFF_1.md → HANDOFF_2.md → HANDOFF_3.md
```

---

## Save Location Summary

| Mode | Location | Purpose |
|------|----------|---------|
| Automatic | `.qe/context/sessions/{sid}/snapshot.md` | Latest context for this terminal (overwrite) |
| Automatic | `.qe/context/sessions/{sid}/decisions.md` | Accumulated decisions for this terminal |
| Manual | `.qe/handoffs/sessions/{sid}/HANDOFF_*.md` | Detailed handoff document for this terminal |

## Will
- Automatic: save context snapshot, accumulate decisions
- Manual: generate detailed handoff document, verify, chain
- Delegate to Ecompact-executor (automatic)
- Delegate to Ecompact-executor (manual handoff)

## Will Not
- Save entire conversation (extract key points only)
- Copy entire code (record file paths only)
- Notify user (during automatic execution)
- Include confidential information
