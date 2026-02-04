---
name: long-task-harness
description: Maintains continuity across long-running tasks that span multiple agent sessions. Use when starting or resuming a complex project that spans multiple sessions, or for tasks with many discrete features requiring iterative development.
---

# Long Task Harness

Structured workflows for maintaining continuity across agent sessions. Addresses the "shift change" problem where context is lost between sessions.

## First-Time Setup

**On first invocation**, check if `.long-task-harness/long-task-progress.md` exists in the project.

### If it doesn't exist: Initialize

```bash
python3 <SKILL_PATH>/scripts/init_harness.py
```

This creates a `.long-task-harness/` directory containing:
- `long-task-progress.md` - Session history and notes
- `features.json` - Feature tracking with pass/fail status
- `init.sh` - Environment setup script (optional)

### Then: Ensure persistent invocation

Check if AGENTS.md (for Codex/Droid/Cursor/Pi) or CLAUDE.md (for Claude Code) contains the harness snippet.

If not, prompt the user:

> "I notice this project doesn't have long-task-harness configured for automatic invocation. Would you like me to add the following to [AGENTS.md / CLAUDE.md]?
>
> ```markdown
> ## Multi-Session Development
> 
> This project uses long-task-harness for session continuity.
> At session start or after context reset, invoke the skill at:
> <SKILL_PATH>
> ```
>
> Where would you like me to add this?"

Use the actual path where you loaded this skill from for `<SKILL_PATH>`.

### Optional: Claude Code Hooks

For Claude Code users who want automatic enforcement:

> "Would you like to install Claude Code hooks? These will:
> - Remind to invoke this skill on session start
> - Warn before git commits if `.long-task-harness/long-task-progress.md` not staged"

If yes: `python3 <SKILL_PATH>/scripts/claude_code_install_hooks.py`

Note: These hooks are for Claude Code only. Other agents should use AGENTS.md instructions.

### Optional: Git Pre-Commit Hook (Unsupported Agents)

If the current agent does not support native hooks (e.g., Codex, Cursor, or other CLI agents),
offer an optional repo-local git pre-commit hook. Warn that it affects all commits in the
current repository clone.

If yes: `python3 <SKILL_PATH>/scripts/precommit_install_hook.py`

## Session Startup Protocol

At the start of each session:

```bash
python3 <SKILL_PATH>/scripts/read_progress.py    # Last 3 sessions
python3 <SKILL_PATH>/scripts/read_features.py    # Incomplete features
git log --oneline -10
```

Then continue from "Next Steps" in the latest session entry.

## During Work

1. Work on **one feature** at a time
2. Commit frequently with descriptive messages
3. Update `.long-task-harness/features.json` when features pass tests
4. Update `.long-task-harness/long-task-progress.md` before ending session

## Session Entry Format

```markdown
### Session N | YYYY-MM-DD | Commits: abc123..def456

#### Goal
[One-liner]

#### Accomplished
- [x] Task done
- [ ] Task carried forward

#### Decisions
- **[D1]** Decision made - reasoning

#### Surprises
- **[S1]** Expected X but found Y - implication

#### Next Steps
1. Priority task
```

### Why Log Surprises?

Surprises indicate model uncertainty and contain information-dense context. If something surprised you, it could trip up the next session (or a different agent). Examples:

- **[S1]** Expected `auth.py` to handle OAuth, but it only does API keys. OAuth is in `oauth_provider.py`.
- **[S2]** Test suite requires Docker running - not documented in README.
- **[S3]** Config file is gitignored but required - must copy from `config.example.yaml`.

This section is optional but valuable for complex or unfamiliar codebases.

## Before Ending Session

1. Update `.long-task-harness/long-task-progress.md` with session notes
2. Commit all changes including progress docs
3. Verify tests pass

## Critical Rules

- Never edit tests to make them pass - fix implementation
- Never mark features passing without testing
- Always update progress docs before ending
- Commit frequently

## Scripts

| Script | Purpose |
|--------|---------|
| `init_harness.py` | Initialize project with tracking files in `.long-task-harness/` |
| `claude_code_install_hooks.py` | Install/uninstall Claude Code hooks (prompt-based, triggers on git add) |
| `pi_install_hooks.py` | Install Pi agent hooks (tool_result modification) |
| `precommit_install_hook.py` | Install repo-local git pre-commit hook (for Codex, Cursor, etc.) |
| `precommit_check.py` | Shared pre-commit check logic (warns if progress not staged) |
| `read_progress.py` | Read sessions (`--list`, `--session N`, `-n 5`) |
| `read_features.py` | Read features (`--feature ID`, `--json`) |
| `session_metadata.py` | Generate git metadata for session entries |
| `status_line.py` | Show session status (`--full`, `--json`) |
| `check_rules.py` | Declarative rules for catching issues |
| `git_add.py` | Git add wrapper with rule checking |

---

## Additional Features

### Status Line

Quick session overview:
```bash
python3 <SKILL_PATH>/scripts/status_line.py          # Compact: S5 | F:3/5 [auth-001] | main (U:2)
python3 <SKILL_PATH>/scripts/status_line.py --full   # Detailed multi-line
python3 <SKILL_PATH>/scripts/status_line.py --json   # JSON output
```

### Declarative Rules

Define rules in `.long-task-harness/rules/*.md` to catch common issues before they're committed:

```markdown
---
name: warn-console-log
enabled: true
event: file
file_pattern: \\.tsx?$
pattern: console\\.log\\(
action: warn
---

🐛 **Debug code detected**

Remove console.log before committing.
```

**Check operations:**
```bash
python3 <SKILL_PATH>/scripts/check_rules.py bash "rm -rf /tmp"
python3 <SKILL_PATH>/scripts/check_rules.py file src/app.ts "console.log('test')"
python3 <SKILL_PATH>/scripts/check_rules.py commit
python3 <SKILL_PATH>/scripts/check_rules.py list
python3 <SKILL_PATH>/scripts/check_rules.py init  # Create default rules
```

**Events:** `bash`, `file`, `stage`, `commit`, `any`  
**Actions:** `warn` (continue), `block` (exit 1)

### Git Add with Rule Checking

Use instead of raw `git add` to catch issues at staging time:

```bash
python3 <SKILL_PATH>/scripts/git_add.py file1.py file2.ts   # Stage specific files
python3 <SKILL_PATH>/scripts/git_add.py .                    # Stage all
python3 <SKILL_PATH>/scripts/git_add.py --check-only .       # Preview without staging
python3 <SKILL_PATH>/scripts/git_add.py --force .            # Stage despite blockers
```

This checks `file` and `stage` event rules before staging, warns about missing progress updates.

---

## History Research (10+ Sessions)

For long projects, use subagents as **scouts** to find relevant history:

```
Research the history of [feature/file] in this project.
Return POINTERS (session numbers, file paths, decision refs) - not summaries.
```

Then read only the specific sessions identified.
