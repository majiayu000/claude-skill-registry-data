---
name: sweep
description: Systematically read an entire codebase to discover quality issues, document findings, then triage them into AgentBoard workspace cards for /orchestrate to fix. Use whenever the user wants to sweep, audit, survey, or clean up a codebase, find technical debt, or inventory what's wrong before fixing — e.g. "sweep the codebase", "audit code quality", "this app is a mess", "find issues in this project". Read-only with respect to the target code; it ends by creating board cards (use codebase-sweep for the read-only methodology without board creation).
---

# Sweep — Codebase Quality Discovery

Systematically read an entire codebase, document every quality issue found, then organize findings into workspace board cards.

**Prerequisite:** The `codebase-sweep` skill provides the methodology for reading code critically. Load it before starting.

## Instructions

Follow these steps in order.

### Step 1: Setup

1. **Load the codebase-sweep skill** — it teaches you how to read code critically and write good findings. Follow its methodology throughout the sweep.

2. **Load tools** by calling `ToolSearch` for `agentboard`, `codegraph`, and `rag`.

3. **Authenticate if needed, then verify connectivity.** If only `agentboard_authenticate` and `agentboard_complete_authentication` are visible, run the OAuth bootstrap from `skills/agentboard/SKILL.md` §1.3 first. Then call `agentboard_health_check`. If it fails post-auth, the cloud service is unreachable — show the error and stop.

4. **Select or create an app:**
   - Call `agentboard_list_apps`
   - If apps exist, ask the user which one
   - If none, call `agentboard_create_app`

5. **Select or create a workspace board:**
   - Call `agentboard_list_boards` for the app
   - If boards exist, ask the user which one
   - If none, call `agentboard_create_board` with a name like "Codebase Cleanup" or similar

6. **Identify the target codebase:**
   - Check the app's `target_project_path`
   - If not set, ask the user for the path to the codebase to sweep
   - Confirm the path exists and contains code

### Step 2: Reconnaissance

Build a structural map before reading any code.

1. **Scan with codegraph:**
   - `codegraph_scan` on the target codebase path
   - `codegraph_get_stats` — note total files, most-connected files, most-depended-on files
   - `codegraph_find_entry_points` — identify application entry points

2. **Codebase RAG is auto-bootstrapped** — no init needed. The first `rag_search` call in a never-indexed project may return `status: "indexing"`; retry after a few seconds.

3. **Read config files** — `package.json`, `tsconfig.json`, build configs, etc. Understand the stack, dependencies, and tooling.

4. **Determine reading order:**
   - Start with entry points (main.js, index.js, App.jsx, etc.)
   - Then most-connected files (highest coupling = highest importance)
   - Then work outward through remaining files by directory
   - Skip `node_modules/`, `dist/`, build artifacts, and vendored code

5. **Create the findings document:**
   - Create `docs/sweep/` directory in the target project if it doesn't exist
   - Start `docs/sweep/YYYY-MM-DD-findings.md` with the header (see skill for format)

### Step 3: Broad Sweep

Read the codebase following your reading order. For each file or logical group of files:

1. **Read the file** using the Read tool
2. **Note every issue you find** — append to the findings document
3. **Follow the codebase-sweep skill's guidance** on what signals to watch for, how to calibrate severity, and how to write findings
4. **When you see the same issue across multiple files**, group them in a single finding entry listing all affected files

**Rules during the sweep:**
- Do NOT create workspace cards yet
- Do NOT categorize or group findings yet
- Do NOT suggest fixes
- Do NOT fix anything
- Just read, find problems, and write them down
- One to two sentences per finding, with file paths and line numbers

**For large codebases:** If the codebase has more than ~100 files, batch the sweep by directory or module. Write findings as you complete each batch. This keeps the findings document growing progressively rather than dumping everything at the end.

### Step 4: Triage

After the sweep is complete:

1. **Read your entire findings document** from top to bottom.

2. **Group related findings** — multiple files with the same type of problem become one group. Use the codebase-sweep skill's triage process.

3. **Let categories emerge** — name the groups based on what you actually found. Do not use predetermined category names.

4. **Set priority** for each group — based on severity concentration and whether the group blocks other groups from being fixed.

5. **Identify dependencies** between groups — what must be fixed before what? Set `depends_on` accordingly.

6. **Create workspace cards** — one per group:
   - Call `agentboard_create_workspace_card` for each group
   - `title`: Clear, actionable (e.g., "Standardize error handling across API routes")
   - `description`: Summarize the findings in this group — which files, what's wrong, severity
   - `priority`: From step 4
   - Set `depends_on` from step 5

### Step 5: Summary

Show the user what was found:

```
## Sweep Complete

**Codebase:** [path]
**Files scanned:** [N]
**Total findings:** [N] issues across [N] files
**Cards created:** [N] on board "[board name]"

### Categories Found
| Category | Cards | Findings | Severity |
|----------|-------|----------|----------|
| [emerged name] | [N] | [N] | [N crit, N high, ...] |

### Dependency Order
[Show which cards block which — the natural fix order]

### Recommended Starting Point
[First 3-5 cards to tackle, based on priority and dependency order]

**Findings document:** docs/sweep/YYYY-MM-DD-findings.md
**Next step:** Run `/orchestrate` to begin fixing, or `/board-status` to review the board.
```

7. **Commit the findings document** to git on the current branch.

## Notes

- The sweep is read-only with respect to the target codebase — no code changes, only the findings document is written
- For very large codebases, the sweep may take a full session. Use `/wrap-up` if you need to pause and `/pickup` to resume
- After the sweep, the board is ready for `/orchestrate` — the existing planning → review → implementation → audit pipeline handles the fixes
- The findings document persists as a reference — planning agents can read it for additional context when building their fix plans
