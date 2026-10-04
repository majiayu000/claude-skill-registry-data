---
name: lessons-sync
description: "Copies new entries from root lesson files (at ~/.claude/memory/lessons/{stack}.md) to the current project's nested copy (at {project}/memory/lessons/{stack}.md), appending only — never overwrites project-specific entries. Syncs all stacks or a named stack on command. Run at session start to ensure the project always has the latest root lessons, at session end to capture lessons learned during the session, or on-demand after adding a new entry to a root file. Best for engineers working across multiple projects who want centralized, consistent lessons without losing project-specific additions. Also for: onboarding new projects with existing lesson libraries, and cross-project lesson audits."
---

# Lesson Sync — Root to Nested

Sync `~/.claude/memory/lessons/{stack}.md` (root canonical) to the current project's `memory/lessons/{stack}.md` (nested copy).

---

## Step 1: Determine current project

Read `medium-term.md` at `~/.claude/memory/medium-term.md` to find the current project and its stacks.

---

## Step 2: Determine stacks to sync

**If no argument provided:** sync ALL stacks for the current project (from medium-term.md project table).

**If argument provided** (e.g., `/lessons-sync vercel`): sync only that stack.

---

## Step 3: Sync each stack

For each stack to sync:

1. Read `~/.claude/memory/lessons/{stack}.md` (root)
2. Read `{project}/memory/lessons/{stack}.md` (nested, if exists)
3. If nested doesn't exist: copy root to nested location
4. If nested exists: find entries in root that are NOT in nested, append those entries to nested

**Sync rule**: Root is always canonical. Nested may have extra entries (project-specific). Do NOT remove extra entries from nested. Only ADD entries from root.

**Format for new entries**: Same format as root file. Entries are identifiable by the `[YYYY-MM-DD]` date prefix.

---

## Step 4: Report

After sync:
```
Synced {n} stacks for {project}:
  ✓ vercel.md    (3 new entries)
  ✓ nextjs.md    (1 new entry)
  ✗ windows.md   (already up to date)
```
