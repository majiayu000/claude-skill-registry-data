---
name: gsd
description: "Get Shit Done — spec-driven development pipeline with XML-structured plans, wave-based parallel execution with fresh-context agents, goal-backward verification, and lightweight ad-hoc quick mode with composable flags. Single skill containing plan/execute/verify/quick modes as sub-workflows."
layer: orchestrator
category: workflow
triggers: ["build this feature", "check must haves", "create execution plan", "execute phase", "execute wave", "fast implementation", "full implementation", "get shit done", "goal backward", "gsd", "gsd execute", "gsd plan", "gsd quick", "gsd verify", "implement this", "just do it", "let's build", "make it happen", "plan phase", "quick fix", "quick task", "run the plans", "ship this", "spec driven plan", "verify work"]
---

# gsd

Get Shit Done — spec-driven development pipeline with XML-structured plans, wave-based parallel execution with fresh-context agents, goal-backward verification, and lightweight ad-hoc quick mode with composable flags. Single skill containing plan/execute/verify/quick modes as sub-workflows.


## Absorbs

- `gsd-plan`
- `gsd-execute`
- `gsd-verify`
- `gsd-quick`


## Core

# Get Shit Done (GSD)

## Purpose

GSD is a **spec-driven development system** that prevents context rot by spawning
fresh-context subagents for heavy lifting while keeping the orchestrator thin.
Adapted from [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)
(34.5K stars) and evolved for UltraThink's skill mesh.

**Core insight**: Quality degrades as context fills. The solution isn't better
prompts — it's **fresh 200K context per agent** with plans that ARE prompts.

Use this when:
- Building a full feature from scratch
- Implementing a multi-file change
- Any task that would fill >50% of context if done inline
- You want atomic commits, verification, and session continuity

### Templates/Presets

GSD is the ONE workflow. Other skills operate as GSD templates:

- **`/forge`** — Product builder preset: clarify→feasibility→plan (gsd-plan), build (gsd-execute), validate (gsd-verify), improve (gsd-execute fix wave), ship (gsd post-verify)

## Key Concepts

### Context Rot Prevention

```
Traditional:  User → Claude (fills context) → quality degrades at 60%+
GSD:          User → Orchestrator (stays at ~10-15%) → Agents (fresh 200K each)
```

The orchestrator NEVER does heavy lifting. It:
1. Creates spec-driven plans
2. Spawns agents with full plan context
3. Verifies results
4. Manages state in `.planning/`

### Plans ARE Prompts

Plans are XML-structured Markdown — not documentation that becomes prompts,
but prompts themselves. Each plan contains everything an agent needs:

```markdown
# Plan: {phase}-{number} — {title}

## Context
- What this plan implements
- Why it exists
- What came before (dependencies)

## Must-Haves (verification criteria)
- [ ] Specific, testable requirement 1
- [ ] Specific, testable requirement 2

## Tasks
### Task 1: {description}
**Files**: list of files to create/modify
**Approach**: exactly how to implement
**Verification**: how to confirm it works

### Task 2: ...
```

### Wave-Based Execution

Plans are grouped into waves based on dependencies:

```
Wave 1: [Plan A, Plan B]    ← parallel (no dependencies)
Wave 2: [Plan C]             ← depends on A
Wave 3: [Plan D, Plan E]    ← parallel (depend on C)
```

Each wave's plans execute as parallel subagents with fresh context.

### Deviation Rules

When executing, agents follow strict deviation rules:

| Rule | Condition | Action |
|------|-----------|--------|
| 1 | Bug blocks current task | Auto-fix, document, continue |
| 2 | Missing dependency | Install/create, document, continue |
| 3 | Minor adjustment needed | Fix if <5 min, document, continue |
| 4 | Architectural change needed | **STOP** — report back to orchestrator |
| 5 | Scope creep detected | **STOP** — document for future phase |

**Never** silently change architecture. **Always** document deviations.

### Goal-Backward Verification

Verify from goals backward, not code forward:

```
1. Read must_haves from plan
2. For each must_have:
   a. Find the artifact that satisfies it
   b. Verify the artifact exists and is correct
   c. Check key links (imports, routes, API calls)
3. Detect stubs/placeholders (TODO, placeholder, mock data in prod)
4. Run build + tests
```

## Workflow

### Stage 0: Initialize (if no .planning/ exists)

```bash
mkdir -p .planning
# Create STATE.md — living memory for session continuity (100 lines max)
# Create config.json — mode, granularity, workflow toggles
```

### Stage 1: Plan

Invoke `gsd-plan` skill:
1. Research the task (scout codebase, understand patterns)
2. Break into phases (if large) or single phase (if small)
3. Create XML-structured PLAN.md files with must_haves
4. Verify plans against deviation rules
5. Assign waves (dependency graph)

### Stage 2: Execute

Invoke `gsd-execute` skill:
1. For each wave (in order):
   a. Spawn parallel subagents (one per plan)
   b. Each agent gets: plan + relevant source files + references
   c. Agent implements, creates atomic commits
   d. Agent writes SUMMARY.md
2. Verify each wave before proceeding to next

### Stage 3: Verify

Invoke `gsd-verify` skill:
1. Goal-backward verification against all must_haves
2. Build + typecheck + lint + test
3. Stub detection (TODO, placeholder, console.log)
4. Integration check across phases
5. Create VERIFICATION.md

### Stage 4: Ship (or iterate)

If verification passes → ready for PR
If verification fails → auto-generate fix plans → re-execute

### Stage 5: Archive (OpenSpec-absorbed lifecycle)

After shipping, invoke `plan-archive` to close the loop:

1. **Archive spec + plans** — Move SPEC.md, PLAN.md files, VERIFICATION.md to `.planning/archive/{date}-{title}/`
2. **Version the spec** — If SPEC.md was updated during execution, diffs are preserved in `SPEC.changelog.md`
3. **Extract docs** — Archived specs become project documentation in `.planning/docs/`
4. **Lessons → Tekiō** — Patterns and anti-patterns feed into wheel-learn (learning adaptations)
5. **Journey journal** — Narrative retrospective stored in memory for future recall

### Spec Update Protocol (mid-execution)

When scope changes during execution:
1. **STOP execution** (deviation rule 5)
2. **Update SPEC.md** — Add/modify acceptance criteria, update constraints
3. **Append to SPEC.changelog.md** — Timestamped diff of what changed and why
4. **Re-plan affected tasks** — Only plans whose must-haves trace to changed criteria
5. **Resume execution** — From the affected wave onward

```markdown
<!-- SPEC.changelog.md format -->
## [2026-03-19] Scope change: added rate limiting
**Reason**: Security review flagged missing rate limits
**Added**: Acceptance criterion #5 — "API endpoints rate-limited to 100 req/min per user"
**Impact**: Plan 1-3 needs new task for middleware
```

## State Management (.planning/)

```
.planning/
  STATE.md              — Living memory (100 lines max, always current)
  config.json           — Mode, granularity, toggles
  SPEC.md               — Formal spec: acceptance criteria, constraints, non-goals
  SPEC.changelog.md     — Timestamped spec revisions (append-only)
  PROJECT.md            — Project overview + decisions
  REQUIREMENTS.md       — What we're building
  ROADMAP.md            — Phases and milestones
  RESEARCH.md           — Codebase analysis from research agents
  {phase}-{n}-PLAN.md   — Individual execution plans (must-haves trace to SPEC.md)
  {phase}-{n}-SUMMARY.md — Execution summaries
  VERIFICATION.md       — Verification results
  UAT.md                — User acceptance testing
  CONTEXT.md            — Gray area decisions
  archive/              — Completed specs + plans (by date-title)
  docs/                 — Extracted documentation from archived specs
```

### STATE.md Format (100 lines max)

```markdown
# State

## Current
Phase: 2, Plan: 1, Status: executing

## Completed
- Phase 1: Auth system (3 plans, all verified)

## Decisions
- Using JWT + refresh tokens (user chose over session-based)
- Postgres for auth tables (existing DB)

## Blocked
- None

## Next
- Phase 2 Plan 2: User profile API
```

## Best Practices

1. **Keep orchestrator thin** — never read full files in the orchestrator, delegate to agents
2. **Plans are prompts** — include everything the agent needs, don't assume context
3. **Atomic commits per task** — each task in a plan gets its own commit
4. **Must-haves are testable** — "works correctly" is bad, "returns 200 with user JSON" is good
5. **Deviation rule 4 is sacred** — never silently change architecture
6. **STATE.md stays under 100 lines** — it's a digest, not a log
7. **Wave before parallelize** — map dependencies first, then find parallelism
8. **Verify before advancing** — never start wave N+1 until wave N is verified

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Orchestrator does implementation | Context fills, quality degrades | Always delegate to fresh-context agents |
| Plans without must_haves | Can't verify completion | Every plan needs testable criteria |
| Skipping verification | Stubs and broken integrations ship | Goal-backward verify after every wave |
| Too many tasks per plan | Agent context fills | 2-3 tasks max per plan |
| STATE.md grows unbounded | Session restoration breaks | Hard cap at 100 lines, summarize |
| Silent architecture changes | Breaks other phases | Deviation rule 4: STOP and report |

## Examples

### Quick Task (Single Agent)

```
User: "Add dark mode toggle to the settings page"

GSD:
1. Plan: 1 plan, 2 tasks (toggle component + theme state)
2. Execute: 1 agent, fresh context, atomic commits
3. Verify: toggle works, theme persists, no regressions
```

### Multi-Phase Feature

```
User: "Build a subscription billing system with Stripe"

GSD:
Phase 1: Stripe integration (2 plans)
  Wave 1: [Plan 1: API routes] [Plan 2: Webhook handler]  ← parallel
Phase 2: UI (2 plans)
  Wave 1: [Plan 3: Pricing page]
  Wave 2: [Plan 4: Billing dashboard]  ← depends on Plan 3
Phase 3: Testing + polish (1 plan)
  Wave 1: [Plan 5: E2E tests + edge cases]
```

## Integration with UltraThink

GSD plugs into the skill mesh:

```
User prompt → auto-trigger detects "build/implement" intent
           → gsd skill activated
           → gsd-plan (spawns research agents)
           → gsd-execute (spawns executor agents per wave)
           → gsd-verify (spawns verifier agent)
           → learn-pattern (extract what we learned)
           → Tekio (adapt from any failures)
```

Context monitor hook tracks usage and warns at 65%/75% thresholds.
Suggest-compact hook catches tool-call-based boundaries.
Together they prevent the context rot that GSD was designed to solve.


---

## From `gsd-plan`

> Spec-driven planning — create XML-structured plans with must_haves, wave assignments, and deviation rules

# GSD Plan

## Purpose

Create spec-driven execution plans where **plans ARE prompts** — each plan contains
everything a fresh-context executor agent needs to implement without any ambient context.

## Workflow

### Phase 1: Research (Parallel Subagents)

Spawn up to 4 parallel research agents:

1. **Codebase scout** — map relevant files, patterns, conventions
2. **Domain research** — understand the problem space (web search if needed)
3. **Dependency check** — what exists, what needs installing
4. **Pattern analysis** — how similar things are done in this codebase

Each agent writes findings to a section. Synthesize into `RESEARCH.md`.

### Phase 1.5: Spec (OpenSpec-absorbed)

After research, before decomposing into plans, write `SPEC.md` — the formal contract.
This prevents scope drift and gives every executor agent clear acceptance criteria.

```markdown
# Spec: {feature/change title}

## Problem Statement
{WHY this change is needed — the motivation, not the solution}

## Acceptance Criteria
- [ ] {Specific, testable criterion — user-visible behavior}
- [ ] {Another criterion — measurable outcome}
- [ ] {Edge case handling}
- [ ] {Performance/security requirement if applicable}

## Constraints
- {Technical constraint — e.g., must use existing auth middleware}
- {Business constraint — e.g., backwards compatible with v2 API}

## Non-Goals (explicit scope fence)
- {What this change does NOT include}
- {Future work explicitly deferred}

## Technical Approach (brief)
{High-level approach from research — 3-5 sentences max}
{Reference RESEARCH.md for details}
```

**Rules:**
- Acceptance criteria MUST be testable (not "works correctly" — HOW to verify)
- Non-goals prevent scope creep during execution (deviation rule #5)
- SPEC.md is the source of truth — PLAN.md must-haves trace back to these criteria
- If the spec changes mid-execution, STOP and update spec first

### Phase 2: Plan Decomposition

Break the task into plans with **2-3 tasks each** (never more).
Each plan's must-haves MUST trace to SPEC.md acceptance criteria:

```markdown
# Plan: {phase}-{number} — {title}

<plan_metadata>
wave: 1
depends_on: []
estimated_tasks: 2
risk: low|medium|high
files_owned: [src/path/to/file.ts, src/path/to/other.ts]
</plan_metadata>

## Context
{Everything the executor needs to understand this plan}
{Include relevant patterns from RESEARCH.md}
{Include relevant code snippets — the agent can't read your context}

## Must-Haves
- [ ] {Specific, testable requirement}
- [ ] {Another specific, testable requirement}
- [ ] Build passes with no new errors
- [ ] Existing tests still pass

## Tasks

### Task 1: {title}
**Files to create/modify:**
- `src/path/to/file.ts` — {what to do}

**Approach:**
{Step-by-step implementation instructions}

**Verification:**
{How to confirm this task is done}

### Task 2: {title}
...

## Deviation Rules
1. Bug blocks task → fix it, add comment, continue
2. Missing dep → install it, continue
3. Minor adjustment (<5 min) → do it, document in SUMMARY.md
4. Architecture change needed → STOP, report back
5. Scope creep → STOP, document for next phase

## References
{Paste relevant code snippets the agent will need}
{The agent gets ONLY this plan — include everything}
```

### Phase 3: Wave Assignment

Map dependencies into waves:

```
Wave 1: Plans with no dependencies (run in parallel)
Wave 2: Plans that depend on Wave 1 outputs
Wave 3: Plans that depend on Wave 2 outputs
```

Rule: **maximize parallelism, respect dependencies**

### Phase 4: Plan Verification

Before handing to executor, verify each plan:

- [ ] Has testable must_haves (not vague "works correctly")
- [ ] Has 2-3 tasks (not more)
- [ ] Includes all context the agent needs (code snippets, patterns)
- [ ] Wave dependencies are correct
- [ ] `files_owned` lists every file the plan creates/modifies (for conflict detection)
- [ ] Deviation rules included
- [ ] No stubs or placeholders in the plan itself

## Must-Have Quality Checklist

Good must-haves are:
- **Specific**: "POST /api/users returns 201 with user JSON" not "user creation works"
- **Testable**: Can be verified by reading code or running a command
- **Independent**: Each must-have is verifiable on its own
- **Complete**: Cover all acceptance criteria, not just happy path

## Best Practices

1. **Include code snippets in plans** — the agent can't read your memory
2. **2-3 tasks per plan, max** — keeps agent context focused
3. **Must-haves drive verification** — if you can't verify it, rewrite it
4. **Wave 1 should be foundation** — types, schemas, shared utilities
5. **Each plan is self-contained** — an agent should understand it without other plans
6. **Use the codebase's conventions** — research phase discovers these

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Vague must-haves | Can't verify completion | Write testable criteria |
| Too many tasks per plan | Agent context overflows | Split into multiple plans |
| Missing code context | Agent reinvents patterns | Include relevant snippets |
| Wrong wave order | Dependent code breaks | Map dependencies carefully |
| Plans reference each other | Agent can't see other plans | Each plan is self-contained |
| Skipping research | Plans miss conventions | Always run parallel research first |

## Examples

### Simple Plan (1 wave)

```markdown
# Plan: 1-1 — Add user avatar upload

<plan_metadata>
wave: 1
depends_on: []
estimated_tasks: 2
risk: low
files_owned: [src/app/api/upload/avatar/route.ts, src/components/ProfileHeader.tsx, prisma/schema.prisma]
</plan_metadata>

## Must-Haves
- [ ] POST /api/upload/avatar accepts image file, stores in /public/avatars
- [ ] User model has `avatar_url` field
- [ ] Avatar displays in profile header component
- [ ] Files >5MB are rejected with 413 status

## Tasks

### Task 1: Upload API route
**Files:** `src/app/api/upload/avatar/route.ts`
**Approach:** Use Next.js route handler, formidable for parsing, sharp for resize
**Verification:** curl -F "file=@test.jpg" localhost:3000/api/upload/avatar returns 200

### Task 2: Profile avatar display
**Files:** `src/components/ProfileHeader.tsx`, `prisma/schema.prisma`
**Approach:** Add avatar_url to User model, display with next/image
**Verification:** Avatar appears in profile page after upload
```


---

## From `gsd-execute`

> Wave-based parallel execution — spawn fresh-context agents per plan with atomic commits

# GSD Execute

## Purpose

Execute plans by spawning **fresh-context subagents** for each plan in wave order.
Each agent gets the full 200K context window dedicated to its plan — no context rot.

## Key Concepts

### Fresh Context = Quality

```
Main orchestrator context: ~10-15% used (thin coordinator)
Agent 1 context: 200K fresh → implements Plan 1    ┐
Agent 2 context: 200K fresh → implements Plan 2    │ Wave 1 (parallel)
Agent 3 context: 200K fresh → implements Plan 3    │
Agent 4 context: 200K fresh → implements Plan 4    ┘
Agent 5 context: 200K fresh → implements Plan 5    ┐ Wave 2 (speculative start
Agent 6 context: 200K fresh → implements Plan 6    ┘  if deps satisfied early)
```

### High-Concurrency Mode (Default)

**Target: 6-8 concurrent agents** using git worktree isolation.

| Mode | Max Agents | Isolation | When |
|------|-----------|-----------|------|
| Standard | 4 | Shared workdir | Plans with disjoint file sets |
| Worktree | 6-8 | `isolation: "worktree"` | Plans that may touch overlapping files |
| Sequential | 1 | Shared workdir | Plans with explicit same-file deps |

**Worktree isolation** gives each agent a full copy of the repo. After completion,
changes are merged back. This eliminates file conflicts entirely.

### Speculative Wave Overlap

Don't wait for ALL of Wave N to finish before starting Wave N+1.
Start Wave N+1 plans whose **specific dependencies** are already satisfied:

```
Wave 1: [Plan A, Plan B, Plan C] — all launch immediately
         Plan A completes ✅
         Plan B still running...
         Plan C completes ✅
Wave 2: [Plan D (depends on A), Plan E (depends on A+C)]
         → Plan D can start NOW (A is done)
         → Plan E can start NOW (A+C are done)
         → Plan F (depends on B) must wait
```

**Rule**: Check `depends_on` per plan, not per wave. A plan is ready when
ALL its listed dependencies are completed — regardless of wave boundaries.

### File Ownership Model

Each plan declares `files_owned` in its metadata — the files it will create/modify.
The orchestrator uses this to detect conflicts and decide parallel vs sequential:

```
Plan A files_owned: [src/auth/jwt.ts, src/auth/login.ts]
Plan B files_owned: [src/api/users.ts, src/api/routes.ts]
Plan C files_owned: [src/auth/jwt.ts, src/api/middleware.ts]  ← conflicts with A

→ A and B: parallel (no overlap)
→ A and C: worktree isolation OR sequential (overlap on jwt.ts)
```

### Atomic Commits

Each **task** within a plan gets its own commit:

```
feat(auth): add JWT token generation (Plan 1-1, Task 1)
feat(auth): add refresh token rotation (Plan 1-1, Task 2)
feat(auth): add login API endpoint (Plan 1-2, Task 1)
```

### Agent Prompt Template

Each spawned agent receives:

```markdown
You are executing a GSD plan. Follow it exactly.

## Plan
{full PLAN.md content}

## Deviation Rules
1. Bug blocks task → fix, document, continue
2. Missing dep → install, continue
3. Minor adjustment → fix if <5min, continue
4. Architecture change → STOP immediately, report what and why
5. Scope creep → STOP, document for next phase

## Commit Convention
After each task, create an atomic commit:
  {type}({scope}): {description} (Plan {phase}-{number}, Task {n})

## On Completion
Write a SUMMARY.md with:
- What was implemented
- Any deviations from plan
- Files created/modified
- Must-haves checklist (checked/unchecked)
```

## Progress Tracking

Write progress to `/tmp/ultrathink-progress-{session_id}` (JSON) so the statusline
and progress-display hook can render live progress bars.

### Bridge File Format

Each agent tracks its own task progress. The statusline shows a summary bar;
the progress-display hook shows per-agent lines on each Agent tool return.

```json
{
  "mode": "gsd",
  "phase": 1,
  "wave": 1,
  "total_waves": 3,
  "agents": [
    {
      "plan": "1-1",
      "status": "done",
      "tasks_total": 3,
      "tasks_done": 3,
      "current_task": ""
    },
    {
      "plan": "1-2",
      "status": "running",
      "tasks_total": 2,
      "tasks_done": 1,
      "current_task": "Task 2: Add refresh token"
    },
    {
      "plan": "1-3",
      "status": "queued",
      "tasks_total": 2,
      "tasks_done": 0,
      "current_task": ""
    }
  ],
  "tasks": {
    "total": 7,
    "completed": 4
  }
}
```

**Agent statuses**: `queued` → `running` → `done` | `failed`

### When to Update

| Event | Update |
|-------|--------|
| Wave starts | Set all wave agents as "queued", set wave/total_waves |
| Agent spawned | Set that agent to "running", set tasks_total from plan |
| Agent reports task done | Increment agent's tasks_done, update current_task, increment global tasks.completed |
| Agent returns | Set agent to "done" or "failed" |
| Wave verified | Advance wave, queue next wave's agents |
| All done | Delete the progress file (statusline reverts to normal) |

### How to Write (Using gsd-utils.sh)

Source the shared utilities for easy progress tracking:

```bash
# Source the GSD utilities
source "$(dirname "${BASH_SOURCE[0]}")/gsd-utils.sh"  # from hooks dir
# OR if not in hooks context:
source ~/.claude/hooks/../Documents/GitHub/InuVerse/ai-agents/ultrathink/.claude/hooks/gsd-utils.sh

# Initialize progress for phase 1 with 2 waves
gsd_progress_init 1 2

# Add agents for wave 1
gsd_progress_add_agent "1-1" 3   # Plan 1-1, 3 tasks
gsd_progress_add_agent "1-2" 2   # Plan 1-2, 2 tasks

# Start agents
gsd_progress_start_agent "1-1" "Task 1: Setup DB schema"
gsd_progress_start_agent "1-2" "Task 1: Create API routes"

# As tasks complete
gsd_progress_task_done "1-1" "Task 2: Add migrations"
gsd_progress_task_done "1-1" "Task 3: Seed data"
gsd_progress_task_done "1-1"  # last task, no next

# Mark agent done
gsd_progress_agent_done "1-1"

# Advance to next wave
gsd_progress_next_wave

# On completion, clean up
gsd_progress_cleanup
```

#### Manual JSON method (fallback)

```bash
# If gsd-utils.sh is not available, write JSON directly:
cat > /tmp/ultrathink-progress-{session_id} << 'PROGRESS'
{"mode":"gsd","phase":1,"wave":1,"total_waves":2,"agents":[{"plan":"1-1","status":"running","tasks_total":3,"tasks_done":0,"current_task":"Task 1"}],"tasks":{"total":5,"completed":0}}
PROGRESS

# Update with jq
jq '.agents[0].tasks_done = 1 | .agents[0].current_task = "Task 2" | .tasks.completed = 1' \
  /tmp/ultrathink-progress-{session_id} > /tmp/ultrathink-progress-{session_id}.tmp \
  && mv /tmp/ultrathink-progress-{session_id}.tmp /tmp/ultrathink-progress-{session_id}
```

On completion, clean up: `rm -f /tmp/ultrathink-progress-{session_id}`

## Workflow

### Step 1: Load Plans and Sort by Wave

```
Read all PLAN.md files from .planning/
Group by wave number
Sort waves ascending
```

### Step 2: Execute Plans (Dependency-Driven, Not Wave-Locked)

Instead of rigid wave-by-wave, use **dependency-driven scheduling**:

```typescript
// Build ready queue: plans whose dependencies are all completed
const ready = allPlans.filter(plan =>
  plan.depends_on.every(dep => completedPlans.has(dep))
)

// Check file ownership conflicts among ready plans
const { parallel, sequential } = resolveConflicts(ready)

// Launch parallel group with worktree isolation
const agents = parallel.map(plan => ({
  type: "general-purpose",
  prompt: buildAgentPrompt(plan),
  isolation: "worktree",  // Default: worktree for safe parallel execution
  run_in_background: true
}))

// Launch all ready agents at once (up to 8)
agents.forEach(a => spawnAgent(a))

// Sequential plans run one at a time after parallel batch
for (const plan of sequential) {
  await spawnAgent({ ...plan, isolation: undefined })
}
```

**Scheduling rules:**
1. A plan is **ready** when ALL its `depends_on` plans are completed
2. Ready plans with **disjoint files_owned** launch in parallel (worktree isolation)
3. Ready plans with **overlapping files_owned** and no worktree → run sequentially
4. With worktree isolation, even overlapping files can run in parallel (merge after)
5. **Max 8 concurrent agents** — queue remainder, launch as slots free up
6. Re-check ready queue after EVERY agent completion (new plans may unblock)

### Step 3: Collect Results (Continuous)

After EACH agent completes (not after entire wave):
1. Read SUMMARY.md from the returned agent
2. Check its must-haves
3. Run quick verification (build + typecheck)
4. If Rule 4 deviation → STOP, report to user
5. **Re-check ready queue** — new plans may now be unblocked
6. Launch any newly-ready plans immediately (up to 8 total concurrent)

### Step 4: Advance (Continuous Flow, Not Wave-Locked)

Plans launch as soon as their dependencies are met — no waiting for entire waves.
The "wave" concept becomes a planning aid, not an execution barrier:

```
Plan A (wave 1) completes → check: which wave 2+ plans depend only on A?
  → Plan D depends on [A] → LAUNCH NOW (don't wait for B, C)
  → Plan E depends on [A, B] → still blocked on B
Plan B (wave 1) completes → check: Plan E depends on [A, B] → both done → LAUNCH NOW
```

**Safety gate**: Build must pass after each batch of completions before launching
plans from the NEXT wave tier. Within the same wave, no gate needed.

### Step 5: Update State

```markdown
# STATE.md update after wave completion

## Current
Phase: 1, Wave: 2 (completed), Status: verified

## Completed
- Wave 1: [Plan 1-1 ✅, Plan 1-2 ✅]
- Wave 2: [Plan 1-3 ✅]
```

## Deviation Handling

| Rule | In Agent | In Orchestrator |
|------|----------|-----------------|
| 1-3 | Agent handles, documents | Orchestrator reviews summary |
| 4 | Agent STOPS | Orchestrator reports to user, creates fix plan |
| 5 | Agent STOPS | Orchestrator defers to next phase |

When an agent reports Rule 4:
1. Read the agent's report
2. Present options to user
3. Create a fix plan if needed
4. Re-execute the affected plan

## Best Practices

1. **Never implement in the orchestrator** — always spawn agents
2. **One plan per agent** — don't combine plans
3. **Verify after each wave** — don't batch all verification to end
4. **Default to worktree isolation** — `isolation: "worktree"` for all parallel agents
5. **Read summaries before advancing** — catch deviations early
6. **Keep STATE.md current** — next session needs it for continuity
7. **Launch up to 8 concurrent agents** — worktree isolation makes this safe
8. **Start plans as soon as deps are met** — don't wait for entire waves

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Executing all waves at once | Later waves break from missing deps | Wave-by-wave with verification |
| Agent modifies unplanned files | Merge conflicts, unexpected changes | Plans list exact files |
| Skipping Rule 4 stops | Architecture breaks silently | Always respect agent STOP signals |
| Not reading summaries | Deviations go unnoticed | Review every summary between waves |
| Too many agents at once | System resource limits | Max 6-8 concurrent agents (worktree isolation) |
| No commits between tasks | Can't revert individual tasks | Atomic commit after each task |

## Examples

### Executing a 2-Wave Phase

```
Wave 1 (parallel):
  → Agent A: Plan 1-1 (API routes)     → SUMMARY: ✅ all must-haves
  → Agent B: Plan 1-2 (Database schema) → SUMMARY: ✅ all must-haves

[Verify Wave 1: build ✅, typecheck ✅, tests ✅]

Wave 2 (sequential — depends on both):
  → Agent C: Plan 1-3 (Frontend integration) → SUMMARY: ⚠️ Rule 3 deviation

[Verify Wave 2: build ✅, typecheck ✅, 1 test needs update]
[Update STATE.md: Phase 1 complete]
```

### Handling a Rule 4 Stop

```
Agent C reports: "Plan requires adding a new database table not in schema.
This is an architectural change (Rule 4). Stopping."

Orchestrator:
  → Presents to user: "Agent found schema needs new 'notifications' table"
  → User confirms: "Yes, add it"
  → Creates fix plan: Add notifications table
  → Re-spawns agent with updated plan
```


---

## From `gsd-verify`

> Goal-backward verification — verify from must-haves backward to artifacts, detect stubs and regressions

# GSD Verify

## Purpose

Verify implementation **from goals backward** — start with must-haves and trace
to artifacts. This catches stubs, missing integrations, and broken links that
forward-only verification (build + test) misses.

## Key Insight

```
Forward verification:  Code → Build → Tests → "Looks good" (misses stubs)
Backward verification: Must-have → Artifact → Key Links → "Actually works"
```

## Workflow

### Step 0: SPEC → PLAN Traceability Gate (MANDATORY)

**This step is non-negotiable.** If `.planning/SPEC.md` exists, verify traceability FIRST:

1. Read all acceptance criteria from SPEC.md
2. Read all must-haves from every PLAN.md in `.planning/`
3. For each acceptance criterion, find at least one PLAN.md must-have that traces to it
4. **If any criterion has NO matching must-have → STOP and report the gap**

The gap means a requirement was specified but never planned for — this is a missed requirement
that will silently ship incomplete. Do NOT proceed to artifact verification until traceability passes.

```
SPEC.md AC#1: "Users can reset password via email"
  → Plan 1-2 Must-Have: "POST /api/auth/reset sends reset email"  ✅ TRACED

SPEC.md AC#4: "Rate-limited to 100 req/min per user"
  → (no matching must-have in any plan)  ❌ GAP — create a fix plan
```

### Step 1: Collect Must-Haves

Read all PLAN.md files, extract every must-have:

```
Plan 1-1:
  - [ ] POST /api/users returns 201 with user JSON
  - [ ] Password hashed with bcrypt
  - [ ] Email uniqueness enforced at DB level

Plan 1-2:
  - [ ] Login returns JWT + refresh token
  - [ ] Refresh token rotates on use
```

### Step 2: Goal-Backward Trace

For each must-have:

1. **Find the artifact** — grep for the implementation
   ```bash
   # "POST /api/users returns 201"
   grep -rn "POST.*users\|/api/users" src/
   ```

2. **Verify correctness** — read the artifact, check it satisfies the goal
   - Does the route actually return 201?
   - Does it return user JSON (not just `{ ok: true }`)?

3. **Check key links** — trace imports, routes, middleware
   - Is the route registered?
   - Is middleware applied (auth, validation)?
   - Are types consistent across boundaries?

4. **Mark result**: PASS, FAIL, or STUB

### Step 3: Stub Detection

Scan for placeholder patterns that indicate incomplete implementation:

```bash
# Stub patterns to grep for
grep -rn \
  -e 'TODO' \
  -e 'FIXME' \
  -e 'HACK' \
  -e 'placeholder' \
  -e 'mock.*data' \
  -e 'fake.*data' \
  -e 'lorem ipsum' \
  -e 'console\.log' \
  -e 'throw new Error.*not implemented' \
  -e 'return null.*//.*temp' \
  src/ --include='*.ts' --include='*.tsx' | grep -v node_modules | grep -v '.test.'
```

### Step 4: Technical Verification

Run the standard verification pipeline:

```bash
# Build
npm run build

# Typecheck
npx tsc --noEmit

# Lint
npx biome lint src/ || npx eslint src/

# Tests
npx vitest run

# Coverage (if available)
npx vitest run --coverage
```

### Step 5: Integration Check

For multi-phase projects, verify cross-phase integration:

- Do phase 1 APIs get called by phase 2 frontend?
- Do shared types match across boundaries?
- Are environment variables consistent?
- Do new routes appear in the router?

### Step 6: Generate Report

```markdown
# VERIFICATION.md

## Summary
Phase: 1 | Plans: 3 | Must-Haves: 12

## Results

### Plan 1-1: User API
| # | Must-Have | Status | Evidence |
|---|----------|--------|----------|
| 1 | POST /api/users returns 201 | ✅ PASS | src/app/api/users/route.ts:24 |
| 2 | Password hashed with bcrypt | ✅ PASS | src/lib/auth.ts:8 |
| 3 | Email uniqueness at DB level | ✅ PASS | prisma/schema.prisma:12 @@unique |

### Plan 1-2: Auth
| 1 | Login returns JWT | ✅ PASS | src/app/api/auth/login/route.ts:31 |
| 2 | Refresh token rotates | ❌ FAIL | Token created but not rotated on reuse |

## Stubs Detected
- src/lib/email.ts:15 — TODO: send verification email

## Technical Checks
- Build: ✅ PASS
- Typecheck: ✅ PASS
- Lint: ⚠️ 2 warnings
- Tests: ✅ 14/14 passed

## Verdict
11/12 must-haves PASSED
1 FAIL: refresh token rotation
1 STUB: email verification

## Auto-Fix Plans
→ Generated: 1-fix-1-PLAN.md (refresh token rotation)
→ Deferred: email verification (documented for Phase 2)
```

### Step 7: Auto-Generate Fix Plans

For each FAIL, create a minimal fix plan:

```markdown
# Plan: 1-fix-1 — Fix refresh token rotation

<plan_metadata>
wave: 1
depends_on: ["1-2"]
estimated_tasks: 1
risk: low
</plan_metadata>

## Context
Refresh token is created on login but not rotated when used.
The /api/auth/refresh endpoint reissues a JWT but reuses the same refresh token.

## Must-Haves
- [ ] Using a refresh token invalidates the old one
- [ ] New refresh token issued alongside new JWT
- [ ] Old refresh tokens cannot be reused (returns 401)

## Tasks
### Task 1: Implement token rotation
**Files:** `src/app/api/auth/refresh/route.ts`, `src/lib/tokens.ts`
**Approach:** On refresh, delete old token from DB, issue new pair
```

## Best Practices

1. **Always verify backward** — must-have → artifact, never artifact → "probably fine"
2. **Check key links** — an API route that exists but isn't registered is useless
3. **Stubs are failures** — TODO in production code means the feature isn't done
4. **Auto-generate fix plans** — don't just report failures, create actionable plans
5. **Integration matters** — phase N features must connect to phase N-1
6. **Console.log is a stub** — treat leftover debug logging as incomplete

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Only running build+test | Stubs pass tests but don't work | Goal-backward trace catches stubs |
| Vague must-haves can't be verified | Verification is hand-wavy | Rewrite must-haves to be specific |
| Not checking key links | Route exists but isn't reachable | Trace imports and registrations |
| Ignoring stubs | Placeholder code ships | Grep for TODO/placeholder/mock |
| Fix plans too large | Defeats minimal-diff philosophy | One fix plan per failure, 1 task each |
| Not re-verifying after fix | Fix introduces new issues | Always re-run verification after fixes |

## Examples

### Catching a Stub

```
Must-have: "Email verification sent on signup"

Trace:
  → src/app/api/users/route.ts:45: await sendVerificationEmail(user.email)
  → src/lib/email.ts:15: export async function sendVerificationEmail(email: string) {
  → src/lib/email.ts:16:   // TODO: implement with Resend
  → src/lib/email.ts:17:   console.log("Would send email to", email);
  → src/lib/email.ts:18: }

Verdict: STUB — function exists but is a no-op
```


---

## From `gsd-quick`

> GSD Quick — lightweight ad-hoc tasks with spec-driven guarantees, no ceremony

# GSD Quick

## Purpose

Execute a single, focused task with GSD guarantees but minimal ceremony.
No phases, no roadmap, no multi-wave execution — just plan-execute-verify
in one shot. Perfect for:

- Bug fixes
- Small features (1-3 files)
- Refactors with clear scope
- Adding a component, route, or utility

## Workflow

### Default (no flags): Scout → Implement → Verify

```
1. Quick scout: grep/glob for relevant files (30 seconds)
2. Create mental plan: what files to touch, what to change
3. Implement: make the changes
4. Quick verify: typecheck + test affected files
5. Commit: atomic commit with clear message
```

### With --discuss: Clarify → Scout → Implement → Verify

```
1. Identify gray areas in the request
2. Ask user to clarify (max 2-3 questions)
3. Then proceed with default flow
```

### With --research: Research → Scout → Implement → Verify

```
1. Spawn research agent to understand approach
2. Read research results
3. Then proceed with default flow
```

### With --full: Plan → Execute → Verify (mini GSD)

```
1. Create 1 PLAN.md with must-haves
2. Write progress file: /tmp/ultrathink-progress-{session_id}
3. Spawn 1 executor agent with fresh context
4. Update progress as tasks complete
5. Goal-backward verify against must-haves
6. Delete progress file, commit
```

## Progress Tracking

Write progress to `/tmp/ultrathink-progress-{session_id}` so the statusline shows a live bar.
Even for quick tasks with --full or --research (agent spawns), update progress:

```bash
# Before spawning agent
echo '{"mode":"gsd-quick","phase":1,"wave":1,"total_waves":1,"agents":[{"plan":"quick","status":"running"}],"tasks":{"total":3,"completed":0,"current":"Implementing"}}' > /tmp/ultrathink-progress-{session_id}

# After agent returns
rm -f /tmp/ultrathink-progress-{session_id}
```

## Deviation Rules (Simplified)

For quick tasks, simplified rules:

| Situation | Action |
|-----------|--------|
| Blocking bug found | Fix it inline, note in commit message |
| Missing dependency | Install it, continue |
| Scope expanding beyond 3 files | STOP — suggest using full `gsd` instead |
| Architecture question | STOP — ask user before proceeding |

## Quick Mode Decision Tree

```
Is it a bug fix?           → Default mode (no flags)
Is it a small feature?     → Default or --research
Is the request ambiguous?  → --discuss
Is it touching >3 files?   → --full or escalate to gsd
Is it a new pattern?       → --research
```

## Best Practices

1. **Quick means quick** — if you're planning for >5 minutes, use full GSD
2. **Still verify** — even quick tasks get a typecheck + test pass
3. **Atomic commits** — one commit per quick task
4. **Know when to escalate** — >3 files or architecture changes = full GSD
5. **Include context in commit** — commit message explains the WHY
6. **Don't skip research for new patterns** — use --research flag

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Quick task grows into feature | Context fills, quality drops | Escalate to full GSD at 3+ files |
| Skipping verification | Ships broken code | Always typecheck at minimum |
| No commit message context | Git history is unhelpful | Include why, not just what |
| Over-engineering quick tasks | Wastes time on ceremony | Quick = minimum viable, iterate later |

## Examples

### Bug Fix (default)

```
User: "The login button doesn't redirect after auth"

Quick:
  Scout: grep for login handler, auth callback
  Fix: Add router.push('/dashboard') after successful auth
  Verify: tsc clean, existing tests pass
  Commit: "fix(auth): redirect to dashboard after login"
```

### Small Feature (--research)

```
User: "Add a loading skeleton to the users table"

Quick --research:
  Research: Check if project uses a skeleton library (shadcn? custom?)
  Scout: Find UsersTable component
  Implement: Add Skeleton component with table row pattern
  Verify: tsc clean, visual check
  Commit: "feat(ui): add loading skeleton to users table"
```

