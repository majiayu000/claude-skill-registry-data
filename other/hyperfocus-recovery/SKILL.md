---
name: hyperfocus-recovery
category: exec-function
codex-short-description: "Rebuild context after a deep session or interruption from git and file artifacts"
description: >
  Reconstruct context after a deep session or interruption from git diff, modified files,
  and recent commits, then propose the next concrete action. Use when the user says "what
  was I doing", "where did I leave off", "lost my place", or invokes /hyperfocus-recovery.
version: 1.0.0
license: MIT
compatibility: claude-code codex opencode
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
related-skills:
  - task-initiation
  - i-have-adhd
  - hyperfocus-exit
loop-eligible: false
---

# Hyperfocus Recovery

The user just surfaced from a deep work session, or got pulled away for an hour, and now has no idea where they were. Their brain went elsewhere; the context is gone. Your job is to reconstruct it from the artifacts they left behind.

## When to activate

When the user says:
- "What was I doing?"
- "Where did I leave off?"
- "I lost my place"
- "Help me get back in"
- "I just came back from [X]"

## Why no council

This is forensic reconstruction, not interpretation. A council call would add noise. Run inline.

## Gathering pass

Run these in parallel, take what works, ignore what doesn't:

0. **Newest file in `.ink-and-agency/park/`** — a park file left by [hyperfocus-exit](../hyperfocus-exit/). Check this first: it holds the head-state that no artifact can reconstruct (what they were about to try, what they already ruled out, what will silently disappear). When one exists and is recent, lead the reconstruction with it and use the rest of this pass to confirm it still matches the tree.
1. **`git status`** — uncommitted changes (the freshest evidence of intent)
2. **`git diff`** (working tree) — what they were actively editing
3. **`git diff --staged`** — what they had decided was ready
4. **`git log --oneline -10`** — the trail of recent committed thinking
5. **`git stash list`** — abandoned work
6. **Modified files in last 4 hours** — `find . -mmin -240 -type f -not -path './.git/*'` (or platform equivalent)
7. **`PARKED`/TODO/FIXME/XXX in recently-touched files** — breadcrumbs they left themselves. A `PARKED` comment is deliberate and points at the exact re-entry line; treat it as the strongest signal in the file.
8. **Open editor file** — from IDE context if available

## Output format

### Where you were

One paragraph reconstructing the apparent goal from the evidence. Cite specific files and changes. Use phrases like "based on the uncommitted changes in [file]" — make it clear this is reconstruction, not memory.

### What you were doing

A bulleted list of the active threads, ranked by recency and certainty:

- **[High confidence]** [Thread 1 — what file, what change, what for]
- **[Medium confidence]** [Thread 2]
- **[Low confidence]** [Thread 3 — old enough that it might not still be live]

### Breadcrumbs you left yourself

Surface any PARKED / TODO / FIXME / XXX / `// TEMP` comments in recently-touched files, with file:line links. These are usually the most reliable signal of intent.

If a park file supplied a **Do not lose** list, restate it here verbatim — running processes and set env vars are the loose ends most likely to be gone by now, and the user needs to know which ones died.

### Loose ends

- Uncommitted changes (count + summary)
- Stashes (if any)
- Failing tests (if known)
- Anything that looks half-done

### Suggested re-entry point

**Pick the smallest, most concrete next action.** Same shape as [task-initiation](../task-initiation/SKILL.md) output — one literal thing, ≤30 seconds:

> **To get back in, do this:**
> [Open `src/foo.ts` line 47. Read the `// TODO: handle empty case` comment. That's where you were.]

If the user wants to start fresh and abandon what they were doing, offer that as an alternative:

> **Or: if you want to drop this thread, [`git stash`] and I can help you pick something new.**

## What NOT to do

- Do not guess at intent beyond what the artifacts support
- Do not produce a plan — just rebuild context and point at the next step
- Do not summarize for the sake of summarizing; if there's nothing to recover, say so plainly
- Do not commit anything, stash anything, or modify state — recovery is read-only
- Do not encourage or validate — the user wants their context back, not a pep talk

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/hyperfocus-recovery.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
