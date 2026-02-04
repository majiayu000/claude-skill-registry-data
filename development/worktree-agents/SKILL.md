---
name: worktree-agents
description: Create worktrees and launch Claude Code agents. USE THIS SKILL when user says "create worktree", "spin up worktree", "new worktree", "worktree for X", or wants parallel development branches. Also handles worktree status, cleanup, and agent launching.
---

# Worktree Agent Management

This skill helps manage parallel development using git worktrees with AI coding agents. Each worktree is an isolated copy of the repo on a different branch, allowing multiple Claude Code agents to work simultaneously without conflicts.

## When This Skill Activates

**Trigger phrases:**
- "spin up worktrees for X, Y, Z"
- "create worktrees and launch agents"
- "parallelize work on these features"
- "what's the status of my worktrees?"
- "launch agent in worktree X"
- "clean up merged worktrees"
- "clean up the X worktree"

## Intent

The user wants to:
1. **Create**: Set up isolated worktrees for parallel feature development
2. **Launch**: Start Claude Code agents in those worktrees
3. **Monitor**: See what's running and what state each worktree is in
4. **Cleanup**: Remove worktrees after PRs are merged

## CRITICAL: Directory Structure

**All worktrees MUST be created in the `worktrees/` subdirectory** relative to the repo root.

```
repo-root/
├── worktrees/                          # All worktrees go here
│   ├── feature/auth/                   # Branch: feature/auth
│   ├── feature/payments/               # Branch: feature/payments
│   └── fix/login-bug/                  # Branch: fix/login-bug
├── src/
├── .claude/
└── ...
```

**NEVER create worktrees as sibling directories** (e.g., `../repo-feature-auth`). This breaks:
- Status tracking
- Cleanup scripts
- Registry path matching

**Correct:**
```bash
git worktree add worktrees/feature/auth -b feature/auth
```

**Wrong:**
```bash
git worktree add ../repo-feature-auth -b feature/auth  # NO!
```

## Architecture

```
.claude/skills/worktree-agents/
├── SKILL.md           # This file - instructions for Claude
├── config.json        # User preferences (terminal, shell, ports)
└── scripts/
    ├── launch-agent.sh    # Opens terminal with Claude Code
    ├── status.sh          # Shows worktree overview
    ├── register.sh        # Adds worktree to registry
    ├── unregister.sh      # Removes from registry
    └── cleanup.sh         # Full cleanup workflow

.claude/worktree-registry.json    # Tracks active worktrees (in repo root)
```

## What You (Claude) Do vs What Scripts Do

| Task | Who Does It | How |
|------|-------------|-----|
| Create git worktree | **You** | `git worktree add worktrees/<branch> -b <branch>` |
| Copy .agents/ directory | **You** | `cp -r .agents worktrees/<branch>/` (for plans, RCAs, etc.) |
| Install dependencies | **You** | `cd worktrees/<branch> && npm install` |
| Run validation | **You** | `npm run type-check && npm run lint && npm test` |
| Pick next available port | **You** | Look at registry, find unused port in range |
| Register worktree | **Script** | `scripts/register.sh <branch> <path> <port> [task]` |
| Launch agent in terminal | **Script** | `scripts/launch-agent.sh <path> [task]` |
| Show status | **Script** | `scripts/status.sh` |
| Full cleanup | **Script** | `scripts/cleanup.sh <branch> [--delete-branch]` |
| Check PR status | **You** | `gh pr list --head <branch> --json number,state` |
| Decide what to clean | **You** | Check if PR merged, ask user if unsure |

## IMPORTANT: Copy .agents/ Directory

**Why**: Uncommitted files (plans, RCA reports, PRPs) only exist in the source worktree. New worktrees start clean from git, so these files won't be there.

**Always copy** the `.agents/` directory to new worktrees so the agent has access to:
- `.agents/plans/` - Implementation plans to execute
- `.agents/rca-reports/` - Root cause analysis reports
- `.agents/PRPs/` - Product requirement plans

```bash
# After creating worktree, copy .agents/
cp -r .agents worktrees/<branch>/.agents
```

## Port Allocation

Ports are assigned from the configured range (default: 8124-8128).

**To find next available port:**
1. Read `.claude/worktree-registry.json`
2. Get list of used ports: `jq '.worktrees[].port' .claude/worktree-registry.json`
3. Pick first unused port in range

**Port range** (from config.json):
- Default: 8124, 8125, 8126, 8127, 8128
- Maximum 5 concurrent worktrees

---

## Workflows

### 1. Create Worktrees with Agents

**User says:** "Spin up worktrees for feature/auth and feature/payments"

**You do:**

```
1. For each branch:
   a. Find next available port (check registry)
   b. Create worktree:
      git worktree add worktrees/<branch> -b <branch>
   c. Copy .agents/ directory (plans, RCAs, PRPs):
      cp -r .agents worktrees/<branch>/.agents
   d. Install dependencies:
      cd worktrees/<branch> && npm install
   e. Run validation (optional but recommended):
      npm run type-check && npm run lint && npm test
   f. Register:
      scripts/register.sh <branch> worktrees/<branch> <port> "[task]"
   g. Launch agent:
      scripts/launch-agent.sh worktrees/<branch> "[task]"

2. Report summary to user
```

**Example commands:**
```bash
# Create worktrees
git worktree add worktrees/feature/auth -b feature/auth
git worktree add worktrees/feature/payments -b feature/payments

# Copy .agents/ directory (uncommitted plans, RCAs, etc.)
cp -r .agents worktrees/feature/auth/.agents
cp -r .agents worktrees/feature/payments/.agents

# Install deps
cd worktrees/feature/auth && npm install
cd worktrees/feature/payments && npm install

# Register (finds script in .claude/skills/worktree-agents/scripts/)
.claude/skills/worktree-agents/scripts/register.sh feature/auth worktrees/feature/auth 8124 "Implement OAuth"
.claude/skills/worktree-agents/scripts/register.sh feature/payments worktrees/feature/payments 8125 "Add Stripe"

# Launch agents
.claude/skills/worktree-agents/scripts/launch-agent.sh worktrees/feature/auth "Implement OAuth"
.claude/skills/worktree-agents/scripts/launch-agent.sh worktrees/feature/payments "Add Stripe"
```

### 2. Check Status

**User says:** "What's the status?" or "Show my worktrees"

**You do:**
```bash
.claude/skills/worktree-agents/scripts/status.sh
```

This shows:
- All registered worktrees
- Port assignments
- PR status (fetched from GitHub)
- When agent was launched
- Whether worktree directory exists

### 3. Launch Agent in Existing Worktree

**User says:** "Launch an agent in the auth worktree"

**You do:**
```bash
# Find the worktree path
git worktree list | grep auth

# Launch
.claude/skills/worktree-agents/scripts/launch-agent.sh worktrees/feature/auth "Continue auth work"
```

### 4. Cleanup Worktrees

**User says:** "Clean up the auth worktree" or "Clean up merged worktrees"

**For single worktree:**
```bash
# Check if PR is merged first
gh pr list --head feature/auth --state merged

# If merged (or user confirms), clean up
.claude/skills/worktree-agents/scripts/cleanup.sh feature/auth

# To also delete the git branch:
.claude/skills/worktree-agents/scripts/cleanup.sh feature/auth --delete-branch
```

**For "merged" worktrees:**
```bash
# Get list of registered worktrees
cat .claude/worktree-registry.json

# For each, check if PR is merged
gh pr list --head <branch> --state merged --json number

# Clean up those with merged PRs
.claude/skills/worktree-agents/scripts/cleanup.sh <branch> --delete-branch
```

**Cleanup script handles:**
- Killing processes on the port
- Removing worktree directory
- Pruning git references
- Unregistering from registry
- Optionally deleting local+remote branches

---

## Registry Schema

Location: `.claude/worktree-registry.json`

```json
{
  "worktrees": [
    {
      "branch": "feature/auth",
      "path": "worktrees/feature/auth",
      "port": 8124,
      "createdAt": "2025-12-02T10:00:00Z",
      "agentLaunchedAt": "2025-12-02T10:05:00Z",
      "task": "Implement OAuth login",
      "prNumber": null
    }
  ]
}
```

**You update `agentLaunchedAt`** after launching by re-running register.sh (it updates existing entries).

**You update `prNumber`** when you discover a PR exists:
```bash
# Check for PR
PR_NUM=$(gh pr list --head feature/auth --json number --jq '.[0].number')

# Update registry with jq
jq ".worktrees |= map(if .branch == \"feature/auth\" then .prNumber = $PR_NUM else . end)" \
  .claude/worktree-registry.json > tmp.json && mv tmp.json .claude/worktree-registry.json
```

---

## Configuration

Location: `.claude/skills/worktree-agents/config.json`

```json
{
  "terminal": "ghostty",      // ghostty, iterm2, or tmux
  "shell": "fish",            // fish, bash, or zsh
  "claudeCommand": "cc",      // command to launch Claude Code
  "portRange": {
    "start": 8124,
    "end": 8128
  }
}
```

**Terminal options:**
- `ghostty` - Opens new Ghostty window (macOS)
- `iterm2` - Opens new iTerm2 window (macOS)
- `tmux` - Creates new tmux session (cross-platform)

---

## Script Reference

### launch-agent.sh
```bash
./scripts/launch-agent.sh <worktree-path> [task-description]

# Examples:
./scripts/launch-agent.sh worktrees/feature/auth
./scripts/launch-agent.sh worktrees/feature/auth "Implement OAuth login"
```

### register.sh
```bash
./scripts/register.sh <branch> <path> <port> [task]

# Examples:
./scripts/register.sh feature/auth worktrees/feature/auth 8124
./scripts/register.sh feature/auth worktrees/feature/auth 8124 "Implement OAuth"
```

### unregister.sh
```bash
./scripts/unregister.sh <branch>

# Example:
./scripts/unregister.sh feature/auth
```

### cleanup.sh
```bash
./scripts/cleanup.sh <branch> [--delete-branch]

# Examples:
./scripts/cleanup.sh feature/auth                    # Keep git branch
./scripts/cleanup.sh feature/auth --delete-branch   # Delete branch too
```

### status.sh
```bash
./scripts/status.sh
```

---

## Safety Guidelines

1. **Before cleaning up**, check PR status:
   - If PR is merged: safe to clean up everything
   - If PR is open: warn user, confirm before proceeding
   - If no PR: warn user there may be unsubmitted work

2. **Before deleting branches**, confirm with user if:
   - PR is not merged
   - No PR exists
   - Worktree has uncommitted changes

3. **Port conflicts**: If a port is in use by a non-worktree process, pick a different port

4. **Max 5 worktrees**: The default port range only supports 5 concurrent worktrees

---

## Common Issues

### "Port already in use"
```bash
# Find what's using it
lsof -i :8124

# Kill if it's a stale process
kill -9 <PID>
```

### "Worktree already exists"
```bash
# Check existing worktrees
git worktree list

# Remove if stale
git worktree remove worktrees/<branch> --force
git worktree prune
```

### "Branch already exists"
The git worktree command handles this:
```bash
# This tries -b (new branch) first, falls back to existing
git worktree add worktrees/<branch> -b <branch> 2>/dev/null || git worktree add worktrees/<branch> <branch>
```

### Registry out of sync
```bash
# Compare registry to actual worktrees
cat .claude/worktree-registry.json
git worktree list

# Manually clean up stale entries
.claude/skills/worktree-agents/scripts/unregister.sh <stale-branch>
```

---

## Example Session

**User:** "Spin up 2 worktrees for feature/dark-mode and fix/login-bug, then launch agents"

**You:**
1. Check registry for used ports → none used, start with 8124
2. Create worktrees:
   ```bash
   git worktree add worktrees/feature/dark-mode -b feature/dark-mode
   git worktree add worktrees/fix/login-bug -b fix/login-bug
   ```
3. Copy .agents/ directory (so agents have access to plans, RCAs):
   ```bash
   cp -r .agents worktrees/feature/dark-mode/.agents
   cp -r .agents worktrees/fix/login-bug/.agents
   ```
4. Install deps:
   ```bash
   cd worktrees/feature/dark-mode && npm install
   cd worktrees/fix/login-bug && npm install
   ```
5. Register:
   ```bash
   .claude/skills/worktree-agents/scripts/register.sh feature/dark-mode worktrees/feature/dark-mode 8124 "Implement dark mode toggle"
   .claude/skills/worktree-agents/scripts/register.sh fix/login-bug worktrees/fix/login-bug 8125 "Fix login redirect bug"
   ```
6. Launch agents:
   ```bash
   .claude/skills/worktree-agents/scripts/launch-agent.sh worktrees/feature/dark-mode "Implement dark mode toggle"
   .claude/skills/worktree-agents/scripts/launch-agent.sh worktrees/fix/login-bug "Fix login redirect bug"
   ```
7. Report:
   ```
   Created 2 worktrees with agents:

   | Branch | Port | Task |
   |--------|------|------|
   | feature/dark-mode | 8124 | Implement dark mode toggle |
   | fix/login-bug | 8125 | Fix login redirect bug |

   Both agents are now running in separate Ghostty windows.
   .agents/ directory copied to each worktree.
   ```
