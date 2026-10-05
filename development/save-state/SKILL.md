---
name: save-state
description: >-
  Use when you need the whole picture of active work in this project — at session start, after a
  context clear or /compact, when finishing a work item, or when asked "what's in flight",
  "what am I building", "show the overall picture", or "save state".
allowed-tools: Bash(git *), Bash(gh *), Bash(find *), Bash(ls *), Bash(bun *)
---

# Save state — the single-pane work index

This regenerates the scratch INDEX, the one screen that shows everything in flight. **Pull, don't
copy:** the index is a thin layer of pointers + live status; the real detail stays in each thread's
STATE doc. Never hand-maintain the INDEX — re-run this skill.

> **Freshness is automatic** — the `auto-compile-index` hook recompiles the INDEX on every STATE
> write, so forgetting this skill loses nothing. Run it for the full dashboard pass: frontmatter
> refresh, orphan-note sweep, and the live environment/PR picture below.

## Live data (injected at load — already current below)

**Project + config:**
!`bun "${CLAUDE_PLUGIN_ROOT}/scripts/where.ts"`

**Branch:** !`git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "(not a git repo)"`

**Worktrees (parallel work):**
!`git worktree list 2>/dev/null || echo "(none)"`

**Recent commits:**
!`git log --oneline -8 2>/dev/null || echo "(no git history)"`

**Uncommitted (working tree):**
!`git status --short 2>/dev/null | head -15`

**Scratch threads:**
!`bun "${CLAUDE_PLUGIN_ROOT}/scripts/threads.ts"`

**Notes missing a graph backlink (orphan risk — each should open with a wikilink to its STATE):**
!`bun "${CLAUDE_PLUGIN_ROOT}/scripts/orphans.ts"`

**Open PRs:**
!`gh pr list --limit 12 2>/dev/null || echo "(gh unavailable / not a GitHub repo)"`

## Then do this

1. **Refresh each active thread's STATE frontmatter** so its INDEX line is right. The INDEX is a
   pure render of these fields — stale frontmatter = stale dashboard:
   - `kind:` — `thread` (in-flight) · `hub` (permanent reference note) · `done` (shipped / prune
     candidate).
   - `summary:` — the single-line INDEX blurb (the **live working-state**, not just the title);
     YAML-quote it `summary: '…'` (double any `'`). A thread missing `summary`/`kind` → add them
     (the compiler falls back to the `**Status:**` first sentence and flags the gap).
   - Also keep the one-line `**Status:**` field under each STATE's H1 current — it is the
     durable working-state that survives context loss.

   **Keep the graph a clean HIERARCHY, not a star** (vault root = the scratch dir; plain paths in
   backticks create no edges):
   - The compiler links **only STATE roots** in the INDEX (never individual notes) — your job is
     to keep each note clustered under its thread: for every note flagged "missing a backlink"
     above, prepend a `> [[STATE]]` line (or `> [[INDEX]]` if its dir has no STATE). (A plugin
     hook does this for notes written during a session; this step catches hand-created ones.)
   - Ensure each STATE opens with `**Hub:** [[INDEX]]`, and add STATE↔STATE cross-links for real
     relationships (siblings under a parent effort, a reference hub → the threads it feeds).

2. **Compile the index** — run via Bash:
   `bun "${CLAUDE_PLUGIN_ROOT}/scripts/compile-index.ts"`
   (If that variable shows as a literal in your context, use the `plugin root:` path printed in the
   injected **Project + config** block above.) It renders the INDEX from every STATE's frontmatter
   (`summary`/`kind`) + live git, written atomically (tmp+rename) so two concurrent sessions
   converge instead of clobbering. **Never hand-edit the INDEX.**

3. **Print a ≤6-line summary:** active threads, branch, # open PRs, and anything stale (a
   `done`/no-PR thread → candidate for /ccx:tidy-scratch).

### STATE frontmatter contract (what the compiler reads)

```yaml
---
title: <slug>              # graph node label (Obsidian Front Matter Title plugin reads this)
kind: thread | hub | done  # which INDEX section it lands in
summary: '<one-liner>'     # the INDEX bullet — keep it current; YAML single-quoted
---
```

The compiler owns the INDEX layout: **Active threads** (`kind: thread`, sorted by STATE mtime —
recently-worked floats up) · **Notes & artifacts** (`kind: hub`, by slug) · **Done / prune
candidates** (`kind: done`) · **Worktrees** / **Open PRs** (only when present). It is a pure
function of the STATE files + live git, so concurrent compiles converge — no last-writer-wins.
