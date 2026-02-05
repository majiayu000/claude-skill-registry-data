---
name: parallel-worktrees
description: Parallel development using git worktrees with Claude Code subagents. Use when spawning multiple async Claude agents across isolated worktrees, running parallel implementations, coordinating multi-agent workflows, leveraging LLM non-determinism for multiple solutions, or running background agents that signal completion. Triggers on "parallel agents", "worktrees", "subagents", "async Claude", "spawn agents", "parallel development", "multi-agent workflow", "background agents", "agent coordination", "parallel tasks".
---

# Parallel Worktrees with Claude Code Subagents

Run multiple Claude Code agents simultaneously across git worktrees to transform a single developer into a team of AI engineers. LLM non-determinism becomes an advantage: running N parallel agents produces multiple valid solutions to choose from.

## Table of Contents

- [Core Workflow](#core-workflow)
- [Git Worktrees Essentials](#git-worktrees-essentials)
- [Claude Code Subagents](#claude-code-subagents)
- [Spawning Parallel Subagents](#spawning-parallel-agents)
- [Workflow Patterns](#workflow-patterns)
- [Dependency Management](#dependency-management)
- [Common Pitfalls](#common-pitfalls)
- [When to Use Parallel vs Sequential](#when-to-use-parallel-vs-sequential)
- [Resource Considerations](#resource-considerations)
- [Background Subagents with Worktree Coordination](#background-agents-with-worktree-coordination)

## Core Workflow

1. Create isolated worktrees for each task
2. Spawn independent Claude sessions in each
3. Cycle through to monitor progress and approve permissions
4. Merge the best results

## Git Worktrees Essentials

Worktrees create additional working directories sharing a single `.git` database. Unlike cloning, they save disk space and keep history unified.

### Key Commands

```bash
# Create worktree with new branch from main
git worktree add ../project-feature-a -b feature-a main

# Create worktree for existing branch
git worktree add ../project-bugfix bugfix-123

# Organized subdirectory pattern (recommended)
mkdir -p .worktrees && echo ".worktrees/" >> .gitignore
git worktree add .worktrees/feature-auth -b feature/auth main

# List all worktrees
git worktree list

# Remove worktree (use --force if uncommitted changes)
git worktree remove ../project-feature-a

# Clean stale metadata
git worktree prune
```

### Directory Patterns

**Adjacent folders**: `my-project/`, `my-project-feature-a/`, `my-project-bugfix/`

**Subdirectory pattern** (keeps things organized):
```
my-project/
├── .worktrees/
│   ├── feature-auth/
│   ├── feature-api/
│   └── bugfix-login/
└── (main working tree)
```

## Claude Code Subagents

Subagents are specialized AI assistants with isolated context windows, custom prompts, and configurable tool access.

### Built-in Subagents

| Subagent | Model | Tools | Purpose |
|----------|-------|-------|---------|
| General-Purpose | Sonnet | All (read/write) | Complex multi-step operations |
| Plan | Sonnet | Read-only | Gather info before planning |
| Explore | Haiku | Read-only | Fast code analysis |

### Creating Custom Subagents

**Interactive**: `/agents` command opens management menu (recommended)

**File-based**: Place markdown with YAML frontmatter in:
- `.claude/agents/*.md` (project-scoped)
- `~/.claude/agents/*.md` (user-scoped)

```markdown
---
name: code-reviewer
description: Expert code review specialist. Use PROACTIVELY after changes.
tools: Read, Grep, Glob, Bash
model: inherit
---

Acts as a senior code reviewer. When invoked:
1. Run git diff to see changes
2. Focus on modified files
3. Prioritize: Critical → Warnings → Suggestions
```

**Note**: Including "PROACTIVELY" or "MUST BE USED" in descriptions increases automatic invocation.

## Spawning Parallel Agents

True parallelism requires separate Claude processes in different worktrees. Within a single REPL, subagents execute sequentially.

```bash
# Terminal 1
cd ../project-feature-a && claude

# Terminal 2
cd ../project-feature-b && claude

# Terminal 3
cd ../project-refactor && claude
```

### Quick Setup Script

```bash
#!/bin/bash
# spawn-parallel.sh FEATURE_NAME NUM_AGENTS
FEATURE=$1
NUM=${2:-3}

for i in $(seq 1 $NUM); do
  git worktree add ".worktrees/${FEATURE}-${i}" -b "${FEATURE}-${i}" main
  cp .env ".worktrees/${FEATURE}-${i}/" 2>/dev/null || true
done

echo "Worktrees created. Start Claude in each:"
for i in $(seq 1 $NUM); do
  echo "  cd .worktrees/${FEATURE}-${i} && claude"
done
```

### Custom Slash Commands

Create `.claude/commands/init-parallel.md`:
```markdown
Create $NUM git worktrees for parallel development of $FEATURE.
1. Create .worktrees/ directory if needed
2. For each tree (1 to $NUM):
   - Create worktree at `.worktrees/$FEATURE-{i}/`
   - Create branch `$FEATURE-{i}`
   - Copy environment files
3. Print commands to start Claude in each
```

## Workflow Patterns

### Pattern 1: Parallel Feature Implementation
Create 3-4 worktrees for the same feature, give each identical instructions, compare results, merge best implementation.

### Pattern 2: Explore, Plan, Code, Commit
1. Ask Claude to read relevant files (no writes)
2. Use thinking keywords ("think hard", "ultrathink") for extended reasoning
3. Have Claude create a plan document
4. Implement and commit

### Pattern 3: Test-Driven Parallel
1. First Claude writes tests, confirms they fail, commits
2. Second Claude (or `/clear`) implements to pass tests
3. Third independent review catches overfitting

### Pattern 4: Dual Claude Verification
1. One Claude writes code
2. After `/clear` or in different session, another Claude reviews
3. Fresh context catches issues original session missed

## Essential CLI Reference

See [references/cli-reference.md](references/cli-reference.md) for the complete CLI command reference.

Key commands:
- `claude` - Start interactive session
- `/clear` - Reset context window
- `/agents` - Manage subagents

## Dependency Management

Each worktree needs its own `node_modules`, venvs, etc.

```bash
# Fast copy (APFS/btrfs copy-on-write)
cp -c -r ../main/node_modules .  # macOS
cp --reflink=auto -r ../main/node_modules .  # Linux

# Deterministic install from lockfile
npm ci

# Copy environment files
cp ../main/.env . 2>/dev/null || true
```

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| "Branch already checked out" | Use different branch name or `--force` |
| Port conflicts | Configure different ports per worktree |
| Missing dependencies | Run setup process in each new worktree |
| Outdated worktrees | `git fetch origin && git rebase origin/main` |
| Claude can't create worktrees | Use shell scripts outside Claude, then start Claude within |
| Context confusion | One terminal tab per worktree, clear naming |

## When to Use Parallel vs Sequential

**Use parallel worktrees when**:
- Multiple valid solutions exist (UI, algorithms)
- Complex tasks have failure risk (run 3, pick winner)
- Clear detailed plan exists for independent execution
- Features don't overlap in file modifications

**Use sequential when**:
- Critical refactors requiring consistency
- Tightly coupled changes to same files
- Merge conflicts would cost more than parallelism saves

## Resource Considerations

- Token usage: ~15x higher with multi-agent workflows
- Subagents cannot spawn other subagents (no infinite nesting)
- Each subagent starts with clean context, needs codebase orientation
- Factor token consumption into subscription limits

## Background Agents with Worktree Coordination

Claude Code natively supports background agents via the Task tool with `run_in_background: true`. This section codifies how background agents coordinate work across git worktrees for parallel task execution.

### Architecture

```
Main Worktree (Orchestrator)
├── .agent-status/           # Coordination hub (tracked in .gitignore)
│   ├── task-api.json        # {"status": "RUNNING|COMPLETE|FAILED", "started": "...", "result": "..."}
│   └── task-ui.json
├── .agent-tasks/            # Task prompts for retry/reference
│   ├── task-api.md
│   └── task-ui.md
└── .worktrees/
    ├── task-api/            # Background agent 1
    │   └── RESULTS.md       # Agent writes summary here
    └── task-ui/             # Background agent 2
        └── RESULTS.md
```

### Using Claude Code's Native Background Agents

Background agents are launched via the Task tool:

```
Task tool with:
  - run_in_background: true
  - prompt: "Work in .worktrees/task-api/. Implement the REST API..."
  - subagent_type: "general-purpose"
```

Use `TaskOutput` to check status and retrieve results when ready.

### Worktree Setup for Background Agents

Before spawning background agents, prepare worktrees:

```bash
# Create worktrees for parallel tasks
./scripts/spawn-parallel.sh feature-api 1    # Creates .worktrees/feature-api-1/
./scripts/spawn-parallel.sh feature-ui 1     # Creates .worktrees/feature-ui-1/

# Or manually
git worktree add .worktrees/task-api -b task-api main
git worktree add .worktrees/task-ui -b task-ui main
```

### Status File Convention

Background agents write status to `.agent-status/TASK_NAME.json`:

```json
{
  "status": "COMPLETE",
  "started": "2024-01-15T10:30:00Z",
  "completed": "2024-01-15T10:45:00Z",
  "worktree": ".worktrees/task-api",
  "branch": "task-api",
  "summary": "Implemented 5 endpoints, 12 tests passing",
  "files_changed": ["src/api/users.ts", "tests/api.test.ts"]
}
```

Status values: `RUNNING`, `COMPLETE`, `FAILED`, `BLOCKED`

### Agent Task Instructions Template

Include these instructions when spawning background agents:

```markdown
## Task: [Task Name]
Work in the worktree at `.worktrees/[task-name]/`

### Requirements
[Specific task requirements]

### On Completion
1. Write a summary to `RESULTS.md` in the worktree
2. Commit all changes: `git add -A && git commit -m "[task-name]: [summary]"`
3. Update status file: Write to `../.agent-status/[task-name].json`:
   {"status": "COMPLETE", "summary": "[summary of accomplishments]"}

### On Failure
1. Document the issue in `RESULTS.md`
2. Update status: {"status": "FAILED", "error": "[what went wrong]"}
```

### Orchestration Patterns

**Pattern 1: Delegate and Continue**
```markdown
Orchestrator workflow:
1. Create worktrees for each task
2. Launch background agents with Task tool (run_in_background: true)
3. Continue working on primary task
4. Periodically check .agent-status/*.json files
5. When agents complete, review RESULTS.md and merge
```

**Pattern 2: Fan-Out/Fan-In**
```markdown
1. Spawn N background agents for N independent subtasks
2. Each works in its own worktree
3. Use TaskOutput to wait for all to complete
4. Run ./scripts/sync-worktrees.sh to merge all results
```

**Pattern 3: Pipeline with Dependencies**
```markdown
1. Background Agent A: Schema changes (no dependencies)
2. Wait for A to complete (check status file)
3. Background Agents B, C: API and UI (depend on schema)
4. Wait for B, C to complete
5. Merge in dependency order: A → B → C
```

### Syncing and Merging Results

```bash
# Review all worktree changes
./scripts/sync-worktrees.sh --status

# Merge completed work to main
./scripts/sync-worktrees.sh --merge

# Interactive mode: review each before merging
./scripts/sync-worktrees.sh --interactive
```

### Git-Based Signaling (Alternative)

For distributed setups or when status files aren't accessible:

```bash
# Background agent signals via branch push
git push origin task-api

# Main agent monitors
git fetch --all
git branch -r | grep -E "origin/(task-|feature-)"

# Check if branch has new commits
git log main..origin/task-api --oneline
```

### Best Practices

1. **One worktree per background agent**: Ensures complete isolation
2. **Non-overlapping file assignments**: Prevents merge conflicts
3. **Always write RESULTS.md**: Provides context for merging
4. **Commit before signaling complete**: Ensures work is preserved
5. **Use descriptive branch names**: Makes merge history readable
6. **Clean up after merge**: Remove worktrees and status files
7. **Set timeouts**: Prevent runaway agents consuming resources

### Checking Agent Status from Main Session

The main Claude session can monitor background agents:

```bash
# Quick status check
cat .agent-status/*.json | jq -r '.status'

# Detailed view
for f in .agent-status/*.json; do
  echo "=== $(basename $f .json) ==="
  cat "$f" | jq .
done

# Check if all complete
if grep -L '"status": "COMPLETE"' .agent-status/*.json; then
  echo "Some agents still running"
else
  echo "All agents complete - ready to merge"
fi
```
