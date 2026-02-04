---
name: ring:dev-cycle
description: |
  Main orchestrator for the 6-gate development cycle system. Loads tasks/subtasks
  from PM team output and executes through implementation, devops, SRE, testing, review,
  and validation gates with state persistence and metrics collection.

trigger: |
  - Starting a new development cycle with a task file
  - Resuming an interrupted development cycle (--resume flag)
  - Need structured, gate-based task execution with quality checkpoints

prerequisite: |
  - Tasks file exists with structured subtasks
  - Not already in a specific gate skill execution
  - Human has not explicitly requested manual workflow

NOT_skip_when: |
  - "Task is simple" → Simple ≠ risk-free. Execute gates.
  - "Tests already pass" → Tests ≠ review. Different concerns.
  - "Time pressure" → Pressure ≠ permission. Document and proceed.
  - "Already did N gates" → Sunk cost is irrelevant. Complete all gates.

sequence:
  before: [ring:dev-feedback-loop]

related:
  complementary: [ring:dev-implementation, ring:dev-devops, ring:dev-ring:sre, ring:dev-testing, ring:requesting-code-review, ring:dev-validation, ring:dev-feedback-loop]

verification:
  automated:
    - command: "test -f docs/ring:dev-cycle/current-cycle.json || test -f docs/ring:dev-refactor/current-cycle.json"
      description: "State file exists (ring:dev-cycle or ring:dev-refactor)"
      success_pattern: "exit 0"
    - command: "cat docs/ring:dev-cycle/current-cycle.json 2>/dev/null || cat docs/ring:dev-refactor/current-cycle.json | jq '.current_gate'"
      description: "Current gate is valid"
      success_pattern: "[0-5]"
  manual:
    - "All gates for current task show PASS in state file"
    - "No tasks have status 'blocked' for more than 3 iterations"

examples:
  - name: "New feature from PM workflow"
    invocation: "/ring:dev-cycle docs/pre-dev/auth/tasks.md"
    expected_flow: |
      1. Load tasks with subtasks from tasks.md
      2. Ask user for checkpoint mode (per-task/per-gate/continuous)
      3. Execute Gate 0-5 for each task sequentially
      4. Generate feedback report after completion
  - name: "Resume interrupted cycle"
    invocation: "/ring:dev-cycle --resume"
    expected_state: "Continues from last saved gate in current-cycle.json"
  - name: "Execute with per-gate checkpoints"
    invocation: "/ring:dev-cycle tasks.md --checkpoint per-gate"
    expected_flow: |
      1. Execute Gate 0, pause for approval
      2. User approves, execute Gate 1, pause
      3. Continue until all gates complete
  - name: "Execute with custom context for agents"
    invocation: "/ring:dev-cycle tasks.md --prompt \"Focus on error handling. Use existing UserRepository.\""
    expected_flow: |
      1. Load tasks and store custom_prompt in state
      2. All agent dispatches include custom prompt as context
      3. Custom context visible in execution report
  - name: "Prompt-only mode (no tasks file)"
    invocation: "/ring:dev-cycle --prompt \"Implement multi-tenant support with organization_id in all entities\""
    expected_flow: |
      1. Detect prompt-only mode (no task file provided)
      2. Dispatch ring:codebase-explorer to analyze project
      3. Generate tasks internally from prompt + codebase analysis
      4. Present generated tasks for user confirmation
      5. Execute Gate 0-5 for each generated task
---

# Development Cycle Orchestrator

## Standards Loading (MANDATORY)

**Before any gate execution, you MUST load Ring standards:**

<fetch_required>
https://raw.githubusercontent.com/LerianStudio/ring/main/CLAUDE.md
</fetch_required>

Fetch URL above and extract: Agent Modification Verification requirements, Anti-Rationalization Tables requirements, and Critical Rules.

<block_condition>
- WebFetch fails or returns empty
- CLAUDE.md not accessible
</block_condition>

If any condition is true, STOP and report blocker. Cannot proceed without Ring standards.

## Overview

The development cycle orchestrator loads tasks/subtasks from PM team output (or manual task files) and executes through 6 quality gates. Tasks are loaded at initialization - no separate import gate.

**Announce at start:** "I'm using the ring:dev-cycle skill to orchestrate task execution through 6 gates."

## ⛔ CRITICAL: Specialized Agents Perform All Tasks

See [shared-patterns/shared-orchestrator-principle.md](../shared-patterns/shared-orchestrator-principle.md) for full ORCHESTRATOR principle, role separation, forbidden/required actions, gate-to-agent mapping, and anti-rationalization table.

**Summary:** You orchestrate. Agents execute. If using Read/Write/Edit/Bash on source code → STOP. Dispatch agent.

---

## ⛔ ORCHESTRATOR BOUNDARIES (HARD GATE)

**This section defines exactly what the orchestrator CAN and CANNOT do.**

### What Orchestrator CAN Do (PERMITTED)

| Action | Tool | Purpose |
|--------|------|---------|
| Read task files | `Read` | Load task definitions from `docs/pre-dev/*/tasks.md` or `docs/refactor/*/tasks.md` |
| Read state files | `Read` | Load/verify `docs/ring:dev-cycle/current-cycle.json` or `docs/ring:dev-refactor/current-cycle.json` |
| Read PROJECT_RULES.md | `Read` | Load project-specific rules |
| Write state files | `Write` | Persist cycle state to JSON |
| Track progress | `TodoWrite` | Maintain task list |
| Dispatch agents | `Task` | Send work to specialist agents |
| Ask user questions | `AskUserQuestion` | Get execution mode, approvals |
| WebFetch standards | `WebFetch` | Load Ring standards |

### What Orchestrator CANNOT Do (FORBIDDEN)

<forbidden>
- Read source code (`Read` on `*.go`, `*.ts`, `*.tsx`) - Agent reads code, not orchestrator
- Write source code (`Write`/`Create` on `*.go`, `*.ts`) - Agent writes code, not orchestrator
- Edit source code (`Edit` on `*.go`, `*.ts`, `*.tsx`) - Agent edits code, not orchestrator
- Run tests (`Execute` with `go test`, `npm test`) - Agent runs tests in TDD cycle
- Analyze code (Direct pattern analysis) - `ring:codebase-explorer` analyzes
- Make architectural decisions (Choosing patterns/libraries) - User decides, agent implements
</forbidden>

Any of these actions by orchestrator = IMMEDIATE VIOLATION. Dispatch agent instead.

---

### The 3-FILE RULE

**If a task requires editing MORE than 3 files → MUST dispatch specialist agent.**

This is not negotiable:
- 1-3 files of non-source content (markdown, json, yaml) → Orchestrator MAY edit directly
- 1+ source code files (`*.go`, `*.ts`, `*.tsx`) → MUST dispatch agent
- 4+ files of any type → MUST dispatch agent

### Orchestrator Workflow Order (MANDATORY)

```text
┌─────────────────────────────────────────────────────────────────┐
│  CORRECT WORKFLOW ORDER                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Load task file (Read docs/pre-dev/*/tasks.md or docs/refactor/*/tasks.md) │
│  2. Ask execution mode (AskUserQuestion)                        │
│  3. Determine state path + Check/Load state (see State Path Selection) │
│  4. WebFetch Ring Standards                                     │
│  5. ⛔ LOAD SUB-SKILL for current gate (Skill tool)            │
│  6. Execute sub-skill instructions (dispatch agent via Task)    │
│  7. Wait for agent completion                                   │
│  8. Verify agent output (Standards Coverage Table)              │
│  9. Update state (Write to JSON)                               │
│  10. Proceed to next gate                                       │
│                                                                 │
│  ════════════════════════════════════════════════════════════   │
│  ❌ WRONG: Load → Mode → Standards → Task(agent) directly       │
│  ✅ RIGHT: Load → Mode → Standards → Skill(sub) → Task(agent)   │
│  ════════════════════════════════════════════════════════════   │
└─────────────────────────────────────────────────────────────────┘
```

### ⛔ SUB-SKILL LOADING IS MANDATORY (HARD GATE)

**Before dispatching any agent, you MUST load the corresponding sub-skill first.**

<cannot_skip>
- Gate 0: `Skill("ring:dev-implementation")` → then `Task(subagent_type="ring:backend-engineer-*", ...)`
- Gate 1: `Skill("ring:dev-devops")` → then `Task(subagent_type="ring:devops-engineer", ...)`
- Gate 2: `Skill("ring:dev-ring:sre")` → then `Task(subagent_type="ring:sre", ...)`
- Gate 3: `Skill("ring:dev-testing")` → then `Task(subagent_type="ring:qa-analyst", ...)`
- Gate 4: `Skill("ring:requesting-code-review")` → then 3x `Task(...)` in parallel
- Gate 5: `Skill("ring:dev-validation")` → N/A (verification only)
</cannot_skip>

Between "WebFetch standards" and "Task(agent)" there MUST be "Skill(sub-skill)".

**The workflow for each gate is:**
```text
1. Skill("[sub-skill-name]")     ← Load sub-skill instructions
2. Follow sub-skill instructions  ← Sub-skill tells you HOW to dispatch
3. Task(subagent_type=...)       ← Dispatch agent as sub-skill instructs
4. Validate agent output          ← Per sub-skill validation rules
5. Update state                   ← Record results
```

### Custom Prompt Injection (--prompt flag)

**Validation:** See [shared-patterns/custom-prompt-validation.md](../shared-patterns/custom-prompt-validation.md) for max length (500 chars), sanitization rules, gate protection, and conflict handling.

**If `custom_prompt` is set in state, inject it into ALL agent dispatches:**

```yaml
Task tool:
  subagent_type: "ring:backend-engineer-golang"
  model: "opus"
  prompt: |
    **CUSTOM CONTEXT (from user):**
    {state.custom_prompt}
    
    ---
    
    **Standard Instructions:**
    [... rest of agent prompt ...]
```

**Rules for custom prompt:**
1. **Inject at TOP of prompt** - User context takes precedence
2. **Preserve in state** - custom_prompt persists for resume
3. **Include in execution report** - Document what context was used
4. **Forward via state** - Sub-skills read `custom_prompt` from state file and inject into their agent dispatches (no explicit parameter passing needed)

**Example custom prompts and their effect:**

| Custom Prompt | Effect on Agents |
|---------------|------------------|
| "Focus on error handling first" | Agents prioritize error-related acceptance criteria |
| "Use existing UserRepository interface" | Agents integrate with specified interface instead of creating new |
| "Deprioritize UI polish" | Gate 3 still enforces 85% coverage, but agents deprioritize non-functional UI tweaks |
| "Prioritize observability gaps" | SRE gate gets more attention, implementation focuses on instrumentation |

### Anti-Rationalization for Skipping Sub-Skills

| Rationalization | Why It's WRONG | Required Action |
|-----------------|----------------|-----------------|
| "I know what the sub-skill does" | Knowledge ≠ execution. Sub-skill has iteration logic. | **Load Skill() first** |
| "Task() directly is faster" | Faster ≠ correct. Sub-skill has validation rules. | **Load Skill() first** |
| "Sub-skill just wraps Task()" | Sub-skills have retry logic, fix dispatch, validation. | **Load Skill() first** |
| "I'll follow the pattern manually" | Manual = error-prone. Sub-skill is the pattern. | **Load Skill() first** |

**Between "WebFetch standards" and "Task(agent)" there MUST be "Skill(sub-skill)".**

---

### Anti-Rationalization for Direct Coding

| Rationalization | Why It's WRONG | Required Action |
|-----------------|----------------|-----------------|
| "It's just one small file" | File count doesn't determine agent need. Language does. | **DISPATCH specialist agent** |
| "I already loaded the standards" | Loading standards ≠ permission to implement. Standards are for AGENTS. | **DISPATCH specialist agent** |
| "Agent dispatch adds overhead" | Overhead ensures compliance. Skip = skip verification. | **DISPATCH specialist agent** |
| "I can write Go/TypeScript" | Knowing language ≠ having Ring standards loaded. Agent has them. | **DISPATCH specialist agent** |
| "Just a quick fix" | "Quick" is irrelevant. all source changes require specialist. | **DISPATCH specialist agent** |
| "I'll read the file first to understand" | Reading source → temptation to edit. Agent reads for you. | **DISPATCH specialist agent** |
| "Let me check if tests pass first" | Agent runs tests in TDD cycle. You don't run tests. | **DISPATCH specialist agent** |

### Red Flags - Orchestrator Violation in Progress

**If you catch yourself doing any of these, STOP IMMEDIATELY:**

```text
🚨 RED FLAG: About to Read *.go or *.ts file
   → STOP. Dispatch agent instead.

🚨 RED FLAG: About to Write/Create source code
   → STOP. Dispatch agent instead.

🚨 RED FLAG: About to Edit source code
   → STOP. Dispatch agent instead.

🚨 RED FLAG: About to run "go test" or "npm test"
   → STOP. Agent runs tests, not you.

🚨 RED FLAG: Thinking "I'll just..."
   → STOP. "Just" is the warning word. Dispatch agent.

🚨 RED FLAG: Thinking "This is simple enough..."
   → STOP. Simplicity is irrelevant. Dispatch agent.

🚨 RED FLAG: Standards loaded, but next action is not Task tool
   → STOP. After standards, IMMEDIATELY dispatch agent.
```

### Recovery from Orchestrator Violation

If you violated orchestrator boundaries:

1. **STOP** current execution immediately
2. **DISCARD** any direct changes (`git checkout -- .`)
3. **DISPATCH** the correct specialist agent
4. **Agent implements** from scratch following TDD
5. **Document** the violation for feedback loop

**Sunk cost of direct work is IRRELEVANT. Agent dispatch is MANDATORY.**

---

## Blocker Criteria - STOP and Report

<block_condition>
- Gate Failure: Tests not passing, review failed → STOP, cannot proceed to next gate
- Missing Standards: No PROJECT_RULES.md → STOP, report blocker and wait
- Agent Failure: Specialist agent returned errors → STOP, diagnose and report
- User Decision Required: Architecture choice, framework selection → STOP, present options
</block_condition>

You CANNOT proceed when blocked. Report and wait for resolution.

### Cannot Be Overridden

<cannot_skip>
- All 6 gates must execute - Each gate catches different issues
- Gates execute in order (0→5) - Dependencies exist between gates
- Gate 4 requires all 3 reviewers - Different review perspectives are complementary
- Coverage threshold ≥ 85% - Industry standard for quality code
- PROJECT_RULES.md must exist - Cannot verify standards without target
</cannot_skip>

No exceptions. User cannot override. Time pressure cannot override.

---

## Severity Calibration

| Severity | Criteria | Examples |
|----------|----------|----------|
| **CRITICAL** | Blocks deployment, security risk, data loss | Gate violation, skipped mandatory step |
| **HIGH** | Major functionality broken, standards violation | Missing tests, wrong agent dispatched |
| **MEDIUM** | Code quality, maintainability issues | Incomplete documentation, minor gaps |
| **LOW** | Best practices, optimization | Style improvements, minor refactoring |

Report all severities. Let user prioritize.

### Reviewer Verdicts Are Final

**MEDIUM issues found in Gate 4 MUST be fixed. No exceptions.**

| Request | Why It's WRONG | Required Action |
|---------|----------------|-----------------|
| "Can reviewer clarify if MEDIUM can defer?" | Reviewer already decided. MEDIUM means FIX. | **Fix the issue, re-run reviewers** |
| "Ask if this specific case is different" | Reviewer verdict accounts for context already. | **Fix the issue, re-run reviewers** |
| "Request exception for business reasons" | Reviewers know business context. Verdict is final. | **Fix the issue, re-run reviewers** |

**Severity mapping is absolute:**
- CRITICAL/HIGH/MEDIUM → Fix NOW, re-run all 3 reviewers
- LOW → Add TODO(review): comment
- Cosmetic → Add FIXME(nitpick): comment

No negotiation. No exceptions. No "special cases".

---

## Pressure Resistance

See [shared-patterns/shared-pressure-resistance.md](../shared-patterns/shared-pressure-resistance.md) for universal pressure scenarios.

**Gate-specific note:** Execution mode selection affects CHECKPOINTS (user approval pauses), not GATES (quality checks). all gates execute regardless of mode.

---

## Common Rationalizations - REJECTED

See [shared-patterns/shared-anti-rationalization.md](../shared-patterns/shared-anti-rationalization.md) for universal anti-rationalizations.

**Gate-specific rationalizations:**

| Excuse | Reality |
|--------|---------|
| "Automatic mode means faster" | Automatic mode skips CHECKPOINTS, not GATES. Same quality, less interruption. |
| "Automatic mode will skip review" | Automatic mode affects user approval pauses, not quality gates. all gates execute regardless. |
| "Defense in depth exists (frontend validates)" | Frontend can be bypassed. Backend is the last line. Fix at source. |
| "Backlog the Medium issue, it's documented" | Documented risk ≠ mitigated risk. Medium in Gate 4 = fix NOW, not later. |
| "Risk-based prioritization allows deferral" | Gates ARE the risk-based system. Reviewers define severity, not you. |

---

## Red Flags - STOP

See [shared-patterns/shared-red-flags.md](../shared-patterns/shared-red-flags.md) for universal red flags.

If you catch yourself thinking any of those patterns, STOP immediately and return to gate execution.

---

## Incremental Compromise Prevention

**The "just this once" pattern leads to complete gate erosion:**

```text
Day 1: "Skip review just this once" → Approved (precedent set)
Day 2: "Skip testing, we did it last time" → Approved (precedent extended)
Day 3: "Skip implementation checks, pattern established" → Approved (gates meaningless)
Day 4: Production incident from Day 1 code
```

**Prevention rules:**
1. **No incremental exceptions** - Each exception becomes the new baseline
2. **Document every pressure** - Log who requested, why, outcome
3. **Escalate patterns** - If same pressure repeats, escalate to team lead
4. **Gates are binary** - Complete or incomplete. No "mostly done".

---

## Gate Completion Definition (HARD GATE)

**A gate is COMPLETE only when all components finish successfully:**

| Gate | Components Required | Partial = FAIL |
|------|---------------------|----------------|
| 0.1 | TDD-RED: Failing test written + failure output captured | Test exists but no failure output = FAIL |
| 0.2 | TDD-GREEN: Implementation passes test | Code exists but test fails = FAIL |
| 0 | Both 0.1 and 0.2 complete | 0.1 done without 0.2 = FAIL |
| 1 | Dockerfile + docker-compose + .env.example | Missing any = FAIL |
| 2 | Structured JSON logs with trace correlation | Partial structured logs = FAIL |
| 3 | Coverage ≥ 85% + all AC tested | 84% = FAIL |
| 4 | **all 3 reviewers PASS** | 2/3 reviewers = FAIL |
| 5 | Explicit "APPROVED" from user | "Looks good" = not approved |

**CRITICAL for Gate 4:** Running 2 of 3 reviewers is not a partial pass - it's a FAIL. Re-run all 3 reviewers.

**Anti-Rationalization for Partial Gates:**

| Rationalization | Why It's WRONG | Required Action |
|-----------------|----------------|-----------------|
| "2 of 3 reviewers passed" | Gate 4 requires all 3. 2/3 = 0/3. | **Re-run all 3 reviewers** |
| "Gate mostly complete" | Mostly ≠ complete. Binary: done or not done. | **Complete all components** |
| "Can finish remaining in next cycle" | Gates don't carry over. Complete NOW. | **Finish current gate** |
| "Core components done, optional can wait" | No component is optional within a gate. | **Complete all components** |

---

## Gate Order Enforcement (HARD GATE)

**Gates MUST execute in order: 0 → 1 → 2 → 3 → 4 → 5. No exceptions.**

| Violation | Why It's WRONG | Consequence |
|-----------|----------------|-------------|
| Skip Gate 1 (DevOps) | "No infra changes" | Code without container = works on my machine only |
| Skip Gate 2 (SRE) | "Observability later" | Blind production = debugging nightmare |
| Reorder Gates | "Review before test" | Reviewing untested code wastes reviewer time |
| Parallel Gates | "Run 2 and 3 together" | Dependencies exist. Order is intentional. |

**Gates are not parallelizable across different gates. Sequential execution is MANDATORY.**

## The 6 Gates

| Gate | Skill | Purpose | Agent |
|------|-------|---------|-------|
| 0 | ring:dev-implementation | Write code following TDD | Based on task language/domain |
| 1 | ring:dev-devops | Infrastructure and deployment | ring:devops-engineer |
| 2 | ring:dev-ring:sre | Observability (health, logging, tracing) | ring:sre |
| 3 | ring:dev-testing | Unit tests for acceptance criteria | ring:qa-analyst |
| 4 | ring:requesting-code-review | Parallel code review | ring:code-reviewer, ring:business-logic-reviewer, ring:security-reviewer (3x parallel) |
| 5 | ring:dev-validation | Final acceptance validation | N/A (verification) |

## Integrated PM → Dev Workflow

**PM Team Output** → **Dev Team Execution** (`/ring:dev-cycle`)

| Input Type | Path | Structure |
|------------|------|-----------|
| **Tasks only** | `docs/pre-dev/{feature}/tasks.md` | T-001, T-002, T-003 with requirements + acceptance criteria |
| **Tasks + Subtasks** | `docs/pre-dev/{feature}/` | tasks.md + `subtasks/{task-id}/ST-XXX-01.md, ST-XXX-02.md...` |

## Execution Order

**Core Principle:** Each execution unit (task or subtask) passes through **all 6 gates** before the next unit.

**Flow:** Unit → Gate 0-5 → 🔒 Unit Checkpoint (Step 7.1) → 🔒 Task Checkpoint (Step 7.2) → Next Unit

| Scenario | Execution Unit | Gates Per Unit |
|----------|----------------|----------------|
| Task without subtasks | Task itself | 6 gates |
| Task with subtasks | Each subtask | 6 gates per subtask |

## Commit Timing

**User selects when commits happen (Step 7 of initialization).**

| Option | When Commit Happens | Use Case |
|--------|---------------------|----------|
| **(a) Per subtask** | After each subtask passes Gate 5 | Fine-grained history, easy rollback per subtask |
| **(b) Per task** | After all subtasks of a task complete | Logical grouping, one commit per feature chunk |
| **(c) At the end** | After entire cycle completes | Single commit with all changes, clean history |

### Commit Message Format

| Timing | Message Format | Example |
|--------|----------------|---------|
| Per subtask | `feat({subtask_id}): {subtask_title}` | `feat(ST-001-02): implement user authentication handler` |
| Per task | `feat({task_id}): {task_title}` | `feat(T-001): implement user authentication` |
| At the end | `feat({cycle_id}): complete dev cycle for {feature}` | `feat(cycle-abc123): complete dev cycle for auth-system` |

### Commit Timing vs Execution Mode

| Execution Mode | Commit Timing | Behavior |
|----------------|---------------|----------|
| Manual per subtask | Per subtask | Commit + checkpoint after each subtask |
| Manual per subtask | Per task | Checkpoint after subtask, commit after task |
| Manual per subtask | At end | Checkpoint after subtask, commit at cycle end |
| Manual per task | Per subtask | Commit after subtask, checkpoint after task |
| Manual per task | Per task | Commit + checkpoint after task |
| Manual per task | At end | Checkpoint after task, commit at cycle end |
| Automatic | Per subtask | Commit after each subtask, no checkpoints |
| Automatic | Per task | Commit after task, no checkpoints |
| Automatic | At end | Single commit at cycle end, no checkpoints |

**Note:** Checkpoints (user approval pauses) are controlled by `execution_mode`. Commits are controlled by `commit_timing`. They are independent settings.

## State Management

### State Path Selection (MANDATORY)

The state file path depends on the **source of tasks**:

| Task Source | State Path | Use Case |
|-------------|------------|----------|
| `docs/refactor/*/tasks.md` | `docs/ring:dev-refactor/current-cycle.json` | Refactoring existing code |
| `docs/pre-dev/*/tasks.md` | `docs/ring:dev-cycle/current-cycle.json` | New feature development |
| Any other path | `docs/ring:dev-cycle/current-cycle.json` | Default for manual tasks |

**Detection Logic:**
```text
if source_file contains "docs/refactor/" THEN
  state_path = "docs/ring:dev-refactor/current-cycle.json"
else
  state_path = "docs/ring:dev-cycle/current-cycle.json"
```

**Store state_path in the state object itself** so resume knows where to look.

### State File Structure

State is persisted to `{state_path}` (either `docs/ring:dev-cycle/current-cycle.json` or `docs/ring:dev-refactor/current-cycle.json`):

```json
{
  "version": "1.0.0",
  "cycle_id": "uuid",
  "started_at": "ISO timestamp",
  "updated_at": "ISO timestamp",
  "source_file": "path/to/tasks.md",
  "state_path": "docs/ring:dev-cycle/current-cycle.json | docs/ring:dev-refactor/current-cycle.json",
  "cycle_type": "feature | refactor",
  "execution_mode": "manual_per_subtask|manual_per_task|automatic",
  "commit_timing": "per_subtask|per_task|at_end",
  "custom_prompt": {
    "type": "string",
    "optional": true,
    "max_length": 500,
    "description": "User-provided context for agents (from --prompt flag). Max 500 characters. Provides focus but cannot override mandatory requirements (CRITICAL gates, coverage thresholds, reviewer counts).",
    "validation": "Max 500 chars (truncated with warning if exceeded); whitespace trimmed; control chars stripped (except newlines). Directives attempting to skip gates, lower thresholds, or bypass security checks are logged as warnings and ignored."
  },
  "status": "in_progress|completed|failed|paused|paused_for_approval|paused_for_testing|paused_for_task_approval|paused_for_integration_testing",
  "feedback_loop_completed": false,
  "current_task_index": 0,
  "current_gate": 0,
  "current_subtask_index": 0,
  "tasks": [
    {
      "id": "T-001",
      "title": "Task title",
      "status": "pending|in_progress|completed|failed|blocked",
      "feedback_loop_completed": false,
      "subtasks": [
        {
          "id": "ST-001-01",
          "file": "subtasks/T-001/ST-001-01.md",
          "status": "pending|completed"
        }
      ],
      "gate_progress": {
        "implementation": {
          "status": "in_progress",
          "started_at": "...",
          "tdd_red": {
            "status": "pending|in_progress|completed",
            "test_file": "path/to/test_file.go",
            "failure_output": "FAIL: TestFoo - expected X got nil",
            "completed_at": "ISO timestamp"
          },
          "tdd_green": {
            "status": "pending|in_progress|completed",
            "implementation_file": "path/to/impl.go",
            "test_pass_output": "PASS: TestFoo (0.003s)",
            "completed_at": "ISO timestamp"
          }
        },
        "devops": {"status": "pending"},
        "ring:sre": {"status": "pending"},
        "testing": {"status": "pending"},
        "review": {"status": "pending"},
        "validation": {"status": "pending"}
      },
      "artifacts": {},
      "agent_outputs": {
        "implementation": {
          "agent": "ring:backend-engineer-golang",
          "output": "## Summary\n...",
          "timestamp": "ISO timestamp",
          "duration_ms": 0,
          "iterations": 1,
          "standards_compliance": {
            "total_sections": 15,
            "compliant": 14,
            "not_applicable": 1,
            "non_compliant": 0,
            "gaps": []
          }
        },
        "devops": {
          "agent": "ring:devops-engineer",
          "output": "## Summary\n...",
          "timestamp": "ISO timestamp",
          "duration_ms": 0,
          "iterations": 1,
          "artifacts_created": ["Dockerfile", "docker-compose.yml", ".env.example"],
          "verification_errors": [],
          "standards_compliance": {
            "total_sections": 8,
            "compliant": 8,
            "not_applicable": 0,
            "non_compliant": 0,
            "gaps": []
          }
        },
        "ring:sre": {
          "agent": "ring:sre",
          "output": "## Summary\n...",
          "timestamp": "ISO timestamp",
          "duration_ms": 0,
          "iterations": 1,
          "instrumentation_coverage": "92%",
          "validation_errors": [],
          "standards_compliance": {
            "total_sections": 10,
            "compliant": 10,
            "not_applicable": 0,
            "non_compliant": 0,
            "gaps": []
          }
        },
        "testing": {
          "agent": "ring:qa-analyst",
          "output": "## Summary\n...",
          "verdict": "PASS",
          "coverage_actual": 87.5,
          "coverage_threshold": 85,
          "iterations": 1,
          "timestamp": "ISO timestamp",
          "duration_ms": 0,
          "failures": [],
          "uncovered_criteria": [],
          "standards_compliance": {
            "total_sections": 6,
            "compliant": 6,
            "not_applicable": 0,
            "non_compliant": 0,
            "gaps": []
          }
        },
        "review": {
          "iterations": 1,
          "timestamp": "ISO timestamp",
          "duration_ms": 0,
          "code_reviewer": {
            "agent": "ring:code-reviewer",
            "output": "...",
            "verdict": "PASS",
            "timestamp": "...",
            "issues": [],
            "standards_compliance": {
              "total_sections": 12,
              "compliant": 12,
              "not_applicable": 0,
              "non_compliant": 0,
              "gaps": []
            }
          },
          "business_logic_reviewer": {
            "agent": "ring:business-logic-reviewer",
            "output": "...",
            "verdict": "PASS",
            "timestamp": "...",
            "issues": [],
            "standards_compliance": {
              "total_sections": 8,
              "compliant": 8,
              "not_applicable": 0,
              "non_compliant": 0,
              "gaps": []
            }
          },
          "security_reviewer": {
            "agent": "ring:security-reviewer",
            "output": "...",
            "verdict": "PASS",
            "timestamp": "...",
            "issues": [],
            "standards_compliance": {
              "total_sections": 10,
              "compliant": 10,
              "not_applicable": 0,
              "non_compliant": 0,
              "gaps": []
            }
          }
        },
        "validation": {
          "result": "approved|rejected",
          "timestamp": "ISO timestamp"
        }
      }
    }
  ],
  "metrics": {
    "total_duration_ms": 0,
    "gate_durations": {},
    "review_iterations": 0,
    "testing_iterations": 0
  }
}
```

### Structured Error/Issue Schemas

**These schemas enable `ring:dev-feedback-loop` to analyze issues without parsing raw output.**

#### Standards Compliance Gap Schema

```json
{
  "section": "Error Handling (MANDATORY)",
  "status": "❌",
  "reason": "Missing error wrapping with context",
  "file": "internal/handler/user.go",
  "line": 45,
  "evidence": "return err // should wrap with additional context"
}
```

#### Test Failure Schema

```json
{
  "test_name": "TestUserCreate_InvalidEmail",
  "test_file": "internal/handler/user_test.go",
  "error_type": "assertion",
  "expected": "ErrInvalidEmail",
  "actual": "nil",
  "message": "Expected validation error for invalid email format",
  "stack_trace": "user_test.go:42 → user.go:28"
}
```

#### Review Issue Schema

```json
{
  "severity": "MEDIUM",
  "category": "error-handling",
  "description": "Error not wrapped with context before returning",
  "file": "internal/handler/user.go",
  "line": 45,
  "suggestion": "Use fmt.Errorf(\"failed to create user: %w\", err)",
  "fixed": false,
  "fixed_in_iteration": null
}
```

#### DevOps Verification Error Schema

```json
{
  "check": "docker_build",
  "status": "FAIL",
  "error": "COPY failed: file not found in build context: go.sum",
  "suggestion": "Ensure go.sum exists and is not in .dockerignore"
}
```

#### SRE Validation Error Schema

```json
{
  "check": "structured_logging",
  "status": "FAIL",
  "file": "internal/handler/user.go",
  "line": 32,
  "error": "Using fmt.Printf instead of structured logger",
  "suggestion": "Use logger.Info().Str(\"user_id\", id).Msg(\"user created\")"
}
```

### Populating Structured Data

**Each gate MUST populate its structured fields when saving to state:**

| Gate | Fields to Populate |
|------|-------------------|
| Gate 0 (Implementation) | `standards_compliance` (total, compliant, gaps[]) |
| Gate 1 (DevOps) | `standards_compliance` + `verification_errors[]` |
| Gate 2 (SRE) | `standards_compliance` + `validation_errors[]` |
| Gate 3 (Testing) | `standards_compliance` + `failures[]` + `uncovered_criteria[]` |
| Gate 4 (Review) | `standards_compliance` per reviewer + `issues[]` per reviewer |

**All gates track `standards_compliance`:**
- `total_sections`: Count from agent's standards file (via standards-coverage-table.md)
- `compliant`: Sections marked ✅ in Standards Coverage Table
- `not_applicable`: Sections marked N/A
- `non_compliant`: Sections marked ❌ (MUST be 0 to pass gate)
- `gaps[]`: Detailed info for each ❌ section (even if later fixed)

**Empty arrays `[]` indicate no issues found - this is valid data for feedback-loop.**

## ⛔ State Persistence Rule (MANDATORY)

**"Update state" means BOTH update the object and write to file. Not just in-memory.**

### After every Gate Transition

You MUST execute these steps after completing any gate (0, 1, 2, 3, 4, or 5):

```yaml
# Step 1: Update state object with gate results
state.tasks[current_task_index].gate_progress.[gate_name].status = "completed"
state.tasks[current_task_index].gate_progress.[gate_name].completed_at = "[ISO timestamp]"
state.current_gate = [next_gate_number]
state.updated_at = "[ISO timestamp]"

# Step 2: Write to file (MANDATORY - use Write tool)
Write tool:
  file_path: [state.state_path]  # Use state_path from state object
  content: [full JSON state]

# Step 3: Verify persistence (MANDATORY - use Read tool)
Read tool:
  file_path: [state.state_path]  # Use state_path from state object
# Confirm current_gate and gate_progress match expected values
```

### State Persistence Checkpoints

| After | MUST Update | MUST Write File |
|-------|-------------|-----------------|
| Gate 0.1 (TDD-RED) | `tdd_red.status`, `tdd_red.failure_output` | ✅ YES |
| Gate 0.2 (TDD-GREEN) | `tdd_green.status`, `implementation.status` | ✅ YES |
| Gate 1 (DevOps) | `devops.status`, `agent_outputs.devops` | ✅ YES |
| Gate 2 (SRE) | `ring:sre.status`, `agent_outputs.ring:sre` | ✅ YES |
| Gate 3 (Testing) | `testing.status`, `agent_outputs.testing` | ✅ YES |
| Gate 4 (Review) | `review.status`, `agent_outputs.review` | ✅ YES |
| Gate 5 (Validation) | `validation.status`, task `status` | ✅ YES |
| Step 7.1 (Unit Approval) | `status = "paused_for_approval"` | ✅ YES |
| Step 7.2 (Task Approval) | `status = "paused_for_task_approval"` | ✅ YES |

### Anti-Rationalization for State Persistence

| Rationalization | Why It's WRONG | Required Action |
|-----------------|----------------|-----------------|
| "I'll save state at the end" | Crash/timeout loses all progress | **Save after each gate** |
| "State is in memory, that's updated" | Memory is volatile. File is persistent. | **Write to JSON file** |
| "Only save on checkpoints" | Gates without saves = unrecoverable on resume | **Save after every gate** |
| "Write tool is slow" | Write takes <100ms. Lost progress takes hours. | **Write after every gate** |
| "I updated the state variable" | Variable ≠ file. Without Write tool, nothing persists. | **Use Write tool explicitly** |

### Verification Command

After each gate, the state file MUST reflect:
- `current_gate` = next gate number
- `updated_at` = recent timestamp
- Previous gate `status` = "completed"

**If verification fails → State was not persisted. Re-execute Write tool.**

---

## Step 0: Verify PROJECT_RULES.md Exists (HARD GATE)

**NON-NEGOTIABLE. Cycle CANNOT proceed without project standards.**

### Step 0 Flow

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│  Check: Does docs/PROJECT_RULES.md exist?                                   │
│                                                                             │
│  ├── YES → Proceed to Step 1 (Initialize or Resume)                        │
│  │                                                                          │
│  └── no → ASK: "Is this a LEGACY project (created without PM workflow)?"   │
│       │                                                                     │
│       ├── YES (legacy project) → LEGACY PROJECT ANALYSIS:                   │
│       │   Step 1: Dispatch ring:codebase-explorer (technical info only)          │
│       │   Step 2: Ask 3 questions (what agent can't determine):             │
│       │     1. What do you need help with?                                  │
│       │     2. Any external APIs not visible in code?                       │
│       │     3. Any specific technology not in Ring Standards?               │
│       │   Step 3: Generate PROJECT_RULES.md (deduplicated from Ring)        │
│       │   Note: Business rules belong in PRD, not in PROJECT_RULES          │
│       │   → Proceed to Step 1                                               │
│       │                                                                     │
│       └── no (new project) → ASK: "Do you have PRD, TRD, or Feature Map?"  │
│           │                                                                 │
│           ├── YES (has PM docs) → "Please provide the file path(s)"        │
│           │   → Read PRD/TRD/Feature Map → Extract info                    │
│           │   → Generate PROJECT_RULES.md                                  │
│           │   → Ask supplementary questions if info is incomplete          │
│           │   → Save and proceed to Step 1                                 │
│           │                                                                 │
│           └── no (no PM docs) → ⛔ HARD BLOCK:                              │
│               "PM documents are REQUIRED for new projects.                  │
│                Run /ring:pre-dev-full or /ring:pre-dev-feature first."               │
│               → STOP (cycle cannot proceed)                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Step 0.1: Check for PROJECT_RULES.md

```yaml
# Check if file exists
Read tool:
  file_path: "docs/PROJECT_RULES.md"

# If file exists and has content → Proceed to Step 1
# If file does not exist or is empty → Continue to Step 0.2
```

### Step 0.2: Check if Legacy Project

#### Ask the User

Use AskUserQuestion:

```text
┌─────────────────────────────────────────────────────────────────┐
│ 📋 PROJECT_RULES.md not FOUND                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ I need to create docs/PROJECT_RULES.md to understand your       │
│ project's specific conventions and domain.                      │
│                                                                 │
│ First, I need to know: Is this a LEGACY project?                │
│                                                                 │
│ A legacy project is one that was created WITHOUT using the      │
│ PM team workflow (no PRD, TRD, or Feature Map documents).       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Question

"Is this a legacy project (created without PM team workflow)?"

#### Options

(a) Yes, this is a legacy project (b) No, this is a new project following Ring workflow

#### If YES (legacy)

Go to Step 0.2.1 (Legacy Project Analysis)

#### If no (new project)

Go to Step 0.3 (Check for PM Documents)

### Step 0.2.1: Legacy Project Analysis (Technical Only)

#### Overview

For legacy projects, analyze codebase for TECHNICAL information only:

```text
┌─────────────────────────────────────────────────────────────────┐
│ 📋 LEGACY PROJECT ANALYSIS                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Since this is a legacy project, I'll analyze the codebase       │
│ for TECHNICAL information (not business rules).                 │
│                                                                 │
│ Step 1: Automated analysis (ring:codebase-explorer)                  │
│ Step 2: Ask for project-specific tech not in Ring Standards     │
│ Step 3: Generate PROJECT_RULES.md (deduplicated)                │
│                                                                 │
│ Note: Business rules belong in PRD/product docs, not here.      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Step 0.2.1a: Automated Codebase Analysis (MANDATORY)

**⛔ You MUST use the Task tool to dispatch ring:codebase-explorer. This is not implicit.**

#### Dispatch Agent

Dispatch ring:codebase-explorer to analyze the legacy project for TECHNICAL information:

```text
Action: Use Task tool with EXACTLY these parameters:

┌─────────────────────────────────────────────────────────────────────────────────┐
│  ⛔ If Task tool not used → Analysis does not happen → PROJECT_RULES.md INVALID │
└─────────────────────────────────────────────────────────────────────────────────┘
```

```yaml
# Agent 1: Codebase Explorer - Technical Analysis
Task tool:
  subagent_type: "ring:codebase-explorer"
  model: "opus"
  description: "Analyze legacy project for PROJECT_RULES.md"
  prompt: |
    Analyze this LEGACY codebase to extract technical information for PROJECT_RULES.md.
    
    This is an existing project created without PM documentation.
    Your job is to understand what exists in the code.
    
    **Extract:**
    1. **Project Structure:** Directory layout, module organization
    2. **Technical Stack:** Languages, frameworks, databases, external services
    3. **Architecture Patterns:** Clean Architecture, MVC, microservices, etc.
    4. **Existing Features:** Main modules, endpoints, capabilities
    5. **Internal Libraries:** Shared packages, utilities
    6. **Configuration:** Environment variables, config patterns
    7. **Database:** Schema patterns, migrations, ORM usage
    8. **External Integrations:** APIs consumed, message queues
    
    **Output format:**
    ## Technical Analysis (Legacy Project)
    
    ### Project Overview
    [What this project appears to do based on code analysis]
    
    ### Technical Stack
    - Language: [detected]
    - Framework: [detected]
    - Database: [detected]
    - External Services: [detected]
    
    ### Architecture Patterns
    [Detected patterns]
    
    ### Existing Features
    [List of features/modules found]
    
    ### Project Structure
    [Directory layout explanation]
    
    ### Configuration
    [Env vars, config files found]
    
    ### External Integrations
    [APIs, services detected]

```

**Note:** Business logic analysis is not needed for PROJECT_RULES.md. Business rules belong in PRD/product docs, not technical project rules.

#### Verification (MANDATORY)

After agent completes, confirm:
- [ ] `ring:codebase-explorer` returned "## Technical Analysis (Legacy Project)" section
- [ ] Output contains non-empty content for: Tech Stack, External Integrations, Configuration

**If agent failed or returned empty output → Re-dispatch. Cannot proceed without technical analysis.**

#### Step 0.2.1b: Supplementary Questions (Only What Agents Can't Determine)

#### Post-Analysis Questions

After agents complete, ask only what they couldn't determine from code:

```text
┌─────────────────────────────────────────────────────────────────┐
│ ✓ Codebase Analysis Complete                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ I've analyzed your codebase. Now I need a few details that      │
│ only you can provide (not visible in the code).                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Questions to Ask

Use AskUserQuestion for each:

| # | Question | Why Agents Can't Determine This |
|---|----------|--------------------------------|
| 1 | **What do you need help with?** (Current task/feature/fix) | Future intent, not in code |
| 2 | **Any external APIs or services not visible in code?** (Third-party integrations planned) | Planned integrations, not yet in code |
| 3 | **Any specific technology not in Ring Standards?** (Message broker, cache, etc.) | Project-specific tech not in Ring |

**Note:** Business rules belong in PRD/product docs, not in PROJECT_RULES.md.

#### Step 0.2.1c: Generate PROJECT_RULES.md

#### Combine Agent Outputs and User Answers

```yaml
Create tool:
  file_path: "docs/PROJECT_RULES.md"
  content: |
    # Project Rules
    
    > Ring Standards apply automatically. This file documents only what Ring does not cover.
    > For error handling, logging, testing, architecture, lib-commons → See Ring Standards (auto-loaded by agents)
    > Generated from legacy project analysis.
    
    ## What Ring Standards Already Cover (DO not ADD HERE)
    
    The following are defined in Ring Standards and MUST not be duplicated:
    - Error handling patterns (no panic, wrap errors)
    - Logging standards (structured JSON, zerolog/zap)
    - Testing patterns (table-driven tests, mocks)
    - Architecture patterns (Hexagonal, Clean Architecture)
    - Observability (OpenTelemetry, trace correlation)
    - lib-commons usage and patterns
    - API directory structure
    
    ---
    
    ## Tech Stack (Not in Ring Standards)
    
    [From ring:codebase-explorer: Technologies not covered by Ring Standards]
    [e.g., specific message broker, specific cache, DB if not PostgreSQL]
    
    | Technology | Purpose | Notes |
    |------------|---------|-------|
    | [detected] | [purpose] | [notes] |
    
    ## Non-Standard Directory Structure
    
    [From ring:codebase-explorer: Directories that deviate from Ring's standard API structure]
    [e.g., workers/, consumers/, polling/]
    
    | Directory | Purpose | Pattern |
    |-----------|---------|---------|
    | [detected] | [purpose] | [pattern] |
    
    ## External Integrations
    
    [From ring:codebase-explorer: Third-party services specific to this project]
    
    | Service | Purpose | Docs |
    |---------|---------|------|
    | [detected] | [purpose] | [link] |
    
    ## Environment Configuration
    
    [From ring:codebase-explorer: Project-specific env vars not covered by Ring]
    
    | Variable | Purpose | Example |
    |----------|---------|---------|
    | [detected] | [purpose] | [example] |
    
    ## Domain Terminology
    
    [From codebase analysis: Technical names used in this codebase]
    
    | Term | Definition | Used In |
    |------|------------|---------|
    | [detected] | [definition] | [location] |
    
    ---
    
    *Generated: [ISO timestamp]*
    *Source: Legacy project analysis (ring:codebase-explorer)*
    *Ring Standards Version: [version from WebFetch]*
```

#### Present to User

```text
┌─────────────────────────────────────────────────────────────────┐
│ ✓ PROJECT_RULES.md Generated for Legacy Project                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ I analyzed your codebase using:                                 │
│   • ring:codebase-explorer (technical patterns, stack, structure)    │
│                                                                 │
│ Combined with your input on:                                    │
│   • Current development goal                                    │
│   • External integrations                                       │
│   • Project-specific technology                                 │
│                                                                 │
│ Generated: docs/PROJECT_RULES.md                                │
│                                                                 │
│ Note: Ring Standards (error handling, logging, testing, etc.)   │
│ are not duplicated - agents load them automatically via WebFetch│
│                                                                 │
│ Please review the file and make any corrections needed.         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Ask for Approval

Use AskUserQuestion:
- Question: "PROJECT_RULES.md has been generated. Would you like to review it before proceeding?"
- Options: (a) Proceed (b) Open for editing first

#### After Approval

Proceed to Step 1

### Step 0.3: Check for PM Documents (PRD/TRD/Feature Map)

#### Check for PM Documents

For NEW projects (not legacy), ask about PM documents:

```text
┌─────────────────────────────────────────────────────────────────┐
│ 📋 NEW PROJECT - PM DOCUMENTS CHECK                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Since this is a new project following Ring workflow, you        │
│ should have PM documents from the pre-dev workflow.             │
│                                                                 │
│ Do you have any of these PM documents?                          │
│   • PRD (Product Requirements Document)                         │
│   • TRD (Technical Requirements Document)                       │
│   • Feature Map (from ring:pre-dev-feature-map skill)                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Question

"Do you have PRD, TRD, or Feature Map documents for this project?"

#### Options

(a) Yes, I have PM documents (b) No, I don't have these documents

#### If YES - Ask for File Paths

```text
"Please provide the file path(s) to your PM documents:
 - PRD path (or 'skip' if none): 
 - TRD path (or 'skip' if none): 
 - Feature Map path (or 'skip' if none): "
```

#### Example Paths

Typical PM team output structure:

```text
docs/pre-dev/{feature-name}/
├── prd.md              → PRD path: docs/pre-dev/auth-system/prd.md
├── trd.md              → TRD path: docs/pre-dev/auth-system/trd.md
├── feature-map.md      → Feature Map path: docs/pre-dev/auth-system/feature-map.md
├── api-design.md
├── data-model.md
└── tasks.md
```

#### Common Patterns

- `/ring:pre-dev-full` output: `docs/pre-dev/{feature}/prd.md`, `trd.md`, `feature-map.md`
- `/ring:pre-dev-feature` output: `docs/pre-dev/{feature}/prd.md`, `feature-map.md`
- Custom locations: User may have docs in different paths (e.g., `requirements/`, `specs/`)

#### Then

Go to Step 0.3.1 (Generate from PM Documents)

#### If no

HARD BLOCK (Step 0.3.2)

### Step 0.3.1: Generate from PM Documents (PRD/TRD/Feature Map)

#### Read the Provided Documents

```yaml
# Read PRD if provided
Read tool:
  file_path: "[user-provided PRD path]"

# Read TRD if provided  
Read tool:
  file_path: "[user-provided TRD path]"

# Read Feature Map if provided
Read tool:
  file_path: "[user-provided Feature Map path]"
```

#### Extract PROJECT_RULES.md Content from PM Documents

**⛔ DEDUPLICATION RULE:** Extract only what Ring Standards DO NOT cover.

| From PRD | Extract For PROJECT_RULES.md | Note |
|----------|------------------------------|------|
| Domain terms, entities | Domain Terminology | Technical names only |
| External service mentions | External Integrations | Third-party APIs |
| ~~Business rules~~ | ~~N/A~~ | ❌ Stays in PRD, not PROJECT_RULES |
| ~~Architecture~~ | ~~N/A~~ | ❌ Ring Standards covers this |

| From TRD | Extract For PROJECT_RULES.md | Note |
|----------|------------------------------|------|
| Tech stack not in Ring | Tech Stack (Not in Ring) | Only non-standard tech |
| External APIs | External Integrations | Third-party services |
| Non-standard directories | Non-Standard Directory Structure | Workers, consumers, etc. |
| ~~Architecture decisions~~ | ~~N/A~~ | ❌ Ring Standards covers this |
| ~~Database patterns~~ | ~~N/A~~ | ❌ Ring Standards covers this |

| From Feature Map | Extract For PROJECT_RULES.md | Note |
|------------------|------------------------------|------|
| Technology choices not in Ring | Tech Stack (Not in Ring) | Only if not in Ring |
| External dependencies | External Integrations | Third-party services |
| ~~Architecture~~ | ~~N/A~~ | ❌ Ring Standards covers this |

#### Generate PROJECT_RULES.md

```yaml
Create tool:
  file_path: "docs/PROJECT_RULES.md"
  content: |
    # Project Rules
    
    > ⛔ IMPORTANT: Ring Standards are not automatic. Agents MUST WebFetch them before implementation.
    > This file documents only project-specific information not covered by Ring Standards.
    > Generated from PM documents (PRD/TRD/Feature Map).
    >
    > Ring Standards URLs:
    > - Go: https://raw.githubusercontent.com/LerianStudio/ring/main/dev-team/docs/standards/golang.md
    > - TypeScript: https://raw.githubusercontent.com/LerianStudio/ring/main/dev-team/docs/standards/typescript.md
    
    ## What Ring Standards Cover (DO not DUPLICATE HERE)
    
    The following are defined in Ring Standards and MUST not be duplicated in this file:
    - Error handling patterns (no panic, wrap errors)
    - Logging standards (structured JSON via lib-commons)
    - Testing patterns (table-driven tests, mocks)
    - Architecture patterns (Hexagonal, Clean Architecture)
    - Observability (OpenTelemetry via lib-commons)
    - lib-commons / lib-common-js usage and patterns
    - API directory structure (Lerian pattern)
    - Database connections (PostgreSQL, MongoDB, Redis via lib-commons)
    - Bootstrap pattern (config.go, service.go, server.go)
    
    **Agents MUST WebFetch Ring Standards and output Standards Coverage Table.**
    
    ---
    
    ## Tech Stack (Not in Ring Standards)
    
    [From TRD/Feature Map: only technologies not covered by Ring Standards]
    
    | Technology | Purpose | Notes |
    |------------|---------|-------|
    | [detected] | [purpose] | [notes] |
    
    ## Non-Standard Directory Structure
    
    [From TRD: Directories that deviate from Ring's standard API structure]
    
    | Directory | Purpose | Pattern |
    |-----------|---------|---------|
    | [detected] | [purpose] | [pattern] |
    
    ## External Integrations
    
    [From TRD/PRD: Third-party services specific to this project]
    
    | Service | Purpose | Docs |
    |---------|---------|------|
    | [detected] | [purpose] | [link] |
    
    ## Environment Configuration
    
    [From TRD: Project-specific env vars not covered by Ring]
    
    | Variable | Purpose | Example |
    |----------|---------|---------|
    | [detected] | [purpose] | [example] |
    
    ## Domain Terminology
    
    [From PRD: Technical names used in this codebase]
    
    | Term | Definition | Used In |
    |------|------------|---------|
    | [detected] | [definition] | [location] |
    
    ---
    
    *Generated from: [PRD path], [TRD path], [Feature Map path]*
    *Ring Standards Version: [version from WebFetch]*
    *Generated: [ISO timestamp]*
```

#### Check for Missing Information

If any section is empty or incomplete, ask supplementary questions:

| Missing Section | Supplementary Question |
|-----------------|------------------------|
| Tech Stack (Not in Ring) | "Any technology not covered by Ring Standards (message broker, cache, etc.)?" |
| External Integrations | "Any third-party APIs or external services?" |
| Domain Terminology | "What are the main entities/classes in this codebase?" |
| Non-Standard Directories | "Any directories that don't follow standard API structure (workers, consumers)?" |

**Note:** Do not ask about architecture, error handling, logging, testing - Ring Standards covers these.

#### After Generation

Present to user for review, then proceed to Step 1.

### Step 0.3.2: HARD BLOCK - No PM Documents (New Projects Only)

#### When User Has No PM Documents

```text
┌─────────────────────────────────────────────────────────────────┐
│ ⛔ CANNOT PROCEED - PM DOCUMENTS REQUIRED                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Development cannot start without PM documents.                  │
│                                                                 │
│ You MUST create PRD, TRD, and/or Feature Map documents first    │
│ using PM team skills:                                           │
│                                                                 │
│   /ring:pre-dev-full     → For features ≥2 days (9 gates)           │
│   /ring:pre-dev-feature  → For features <2 days (4 gates)           │
│                                                                 │
│ These commands will guide you through creating:                 │
│   • PRD (Product Requirements Document)                         │
│   • TRD (Technical Requirements Document)                       │
│   • Feature Map (technology choices, feature relationships)     │
│                                                                 │
│ After completing pre-dev workflow, run /ring:dev-cycle again.        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Action

STOP EXECUTION. Do not proceed to Step 1.

### Step 0 Anti-Rationalization

| Rationalization | Why It's WRONG | Required Action |
|-----------------|----------------|-----------------|
| "Skip PM docs, I'll add them later" | Later = never. No PM docs = no project context = agents guessing. | **Run /ring:pre-dev-full or /ring:pre-dev-feature NOW** |
| "Project is simple, doesn't need PM docs" | Simple projects still need domain context defined upfront. | **Create PM documents first** |
| "I know what I want to build" | Your knowledge ≠ documented knowledge agents can use. | **Document in PRD/TRD/Feature Map** |
| "PM workflow takes too long" | PM workflow takes 30-60 min. Rework from unclear requirements takes days. | **Invest time upfront** |
| "Just let me start coding" | Coding without requirements = building the wrong thing. | **Requirements first, code second** |
| "It's legacy but I don't want to answer questions" | Legacy analysis takes ~5 min. Without it, agents have zero context. | **Answer the 4 questions** |
| "Legacy project is too complex to explain" | Start with high-level answers. PROJECT_RULES.md can be refined later. | **Provide what you know NOW** |

### Pressure Resistance

| User Says | Your Response |
|-----------|---------------|
| "Just skip this, I'll create PM docs later" | "PM documents are REQUIRED for new projects. Without them, agents cannot understand your project's domain context or technical requirements. Run `/ring:pre-dev-full` or `/ring:pre-dev-feature` first." |
| "I don't need formal documents" | "PM documents are the source of truth for PROJECT_RULES.md. Development cannot start without documented requirements." |
| "This is just a quick prototype" | "Even prototypes need clear requirements. `/ring:pre-dev-feature` takes ~30 minutes and prevents hours of rework." |
| "I already explained what I want verbally" | "Verbal explanations cannot be used by agents. Requirements MUST be documented in PRD/TRD/Feature Map files." |
| "It's a legacy project but skip the questions" | "The legacy analysis (ring:codebase-explorer + 3 questions) is the only way I can understand your project. It takes ~5 minutes and enables me to help you effectively." |
| "I'll fill in PROJECT_RULES.md myself" | "That works! Create `docs/PROJECT_RULES.md` with: Tech Stack (not in Ring), External Integrations, Domain Terminology. Do not duplicate Ring Standards content. Then run `/ring:dev-cycle` again." |

---

## Step 1: Initialize or Resume

### Prompt-Only Mode (no task file)

**Input:** `--prompt "..."` without a task file path

When `--prompt` is provided without a tasks file, ring:dev-cycle generates tasks internally:

1. **Detect prompt-only mode:** No task file argument AND `--prompt` provided
2. **Analyze prompt:** Extract intent, scope, and requirements from the prompt
3. **Explore codebase:** Dispatch `ring:codebase-explorer` to understand project structure
4. **Generate tasks:** Create task structure internally based on prompt + codebase analysis

```yaml
Task tool:
  subagent_type: "ring:codebase-explorer"
  model: "opus"
  prompt: |
    Analyze this codebase to support the following implementation request:
    
    **User Request:** {prompt}
    
    Provide:
    1. Relevant files and patterns for this request
    2. Suggested task breakdown (T-001, T-002, etc.)
    3. Acceptance criteria for each task
    4. Files that will need modification
    
    Output as structured task list compatible with ring:dev-cycle.
```

5. **Present generated tasks:** Show user the auto-generated task breakdown
6. **Confirm with user:** "I generated X tasks from your prompt. Proceed?"
7. **Set state:**
   - `state_path = "docs/ring:dev-cycle/current-cycle.json"`
   - `cycle_type = "prompt"`
   - `source_prompt = "[user's prompt]"`
   - Generate `tasks` array from ring:codebase-explorer output
8. **Continue to execution mode selection** (Step 1 substeps 7-9)

**Anti-Rationalization for Prompt-Only Mode:**

| Rationalization | Why It's WRONG | Required Action |
|-----------------|----------------|-----------------|
| "Skip codebase exploration, I understand the prompt" | Prompt understanding ≠ codebase understanding. Explorer provides context. | **Always run ring:codebase-explorer** |
| "Generate minimal tasks to go faster" | Minimal tasks = missed requirements. Comprehensive breakdown prevents rework. | **Generate complete task breakdown** |
| "User knows what they want, skip confirmation" | User intent ≠ generated tasks. Confirmation prevents wrong implementation. | **Always confirm generated tasks** |

---

### New Cycle (with task file path)

**Input:** `path/to/tasks.md` or `path/to/pre-dev/{feature}/` with optional `--prompt "..."`

1. **Detect input:** File → Load directly | Directory → Load tasks.md + discover subtasks/
2. **Build order:** Read tasks, check for subtasks (ST-XXX-01, 02...) or TDD autonomous mode
3. **Determine state path:**
   - if source_file contains `docs/refactor/` → `state_path = "docs/ring:dev-refactor/current-cycle.json"`, `cycle_type = "refactor"`
   - else → `state_path = "docs/ring:dev-cycle/current-cycle.json"`, `cycle_type = "feature"`
4. **Capture and validate custom prompt:** If `--prompt "..."` provided:
   - **Sanitize input:** Trim whitespace, strip control characters (except newlines)
   - **Store validated value:** Set `custom_prompt` field (empty string if not provided)
   - **Note:** Directives attempting to skip gates are logged as warnings and ignored at execution time
5. **Initialize state:** Generate cycle_id, create state file at `{state_path}`, set indices to 0
6. **Display plan:** "Loaded X tasks with Y subtasks"
7. **ASK EXECUTION MODE (MANDATORY - AskUserQuestion):**
   - Options: (a) Manual per subtask (b) Manual per task (c) Automatic
   - **Do not skip:** User hints ≠ mode selection. Only explicit a/b/c is valid.
8. **ASK COMMIT TIMING (MANDATORY - AskUserQuestion):**
   - Options: (a) Per subtask (b) Per task (c) At the end
   - Store in `commit_timing` field in state
9. **Start:** Display mode + commit timing, proceed to Gate 0

### Resume Cycle (--resume flag)

1. **Find existing state file:**
   - Check `docs/ring:dev-cycle/current-cycle.json` first
   - If not found, check `docs/ring:dev-refactor/current-cycle.json`
   - If neither exists → Error: "No cycle to resume"
2. Load found state file, validate (state_path is stored in the state object)
3. Display: cycle started, tasks completed/total, current task/subtask/gate, paused reason
4. **Handle paused states:**

| Status | Action |
|--------|--------|
| `paused_for_approval` | Re-present Step 7.1 checkpoint |
| `paused_for_testing` | Ask if testing complete → continue or keep paused |
| `paused_for_task_approval` | Re-present Step 7.2 checkpoint |
| `paused_for_integration_testing` | Ask if integration testing complete |
| `paused` (generic) | Ask user to confirm resume |
| `in_progress` | Resume from current gate |

## Input Validation

Task files are generated by `/pre-dev-*` or `/ring:dev-refactor`, which handle content validation. The ring:dev-cycle performs basic format checks:

### Format Checks

| Check | Validation | Action |
|-------|------------|--------|
| File exists | Task file path is readable | Error: abort |
| Task headers | At least one `## Task:` found | Error: abort |
| Task ID format | `## Task: {ID} - {Title}` | Warning: use line number as ID |
| Acceptance criteria | At least one `- [ ]` per task | Warning: task may fail validation gate |

## Step 2: Gate 0 - Implementation (Per Execution Unit)

**REQUIRED SUB-SKILL:** Use ring:dev-implementation

**Execution Unit:** Task (if no subtasks) or Subtask (if task has subtasks)

### ⛔ MANDATORY: Agent Dispatch Required

See [shared-patterns/shared-orchestrator-principle.md](../shared-patterns/shared-orchestrator-principle.md) for full details.

**Gate 0 has TWO explicit sub-phases with a HARD GATE between them:**

```text
┌─────────────────────────────────────────────────────────────────┐
│  GATE 0.1: TDD-RED                                              │
│  ─────────────────                                              │
│  Write failing test → Run test → Capture FAILURE output         │
│                                                                 │
│  ═══════════════════ HARD GATE ═══════════════════════════════  │
│  CANNOT proceed to 0.2 until failure output is captured         │
│  ════════════════════════════════════════════════════════════   │
│                                                                 │
│  GATE 0.2: TDD-GREEN                                            │
│  ──────────────────                                             │
│  Implement minimal code → Run test → Verify PASS                │
└─────────────────────────────────────────────────────────────────┘
```

### Step 2.1: Gate 0.1 - TDD-RED (Write Failing Test)

1. Record gate start timestamp
2. Set `gate_progress.implementation.tdd_red.status = "in_progress"`

3. Determine appropriate agent based on content:
   - Go files/go.mod → ring:backend-engineer-golang
   - TypeScript backend → ring:backend-engineer-typescript
   - React/Frontend → ring:frontend-engineer-typescript
   - Infrastructure → ring:devops-engineer

4. Dispatch to selected agent for TDD-RED only:

   See [shared-patterns/template-tdd-prompts.md](../shared-patterns/template-tdd-prompts.md) for the TDD-RED prompt template.

   Include: unit_id, title, requirements, acceptance_criteria in the prompt.

5. Receive TDD-RED report from agent
6. **VERIFY FAILURE OUTPUT EXISTS (HARD GATE):** See shared-patterns/template-tdd-prompts.md for verification rules.

7. Update state:
   ```json
   gate_progress.implementation.tdd_red = {
     "status": "completed",
     "test_file": "[path from agent]",
     "failure_output": "[actual failure output from agent]",
     "completed_at": "[ISO timestamp]"
   }
   ```

8. **Display to user:**
   ```text
   ┌─────────────────────────────────────────────────┐
   │ ✓ TDD-RED COMPLETE                              │
   ├─────────────────────────────────────────────────┤
   │ Test: [test_file]:[test_function]               │
   │ Failure: [first line of failure output]         │
   │                                                 │
   │ Proceeding to TDD-GREEN...                      │
   └─────────────────────────────────────────────────┘
   ```

9. Proceed to Gate 0.2

### Step 2.2: Gate 0.2 - TDD-GREEN (Implementation)

**PREREQUISITE:** `gate_progress.implementation.tdd_red.status == "completed"`

1. Set `gate_progress.implementation.tdd_green.status = "in_progress"`

2. Dispatch to same agent for TDD-GREEN:

   See [shared-patterns/template-tdd-prompts.md](../shared-patterns/template-tdd-prompts.md) for the TDD-GREEN prompt template (includes observability requirements).

   Include: unit_id, title, tdd_red.test_file, tdd_red.failure_output in the prompt.

3. Receive TDD-GREEN report from agent
4. **VERIFY PASS OUTPUT EXISTS (HARD GATE):** See shared-patterns/template-tdd-prompts.md for verification rules.

5. Update state:
   ```json
   gate_progress.implementation.tdd_green = {
     "status": "completed",
     "implementation_file": "[path from agent]",
     "test_pass_output": "[actual pass output from agent]",
     "completed_at": "[ISO timestamp]"
   }
   gate_progress.implementation.status = "completed"
   artifacts.implementation = {files_changed, commit_sha}
   agent_outputs.implementation = {
     agent: "[selected_agent]",
     output: "[full agent output for feedback analysis]",
     timestamp: "[ISO timestamp]",
     duration_ms: [execution time],
     iterations: [standards_compliance_iterations from Step 2.3],
     standards_compliance: {
       total_sections: [N from final verification],
       compliant: [N sections with ✅],
       not_applicable: [N sections with N/A],
       non_compliant: 0,
       gaps: []  // Empty when gate passes; populated during iterations
     }
   }
   ```
   
   **If iterations > 1, populate `gaps[]` with issues found in previous iterations:**
   ```json
   gaps: [
     {
       "section": "[section name from ❌ row]",
       "status": "❌",
       "reason": "[why it failed]",
       "file": "[file path if available]",
       "line": [line number if available],
       "evidence": "[code snippet or description]",
       "fixed_in_iteration": [iteration number when fixed]
     }
   ]
   ```

6. **Display to user:**
   ```text
   ┌─────────────────────────────────────────────────┐
   │ ✓ GATE 0 COMPLETE (TDD-RED → TDD-GREEN)        │
   ├─────────────────────────────────────────────────┤
   │ RED:   [test_file] - FAIL captured ✓           │
   │ GREEN: [impl_file] - PASS verified ✓           │
   │                                                 │
   │ Proceeding to Gate 1 (DevOps)...               │
   └─────────────────────────────────────────────────┘
   ```

7. **Proceed to Step 2.3 (Standards Compliance Verification)**

### Step 2.3: Standards Compliance Verification (HARD GATE)

**PREREQUISITE:** `gate_progress.implementation.tdd_green.status == "completed"`

**Purpose:** Verify implementation follows all standards defined in agent's standards file.

See [shared-patterns/template-tdd-prompts.md](../shared-patterns/template-tdd-prompts.md) → "Orchestrator Enforcement" section for full verification process.

**Process:**

### Step 2.3.1: Initialize Iteration Counter

```text
Set standards_compliance_iterations = 0
Set MAX_ITERATIONS = 3
```

### Step 2.3.2: Verification Loop

```text
LOOP while standards_compliance_iterations < MAX_ITERATIONS:
  
  1. INCREMENT counter FIRST (before any verification):
     standards_compliance_iterations += 1
  
  2. PARSE agent output for "## Standards Coverage Table":
     if not FOUND:
       → Output INCOMPLETE
       → Log: "Iteration [N]: Standards Coverage Table missing"
       → Re-dispatch agent (see Step 2.3.3)
       → CONTINUE loop
  
  3. PARSE "all STANDARDS MET:" value:
     if not FOUND:
       → Output INCOMPLETE
       → Log: "Iteration [N]: Compliance Summary missing"
       → Re-dispatch agent (see Step 2.3.3)
       → CONTINUE loop
  
  4. COUNT sections from Standards Coverage Table:
     total_sections = count all rows
     compliant = count rows with ✅
     not_applicable = count rows with N/A
     non_compliant = count rows with ❌
  
  5. VERIFY compliance:
     if "all STANDARDS MET: ✅ YES" and non_compliant == 0:
       → Gate 0 PASSED
       → BREAK loop (proceed to Step 2.3.4)
     
     if "all STANDARDS MET: ❌ no" or non_compliant > 0:
       → Gate 0 BLOCKED
       → Extract ❌ sections
       → Log: "Iteration [N]: [non_compliant] sections non-compliant"
       → Re-dispatch agent (see Step 2.3.3)
       → CONTINUE loop

END LOOP

if standards_compliance_iterations >= MAX_ITERATIONS and non_compliant > 0:
  → HARD BLOCK
  → Update state with failure info
  → Report to user: "Standards compliance failed after 3 attempts"
  → STOP execution
```

### Step 2.3.3: Re-dispatch Agent for Compliance Fix

```yaml
Task tool:
  subagent_type: "[same agent from TDD-GREEN]"
  model: "opus"
  description: "Fix missing Ring Standards for [unit_id] (attempt [N]/3)"
  prompt: |
    ⛔ STANDARDS not MET - Fix Required (Attempt [standards_compliance_iterations] of 3)
    
    Your Standards Coverage Table shows these sections as ❌:
    [list ❌ sections extracted from table]
    
    WebFetch your standards file:
    [URL for agent's standards - golang.md, typescript.md, etc.]
    
    Implement all missing sections.
    Return updated Standards Coverage Table with all ✅ or N/A.
    
    Previous attempt summary:
    - Total sections: [total_sections]
    - Compliant: [compliant]
    - Not applicable: [not_applicable]
    - Non-compliant: [non_compliant]
```

### Step 2.3.4: Update State with Compliance Metrics

```json
gate_progress.implementation = {
  "status": "completed",
  "tdd_red": {...},
  "tdd_green": {...},
  "standards_verified": true,
  "standards_compliance_iterations": [final count - e.g., 1, 2, or 3],
  "standards_coverage": {
    "total_sections": [N - from final successful verification],
    "compliant": [N - sections with ✅],
    "not_applicable": [N - sections with N/A],
    "non_compliant": 0
  }
}
```

**Note:** `non_compliant` MUST be 0 when gate passes. If non-zero after 3 iterations, gate is BLOCKED.

5. **Display to user:**
   ```text
   ┌─────────────────────────────────────────────────┐
   │ ✓ GATE 0 COMPLETE                              │
   ├─────────────────────────────────────────────────┤
   │ TDD-RED:   [test_file] - FAIL captured ✓       │
   │ TDD-GREEN: [impl_file] - PASS verified ✓       │
   │ STANDARDS: [N]/[N] sections compliant ✓        │
   │ ITERATIONS: [standards_compliance_iterations]   │
   │                                                 │
   │ Proceeding to Gate 1 (DevOps)...               │
   └─────────────────────────────────────────────────┘
   ```

6. **⛔ SAVE STATE TO FILE (MANDATORY):**
   ```yaml
   Write tool:
     file_path: [state.state_path]  # "docs/ring:dev-cycle/current-cycle.json" or "docs/ring:dev-refactor/current-cycle.json"
     content: [full updated state JSON]
   ```
   See "State Persistence Rule" section. State MUST be written to file after Gate 0.

7. **Proceed to Gate 1**

### Standards Compliance Anti-Rationalization

| Rationalization | Why It's WRONG | Required Action |
|-----------------|----------------|-----------------|
| "Agent said implementation is complete" | Agent completion ≠ Standards compliance. Verify table. | **Parse and verify Standards Coverage Table** |
| "Table wasn't in agent output" | Missing table = Incomplete output = Re-dispatch | **Re-dispatch agent to output table** |
| "Only 1-2 sections are ❌" | any ❌ = BLOCKED. Count is irrelevant. | **Re-dispatch to fix all ❌ sections** |
| "lib-commons is the main thing" | all sections are equally required. No prioritization. | **Verify all sections from standards-coverage-table.md** |
| "Agent knows the standards" | Knowledge ≠ implementation. Evidence required. | **Check file:line evidence in table** |
| "Standards verification is slow" | Verification prevents rework. 30 seconds vs hours. | **Always verify before proceeding** |

### TDD Sub-Phase Anti-Rationalization

| Rationalization | Why It's WRONG | Required Action |
|-----------------|----------------|-----------------|
| "Test passes on first run, skip RED" | Passing test ≠ TDD. Test MUST fail first. | **Delete test, rewrite to fail first** |
| "I'll capture failure output later" | Later = never. Failure output is the gate. | **Capture NOW or cannot proceed** |
| "Failure output is in the logs somewhere" | "Somewhere" ≠ captured. Must be in state. | **Extract and store in tdd_red.failure_output** |
| "GREEN passed, RED doesn't matter now" | RED proves test validity. Skip = invalid test. | **Re-run RED phase, capture failure** |
| "Agent already did TDD internally" | Internal ≠ verified. State must show evidence. | **Agent must output failure explicitly** |

## Step 3: Gate 1 - DevOps (Per Execution Unit)

**REQUIRED SUB-SKILL:** Use ring:dev-devops

### ⛔ HARD GATE: Required Artifacts MUST Be Created

**Gate 1 is a BLOCKING gate.** DevOps agent MUST create all required artifacts. If any artifact is missing:
- You CANNOT proceed to Gate 2
- You MUST re-dispatch to ring:devops-engineer to create missing artifacts
- You MUST verify all artifacts exist before proceeding

### Required Artifacts

**See [shared-patterns/standards-coverage-table.md](../skills/shared-patterns/standards-coverage-table.md) → "ring:devops-engineer → devops.md" for all required sections.**

**Key artifacts from devops.md:**
- Containers (Dockerfile + Docker Compose)
- Makefile Standards (all required commands)
- Infrastructure as Code (if applicable)
- Helm charts (if K8s deployment)

### Step 3.1: Prepare Input for ring:dev-devops Skill

```text
Gather from previous gates:

devops_input = {
  // REQUIRED - from current execution unit
  unit_id: state.current_unit.id,
  
  // REQUIRED - from Gate 0 context
  language: state.current_unit.language,  // "go" | "typescript" | "python"
  service_type: state.current_unit.service_type,  // "api" | "worker" | "batch" | "cli"
  implementation_files: agent_outputs.implementation.files_changed,  // list of files from Gate 0
  
  // OPTIONAL - additional context
  gate0_handoff: agent_outputs.implementation,  // full Gate 0 output
  new_dependencies: state.current_unit.new_deps || [],  // new deps added in Gate 0
  new_env_vars: state.current_unit.env_vars || [],  // env vars needed
  new_services: state.current_unit.services || [],  // postgres, redis, etc.
  existing_dockerfile: [check if Dockerfile exists],
  existing_compose: [check if docker-compose.yml exists]
}
```

### Step 3.2: Invoke ring:dev-devops Skill

```text
1. Record gate start timestamp

2. Invoke ring:dev-devops skill with structured input:

   Skill("ring:dev-devops") with input:
     unit_id: devops_input.unit_id
     language: devops_input.language
     service_type: devops_input.service_type
     implementation_files: devops_input.implementation_files
     gate0_handoff: devops_input.gate0_handoff
     new_dependencies: devops_input.new_dependencies
     new_env_vars: devops_input.new_env_vars
     new_services: devops_input.new_services
     existing_dockerfile: devops_input.existing_dockerfile
     existing_compose: devops_input.existing_compose

   The skill handles:
   - Dispatching ring:devops-engineer agent
   - Dockerfile creation/update
   - docker-compose.yml configuration
   - .env.example documentation
   - Verification commands execution
   - Fix iteration loop (max 3 attempts)

3. Parse skill output for results:
   
   Expected output sections:
   - "## DevOps Summary" → status, iterations
   - "## Files Changed" → Dockerfile, docker-compose, .env.example actions
   - "## Verification Results" → build, startup, health checks
   - "## Handoff to Next Gate" → ready_for_sre: YES/no
   
   if skill output contains "Status: PASS" and "Ready for Gate 2: YES":
     → Gate 1 PASSED. Proceed to Step 3.3.
   
   if skill output contains "Status: FAIL" or "Ready for Gate 2: no":
     → Gate 1 BLOCKED.
     → Skill already dispatched fixes to ring:devops-engineer
     → Skill already re-ran verification
     → If "ESCALATION" in output: STOP and report to user

4. **⛔ SAVE STATE TO FILE (MANDATORY):**
   Write tool → [state.state_path]
```

### Step 3.3: Gate 1 Complete

```text
5. When ring:dev-devops skill returns PASS:
   
   Parse from skill output:
   - status: extract from "## DevOps Summary"
   - dockerfile_action: extract from "## Files Changed" table
   - compose_action: extract from "## Files Changed" table
   - verification_passed: extract from "## Verification Results"
   
   - agent_outputs.devops = {
       skill: "ring:dev-devops",
       output: "[full skill output]",
       artifacts_created: ["Dockerfile", "docker-compose.yml", ".env.example"],
       verification_passed: true,
       timestamp: "[ISO timestamp]",
       duration_ms: [execution time]
     }

6. Update state:
   - gate_progress.devops.status = "completed"
   - gate_progress.devops.artifacts = [list from skill output]

7. Proceed to Gate 2
```

### Gate 1 Anti-Rationalization Table

| Rationalization | Why It's WRONG | Required Action |
|-----------------|----------------|-----------------|
| "Dockerfile exists, skip other artifacts" | all artifacts required. 1/4 ≠ complete. | **Create all artifacts** |
| "docker-compose not needed locally" | docker-compose is MANDATORY for local dev. | **Create docker-compose.yml** |
| "Makefile is optional" | Makefile is MANDATORY for standardized commands. | **Create Makefile** |
| ".env.example can be added later" | .env.example documents required config NOW. | **Create .env.example** |
| "Small service doesn't need all this" | Size is irrelevant. Standards apply uniformly. | **Create all artifacts** |

## Step 4: Gate 2 - SRE (Per Execution Unit)

**REQUIRED SUB-SKILL:** Use `ring:dev-ring:sre`

### Step 4.1: Prepare Input for ring:dev-ring:sre Skill

```text
Gather from previous gates:

sre_input = {
  // REQUIRED - from current execution unit
  unit_id: state.current_unit.id,
  
  // REQUIRED - from Gate 0 context
  language: state.current_unit.language,  // "go" | "typescript" | "python"
  service_type: state.current_unit.service_type,  // "api" | "worker" | "batch" | "cli"
  implementation_agent: agent_outputs.implementation.agent,  // e.g., "ring:backend-engineer-golang"
  implementation_files: agent_outputs.implementation.files_changed,  // list of files from Gate 0
  
  // OPTIONAL - additional context
  external_dependencies: state.current_unit.external_deps || [],  // HTTP clients, gRPC, queues
  gate0_handoff: agent_outputs.implementation,  // full Gate 0 output
  gate1_handoff: agent_outputs.devops  // full Gate 1 output
}
```

### Step 4.2: Invoke ring:dev-ring:sre Skill

```text
1. Record gate start timestamp

2. Invoke ring:dev-ring:sre skill with structured input:

   Skill("ring:dev-ring:sre") with input:
     unit_id: sre_input.unit_id
     language: sre_input.language
     service_type: sre_input.service_type
     implementation_agent: sre_input.implementation_agent
     implementation_files: sre_input.implementation_files
     external_dependencies: sre_input.external_dependencies
     gate0_handoff: sre_input.gate0_handoff
     gate1_handoff: sre_input.gate1_handoff

   The skill handles:
   - Dispatching SRE agent for validation
   - Structured logging validation
   - Distributed tracing validation
   - Code instrumentation coverage (90%+ required)
   - Context propagation validation (InjectHTTPContext/InjectGRPCContext)
   - Dispatching fixes to implementation agent if needed
   - Re-validation loop (max 3 iterations)

3. Parse skill output for validation results:
   
   Expected output sections:
   - "## Validation Result" → status, iterations, coverage
   - "## Instrumentation Coverage" → table with per-layer coverage
   - "## Issues Found" → list or "None"
   - "## Handoff to Next Gate" → ready_for_testing: YES/no
   
   if skill output contains "Status: PASS" and "Ready for Gate 3: YES":
     → Gate 2 PASSED. Proceed to Step 4.3.
   
   if skill output contains "Status: FAIL" or "Ready for Gate 3: no":
     → Gate 2 BLOCKED. 
     → Skill already dispatched fixes to implementation agent
     → Skill already re-ran validation
     → If "ESCALATION" in output: STOP and report to user

4. **⛔ SAVE STATE TO FILE (MANDATORY):**
   Write tool → [state.state_path]
```

### Step 4.3: Gate 2 Complete

```text
5. When ring:dev-ring:sre skill returns PASS:
   
   Parse from skill output:
   - status: extract from "## Validation Result"
   - instrumentation_coverage: extract percentage from coverage table
   - iterations: extract from "Iterations:" line
   
   - agent_outputs.ring:sre = {
       skill: "ring:dev-ring:sre",
       output: "[full skill output]",
       validation_result: "PASS",
       instrumentation_coverage: "[X%]",
       iterations: [count],
       timestamp: "[ISO timestamp]",
       duration_ms: [execution time]
     }

6. Update state:
   - gate_progress.ring:sre.status = "completed"
   - gate_progress.ring:sre.observability_validated = true
   - gate_progress.ring:sre.instrumentation_coverage = "[X%]"

7. Proceed to Gate 3
```

### Gate 2 Anti-Rationalization Table

See [ring:dev-ring:sre/SKILL.md](../dev-ring:sre/SKILL.md) for complete anti-rationalization tables covering:
- Observability deferral rationalizations
- Instrumentation coverage rationalizations
- Context propagation rationalizations

### Gate 2 Pressure Resistance

| User Says | Your Response |
|-----------|---------------|
| "Skip SRE validation, we'll add observability later" | "Observability is MANDATORY for Gate 2. Invoking ring:dev-ring:sre skill now." |
| "SRE found issues but let's continue" | "Gate 2 is a HARD GATE. ring:dev-ring:sre skill handles fix dispatch and re-validation." |
| "Instrumentation coverage is low but code works" | "90%+ instrumentation coverage is REQUIRED. ring:dev-ring:sre skill will not pass until met." |

## Step 5: Gate 3 - Testing (Per Execution Unit)

**REQUIRED SUB-SKILL:** Use `ring:dev-testing`

### Step 5.1: Prepare Input for ring:dev-testing Skill

```text
Gather from previous gates:

testing_input = {
  // REQUIRED - from current execution unit
  unit_id: state.current_unit.id,
  acceptance_criteria: state.current_unit.acceptance_criteria,  // list of ACs to test
  implementation_files: agent_outputs.implementation.files_changed,
  language: state.current_unit.language,  // "go" | "typescript" | "python"
  
  // OPTIONAL - additional context
  coverage_threshold: 85,  // Ring minimum, PROJECT_RULES.md can raise
  gate0_handoff: agent_outputs.implementation,  // full Gate 0 output
  existing_tests: [check for existing test files]
}
```

### Step 5.2: Invoke ring:dev-testing Skill

```text
1. Record gate start timestamp

2. Invoke ring:dev-testing skill with structured input:

   Skill("ring:dev-testing") with input:
     unit_id: testing_input.unit_id
     acceptance_criteria: testing_input.acceptance_criteria
     implementation_files: testing_input.implementation_files
     language: testing_input.language
     coverage_threshold: testing_input.coverage_threshold
     gate0_handoff: testing_input.gate0_handoff
     existing_tests: testing_input.existing_tests

   The skill handles:
   - Dispatching ring:qa-analyst agent
   - Test creation following TDD methodology
   - Coverage measurement and validation (85%+ required)
   - Traceability matrix (AC → Test mapping)
   - Dispatching fixes to implementation agent if coverage < threshold
   - Re-validation loop (max 3 iterations)

3. Parse skill output for results:
   
   Expected output sections:
   - "## Testing Summary" → status, iterations
   - "## Coverage Report" → threshold vs actual
   - "## Traceability Matrix" → AC-to-test mapping
   - "## Handoff to Next Gate" → ready_for_review: YES/no
   
   if skill output contains "Status: PASS" and "Ready for Gate 4: YES":
     → Gate 3 PASSED. Proceed to Step 5.3.
   
   if skill output contains "Status: FAIL" or "Ready for Gate 4: no":
     → Gate 3 BLOCKED.
     → Skill already dispatched fixes to implementation agent
     → Skill already re-ran coverage check
     → If "ESCALATION" in output: STOP and report to user

4. **⛔ SAVE STATE TO FILE (MANDATORY):**
   Write tool → [state.state_path]
```

### Step 5.3: Gate 3 Complete

```text
5. When ring:dev-testing skill returns PASS:
   
   Parse from skill output:
   - coverage_actual: extract percentage from "## Coverage Report"
   - coverage_threshold: extract from "## Coverage Report"
   - criteria_covered: extract from "## Traceability Matrix"
   - iterations: extract from "Iterations:" line
   
   - agent_outputs.testing = {
       skill: "ring:dev-testing",
       output: "[full skill output]",
       verdict: "PASS",
       coverage_actual: [X%],
       coverage_threshold: [85%],
       criteria_covered: "[X/Y]",
       iterations: [count],
       timestamp: "[ISO timestamp]",
       duration_ms: [execution time],
       failures: [],  // Empty when PASS; see schema below for FAIL
       uncovered_criteria: []  // Empty when all ACs covered
     }
   
   **If iterations > 1 (tests failed before passing), populate `failures[]`:**
   ```json
   failures: [
     {
       "test_name": "TestUserCreate_InvalidEmail",
       "test_file": "internal/handler/user_test.go",
       "error_type": "assertion|panic|timeout|compilation",
       "expected": "[expected value]",
       "actual": "[actual value]",
       "message": "[error message from test output]",
       "stack_trace": "[relevant stack trace]",
       "fixed_in_iteration": [iteration number when fixed]
     }
   ]
   ```
   
   **If coverage < 100% of acceptance criteria, populate `uncovered_criteria[]`:**
   ```json
   uncovered_criteria: [
     {
       "criterion_id": "AC-001",
       "description": "User should receive email confirmation",
       "reason": "No test found for email sending functionality"
     }
   ]
   ```

6. Update state:
   - gate_progress.testing.status = "completed"
   - gate_progress.testing.coverage = [coverage_actual]

7. Proceed to Gate 4
```

### Gate 3 Thresholds

- **Minimum:** 85% (Ring standard - CANNOT be lowered)
- **Project-specific:** Can be higher if defined in `docs/PROJECT_RULES.md`
- **Validation:** Threshold < 85% → Use 85%

### Gate 3 Pressure Resistance

| User Says | Your Response |
|-----------|---------------|
| "84% is close enough" | "85% is Ring minimum. ring:dev-testing skill enforces this." |
| "Skip testing, deadline" | "Testing is MANDATORY. ring:dev-testing skill handles iterations." |
| "Manual testing covers it" | "Gate 3 requires executable unit tests. Invoking ring:dev-testing now." |

## Step 6: Gate 4 - Review (Per Execution Unit)

**REQUIRED SUB-SKILL:** Use `ring:requesting-code-review`

### Step 6.1: Prepare Input for ring:requesting-code-review Skill

```text
Gather from previous gates:

review_input = {
  // REQUIRED - from current execution unit
  unit_id: state.current_unit.id,
  base_sha: state.current_unit.base_sha,  // SHA before implementation
  head_sha: [current HEAD],  // SHA after all gates
  implementation_summary: state.current_unit.title + requirements,
  requirements: state.current_unit.acceptance_criteria,
  
  // OPTIONAL - additional context
  implementation_files: agent_outputs.implementation.files_changed,
  gate0_handoff: agent_outputs.implementation  // full Gate 0 output
}
```

### Step 6.2: Invoke ring:requesting-code-review Skill

```text
1. Record gate start timestamp

2. Invoke ring:requesting-code-review skill with structured input:

   Skill("ring:requesting-code-review") with input:
     unit_id: review_input.unit_id
     base_sha: review_input.base_sha
     head_sha: review_input.head_sha
     implementation_summary: review_input.implementation_summary
     requirements: review_input.requirements
     implementation_files: review_input.implementation_files
     gate0_handoff: review_input.gate0_handoff

   The skill handles:
   - Dispatching all 3 reviewers in PARALLEL (single message with 3 Task calls)
   - Aggregating issues by severity (CRITICAL/HIGH/MEDIUM/LOW/COSMETIC)
   - Dispatching fixes to implementation agent for blocking issues
   - Re-running all 3 reviewers after fixes
   - Iteration tracking (max 3 attempts)
   - Adding TODO/FIXME comments for non-blocking issues

3. Parse skill output for results:
   
   Expected output sections:
   - "## Review Summary" → status, iterations
   - "## Issues by Severity" → counts per severity level
   - "## Reviewer Verdicts" → ring:code-reviewer, ring:business-logic-reviewer, ring:security-reviewer
   - "## Handoff to Next Gate" → ready_for_validation: YES/no
   
   if skill output contains "Status: PASS" and "Ready for Gate 5: YES":
     → Gate 4 PASSED. Proceed to Step 6.3.
   
   if skill output contains "Status: FAIL" or "Ready for Gate 5: no":
     → Gate 4 BLOCKED.
     → Skill already dispatched fixes to implementation agent
     → Skill already re-ran all 3 reviewers
     → If "ESCALATION" in output: STOP and report to user

4. **⛔ SAVE STATE TO FILE (MANDATORY):**
   Write tool → [state.state_path]
```

### Step 6.3: Gate 4 Complete

```text
5. When ring:requesting-code-review skill returns PASS:
   
   Parse from skill output:
   - reviewers_passed: extract from "## Reviewer Verdicts" (should be "3/3")
   - issues_critical: extract count from "## Issues by Severity"
   - issues_high: extract count from "## Issues by Severity"
   - issues_medium: extract count from "## Issues by Severity"
   - iterations: extract from "Iterations:" line
   
   - agent_outputs.review = {
       skill: "ring:requesting-code-review",
       output: "[full skill output]",
       iterations: [count],
       timestamp: "[ISO timestamp]",
       duration_ms: [execution time],
       reviewers_passed: "3/3",
       code_reviewer: {
         verdict: "PASS",
         issues_count: N,
         issues: []  // Structured issues - see schema below
       },
       business_logic_reviewer: {
         verdict: "PASS",
         issues_count: N,
         issues: []
       },
       security_reviewer: {
         verdict: "PASS",
         issues_count: N,
         issues: []
       }
     }
   
   **Populate `issues[]` for each reviewer with all issues found (even if fixed):**
   ```json
   issues: [
     {
       "severity": "CRITICAL|HIGH|MEDIUM|LOW|COSMETIC",
       "category": "error-handling|security|performance|maintainability|business-logic|...",
       "description": "[detailed description of the issue]",
       "file": "internal/handler/user.go",
       "line": 45,
       "code_snippet": "return err",
       "suggestion": "Use fmt.Errorf(\"failed to create user: %w\", err)",
       "fixed": true|false,
       "fixed_in_iteration": [iteration number when fixed, null if not fixed]
     }
   ]
   ```
   
   **Issue tracking rules:**
   - all issues found across all iterations MUST be recorded
   - `fixed: true` + `fixed_in_iteration: N` for issues resolved during review
   - `fixed: false` + `fixed_in_iteration: null` for LOW/COSMETIC (TODO/FIXME added)
   - This enables feedback-loop to analyze recurring issue patterns

6. Update state:
   - gate_progress.review.status = "completed"
   - gate_progress.review.reviewers_passed = "3/3"

7. Proceed to Gate 5
```

### Gate 4 Anti-Rationalization Table

| Rationalization | Why It's WRONG | Required Action |
|-----------------|----------------|-----------------|
| "Only 1 MEDIUM issue, can proceed" | MEDIUM = MUST FIX. Quantity is irrelevant. | **Fix the issue, re-run all reviewers** |
| "Issue is cosmetic, not really MEDIUM" | Reviewer decided severity. Accept their judgment. | **Fix the issue, re-run all reviewers** |
| "Will fix in next sprint" | Deferred fixes = technical debt = production bugs. | **Fix NOW before Gate 5** |
| "User approved, can skip fix" | User approval ≠ reviewer override. Fixes are mandatory. | **Fix the issue, re-run all reviewers** |
| "Same issue keeps appearing, skip it" | Recurring issue = fix is wrong. Debug properly. | **Root cause analysis, then fix** |
| "Only security reviewer found it" | One reviewer = valid finding. All findings matter. | **Fix the issue, re-run all reviewers** |
| "Iteration limit reached, just proceed" | Limit = escalate, not bypass. Quality is non-negotiable. | **Escalate to user, DO NOT proceed** |
| "Tests pass, review issues don't matter" | Tests ≠ review. Different quality dimensions. | **Fix the issue, re-run all reviewers** |

### Gate 4 Pressure Resistance

| User Says | Your Response |
|-----------|---------------|
| "Just skip this MEDIUM issue" | "MEDIUM severity issues are blocking by definition. I MUST dispatch a fix to the appropriate agent before proceeding. This protects code quality." |
| "I'll fix it later, let's continue" | "Gate 4 is a HARD GATE. All CRITICAL/HIGH/MEDIUM issues must be resolved NOW. I'm dispatching the fix to [agent] and will re-run reviewers after." |
| "We're running out of time" | "Proceeding with known issues creates larger problems later. The fix dispatch is automated and typically takes 2-5 minutes. Quality gates exist to save time overall." |
| "Override the gate, I approve" | "User approval cannot override reviewer findings. The gate ensures code quality. I'll dispatch the fix now." |
| "It's just a style issue" | "If it's truly cosmetic, reviewers would mark it COSMETIC (non-blocking). MEDIUM means it affects maintainability or correctness. Fixing now." |

## Step 7: Gate 5 - Validation (Per Execution Unit)

```text
For current execution unit:

1. Record gate start timestamp
2. Verify acceptance criteria:
   For each criterion in acceptance_criteria:
     - Check if implemented
     - Check if tested
     - Mark as PASS/FAIL

3. Run final verification:
   - All tests pass?
   - No Critical/High/Medium review issues?
   - All acceptance criteria met?

4. If validation fails:
   - Log failure reasons
   - Determine which gate to revisit
   - Loop back to appropriate gate

5. If validation passes:
   - Set unit status = "completed"
   - Record gate end timestamp
   - agent_outputs.validation = {
       result: "approved",
       timestamp: "[ISO timestamp]",
       criteria_results: [{criterion, status}]
     }
   - Proceed to Step 7.1 (Execution Unit Approval)
```

## Step 7.1: Execution Unit Approval (Conditional)

**Checkpoint depends on `execution_mode`:** `manual_per_subtask` → Execute | `manual_per_task` / `automatic` → Skip

0. **COMMIT CHECK (before checkpoint):**
   - if `commit_timing == "per_subtask"`:
     - Execute `/ring:commit` command with message: `feat({unit_id}): {unit_title}`
     - Include all changed files from this subtask
   - else: Skip commit (will happen at task or cycle end)

1. Set `status = "paused_for_approval"`, save state
2. Present summary: Unit ID, Parent Task, Gates 0-5 status, Criteria X/X, Duration, Files Changed, Commit Status
3. **AskUserQuestion:** "Ready to proceed?" Options: (a) Continue (b) Test First (c) Stop Here
4. **Handle response:**

| Response | Action |
|----------|--------|
| Continue | Set in_progress, move to next unit (or Step 7.2 if last) |
| Test First | Set `paused_for_testing`, STOP, output resume command |
| Stop Here | Set `paused`, STOP, output resume command |

## Step 7.2: Task Approval Checkpoint (Conditional)

**Checkpoint depends on `execution_mode`:** `manual_per_subtask` / `manual_per_task` → Execute | `automatic` → Skip

0. **COMMIT CHECK (before task checkpoint):**
   - if `commit_timing == "per_task"`:
     - Execute `/ring:commit` command with message: `feat({task_id}): {task_title}`
     - Include all changed files from this task (all subtasks combined)
   - else if `commit_timing == "per_subtask"`: Already committed per subtask
   - else: Skip commit (will happen at cycle end)

1. Set task `status = "completed"`, cycle `status = "paused_for_task_approval"`, save state
2. Present summary: Task ID, Subtasks X/X, Total Duration, Review Iterations, Files Changed, Commit Status
3. **AskUserQuestion:** "Task complete. Ready for next?" Options: (a) Continue (b) Integration Test (c) Stop Here
4. **Handle response:**

```text
After completing all subtasks of a task:

0. Check execution_mode from state:
   - If "automatic": Still run feedback, then skip to next task
   - If "manual_per_subtask" or "manual_per_task": Continue with checkpoint below

1. Set task status = "completed"

2. **⛔ MANDATORY: Run ring:dev-feedback-loop skill**

   ```yaml
   Skill tool:
     skill: "ring:dev-feedback-loop"
   ```

   **Note:** ring:dev-feedback-loop manages its own TodoWrite tracking internally.
   
   The skill will:
   - Add its own todo item for tracking
   - Calculate assertiveness score for the task
   - Dispatch prompt-quality-reviewer agent with agent_outputs from state
   - Generate improvement suggestions
   - Write feedback to docs/feedbacks/cycle-{date}/{agent}.md
   - Mark its todo as completed

   **After feedback-loop completes, update state:**
   - Set `tasks[current].feedback_loop_completed = true` in state file

   **Anti-Rationalization for Feedback Loop:**

   | Rationalization | Why It's WRONG | Required Action |
   |-----------------|----------------|-----------------|
   | "Task was simple, skip feedback" | Simple tasks still contribute to patterns | **Execute Skill tool** |
   | "Already at 100% score" | High scores need tracking for replication | **Execute Skill tool** |
   | "User approved, feedback unnecessary" | Approval ≠ process quality metrics | **Execute Skill tool** |
   | "No issues found, nothing to report" | Absence of issues IS data | **Execute Skill tool** |
   | "Time pressure, skip metrics" | Metrics take <2 min, prevent future issues | **Execute Skill tool** |

   **⛔ HARD GATE: You CANNOT proceed to step 3 without executing the Skill tool above.**

3. Set cycle status = "paused_for_task_approval"
4. Save state

5. Present task completion summary (with feedback metrics):
   ┌─────────────────────────────────────────────────┐
   │ ✓ TASK COMPLETED                                │
   ├─────────────────────────────────────────────────┤
   │ Task: [task_id] - [task_title]                  │
   │                                                  │
   │ Subtasks Completed: X/X                         │
   │   ✓ ST-001-01: [title]                          │
   │   ✓ ST-001-02: [title]                          │
   │   ✓ ST-001-03: [title]                          │
   │                                                  │
   │ Total Duration: Xh Xm                           │
   │ Total Review Iterations: N                      │
   │                                                  │
   │ ═══════════════════════════════════════════════ │
   │ FEEDBACK METRICS                                │
   │ ═══════════════════════════════════════════════ │
   │                                                  │
   │ Assertiveness Score: XX% (Rating)               │
   │                                                  │
   │ Prompt Quality by Agent:                        │
   │   ring:backend-engineer-golang: 90% (Excellent)     │
   │   ring:qa-analyst: 75% (Acceptable)                 │
   │   ring:code-reviewer: 88% (Good)               │
   │                                                  │
   │ Improvements Suggested: N                       │
   │ Feedback Location:                              │
   │   docs/feedbacks/cycle-YYYY-MM-DD/             │
   │                                                  │
   │ ═══════════════════════════════════════════════ │
   │                                                  │
   │ All Files Changed This Task:                    │
   │   - file1.go                                    │
   │   - file2.go                                    │
   │   - ...                                         │
   │                                                  │
   │ Next Task: [next_task_id] - [next_task_title]   │
   │            Subtasks: N (or "TDD autonomous")    │
   │            or "No more tasks - cycle complete"  │
   └─────────────────────────────────────────────────┘

6. **ASK FOR EXPLICIT APPROVAL using AskUserQuestion tool:**

   Question: "Task [task_id] complete. Ready to start the next task?"
   Options:
     a) "Continue" - Proceed to next task
     b) "Integration Test" - User wants to test the full task integration
     c) "Stop Here" - Pause cycle

7. Handle user response:

   If "Continue":
     - Set status = "in_progress"
     - Move to next task
     - Set current_task_index += 1
     - Set current_subtask_index = 0
     - Reset to Gate 0
     - Continue execution

   If "Integration Test":
     - Set status = "paused_for_integration_testing"
     - Save state
     - Output: "Cycle paused for integration testing.
                Test task [task_id] integration and run:
                /ring:dev-cycle --resume
                when ready to continue."
     - STOP execution

   If "Stop Here":
     - Set status = "paused"
     - Save state
     - Output: "Cycle paused after task [task_id]. Resume with:
                /ring:dev-cycle --resume"
     - STOP execution
```

**Note:** Tasks without subtasks execute both 7.1 and 7.2 in sequence.

## Step 8: Cycle Completion

0. **FINAL COMMIT CHECK (before completion):**
   - if `commit_timing == "at_end"`:
     - Execute `/ring:commit` command with message: `feat({cycle_id}): complete dev cycle for {feature_name}`
     - Include all changed files from the entire cycle
   - else: Already committed per subtask or per task

1. **Calculate metrics:** total_duration_ms, average gate durations, review iterations, pass/fail ratio
2. **Update state:** `status = "completed"`, `completed_at = timestamp`
3. **Generate report:** Task | Subtasks | Duration | Review Iterations | Status | Commit Status

4. **⛔ MANDATORY: Run ring:dev-feedback-loop skill for cycle metrics**

   ```yaml
   Skill tool:
     skill: "ring:dev-feedback-loop"
   ```

   **Note:** ring:dev-feedback-loop manages its own TodoWrite tracking internally.

   **After feedback-loop completes, update state:**
   - Set `feedback_loop_completed = true` at cycle level in state file

   **⛔ HARD GATE: Cycle incomplete until feedback-loop executes.**

   | Rationalization | Why It's WRONG | Required Action |
   |-----------------|----------------|-----------------|
   | "Cycle done, feedback is extra" | Feedback IS part of cycle completion | **Execute Skill tool** |
   | "Will run feedback next session" | Next session = never. Run NOW. | **Execute Skill tool** |
   | "All tasks passed, no insights" | Pass patterns need documentation too | **Execute Skill tool** |

5. **Report:** "Cycle completed. Tasks X/X, Subtasks Y, Time Xh Xm, Review iterations X"

## Quick Commands

```bash
# Full PM workflow then dev execution
/ring:pre-dev-full my-feature
/ring:dev-cycle docs/pre-dev/my-feature/

# Simple PM workflow then dev execution
/ring:pre-dev-feature my-feature
/ring:dev-cycle docs/pre-dev/my-feature/tasks.md

# Manual task file
/ring:dev-cycle docs/tasks/sprint-001.md

# Resume interrupted cycle
/ring:dev-cycle --resume
```

## Error Recovery

| Type | Condition | Action |
|------|-----------|--------|
| **Recoverable** | Network timeout | Retry with exponential backoff |
| **Recoverable** | Agent failure | Retry once, then pause for user |
| **Recoverable** | Test flakiness | Re-run tests up to 2 times |
| **Non-Recoverable** | Missing required files | Stop and report |
| **Non-Recoverable** | Invalid state file | Must restart (cannot resume) |
| **Non-Recoverable** | Max review iterations | Pause for user |

**On any error:** Update state → Set status (failed/paused) → Save immediately → Report (what failed, why, how to recover, resume command)

## Execution Report

Base metrics per [shared-patterns/output-execution-report.md](../shared-patterns/output-execution-report.md).

| Metric | Value |
|--------|-------|
| Duration | Xh Xm Ys |
| Tasks Processed | N/M |
| Current Gate | Gate X - [name] |
| Review Iterations | N |
| Result | PASS/FAIL/IN_PROGRESS |

### Gate Timings
| Gate | Duration | Status |
|------|----------|--------|
| Implementation | Xm Ys | in_progress |
| DevOps | - | pending |
| SRE | - | pending |
| Testing | - | pending |
| Review | - | pending |
| Validation | - | pending |

### State File Location
`docs/ring:dev-cycle/current-cycle.json` (feature) or `docs/ring:dev-refactor/current-cycle.json` (refactor)
