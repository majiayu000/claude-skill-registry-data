---
name: jmo-ralph
description: Run the Ralph autonomous agent loop on a PRD. Sets up scripts/ralph/ and executes ralph.sh to iterate through user stories.
argument-hint: "[--tool amp|claude] [max_iterations] [--prd path/to/prd.json]"
---

# JMO Ralph Loop

Run the Ralph autonomous coding agent loop on the current project's PRD.

## Setup Phase

Before running, ensure the project has the ralph infrastructure. Do these steps **only if the files don't already exist**:

```bash
# 1. Create the scripts/ralph directory
mkdir -p scripts/ralph

# 2. Copy runner files from ~/ralph/ (the ralph repo)
# Only copy if the destination doesn't exist or is older
[ ! -f scripts/ralph/ralph.sh ] && cp ~/ralph/ralph.sh scripts/ralph/ralph.sh
[ ! -f scripts/ralph/CLAUDE.md ] && cp ~/ralph/CLAUDE.md scripts/ralph/CLAUDE.md
[ ! -f scripts/ralph/prompt.md ] && cp ~/ralph/prompt.md scripts/ralph/prompt.md

# 3. Ensure ralph.sh is executable
chmod +x scripts/ralph/ralph.sh

# 4. Initialize progress.txt if missing
[ ! -f scripts/ralph/progress.txt ] && printf '# Ralph Progress Log\nStarted: %s\n---\n' "$(date)" > scripts/ralph/progress.txt
```

## PRD Resolution

Ralph needs a `prd.json` in `scripts/ralph/`. Resolve it in this order:

1. If `--prd <path>` argument provided: copy that file to `scripts/ralph/prd.json`
2. If `scripts/ralph/prd.json` already exists: use it as-is
3. If `ralph/prd.json` exists (from the ralph PRD converter skill): copy it to `scripts/ralph/prd.json`
4. If none found: **stop and tell the user** they need a prd.json first (suggest using `/ralph-skills:ralph` to convert a PRD)

## Nested Session Fix

After copying ralph.sh, patch it to allow running from within a Claude Code session. The `claude` CLI refuses to run inside another Claude Code session unless the `CLAUDECODE` env var is unset. Ensure the claude command line in ralph.sh uses `env -u CLAUDECODE claude ...` instead of bare `claude ...`.

Check if the fix is already applied (`grep -q 'env -u CLAUDECODE' scripts/ralph/ralph.sh`). If not, apply it with sed or Edit.

## Run Phase

Parse `$ARGUMENTS` for options:
- `--tool amp` or `--tool claude` (default: `claude`)
- A number for max iterations (default: `10`)
- `--prd path/to/prd.json` to specify a custom PRD location

Then run the ralph loop:

```bash
cd "$(git rev-parse --show-toplevel)" && scripts/ralph/ralph.sh --tool <tool> <max_iterations>
```

**IMPORTANT:** Run this command using Bash with `run_in_background: true` so it doesn't block the conversation. The ralph loop is long-running (each iteration spawns a full agent session).

After launching, tell the user:
- Ralph is running in the background
- How many iterations are configured
- Which tool (amp/claude) is being used
- They can check `scripts/ralph/progress.txt` for status
- They can check `scripts/ralph/prd.json` to see which stories have passed

## Argument Parsing

Parse `$ARGUMENTS` to extract:
- `--tool <value>`: "amp" or "claude" (default "claude")
- `--prd <path>`: path to a prd.json file to use
- Any bare number: max iterations (default 10)

Examples:
- `/jmo-ralph` → claude, 10 iterations, auto-find prd.json
- `/jmo-ralph --tool amp 20` → amp, 20 iterations
- `/jmo-ralph 5` → claude, 5 iterations
- `/jmo-ralph --prd tasks/my-feature-prd.json --tool amp 15` → amp, 15 iterations, specific PRD
