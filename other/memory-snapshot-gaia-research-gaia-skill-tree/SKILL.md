---
name: memory-snapshot
description: >-
  Append a session/state snapshot to MEMORY.md (regardless of where it lives — for this
  repo it's `founder/MEMORY.md`). Use when the user says "snapshot memory", "save state to
  memory", "/memory-snapshot", "log what happened in MEMORY", or otherwise asks to record
  the current session's outcomes for the next orchestrator. Locates the project's
  MEMORY.md, prepends a dated entry above the previous snapshot (newest first), preserves
  every existing entry (NEVER overwrites or truncates), and reports back the file path +
  byte delta. Not for one-off feedback memories (use the user-level memory system at
  ~/.claude/.../memory/ for those). Not for trimming or deleting old entries.
version: 1.0.0
argument-hint: "<optional one-line headline for the snapshot>"
---

# memory-snapshot

A **deterministic, additive** skill: prepend a dated state snapshot to whichever MEMORY.md
governs the current project. Newest first. Existing entries are preserved verbatim.

For this repo (`gaia-skill-tree`), the canonical location is `founder/MEMORY.md`. For
other projects, the skill auto-detects: searches for `MEMORY.md` at the repo root, then
`founder/MEMORY.md`, then `docs/MEMORY.md`, then any single `MEMORY.md` reachable via
`git ls-files`. If multiple are found, picks the one closest to the project root and
asks the user to confirm.

## When to invoke

Trigger on any of:

- `/memory-snapshot`
- "snapshot memory" / "save state to memory" / "log to MEMORY.md"
- "update orchestrator memory with what happened"
- "record this session in MEMORY before we close"
- End-of-session checkpoints where the user says "and add to founder/MEMORY.md"

Do NOT use for:

- User-level feedback memories (use `~/.claude/projects/<repo>/memory/*.md` with frontmatter)
- Trimming, editing, or deleting existing snapshots (separate manual operation)
- The orchestrator's `/CLAUDE.md` — that's a static rulebook, not a session log

## Operating contract — additive only

1. **Locate MEMORY.md.** Order of preference:
   - `founder/MEMORY.md` (gaia-skill-tree convention)
   - `MEMORY.md` (repo root)
   - `docs/MEMORY.md`
   - Any `MEMORY.md` from `git ls-files MEMORY.md`
2. **Read the existing file.** If it doesn't exist, create with a `# Memory` header.
3. **Compose the snapshot block.** Format:
   ```
   ## State Snapshot (YYYY-MM-DD, <session/turn label> — <one-line headline>)
   
   ### TLDR
   - bullet 1
   - bullet 2
   
   ### What changed this session
   | Layer | State |
   |---|---|
   | ... | ✅/⏳/❌ ... |
   
   ### Branches at end of session
   | Branch | Head SHA | Status |
   ...
   
   ### Issues + PRs touched
   ...
   
   ### Routing — where things live now
   ...
   
   ### Lessons / hazards preserved
   ...
   
   ### Open questions for next orchestrator
   ...
   
   ### Token cost (this session)
   ...
   ```
4. **Prepend** above the most recent prior snapshot, NEVER above the file header.
   - File starts with `# Orchestrator Memory` (or similar) followed by an intro paragraph.
   - The new snapshot inserts AFTER the intro, BEFORE the previous `## State Snapshot` block.
5. **NEVER delete or modify existing snapshots.** Even when they reference state that's
   since changed — they are an audit log.
6. **Report** the file path, byte delta, and a one-line summary of what was added.

## What the orchestrator brings to the snapshot

The skill assumes the calling conversation has the relevant context. Pull from:

- `git log --oneline origin/main..HEAD` for commits since the last snapshot
- `gh pr list --author @me --json number,title,state` for PRs touched
- `gh issue list --search "involves:@me" --json number,title,state` for issues touched
- The TaskList at end of session for what got done vs. deferred
- Any explicit headline the user provided as `argument-hint`
- Token spend:
  - If in the Pi harness (indicated by `PI_CODING_AGENT=true` in `env`), run the `pi-cost` skill (`python3 .claude/skills/pi-cost/scripts/pi_cost.py` or `/skill:pi-cost`) to obtain the exact session token counts, subagent breakdown, and calculated session cost.
  - Otherwise, pull from `founder/COST.md` if it exists, or estimate from the message count + average tokens-per-turn.

## Failure modes — refuse cleanly

- **Two MEMORY.md files at the same depth.** Report both paths and ask the user which.
- **MEMORY.md outside `git ls-files` (untracked).** Warn but proceed — the file is real.
- **Read-only filesystem / permission denied.** Surface the OS error, do not retry.
- **The composed snapshot is empty.** Refuse to write — empty is not auditable.

## Example invocation

```
User: /memory-snapshot Phase 1 closed, ready to merge
Agent:
  1. Locates founder/MEMORY.md (gaia-skill-tree convention)
  2. Reads existing 704 lines, 33 KB
  3. Composes "State Snapshot (2026-06-20, session 15 FINAL — Phase 1 closed, ready to merge)"
  4. Prepends after the # Orchestrator Memory header, before the prior snapshot
  5. Writes 854 lines, 41 KB (+8 KB)
  6. Reports: "founder/MEMORY.md updated. 704 → 854 lines (+150). Headline: 'Phase 1 closed, ready to merge'."
```

## Why this skill exists

Marco's pattern (observed sessions 11–15): every closing turn, he asks for a memory
update. Every turn, the orchestrator hand-writes the snapshot, sometimes forgetting:

- Where MEMORY.md lives in the project (varies: root vs. `founder/` vs. `docs/`)
- The newest-first ordering (some sessions appended at the bottom by accident)
- That existing snapshots must be preserved, not summarized over
- That the headline should land in the section title for searchability

The skill removes the variance. One slash command, one consistent additive write.

## Out of scope (route elsewhere)

- **User-level feedback memories** → write directly to
  `~/.claude/projects/<repo-slug>/memory/*.md` with frontmatter. That's a different
  surface (cross-session, frontmatter-indexed) for a different purpose (your guidance to
  Claude vs. orchestrator's own state log).
- **Trimming MEMORY.md** when it grows too large → manual operation (the orchestrator
  reviews + collapses old snapshots into a "## Archive" section, never silently).
- **Updating CLAUDE.md / GIT.md** with rules that emerged this session → those are
  rulebooks, not logs. Edit them directly, don't route through this skill.
