---
name: klondike-agent-workflow
description: Manage multi-session AI agent workflows using klondike CLI. Use when working on klondike-managed projects (those with .klondike/ directory), when starting/ending coding sessions, tracking features through lifecycle, or maintaining coherence across context window resets. Triggers on session management, feature tracking, progress handoffs, and verification workflows.
---

# Klondike Agent Workflow

Klondike bridges context windows for long-running agent sessions. **Critical: Always use CLI commands—never directly read/edit .klondike/*.json files or agent-progress.md.**

## CRITICAL: Common Mistakes to Avoid

**❌ NEVER do these:**
- `klondike --help` (wrong syntax - use `klondike` alone or `klondike <command>` without --help)
- `klondike feature --help` (wrong - just run the command, it will show usage)
- Read `.klondike/features.json` directly (use `klondike feature list`)
- Edit `agent-progress.md` manually (auto-generated, changes are lost)
- `klondike feature start` without feature ID (must be `klondike feature start F001`)
- Feature IDs like `f001` or `1` (must be uppercase: `F001`)

**✓ DO these:**
- `klondike` alone shows all commands
- `klondike feature list` to see features
- `klondike feature show F001` for details
- `klondike status` to see project overview

## Quick Decision Tree

```
Starting work?     → klondike status → klondike session start --focus "F001 - desc"
Working on feature → klondike feature start F001
Feature complete?  → Test E2E → klondike feature verify F001 --evidence "..."
Blocked?           → klondike feature block F001 --reason "..."
Ending session?    → klondike session end --summary "..." --next "..."
```

## Session Lifecycle

### 1. Session Start (Always Do First!)

```bash
klondike status                                    # See project state
klondike validate                                  # Check artifact integrity
klondike session start --focus "F001 - Login UI"  # Begin session
klondike feature start F001                        # Mark feature in-progress
```

### 2. During Work

- **One feature at a time** (tracked by `feature start`)
- Commit after each meaningful change
- Test incrementally, not at end
- If blocked: `klondike feature block F001 --reason "..."`

### 3. Session End (Before Leaving!)

```bash
klondike feature verify F001 --evidence "test-results/F001.png"
klondike session end --summary "Done" --next "Implement logout"
```

## Core Commands

| Action | Command | Notes |
|--------|---------|-------|
| Status | `klondike status` | Always start here |
| Add feature | `klondike feature add "desc" --notes "hints"` | **--notes is critical** |
| Start feature | `klondike feature start F001` | One at a time |
| List features | `klondike feature list` | Never read JSON directly |
| Show details | `klondike feature show F001` | View single feature |
| Verify | `klondike feature verify F001 --evidence "proof"` | E2E test first |
| Block | `klondike feature block F001 --reason "why"` | When stuck |
| Start session | `klondike session start --focus "F001 - desc"` | Begin work |
| End session | `klondike session end --summary "..." --next "..."` | Before leaving |

## Essential Rules

**Always:**
- Start every session with `klondike status` to see project state
- Use `--notes` when adding features (gives future agents critical context)
- Capture evidence (screenshots, logs) before `feature verify`
- Run pre-commit checks before every commit
- End sessions with `session end --summary ... --next ...`

**Never:**
- Use `klondike --help` or `klondike feature --help` (wrong syntax - see Common Mistakes)
- Read or edit `.klondike/*.json` files directly (use CLI commands)
- Edit `agent-progress.md` manually (auto-generated, edits are lost)
- Verify features without E2E testing (unit tests aren't enough)
- Commit code with failing tests, lint errors, or build failures

## Pre-Commit Checks

Detect project type and run checks. **Never commit if any fail.**

**Python (uv):** `uv run ruff check src tests && uv run pytest`  
**Node.js:** `npm run lint && npm run build && CI=true npm test`  
**Rust:** `cargo clippy && cargo test`  
**Go:** `golangci-lint run && go test ./...`

## Reference Files (Load As Needed)

Load these only when you need specific details:

- **[commands.md](references/commands.md)**: Full CLI reference with all options/flags
- **[workflows.md](references/workflows.md)**: Multi-session patterns, worktrees, complex scenarios
- **[troubleshooting.md](references/troubleshooting.md)**: Error recovery and corrupted state fixes
