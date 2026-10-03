---
name: status-memory
description: Maintains a compact, agent-readable PROJECT_MEMORY.md inside the active project. Updates it in-place on each invocation. Automatically configures session-start memory loading on first run. Use when the user asks for a status update, session recap, or "save progress".
allowed-tools: [Read, Write, Glob, Grep, Bash]
---

# Status Memory

Maintains a single compact living memory file per project — optimised for agent consumption, not human reading. Updated in-place on every invocation. On first run it self-configures so that future sessions load this memory automatically.

---

## Setup Requirements for Users

**Minimum one-time setup (copy one file):**
```
<your-project>/.claude/skills/status-memory/SKILL.md
```

After that, run `/status-memory` once. The skill handles everything else automatically:
- Writes `PROJECT_MEMORY.md` into the project
- Adds the session-start loading instruction to `CLAUDE.md` (creates it if absent)
- Future sessions automatically read `PROJECT_MEMORY.md` at startup

**There is no automatic periodic update.** Users must invoke `/status-memory` manually to refresh the memory — at the end of a session, after a big feature, or whenever they want a checkpoint. This is intentional: automatic updates risk writing stale or mid-task state.

---

## Step 1 — Establish the Project Root

```bash
git rev-parse --show-toplevel 2>/dev/null || pwd
```

- Git root wins if available; otherwise use `pwd`
- Extract **project name** from the last path component
- All subsequent paths must be descendants of this root

---

## Step 2 — Derive the Project-Scoped Memory Path

```
~/.claude/projects/<encoded-root>/memory/MEMORY.md
```

`<encoded-root>` = project root with every `/` replaced by `-`

Read only if the file exists at that exact path. Never read another project's folder.

---

## Step 3 — Self-Configure on First Run

Check whether `<project-root>/status/PROJECT_MEMORY.md` already exists.

**If it does not exist (first run):**

1. **Patch `CLAUDE.md`** — add the session-start block below at the very top of the file, before any existing content. Create `CLAUDE.md` if it does not exist.

   ```
   ## Session Start — Restore Context
   At the start of every session, read `status/PROJECT_MEMORY.md` if it
   exists. Ingest it silently — do not repeat its contents unless asked. Use it
   to inform all decisions: architecture, completed work, pending tasks, open questions.

   ---
   ```

   Skip this step if the string `PROJECT_MEMORY.md` already appears anywhere in `CLAUDE.md`.

2. **Confirm to the user** that self-configuration is complete and that future sessions will load memory automatically.

**If `PROJECT_MEMORY.md` already exists (subsequent runs):** skip Step 3 entirely and proceed to Step 4.

---

## Step 4 — Gather Context (all scoped to project root)

Run in parallel:

```bash
git log --oneline -20
git diff --stat HEAD~5 HEAD 2>/dev/null
git branch --show-current 2>/dev/null
git status --short 2>/dev/null
```

Read whichever exist inside the project root:
- Task tracker: `Feature_doc.md`, `FEATURES.md`, `TODO.md`, `ROADMAP.md`, `CHANGELOG.md`, `docs/tasks.md`
- Project description: `CLAUDE.md`, `AGENTS.md`, `README.md`
- Existing memory: `<project-root>/status/PROJECT_MEMORY.md`
- Project-scoped Claude memory (derived in Step 2)

---

## Step 5 — Build the Updated Memory

Synthesise all sources into the compact format below.

**Include:**
- Tech stack and architecture (one line)
- Completed features/tasks (from tracker `[x]` items + git log)
- Pending features/tasks (from tracker `[ ]` items)
- What changed this session (from git log + conversation context)
- Key architectural decisions that affect future work
- Open questions blocking future decisions
- Critical files an agent needs to know

**Exclude:**
- Prose, narrative, and explanation
- Anything trivially derivable by reading the code
- Decorative formatting that wastes tokens
- Completed items that encode no lasting decision

---

## Step 6 — Write / Overwrite the Memory File

```
<project-root>/status/PROJECT_MEMORY.md
```

- `mkdir -p` the directory if needed
- **Always overwrite** — this is a living file, not an append log
- Target length: **under 120 lines** — compress aggressively
- After writing, print the file path and a 2–3 sentence plain-English summary

---

## Output Format (compact, agent-optimised)

```markdown
<!-- <ProjectName> PROJECT_MEMORY — updated <YYYY-MM-DD> -->
<!-- Read this file at the start of every session to restore context -->

## Stack
<one line: language, framework, architecture, backend, auth>

## Features Complete
<comma-separated short labels, e.g.: Auth, ProfilePage, RecipeRating, Discover>

## Features Pending
- **<Name>**: one-line description + what decision or work is blocking it

## Last Session (<YYYY-MM-DD>)
- `path/to/file` — what changed and why (one line each)

## Key Decisions
- <decision> — <why it matters / what it affects>

## Open Questions
- <question> — <why it blocks and what the options are>

## Critical Files
- `path/to/file` — what it owns or why an agent needs to know it
```

---

## Session Restoration (READ mode)

When starting a session in a project that has `status/PROJECT_MEMORY.md`:

1. Read the file immediately and silently
2. Do not summarise or repeat its contents unless the user asks
3. Use it to inform all responses: file locations, decisions already made, pending tasks, open questions
4. If the memory is stale (last updated > 7 days ago), note it once and offer to refresh

---

## Isolation Rules

1. Project root fixed in Step 1 — all file ops must be under that root or its scoped memory path
2. Only read `~/.claude/projects/<encoded-root>/memory/MEMORY.md` — never another project's folder
3. Output goes only to `<project-root>/status/PROJECT_MEMORY.md`
4. `CLAUDE.md` patching is scoped to the project root only
5. No cross-project inference from sibling or parent directories

---

## Compression Rules

- No section may exceed 10 lines — summarise aggressively
- Combine related decisions into one bullet
- Drop sections with no content
- Prefer tokens that reduce future ambiguity over tokens that restate the obvious
