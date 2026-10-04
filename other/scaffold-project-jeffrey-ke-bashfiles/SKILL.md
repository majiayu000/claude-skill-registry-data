---
name: scaffold-project
description: Create or update a CLAUDE.md and .docs_claude/ structure for the current project. Auto-explores the repo, interviews the user to fill gaps, generates the module index and data flow. Idempotent — safe to re-run when new files are added or folders are missing.
user_invocable: true
argument-hint: "[force] — skip the overwrite prompt and regenerate CLAUDE.md"
allowed-tools: Read, Write, Edit, Bash(mkdir:*), Bash(ls:*), Bash(ln:*), Glob, Grep, Agent, AskUserQuestion
---

# Scaffold Project

Generate (or regenerate) a `CLAUDE.md` and `.docs_claude/` documentation structure for the current working directory.

## Core Recipe

### Step 1 — Check existing state

1. Check if `CLAUDE.md` exists in cwd.
   - **Exists and no `force` argument**: Ask the user whether to overwrite or abort. If abort, stop.
   - **Exists and `force`**: Proceed — will overwrite.
   - **Does not exist**: Proceed.
2. Check which `.docs_claude/` subdirectories already exist. Note any missing ones.

### Step 2 — Create folder structure

Create any missing directories. Never delete existing contents.

```
.docs_claude/
  plans/
    active/
    completed/
  style-and-beliefs/
```

Use `mkdir -p` — idempotent by nature.

### Step 3 — Explore the codebase

Spawn an Explore agent (subagent_type: Explore, thoroughness: very thorough) with this prompt:

```
Very thorough exploration of [CWD]. I need a complete map:

1. List ALL source files and their roles (read the top of each file — imports, main classes/functions)
2. List all config files, data files, and non-code artifacts
3. List all directories and their purposes
4. Identify entry points (main scripts, CLI tools)
5. Identify data flow — what calls what, what produces/consumes what
6. Note external dependencies that are imported but not defined in this repo

Be exhaustive. Read every source file at least partially (first 50-100 lines). Report back with a structured summary including a module table (Module | Role | Key exports) and a data flow description.
```

### Step 4 — Interview the user

Present the exploration findings as a draft module index table and data flow summary. Use AskUserQuestion to ask:

1. **"Is this module index accurate? What's wrong or missing?"** — Options: "Looks good", "Needs corrections" (user provides corrections via Other)
2. **"How would you describe this project in one line?"** — Free text (all options should be reasonable guesses from the exploration; user picks one or writes their own)
3. **"What's the quick start command to run this project?"** — Free text (guess from entry points found; user corrects if wrong)

Incorporate corrections before generating the final CLAUDE.md.

### Step 5 — Write CLAUDE.md

Write `CLAUDE.md` in the cwd with this structure. Use the frontmatter exactly as shown.

```markdown
---
description:
alwaysApply: true
---

# {project-name}

{one-line description from interview}

## Quick start

```
{quick start command from interview}
```

## Module index

| Module | Role | Key exports |
|---|---|---|
{rows from exploration + interview corrections}

## Data flow

{data flow description or ASCII diagram from exploration + interview corrections}

## Where to look next

Documentation, plans, style guidance, and investigation notes live in `.docs_claude/`.

- `.docs_claude/plans/active/` -- plans currently in progress
- `.docs_claude/plans/completed/` -- finished plans
- `.docs_claude/style-and-beliefs/` -- code style and design principles

## Plans & workflow

Plans are first-class artifacts in `.docs_claude/plans/`.

- **Small change** (one file, obvious fix): no plan needed.
- **Medium change** (new feature, wire up a subsystem): lightweight plan in `plans/active/`.
- **Complex change** (new architecture, pipeline redesign): full execution plan with goal, approach, staged checklist, and decision log in `plans/active/`.

Move completed plans to `plans/completed/`.

**Before planning any new implementation:**
1. Read `plans/active/` -- don't duplicate in-progress work.
2. Read `plans/completed/` -- learn from past decisions and avoid re-solving solved problems.
3. Read relevant docs in `.docs_claude/` -- context that shaped the current design.

## Core beliefs

Before planning any implementation, read `/reusable-parts` and apply its guidelines to the design.
```

### Step 6 — Report

Tell the user what was created or updated. List any folders that were newly created vs already existed. Remind them the files are unstaged.

## Idempotency

This skill is designed to be re-run safely:

- `mkdir -p` never fails on existing directories
- Existing contents of `.docs_claude/` (plans, style docs, notes) are never touched
- Only `CLAUDE.md` is overwritten (with user permission unless `force` is passed)
- The explore + interview cycle picks up new files on each run

## When Applying This Skill

1. Always run from the project root (cwd).
2. Never delete anything inside `.docs_claude/` — only create missing structure.
3. Never commit or stage files. Leave them for the user to review.
4. The Core Beliefs section is always exactly one line: the `/reusable-parts` instruction. Do not add other beliefs.
5. If re-running on an existing project, the new CLAUDE.md should reflect the *current* state of the code, not the old CLAUDE.md's contents.

## .docs_claude Doc Conventions

Every `.md` file created or updated inside `.docs_claude/` (including plans) **must** begin with a `## Keywords / Tags` section as its very first content, before any headings. Use a bulleted list of lowercase-kebab-case tags. Example:

```markdown
## Keywords / Tags
- isaac-sim
- replicator
- camera-intrinsics
- investigation
- gotchas
```

Choose tags covering: system/module (e.g. `training-pipeline`, `datagen`, `sam2`), doc type (e.g. `architecture`, `api-reference`, `investigation`, `plan-completed`, `plan-active`, `style-guide`, `gotchas`, `debugging`), and key concepts. Aim for 5–12 tags. This makes docs findable via "has X been done?" or "did we learn anything about Y?" queries.
