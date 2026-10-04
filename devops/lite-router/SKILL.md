---
name: lite-router
description: Lite task router that bypasses Opus CEO entirely. Classifies tasks and routes directly to Sonnet and Haiku agents only. Use when user runs /crew lite or /crew task --lite.
---

# Lite Router - Task Router (No Opus)

Performs task classification and routing WITHOUT spawning the CEO (Opus) agent. All classification happens in the current session context (Sonnet-level), and agents are dispatched using only Sonnet and Haiku tiers.

## When to Activate

- User runs `/crew lite "description"`
- User runs `/crew task --lite "description"` (backward compatible)

## Prerequisites

These files MUST exist (run `/crew init` first):
- `.claude/crew-profile.md` — project context
- `.claude/crew-team.json` — agent configuration
- `.claude/crew-skills.json` — skill catalog
- `.claude/crew-index.json` — codebase index (Layer 1)
- `.claude/crew-symbols.json` — symbol map (Layer 2)

If any are missing, tell the user to run `/crew init` first.

## Lite Mode Advantage

In LITE mode:
- **0 Opus calls** — CEO is bypassed entirely
- Classification is done by this skill (runs in user's Sonnet session)
- vp-engineering (Sonnet) takes over planning/architecture duties that CEO would normally handle

## Routing Algorithm

### Step 1: Read Context
```
1. Read .claude/crew-profile.md for project context
2. Read .claude/crew-team.json for available agents
3. Read .claude/crew-index.json for codebase awareness
4. Check for .claude/.index-stale — if present, invoke index-updater for listed files, then delete the marker
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

### Step 3: Select Agent Chain (LITE — No Opus)

```
LITE ROUTING TABLE (Sonnet + Haiku only):

bug-fix:
  trivial    → junior-dev (haiku)
  simple     → debugger (sonnet) investigates → junior-dev (haiku) fixes
  moderate   → debugger (sonnet) investigates → senior-dev (sonnet) fixes
  complex    → vp-engineering (sonnet) analyzes → debugger investigates → senior-dev fixes → code-reviewer reviews
  architectural → vp-engineering (sonnet) plans → debugger + senior-dev execute → vp-quality reviews

feature:
  trivial    → junior-dev (haiku)
  simple     → senior-dev (sonnet)
  moderate   → vp-engineering (sonnet) plans → senior-dev implements → test-engineer tests
  complex    → vp-engineering (sonnet) architects → [parallel: senior-dev implements, test-engineer writes tests] → code-reviewer reviews
  architectural → vp-engineering (sonnet) designs + plans → [parallel: multiple agents] → vp-quality reviews all

refactor:
  any        → vp-engineering (sonnet) plans → senior-dev executes → code-reviewer reviews

docs:
  any        → doc-writer (haiku)

test:
  trivial/simple → test-engineer (sonnet)
  moderate+  → vp-quality (sonnet) strategizes → test-engineer implements

security:
  any        → security-analyst (sonnet) → senior-dev fixes findings

devops:
  trivial/simple → devops-engineer (haiku)
  moderate+  → senior-dev (sonnet) handles complex infra

review:
  any        → code-reviewer (sonnet) → report to user

performance:
  any        → vp-engineering (sonnet) analyzes → senior-dev optimizes → test-engineer verifies
```

**Key difference from full mode**: vp-engineering (Sonnet) takes over the CEO's planning and architecture role. No Opus agent is ever spawned.

### Step 4: Decide Execution Strategy

```
PARALLEL when:
- Subtasks operate on DIFFERENT files (check via crew-index.json)
- Implementation + test writing (test-engineer on test files, senior-dev on source files)
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
4. Each agent gets ONLY the skills relevant to their subtask
5. vp-engineering gets expanded budget (2500 tokens) when acting as planner in lite mode
```

### Step 6: Generate Execution Plan

Create a structured plan before executing:

```
[LITE] {type}/{complexity}: "{task}"
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
7. **Note**: In lite mode, if an agent needs to escalate, escalate to vp-engineering (not CEO)

### Step 8: Collect Results & Report

After all agents complete:
1. Collect each agent's output
2. Check for conflicts (multiple agents editing same lines)
3. If conflicts: escalate to vp-engineering for resolution (NOT CEO)
4. Auto-update index for all `FILES_MODIFIED` (handled automatically by execution-orchestrator)
5. Log task to `.claude/crew-history.json` (with `"mode": "lite"` flag, including `skillsInjected` and agent details)
6. Report final status to user (including index update status and skills injected)
7. Include skills used in the report — execution-orchestrator's Result Collection template handles the format

## Error Handling

- If agent fails → retry once with more context
- If agent reports index is stale → trigger incremental update, then retry
- If parallel agents conflict → fall back to sequential for conflicting files
- If task is unclear → ask user for clarification instead of guessing
- If task complexity exceeds expectations → escalate to vp-engineering (NOT CEO)
