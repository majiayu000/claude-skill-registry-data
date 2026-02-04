---
name: stacked-pr
description: Create and update stacked pull requests. Use this after completing an implementation phase to commit changed files.
---

# Stacked PR Workflow

This skill enables Claude to create stacked pull requests using git-town automation scripts. Each phase becomes an atomic PR that builds on previous phases.

## When to Use This Skill

Invoke this skill after completing a phase from `/implement_plan` when:
1. All automated verification has passed (`just check-test`)
2. User has confirmed manual verification is complete
3. There are uncommitted changes ready to be stacked

DO NOT use this skill:
- Before verification is complete
- When there are no changes to commit
- For non-plan-based work (use standard git workflow instead)

## Pre-Flight Checks

Before creating the stack, verify:
1. Current git status shows modified/new files
2. All tests and checks have passed
3. You know the phase number and plan context

## Workflow Instructions

### Step 1: Determine Phase Type

Check the current branch to determine if this is Phase 1 or Phase N:

```bash
git branch --show-current
```

**Decision Logic:**
- **If on `main`**: This is Phase 1 → Use `just new-stack`
- **If on `phase-X-*`**: This is Phase N (where N = X + 1) → Use `just append-stack`

### Step 2: Prepare Arguments

Both scripts require the same arguments (in order):
1. **phase-num**: The phase number (e.g., `1`, `2`, `3`)
2. **branch-name**: Short descriptive name (e.g., `websocket-foundation`, `message-parser`)
3. **commit-msg**: Full commit message (multiline string)
4. **pr-title**: PR title (e.g., `Phase 1: WebSocket Connection Foundation`)
5. **pr-body**: PR body/description (multiline string)

#### Branch Naming Convention
- Format: `phase-N-<short-description>`
- Examples:
  - `phase-1-websocket-foundation`
  - `phase-2-message-parser`
  - `phase-3-orderbook-state`

#### Commit Message Format

```
<type>: <phase-summary>

Phase N: <detailed-description>

Changes:
- <key change 1>
- <key change 2>
- <key change 3>

<any relevant context or notes>
```

Types: `feat`, `fix`, `refactor`, `test`, `chore`, `docs`

#### PR Body Format

```
## Phase N: <Title>

### Summary
<1-2 sentence overview of what this phase accomplishes>

### Changes
- <key change 1>
- <key change 2>
- <key change 3>

### Stack
<!-- branch-stack -->

### Verification
- [x] All automated tests passed (\`just check-test\`)
- [x] Manual verification completed
- [x] Code follows project patterns

### Related
Part of implementation plan: [link to plan if available]

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### Step 3: Execute the Appropriate Script

**For Phase 1 (on `main` branch):**

```bash
just new-stack \
  "<phase-num>" \
  "<branch-name>" \
  "<commit-msg>" \
  "<pr-title>" \
  "<pr-body>"
```

**For Phase N > 1 (on `phase-X-*` branch):**

```bash
just append-stack \
  "<phase-num>" \
  "<branch-name>" \
  "<commit-msg>" \
  "<pr-title>" \
  "<pr-body>"
```

## Example Workflows

### Example 1: Phase 1 (Starting New Stack)

```bash
# Current state check
$ git branch --show-current
main

$ git status
# Shows: modified files in src/connection/ (uncommitted)

# Execute new-stack
just new-stack \
  "1" \
  "websocket-foundation" \
  "feat: Add WebSocket connection foundation

Phase 1: Implement core WebSocket connection logic

Changes:
- Add WebsocketConnection class with lifecycle management
- Implement exponential backoff reconnection strategy
- Add connection health monitoring
- Create connection stats tracking

Establishes the foundation for real-time market data streaming." \
  "Phase 1: WebSocket Connection Foundation" \
  "## Phase 1: WebSocket Connection Foundation

### Summary
Implements the core WebSocket connection class with automatic reconnection, health monitoring, and stats tracking.

### Changes
- Add WebsocketConnection class with lifecycle management
- Implement exponential backoff reconnection strategy (1s → 30s)
- Add connection health monitoring (60s silence detection)
- Create connection stats tracking

### Stack
<!-- branch-stack -->

### Verification
- [x] All automated tests passed (\`just check-test\`)
- [x] Manual verification: Connected to Polymarket API successfully
- [x] Code follows project patterns

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)"
```

**What the script does:**
1. ✓ Verifies you're on `main` branch
2. ✓ Checks for uncommitted changes
3. ✓ Creates branch `phase-1-websocket-foundation` via `git town hack`
4. ✓ Commits changes (excluding `thoughts/` directory)
5. ✓ Creates PR with `--base main`
6. ✓ Syncs the stack

### Example 2: Phase 2 (Extending Stack)

```bash
# Current state check
$ git branch --show-current
phase-1-websocket-foundation

$ git status
# Shows: modified files (uncommitted)

# Execute append-stack
just append-stack \
  "2" \
  "message-parser" \
  "feat: Add message parsing with msgspec

Phase 2: Implement zero-copy message parser

Changes:
- Add msgspec-based message parser
- Define protocol structures for BookSnapshot, PriceChange, LastTradePrice
- Implement generator-based parsing for streaming
- Handle integer scaling for prices/sizes

Enables efficient parsing of WebSocket messages with zero-copy optimization." \
  "Phase 2: Message Parser with msgspec" \
  "## Phase 2: Message Parser with msgspec

### Summary
Implements zero-copy message parsing using msgspec, enabling efficient processing of WebSocket events.

### Changes
- Add msgspec-based MessageParser class
- Define protocol structures (BookSnapshot, PriceChange, LastTradePrice)
- Implement generator-based parsing for streaming
- Handle integer scaling (PRICE_SCALE=1000, SIZE_SCALE=100)

### Stack
<!-- branch-stack -->

Merge order: This PR should be merged after Phase 1.

### Verification
- [x] All automated tests passed (\`just check-test\`)
- [x] Manual verification: Parsed live messages successfully
- [x] Code follows project patterns

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)"
```

**What the script does:**
1. ✓ Verifies you're NOT on `main` (you must be on previous phase branch)
2. ✓ Auto-detects previous phase branch (`phase-1-websocket-foundation`)
3. ✓ Checks for uncommitted changes
4. ✓ Creates branch `phase-2-message-parser` via `git town append`
5. ✓ Commits changes (excluding `thoughts/` directory)
6. ✓ Creates PR with `--base phase-1-websocket-foundation`
7. ✓ Syncs the stack

## Script Features

Both scripts automatically:
- Validate pre-conditions (branch state, uncommitted changes)
- Create properly named branches with git-town
- Stage changes (excluding `thoughts/` directory)
- Commit with your provided message
- Create GitHub PR with proper base branch
- Sync the stack after PR creation
- Provide clear output with emoji indicators

## Common Issues and Solutions

### Issue: "No uncommitted changes detected"

The script checks `git status --porcelain`. Ensure:
- You have modified, added, or deleted files
- Changes are not in the `thoughts/` directory (which is excluded)

### Issue: "Previous phase branch does not exist"

For `append-stack`, ensure:
- You're on the correct previous phase branch before running
- The branch name follows the `phase-N-*` pattern

### Issue: Wrong base branch in PR

Use GitHub CLI to fix:
```bash
gh pr edit <pr-number> --base <correct-base-branch>
```

### Issue: Need to update an earlier phase

```bash
# Checkout the phase that needs changes
git checkout phase-N-<name>

# Make changes and commit
# ...

# Sync stack to propagate changes forward
git town sync --stack
```

## Key Principles

1. **One phase = One PR**: Each phase should be atomic with passing CI
2. **Sequential dependencies**: Phase N+1 builds on Phase N
3. **Clear commit messages**: Reference phase number and provide context
4. **Automatic base branches**: Scripts handle this (Phase 1 → main, Phase N → Phase N-1)
5. **Always sync**: Scripts automatically sync the stack after PR creation
6. **Thoughts excluded**: Both scripts exclude the `thoughts/` directory from commits

## Integration with /implement_plan

This skill integrates with the `/implement_plan` workflow:

1. `/implement_plan` implements a phase
2. Automated verification runs (`just check-test`)
3. Claude pauses for manual verification
4. User confirms: "Manual verification complete"
5. **Claude invokes stacked-pr skill**
6. Skill executes appropriate script (new-stack or append-stack)
7. PR created and stack synced
8. Ready for next phase

## Notes

- Uses `git-town` for stack management
- PRs created using GitHub CLI (`gh`)
- Main branch is `main` (configured in git-town)
- Stack branches should be merged in order (Phase 1, then 2, then 3, etc.)
- After all phases are merged, the stack is automatically cleaned up by git-town
- The `thoughts/` directory is automatically excluded from all commits
