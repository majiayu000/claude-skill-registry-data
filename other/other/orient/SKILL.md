---
name: orient
description: "Orient to a project - review structure, docs, and beads tasks to identify parallelizable work"
allowed-tools: Read, Bash, Glob, Grep, Task
---

# Project Orientation

You are an orchestrating agent orienting to this project. Your goal is to build comprehensive context and identify parallelizable work streams.

**IMPORTANT**: Use extended thinking (ultrathink) throughout this process. Take your time to deeply analyze the project state.

## Phase 1: Project Discovery

### 1.1 Identify Project Root and Type

```bash
pwd
ls -la
git remote -v 2>/dev/null || echo "Not a git repo"
```

Determine:
- Project name
- Primary language/framework
- Monorepo vs single project

### 1.2 Read Core Documentation

Read these files IN ORDER (skip if not found):

1. **CLAUDE.md** - AI assistant guidelines (HIGHEST PRIORITY)
2. **AGENTS.md** - Multi-agent workflow documentation
3. **PROJECT_SPEC.md** - Project specification and requirements
4. **README.md** - Project overview and setup

For each file found, extract:
- Project purpose and goals
- Key architectural decisions
- Development workflow and commands
- Patterns and conventions to follow

### 1.3 Understand Project Structure

```bash
# Get directory structure (2 levels deep)
find . -type d -maxdepth 2 -not -path '*/\.*' -not -path './node_modules/*' -not -path './.venv/*' -not -path './venv/*' | head -50

# Identify key source directories
ls -la src/ app/ lib/ moneyprinter/ fastapi_backend/ nextjs-frontend/ 2>/dev/null | head -30
```

Map out:
- Source code locations
- Test locations
- Configuration files
- Build/deployment setup

## Phase 1.5: Deep Research (Parallel)

When the project has significant complexity or unfamiliar patterns, run these research agents in parallel using the Task tool to build deeper context:

### Research Agents

1. **repo-research-analyst**
   - Read agent definition: `~/.claude/agents/research/repo-research-analyst.md`
   - Input: Project root path, file structure from Phase 1
   - Output: Convention guide, architecture map, code style patterns
   - Use when: New to the codebase, unfamiliar framework, or complex architecture

2. **git-history-analyzer**
   - Read agent definition: `~/.claude/agents/research/git-history-analyzer.md`
   - Input: Git repository path
   - Output: Contributor expertise areas, decision patterns, hot spots
   - Use when: Need to understand who knows what, or why decisions were made

### Launch Pattern

```
Use Task tool with subagent_type=general-purpose to run research agents in parallel:

Task 1: repo-research-analyst
- Read ~/.claude/agents/research/repo-research-analyst.md
- Analyze project structure and conventions
- Return: architecture summary, conventions guide

Task 2: git-history-analyzer
- Read ~/.claude/agents/research/git-history-analyzer.md
- Analyze git history for patterns
- Return: contributor map, decision patterns
```

### Incorporate Findings

Add research findings to the "CONTEXT FOR NEW SESSIONS" section of the orientation report:
- Key conventions discovered
- Architecture patterns identified
- Expert contributors for different areas
- Historical decisions that inform current work

### Skip Research If

- Already familiar with the codebase
- Small/simple project with clear structure
- Time-sensitive orientation (defer to later)

---

## Phase 1.7: Investigation Recommendation (Optional)

When the project state suggests ambiguity — multiple possible root causes, unclear architecture, or conflicting evidence — consider recommending an investigative dispatch before implementation.

**Indicators:**
- Tests failing with unclear cause
- Recent reverts or fix-on-fix commits in git log
- Task descriptions reference "investigate", "debug", "figure out"
- Stale worktrees from abandoned parallel work

**If investigation is warranted**, create investigation tasks in beads:

```bash
bd create --title="Investigate hypothesis A: <description>" --type=task --priority=1
bd create --title="Investigate hypothesis B: <description>" --type=task --priority=1
```

Then recommend in Phase 5:

"Investigation recommended before implementation dispatch.
Run `/dispatch --plan-first <task-A> <task-B>` to spawn investigators
who will plan their approach before diving in."

**Skip if:** Task board is clear, all ready tasks are straightforward, or user wants to proceed directly.

---

## Phase 2: Task State Analysis

### 2.1 Beads Overview

```bash
bd status 2>/dev/null || echo "Beads not configured"
bd version 2>/dev/null
```

### 2.2 Recently Completed Work

```bash
# Recent git activity
git log --oneline -15

# Recently closed tasks
bd list --all 2>/dev/null | grep -i closed | head -10
```

Understand:
- What was just completed
- Patterns in recent work
- Momentum and direction

### 2.3 Current Task State

```bash
# All open tasks by priority
bd list 2>/dev/null

# Ready work (no blockers)
bd ready 2>/dev/null
```

### 2.4 Dependency Analysis

For each ready task, check what it blocks:

```bash
bd show <task-id>
```

Identify:
- Critical path tasks (block the most downstream work)
- Independent tasks (can run in parallel)
- Research vs implementation tasks

## Phase 3: Codebase Health Check

### 3.1 Test Status

```bash
# Quick test run to verify health
uv run pytest --tb=no -q 2>&1 | tail -10  # Python
pnpm test 2>&1 | tail -10                  # Node
```

### 3.2 Git State

```bash
git status
git branch -a | head -20
git worktree list
git stash list
```

Check for:
- Uncommitted changes
- Active worktrees (parallel work in progress)
- Stashed work that needs attention

## Phase 4: Synthesis & Recommendations

After gathering all information, provide a structured orientation report:

```
===============================================
PROJECT ORIENTATION REPORT
===============================================

PROJECT IDENTITY
----------------
Name: <project name>
Purpose: <1-2 sentence description>
Stack: <key technologies>
Repo: <git remote URL>

DOCUMENTATION STATUS
--------------------
<List docs found and key takeaways from each>

CURRENT STATE
-------------
Git branch: <current branch>
Working tree: <clean/dirty>
Active worktrees: <count and purpose>
Test health: <passing/failing count>

TASK OVERVIEW
-------------
Total open: <count>
Ready (no blockers): <count>
In progress: <count>
Recently completed: <list last 3-5>

CRITICAL PATH ANALYSIS
----------------------
<Identify which tasks block the most downstream work>

RECOMMENDED PARALLEL WORK STREAMS
---------------------------------
The following tasks can be executed simultaneously in separate Claude sessions:

Stream 1: <task-id> - <title>
  Priority: <P1/P2/P3>
  Type: <feature/task/research>
  Rationale: <why this should be worked on>
  Blocks: <what this unblocks when done>
  Start command: /start-task <task-id>

Stream 2: <task-id> - <title>
  Priority: <P1/P2/P3>
  Type: <feature/task/research>
  Rationale: <why this should be worked on>
  Blocks: <what this unblocks when done>
  Start command: /start-task <task-id>

Stream 3: <task-id> - <title>
  Priority: <P1/P2/P3>
  Type: <feature/task/research>
  Rationale: <why this should be worked on>
  Blocks: <what this unblocks when done>
  Start command: /start-task <task-id>

BLOCKERS & RISKS
----------------
<Any issues that could impede progress>
- <blocker 1>
- <blocker 2>

CONTEXT FOR NEW SESSIONS
------------------------
Key things any agent working on this project should know:
- <important pattern or convention>
- <gotcha or common mistake>
- <architectural constraint>

===============================================
END ORIENTATION REPORT
===============================================
```

## Phase 5: Ready for Action

After presenting the orientation report, **ALWAYS offer `/dispatch` as the primary action when there are 2+ ready tasks.**

Present the following call-to-action:

---

"Orientation complete. **Recommended next step:**

```
/dispatch
```

This will spawn parallel Claude Code workers for the ready tasks. Each worker will:
1. Auto-receive their task assignment via the handoff queue
2. Create a git worktree for isolation
3. Run `/start-task <task-id>` automatically
4. Work autonomously until completion

You stay in THIS session as the orchestrator to coordinate as workers complete.

---

**Alternative options:**

1. **Dispatch workers** - Run `/dispatch` to spawn parallel workers (RECOMMENDED)
2. **Manual parallel** - Open separate terminals and run `/start-task <id>` in each
3. **Work solo** - Pick one task with `/start-task <id>` in this session
4. **Deep dive** - Explore a specific task or area in more detail
5. **Coordinate** - Help manage existing parallel work as tasks complete

What would you like to do?"

---

**CRITICAL**: You MUST present `/dispatch` prominently. Do not bury it in a list of options. The whole point of orientation is to enable parallel execution via dispatch.

Await user direction before taking action.
