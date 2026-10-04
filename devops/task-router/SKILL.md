---
name: task-router
description: CEO's task decomposition and routing engine. Classifies tasks by type and complexity, selects agents with appropriate model tiers, decides parallel vs sequential execution, and auto-injects relevant skills.
---

# Task Router - CEO's Decision Engine

The brain of CodeCrew. When a task comes in, this skill classifies it, picks the right agents, decides the execution strategy, and kicks off the work.

## When to Activate

- User runs `/crew task "description"`
- CEO agent needs to route a subtask

## Prerequisites

These files MUST exist (run `/crew init` first):
- `.claude/crew-profile.md` — project context
- `.claude/crew-team.json` — agent configuration
- `.claude/crew-skills.json` — skill catalog
- `.claude/crew-index.json` — codebase index (Layer 1)
- `.claude/crew-symbols.json` — symbol map (Layer 2)

If any are missing, tell the user to run `/crew init` first.

## Routing Algorithm

### Step 1: Read Context
```
1. Check if .claude/.index-stale exists
   - If yes: read the file paths listed, invoke index-updater for those files, then delete .claude/.index-stale
   - This handles files edited outside of /crew task (e.g., manual edits, other tools)
2. Read .claude/crew-profile.md for project context
3. Read .claude/crew-team.json for available agents
4. Read .claude/crew-config.json (if exists) for user overrides (default mode, budgets, etc.)
5. Read .claude/crew-index.json for codebase awareness
```

### Step 2: Classify Task

**Task Type** (pick one):
| Type | Signals |
|------|---------|
| `bug-fix` | "fix", "bug", "broken", "error", "crash", "not working", "issue" |
| `feature` | "add", "implement", "create", "build", "new", "feature" |
| `refactor` | "refactor", "clean up", "reorganize", "restructure", "improve" |
| `docs` | "document", "readme", "comment", "explain", "docs" |
| `test` | "test", "coverage", "spec", "TDD", "unit test", "e2e" |
| `security` | "security", "vulnerability", "auth", "permission", "XSS", "injection" |
| `devops` | "deploy", "docker", "CI/CD", "pipeline", "kubernetes", "build" |
| `review` | "review", "check", "audit", "quality" |
| `performance` | "slow", "optimize", "performance", "speed", "memory", "cache" |

**Complexity** (assess based on scope):
| Level | Signals |
|-------|---------|
| `trivial` | Single word change, typo, formatting, one-line fix |
| `simple` | Single file, clear fix, under 20 lines changed |
| `moderate` | 2-4 files, some design decisions, 20-100 lines |
| `complex` | 5+ files, architecture decisions, new patterns, 100+ lines |
| `architectural` | System-wide changes, new subsystems, major refactors |

### Step 3: Select Agent Chain

Based on (type, complexity), select the execution plan:

```
ROUTING TABLE:

bug-fix:
  trivial    → junior-dev (haiku)
  simple     → debugger (sonnet) investigates → junior-dev (haiku) fixes
  moderate   → debugger (sonnet) investigates → senior-dev (sonnet) fixes
  complex    → CEO reads index → debugger investigates → senior-dev fixes → code-reviewer reviews
  architectural → CEO + vp-engineering analyze → debugger + senior-dev → vp-quality reviews

feature:
  trivial    → junior-dev (haiku)
  simple     → senior-dev (sonnet)
  moderate   → vp-engineering plans → senior-dev implements → test-engineer tests
  complex    → CEO + vp-engineering architect → [parallel: senior-dev implements, test-engineer writes tests] → code-reviewer reviews
  architectural → CEO designs → vp-engineering plans → [parallel: multiple senior-devs] → vp-quality reviews all

refactor:
  any        → vp-engineering plans → senior-dev executes → code-reviewer reviews

docs:
  any        → doc-writer (haiku)

test:
  trivial/simple → test-engineer (sonnet)
  moderate+  → vp-quality strategizes → test-engineer implements

security:
  any        → security-analyst (sonnet) → senior-dev fixes findings

devops:
  trivial/simple → devops-engineer (haiku)
  moderate+  → senior-dev (sonnet) handles complex infra

review:
  any        → code-reviewer (sonnet) → report to user

performance:
  any        → vp-engineering analyzes → senior-dev optimizes → test-engineer verifies
```

### Step 4: Decide Execution Strategy

```
PARALLEL when:
- Subtasks operate on DIFFERENT files (check via crew-index.json)
- Implementation + test writing (test-engineer works on test files, senior-dev on source files)
- Multiple independent bug fixes
- Documentation for different components

SEQUENTIAL when:
- Investigation must complete before fix begins
- Planning must complete before implementation
- Implementation must complete before review
- Subtasks modify the SAME files

HYBRID (most common for moderate+ tasks):
1. Sequential: investigation/planning phase
2. Parallel: independent implementation subtasks
3. Sequential: integration review
```

### Step 5: Inject Relevant Skills

Read `.claude/crew-skills.json` and select skills to inject into agent prompts:

```
1. Always include: "always" category skills
2. Add stack-specific skills based on detectedStack
3. Add task-type skills based on classified type
4. Each agent gets ONLY the skills relevant to their subtask (not all skills)
```

### Step 6: Generate Execution Plan

Create a structured plan before executing:

```
[FULL] {type}/{complexity}: "{task}"
  1. {agent} → {subtask}
  2. {agent} + {agent} → {subtask A} | {subtask B}
  3. {agent} → {review}
```

Display this plan to the user, then execute.

### Step 7: Execute

Use the **execution-orchestrator** skill to dispatch agents according to the plan.

For each agent dispatch, construct a self-contained prompt that includes:
1. The subtask description
2. Relevant project context from crew-profile.md
3. The Index-First Protocol instructions
4. Injected skill guidance
5. Files the agent should focus on (from index analysis)
6. Expected output format

### Step 8: Collect Results & Report

After all agents complete:
1. Collect each agent's output
2. Check for conflicts (multiple agents editing same lines)
3. If conflicts: escalate to vp-engineering for resolution
4. Auto-update index for all `FILES_MODIFIED` (handled automatically by execution-orchestrator)
5. Log task to `.claude/crew-history.json` (including `skillsInjected` and agent details)
6. Report final status to user (including index update status and skills injected)
7. Include skills used in the report — execution-orchestrator's Result Collection template handles the format

## Error Handling

- If agent fails → retry once with more context
- If agent reports index is stale → trigger incremental update, then retry
- If parallel agents conflict → fall back to sequential for conflicting files
- If task is unclear → CEO asks user for clarification instead of guessing
