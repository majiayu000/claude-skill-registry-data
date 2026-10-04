---
name: automate-dev
description: "Autonomous development workflow with iterative self-correction loops and multi-agent team coordination. Orchestrates the full build-review-test-fix cycle for any development task: delegates work to specialised solo subagents (code-explorer, code-architect, code-reviewer) and parallel agent teams (team-lead, team-implementer, team-reviewer, team-debugger), runs multi-dimensional code review and simplification passes, executes automated testing, detects and rejects band-aid fixes, enforces zero breaking changes, and loops until all issues are permanently resolved with production-ready, backwards-compatible code. Use whenever building features, fixing bugs, refactoring, or performing any multi-step development work. Triggers on: 'build', 'implement', 'develop', 'create feature', 'fix bug', 'refactor', 'automate', 'iterate until done', 'development workflow', 'build and test', 'team review', 'parallel debug', 'multi-agent', 'spawn team', or any task requiring autonomous code production with quality enforcement."
---

# Automated Development Skill

Autonomous, iterative development workflow that builds, reviews, tests, simplifies, and self-corrects code in a continuous loop until all quality gates pass. Zero tolerance for breaking changes, band-aid fixes, or workarounds.

## Core Principles

1. **Iterate Until Done**: Work loops through build → review → test → fix cycles until every issue is permanently resolved
2. **No Band-Aids**: Every fix must address root cause. Workarounds, suppressions, and temporary patches are rejected
3. **No Breaking Changes**: Existing functionality is preserved unconditionally. Any removal or signature change halts the workflow
4. **Simplicity Is Strength**: Code is simplified for clarity and maintainability without sacrificing capability
5. **Production-Ready Always**: Every output is deployable — complete error handling, security, validation, and documentation
6. **Backwards Compatible**: New code integrates with existing codebases without modification to dependents

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   AUTOMATE-DEV WORKFLOW                      │
│                                                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │ PHASE 1  │──▸│ PHASE 2  │──▸│ PHASE 3  │──▸│ PHASE 4  │ │
│  │ ANALYSE  │   │  BUILD   │   │ REVIEW   │   │  TEST    │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
│       │                                             │        │
│       │         ┌──────────┐   ┌──────────┐         │        │
│       │         │ PHASE 6  │◂──│ PHASE 5  │◂────────┘        │
│       │         │ SIMPLIFY │   │   FIX    │                  │
│       │         └──────────┘   └──────────┘                  │
│       │              │                                       │
│       │         ┌──────────┐                                 │
│       │         │ PHASE 7  │                                 │
│       │         │ VALIDATE │──▸ ALL PASS? ──▸ PHASE 8: SHIP │
│       │         └──────────┘        │                        │
│       │                        NO   │                        │
│       └◂────────────────────────────┘                        │
│                 (iteration loop)                             │
└─────────────────────────────────────────────────────────────┘
```

## Workflow Modes

### Mode 1: Core Loop (Default)

For bug fixes, well-defined modifications, and refactoring with clear scope.
Enters directly at Phase 1 (Analyse) and runs the full build-review-test-fix loop.

### Mode 2: Feature Development (Guided)

For new features requiring codebase exploration, architecture decisions, and
user clarification before building. Adds structured discovery phases before
the core loop:

```
FD-1: Discovery → FD-2: Codebase Exploration → FD-3: Clarifying Questions
    → FD-4: Architecture Design → FD-5: Implementation
    → Core Loop (Phase 3 onward) takes over automatically
```

Read `references/feature-development.md` when entering Feature Development mode.

### Mode 3: Team Coordination (Parallel Multi-Agent)

For complex work requiring multiple agents operating in parallel with file
ownership boundaries, competing hypotheses, or multi-dimensional review.
Activates the team-agents toolkit (team-lead, team-implementer, team-reviewer,
team-debugger) via the `/team-*` slash commands.

```
Trigger detected → Spawn team via /team-{spawn|feature|debug|review}
    → Decompose into parallel work streams (file ownership, hypotheses, dimensions)
    → Monitor via /team-status, rebalance via /team-delegate
    → Synthesize consolidated output
    → Hand off to Core Loop (Phase 3 onward) for quality gates
    → /team-shutdown when complete
```

Read `references/agent-teams-integration.md` when activating team mode, plus
the relevant internal skill: `skills/team-composition-patterns/SKILL.md`,
`skills/parallel-feature-development/SKILL.md`, `skills/multi-reviewer-patterns/SKILL.md`,
`skills/parallel-debugging/SKILL.md`, `skills/task-coordination-strategies/SKILL.md`,
or `skills/team-communication-protocols/SKILL.md`.

### Mode Selection

| Task Type | Mode | Entry Point | Team Escalation |
|-----------|------|-------------|-----------------|
| New feature in unfamiliar area | Feature Development | FD-1: Discovery | `/team-feature` if multi-stream |
| Bug fix with known location | Core Loop | Phase 1: Analyse | — |
| Bug with multiple plausible causes | Core Loop + Team | Phase 1 then `/team-debug` | `/team-debug --hypotheses 3+` |
| Refactor with clear scope | Core Loop | Phase 1: Analyse | `/team-feature` for large refactors |
| New feature, architecture known | Core Loop | Phase 1: Analyse | `/team-feature` if 3+ work streams |
| Ambiguous request needing exploration | Feature Development | FD-1: Discovery | `/team-spawn research` for parallel exploration |
| Multi-dimensional code review | Core Loop | Phase 3 | `/team-review` (security/perf/arch/testing/a11y) |
| Full-stack feature | Feature Development | FD-1: Discovery | `/team-spawn fullstack` |
| Migration / large refactor | Feature Development | FD-1: Discovery | `/team-spawn migration` |
| Comprehensive security audit | Core Loop | Phase 3 | `/team-spawn security` |

**Team escalation rule of thumb**: Engage Mode 3 when the task can be cleanly
decomposed into 3+ independent work streams, OR when multi-dimensional analysis
is needed (≥3 review dimensions, ≥3 competing hypotheses), OR when the
work spans multiple architectural layers (frontend/backend/tests/infrastructure).
For everything else, the solo subagent patterns from Modes 1–2 are more
efficient.

## Model Deployment Strategy

Optimised for **Claude Opus 4.8** (`claude-opus-4-8`) as the flagship model
for high-difficulty workflows, with Sonnet retained for exploration and
breadth-focused work. Opus 4.8 keeps the same request surface as Opus 4.7
(adaptive thinking only, `xhigh` effort, no sampling parameters), so moving
from a 4.7 deployment is a model-ID swap plus light prompt re-tuning — no
breaking changes.

### Difficulty-Based Routing

| Difficulty | Model | Effort | Examples |
|-----------|-------|--------|----------|
| low | sonnet | default | Simple reads, formatting |
| medium | sonnet | high | Multi-file tracing, routine refactors |
| **high** | **claude-opus-4-8** | **xhigh** | Code review, architecture, self-assessment, quality gates |
| xhigh | **claude-opus-4-8** | **xhigh** | Complex refactoring, subtle debugging |
| max | **claude-opus-4-8** | **max** | Formal verification, security audits |

`xhigh` is the recommended effort for the coding and agentic work this skill
performs. Treat effort as a per-task dial, not a fixed maximum: for routine,
latency-sensitive, or cost-sensitive steps, sweep down to `high`/`medium` —
Opus 4.8 often matches `xhigh` quality at lower effort and cost.

### Opus 4.8 Is Required For

- **Agent output self-review** — any agent reviewing work produced by another agent
- **Code quality assessment** — simplicity, DRY, elegance judgment
- **Linting judgment** — subjective quality gates beyond rule-based scripts
- **Architectural decisions** — choosing between implementation approaches
- **Final validation (Phase 7)** — comprehensive quality gate before ship
- **Any task classified as `high` difficulty or above**

### Retained Sonnet Usage

- **code-explorer agents** — breadth-focused codebase tracing (medium difficulty)
- **Initial inventory and dependency mapping** — rule-based, high-volume work
- **Test execution orchestration** — mostly deterministic
- **Deployment readiness checks** — script-based validation

### Opus 4.8 Behavioural Notes

Opus 4.8 is more autonomous yet more conservative about reaching for subagents
than earlier models — when a phase needs parallel exploration, review, or
debugging, instruct it **explicitly** (the "launch N subagents in parallel"
patterns and the `/team-*` commands below do exactly this). It also narrates
more and asks for confirmation more often; the agent prompts in `agents/` and
`agent-teams/agents/` are tuned to keep output focused and decisions autonomous
within scope. For operator instructions that arrive mid-run, Opus 4.8 supports
**mid-session system prompts** (no cache invalidation) — see
`references/model-deployment.md`.

See `references/model-deployment.md` for the complete strategy, the
Opus 4.7→4.8 migration guide, mid-session steering, and prompt adjustments for
Opus 4.8's literal instruction following.

## Specialised Agents

Two complementary agent families serve the workflow:

### Solo Subagents (Default — `delegation` skill)

Three agent types launched via `subagent` / `startAsyncSubagent` for
judgment-intensive analysis. Use alongside automated scripts for
comprehensive coverage.

| Agent | Role | Model | Effort | Primary Phase |
|-------|------|-------|--------|--------------|
| **code-explorer** | Deep codebase tracing and pattern discovery | sonnet | high | 1 (Analyse) |
| **code-architect** | Architecture design and implementation blueprints | **claude-opus-4-8** | **xhigh** | 2 (Build) |
| **code-reviewer** | Quality review — simplicity, correctness, conventions | **claude-opus-4-8** | **xhigh** | 3 (Review), 7 (Validate) |

Solo subagent definitions live in `agents/`. Read `references/agents.md` for
full prompts and orchestration patterns.

### Team Agents (Escalation — `/team-*` commands)

Four coordinated agent types launched as a managed team via the team-spawn
infrastructure. Use when work decomposes into ≥3 independent streams or
requires multi-dimensional parallel analysis.

| Agent | Role | Model | Colour | Primary Use |
|-------|------|-------|--------|-------------|
| **team-lead** | Orchestrator: decomposes work, manages file ownership, synthesises results | **claude-opus-4-8** | blue | Coordinate `/team-feature`, `/team-spawn fullstack/migration` |
| **team-implementer** | Builds within strict file ownership boundaries; coordinates at integration points | **claude-opus-4-8** | yellow | `/team-feature`, `/team-spawn fullstack/migration` |
| **team-reviewer** | Single-dimension reviewer (security / performance / architecture / testing / accessibility) | **claude-opus-4-8** | green | `/team-review`, `/team-spawn security` |
| **team-debugger** | Hypothesis-driven investigator with confidence ratings and causal chains | **claude-opus-4-8** | red | `/team-debug` (Analysis of Competing Hypotheses) |

Team agent definitions live in `agent-teams/agents/`. Read
`references/agent-teams-integration.md` for command-by-phase mapping and
team selection heuristics.

**Solo vs team selection rule**:

| Signal | Choose Solo | Choose Team |
|--------|-------------|-------------|
| Work scope | Single concern, ≤2 streams | ≥3 independent streams |
| Coordination cost | Low (no shared files) | Worth the overhead (clear ownership boundaries) |
| Review breadth | 3 standard dimensions (simplicity/correctness/conventions) | 4-5 dimensions (add security/perf/a11y) |
| Debug clarity | Single suspected cause | Multiple plausible root causes |
| Display | Inline | tmux/iTerm2 panes (set `teammateMode` in `~/.claude/settings.json`) |
| Pre-flight | Always available | Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` |

### Agent + Script Combination

Agents provide **judgment**. Scripts provide **rule enforcement**. Teams provide
**parallel scale**. Use all three layers:

```
Phase 3 (Review):
├── Solo Agent: code-reviewer (simplicity)     ─┐
├── Solo Agent: code-reviewer (correctness)     │
├── Solo Agent: code-reviewer (conventions)    ─┤──▸ Consolidated quality report
├── (escalation) Team: /team-review            ─┤    (deduplicated, severity-ranked
│   └── team-reviewer × {security, perf,         │     per multi-reviewer-patterns)
│       architecture, testing, accessibility}    │
├── Script: code_reviewer.py (band-aids, security, breaking changes)
└── Script: fix_validator.py (preservation check)
```

## Token Budgeting

Opus 4.8 shares the Opus 4.7 tokenizer (1.0–1.35× tokens vs the older 4.6
tokenizer; counts are unchanged when migrating from 4.7) and `xhigh` effort
increases reasoning depth. Cost control is enforced at three layers:

1. **Phase budgets** — default caps per workflow phase
2. **Agent budgets** — per-invocation limits (instructed in agent prompts)
3. **Task budgets** — total workflow cap (via `token_budget_monitor.py`
   and Opus 4.8's `task_budget` API feature)

### Default Budgets (medium difficulty)

| Phase | Budget | Typical Cost (Opus 4.8) |
|-------|--------|------------------------|
| 1 Analyse | 80,000 | ~$0.50 |
| 2 Build | 150,000 | ~$0.95 |
| 3 Review | 120,000 | ~$0.75 |
| 4 Test | 40,000 | ~$0.25 |
| 5 Fix | 60,000/iter | ~$0.38/iter |
| 6 Simplify | 40,000 | ~$0.25 |
| 7 Validate | 80,000 | ~$0.50 |
| 8 Ship | 20,000 | ~$0.13 |
| **Total (1 pass)** | **~590,000** | **~$3.70** |

Budgets scale by difficulty multiplier: low 0.5× / medium 1.0× / high 1.5× /
xhigh 2.0× / max 3.0×.

**Team mode multipliers** (Mode 3): when escalating a phase to a team,
multiply that phase's budget by team size. Example: `/team-review` with 5
reviewers → Phase 3 budget × 5. Track per-team token usage via
`token_budget_monitor.py` records tagged with the team name. The `90%`
alert threshold halts new parallel team launches first; existing teammates
finish their current task.

### Usage

```bash
# Initialise at workflow start
python scripts/token_budget_monitor.py init <project_root> --difficulty high

# Before each phase
python scripts/token_budget_monitor.py check <project_root> \
    --phase review --requested 120000

# After each phase
python scripts/token_budget_monitor.py record <project_root> \
    --phase review --tokens 115000 --model claude-opus-4-8

# Generate report at end
python scripts/token_budget_monitor.py report <project_root>
```

### Alert Thresholds

| Threshold | Action |
|-----------|--------|
| 50% | Log warning, continue |
| 75% | Log warning, flag in iteration plan |
| 90% | Halt new parallel launches, serialise work |
| 100% | Escalate to user with usage report |

See `references/token-budgeting.md` for caching strategies, cost patterns,
and detailed monitoring guidance.

## Phase Execution

### Phase 1: Analyse

Before writing any code:

1. **Inventory existing code** in target files — catalogue every function, class, export, route, model, and integration point
2. **Map dependencies** — identify what imports the target files and what they import
3. **Document current behaviour** — capture what the code does today as the preservation baseline
4. **Define acceptance criteria** — establish clear, testable conditions for "done"
5. **Create iteration plan** — write `.automate-dev/iteration_plan.md` with tasks, dependencies, and quality gates

**Agent-Enhanced Analysis** (when subagents available):
Launch 2-3 code-explorer agents in parallel for deep codebase understanding:
```javascript
await startAsyncSubagent({
    task: 'Find features similar to [feature] and trace their implementation. Return 5-10 key files.',
    relevantFiles: ['app/', 'src/']
});
await startAsyncSubagent({
    task: 'Map architecture and abstractions for [area]. Return 5-10 key files.',
    relevantFiles: ['app/', 'src/']
});
```
After agents return, read all identified files to build context.

**Team-Escalated Analysis** (broad / multi-area exploration):
When the analysis spans ≥3 distinct areas (e.g. backend + frontend + infra +
docs), prefer the research team preset:
```
/team-spawn research --members 3
```
Each `general-purpose` teammate is assigned a different research question
(codebase area, library comparison, doc set). Apply
`skills/task-coordination-strategies/SKILL.md` for decomposition and
`skills/team-communication-protocols/SKILL.md` for messaging discipline.
Synthesise results into the iteration plan, then resume Phase 1 inventory.

Run: `python scripts/dev_orchestrator.py analyse <project_root> --targets <file1> <file2>`

### Phase 2: Build

Implement the feature or fix:

1. Write production-ready code following project conventions
2. Include complete error handling with specific exceptions
3. Add type hints, docstrings, and inline comments for complex logic only
4. Ensure backwards compatibility — never remove or rename public APIs
5. Use the simplest correct implementation — avoid over-engineering

**Agent-Enhanced Architecture** (when subagents available):
Before implementation, launch code-architect agents to explore trade-offs:
```javascript
await startAsyncSubagent({
    task: 'Design MINIMAL implementation for [feature] — smallest change, max reuse.',
    relevantFiles: ['app/', '.CLAUDE.md']
});
await startAsyncSubagent({
    task: 'Design CLEAN ARCHITECTURE for [feature] — maintainability, proper separation.',
    relevantFiles: ['app/', '.CLAUDE.md']
});
```
Compare approaches, form recommendation, present to user for approval.

For delegated tasks (when `subagent` / `startAsyncSubagent` is available):
- Create `.local/session_plan.md` with task breakdown
- Launch independent tasks in parallel via `startAsyncSubagent`
- Use `subagent` for sequential dependencies
- Pass skill files via `relevantFiles` when subagents need skill context

**Team-Escalated Build** (parallel multi-stream implementation):
For features that decompose cleanly into ≥3 work streams with non-overlapping
file ownership, escalate to a managed team:

```
# Standard parallel build (1 lead + 2 implementers)
/team-feature "<feature description>" --team-size 2 --plan-first

# Full-stack split (1 lead + frontend + backend + tests)
/team-spawn fullstack --name <feature-team>

# Large refactor / migration (1 lead + 2 implementers + 1 reviewer)
/team-spawn migration --name <migration-team>
```

Apply `skills/parallel-feature-development/SKILL.md` for file-ownership
strategies (by directory / module / layer) and integration patterns
(vertical slice / horizontal layer / hybrid). Apply
`skills/team-composition-patterns/SKILL.md` for team-size sizing heuristics.

The team-lead enforces:
- One owner per file (Cardinal Rule from parallel-feature-development)
- Interface contracts for cross-team boundaries (immutable mid-stream)
- Sequential application of any genuinely shared files via the lead
- `blockedBy` / `blocks` task relationships for dependency sequencing

Once the team reports completion, the workflow re-enters Phase 3 (Review)
with all modified files. **Quality gates remain non-negotiable** — team output
is reviewed identically to solo output.

### Phase 3: Review

Automated code review against quality gates:

Run: `python scripts/code_reviewer.py <file> --project-root <root> [--original <original_file>]`

**Agent-Enhanced Review** (when subagents available):
Launch 3 code-reviewer agents in parallel with different focuses:
```javascript
await startAsyncSubagent({
    task: 'Review [files] for SIMPLICITY, DRY, ELEGANCE. Top 3-5 issues.',
    relevantFiles: [/* modified files */]
});
await startAsyncSubagent({
    task: 'Review [files] for BUGS, FUNCTIONAL CORRECTNESS. Top 3-5 issues.',
    relevantFiles: [/* modified files */]
});
await startAsyncSubagent({
    task: 'Review [files] for PROJECT CONVENTIONS, ABSTRACTIONS. Top 3-5 issues.',
    relevantFiles: [/* modified files */, '.CLAUDE.md']
});
```
Consolidate agent findings with script results into a unified quality report.

**Team-Escalated Review** (multi-dimensional / security audit):
For changes touching auth, data, public APIs, or UI — or any change requiring
≥4 review dimensions — escalate to a parallel reviewer team:

```
# Standard multi-dimensional review (security, performance, architecture)
/team-review <target> --reviewers security,performance,architecture

# Full review with testing + accessibility for UI/feature work
/team-review <target> --reviewers security,performance,architecture,testing,accessibility

# Comprehensive security audit
/team-spawn security --name security-audit
```

`<target>` accepts: file path, directory, git diff range (e.g. `main...HEAD`),
or PR number (`#123`).

Apply `skills/multi-reviewer-patterns/SKILL.md` for:
- Review-dimension allocation by scenario (API / frontend / DB migration / etc.)
- Finding deduplication rules (same-location merge, conflicting-severity escalation)
- Severity calibration (Critical / High / Medium / Low criteria)
- Consolidated report template with per-dimension counts

Combine team findings with solo-agent findings AND script results into the
unified quality report. The same gates apply.

Review checks:
- **Breaking changes**: Any detected → HALT, do not proceed
- **Functionality preservation**: 100% required
- **Compatibility score**: ≥95 required
- **Code quality**: Complexity ≤10 per function, no bare excepts, no TODOs in deliverables
- **Security**: Input validation, parameterised queries, no credential exposure
- **Band-aid detection**: Pattern matching for suppressed errors, commented-out code, hardcoded workarounds

### Phase 4: Test

Execute automated testing:

1. **Unit tests** — run existing test suite, verify no regressions
2. **Integration tests** — verify new code works with existing components
3. **End-to-end tests** (when Playwright/testing subagent available) — validate user-facing flows

For Playwright-based testing, write focused test plans:
```text
1. [New Context] Create a new browser context
2. [Browser] Navigate to the target page
3. [Browser] Perform user actions
4. [Verify] Assert expected outcomes
```

Run: `python scripts/dev_orchestrator.py test <project_root> --targets <file1> <file2>`

### Phase 5: Fix

When tests or review reveal issues:

1. **Root cause analysis** — identify the actual source, not just the symptom
2. **Permanent fix** — address the root cause directly
3. **Regression check** — verify the fix doesn't break other functionality
4. **Band-aid rejection** — automatically reject fixes that:
   - Suppress or swallow exceptions
   - Add `try/except: pass` blocks
   - Comment out failing code
   - Hardcode values to bypass logic
   - Add conditional branches that skip broken paths
   - Use `# noqa`, `# type: ignore`, or similar suppressions as the fix itself

**Team-Escalated Debugging** (multiple plausible root causes):
When initial root-cause analysis surfaces ≥2 plausible hypotheses, escalate
to the Analysis of Competing Hypotheses (ACH) workflow:

```
/team-debug "<error description or file path>" --hypotheses 3 --scope module
```

Each `team-debugger` teammate is assigned one hypothesis from the 6 failure-mode
categories (Logic / Data / State / Integration / Resource / Environment) and
investigates independently with file:line evidence and confidence ratings.
The lead arbitrates and ranks confirmed hypotheses to determine the true root
cause. Apply `skills/parallel-debugging/SKILL.md` for:
- Hypothesis generation framework (6 categories)
- Evidence collection standards (Direct / Correlational / Testimonial / Absence)
- Confidence calibration (High >80% / Medium 50-80% / Low <50%)
- Result arbitration protocol

The chosen fix still passes through `fix_validator.py` and the band-aid
rejection rules. **No exceptions to the band-aid policy regardless of how
the root cause was identified.**

Run: `python scripts/fix_validator.py <original> <fixed> --project-root <root>`

### Phase 6: Simplify

After fixes pass validation:

1. **Reduce complexity** — flatten nested conditionals, extract helper functions
2. **Eliminate redundancy** — remove duplicate logic, consolidate related code
3. **Improve naming** — use descriptive, project-consistent names
4. **Remove dead code** — strip unreachable paths and unused imports
5. **Preserve behaviour** — simplification must not alter functionality

Run: `python scripts/code_simplifier.py <file> --project-root <root> [--original <original_file>]`

Simplification rules:
- Prefer `if/elif/else` over nested ternaries
- Prefer explicit over clever
- Prefer readability over line count
- Never combine unrelated concerns into single functions
- Maintain project naming conventions

### Phase 7: Validate

Final gate before delivery:

Run: `python scripts/dev_orchestrator.py validate <project_root> --targets <file1> <file2>`

Validation checks:
- All Phase 3 review checks pass
- All Phase 4 tests pass
- No band-aid patterns detected
- Compatibility score ≥95
- Zero breaking changes
- 100% functionality preservation
- Code simplified to project standards

**If ANY check fails**: Loop back to Phase 5 with the specific failure details. Update `.automate-dev/iteration_plan.md` with:
- Iteration number
- What failed
- Root cause identified
- Fix strategy
- Expected outcome

**Maximum iterations**: 10 (configurable). If unresolved after max iterations:
- Document all attempted fixes
- Document the blocking issue
- Present findings to user with clear options

### Phase 8: Ship

When all validation passes:

1. **Generate assessment report** with scores and verification status
2. **Confirm deployment readiness** — run `python scripts/deployment_readiness.py <project_root>`
3. **Deliver code** with assessment summary

## Reference Documentation

Load these as needed during workflow execution:

| Reference | Path | When to Read |
|-----------|------|-------------|
| Workflow Phases | `references/workflow-phases.md` | Detailed phase instructions with examples |
| Iteration Protocols | `references/iteration-protocols.md` | Loop management, max iterations, escalation |
| Quality Gates | `references/quality-gates.md` | Thresholds, scoring, pass/fail criteria |
| Code Simplification | `references/code-simplification.md` | Simplification rules and patterns |
| Agents | `references/agents.md` | Solo agent definitions, prompts, orchestration patterns |
| Feature Development | `references/feature-development.md` | Guided feature development workflow (FD-1 through FD-7) |
| Model Deployment | `references/model-deployment.md` | Opus 4.8 strategy, difficulty classification, routing |
| Token Budgeting | `references/token-budgeting.md` | Phase budgets, caching, monitoring, cost patterns |
| **Agent Teams Integration** | `references/agent-teams-integration.md` | When to escalate to teams, command-by-phase mapping |

## Internal Skills Library (Team Coordination)

When operating in Mode 3 (Team Coordination), load the relevant internal skill
SKILL.md as the authoritative reference. These skills live under `skills/`
inside this package and are loaded on-demand:

| Skill | Path | When to Read |
|-------|------|-------------|
| **team-composition-patterns** | `skills/team-composition-patterns/SKILL.md` | Choosing team size, preset selection, agent-type selection, display-mode config |
| **parallel-feature-development** | `skills/parallel-feature-development/SKILL.md` | File-ownership strategies, conflict avoidance, integration patterns, branch management |
| **multi-reviewer-patterns** | `skills/multi-reviewer-patterns/SKILL.md` | Review-dimension allocation, finding deduplication, severity calibration, consolidated reporting |
| **parallel-debugging** | `skills/parallel-debugging/SKILL.md` | Analysis of Competing Hypotheses, evidence standards, confidence levels, root-cause arbitration |
| **task-coordination-strategies** | `skills/task-coordination-strategies/SKILL.md` | Task decomposition, dependency graphs, task description templates, workload monitoring |
| **team-communication-protocols** | `skills/team-communication-protocols/SKILL.md` | Message-type selection, plan approval, shutdown procedures, anti-patterns |

**Skill loading rule**: Read the relevant SKILL.md *before* invoking the
matching `/team-*` command. This ensures the workflow applies the skill's
heuristics (sizing, dimensions, ownership rules) rather than improvising.

## Slash Commands (Team Coordination)

Eight slash commands ship with this skill. The seven `/team-*` commands handle
team lifecycle and operations and require `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
in the environment; `/feature-development` (Mode 2) runs in any environment.

| Command | Purpose | Primary Phase |
|---------|---------|---------------|
| `/feature-development` | Launches the guided 7-phase feature development workflow (Mode 2) | Pre-Phase 1 |
| `/team-spawn <preset\|custom>` | Spawn a team using a preset (review/debug/feature/fullstack/research/security/migration) or custom composition | Setup |
| `/team-feature <description>` | Parallel feature build with file-ownership boundaries (lead + N implementers) | 2 (Build) |
| `/team-debug <error>` | Competing-hypotheses debugging with N parallel investigators | 5 (Fix) |
| `/team-review <target>` | Multi-dimensional parallel code review with consolidated, deduplicated report | 3 (Review), 7 (Validate) |
| `/team-status [team]` | Display team members, task statuses, and progress | All (monitoring) |
| `/team-delegate [team]` | Workload dashboard, task assignment, rebalancing | All (coordination) |
| `/team-shutdown [team]` | Graceful shutdown — collect final results, clean up resources | Cleanup |

**Lifecycle**: every team launched (via spawn / feature / debug / review)
must be terminated via `/team-shutdown` before the workflow declares
completion. Leaving teams running wastes API resources and pollutes
`~/.claude/teams/`.

## Script Reference

| Script | Purpose | Phase |
|--------|---------|-------|
| `dev_orchestrator.py` | Main workflow orchestration | All |
| `code_reviewer.py` | Automated code review with band-aid detection | 3, 7 |
| `code_simplifier.py` | Code refinement and clarity improvement | 6 |
| `fix_validator.py` | Validates fixes are permanent, not workarounds | 5 |
| `iteration_planner.py` | Creates and updates iteration plans | 1, 7 |
| `deployment_readiness.py` | Pre-deployment verification | 8 |
| `token_budget_monitor.py` | Tracks token usage, enforces budgets, cost reporting | All |

## Integration with Existing Skills

This skill orchestrates and delegates to other skills:

- **production-code-quality**: Called during Phase 3 and Phase 7 for assessment
- **delegation**: Used across all phases for parallel task execution via solo subagents and specialised agents (code-explorer, code-architect, code-reviewer)
- **testing**: Used in Phase 4 for end-to-end Playwright-based testing
- **code_review (architect)**: Used in Phase 3 for deep architectural analysis via the `architect()` function
- **deployment**: Used in Phase 8 for deployment configuration

### Internal Team Skills (bundled, see `skills/`)

When Mode 3 (Team Coordination) is active, the workflow autonomously loads:

- **team-composition-patterns** — sizing & preset selection before any team spawn
- **task-coordination-strategies** — task decomposition & dependency-graph design
- **team-communication-protocols** — message-type discipline, plan approval, shutdown
- **parallel-feature-development** — file ownership & integration patterns (`/team-feature`)
- **multi-reviewer-patterns** — dimension allocation & finding deduplication (`/team-review`)
- **parallel-debugging** — Analysis of Competing Hypotheses (`/team-debug`)

### Agent Integration Summary

| Workflow Phase | Solo Agents | Team Escalation | Script Complement |
|---------------|------------|-----------------|-------------------|
| Phase 1 (Analyse) | code-explorer × 2-3 | `/team-spawn research` (≥3 areas) | `dev_orchestrator.py analyse` |
| Phase 2 (Build) | code-architect × 2-3 | `/team-feature`, `/team-spawn fullstack/migration` | — |
| Phase 3 (Review) | code-reviewer × 3 | `/team-review`, `/team-spawn security` | `code_reviewer.py`, `fix_validator.py` |
| Phase 5 (Fix) | — | `/team-debug` (≥2 hypotheses) | `fix_validator.py` |
| Phase 6 (Simplify) | — | — | `code_simplifier.py` |
| Phase 7 (Validate) | code-reviewer × 3 | `/team-review` (full dimensions) | `dev_orchestrator.py validate` |
| Phase 8 (Ship) | — | `/team-shutdown` (cleanup) | `deployment_readiness.py` |

## Iteration Plan Format

File: `.automate-dev/iteration_plan.md`

```markdown
# Iteration Plan: [Task Description]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Iteration 1
- **Status**: PASS | FAIL | IN_PROGRESS
- **Phase reached**: 7
- **Failures**: [List of failures]
- **Root causes**: [Identified root causes]
- **Fixes applied**: [Description of fixes]
- **Result**: [Outcome]

## Current State
- **Iteration**: N
- **Blocking issues**: [None | List]
- **Quality scores**: Compatibility: XX | Preservation: XX | Quality: XX
```

## Troubleshooting

### Infinite Loop Prevention
- Hard cap at 10 iterations (configurable via `--max-iterations`)
- Each iteration must make measurable progress (at least one new fix or score improvement)
- If two consecutive iterations produce identical scores, escalate to user

### Cannot Achieve 100% Preservation
1. Document what cannot be preserved and why
2. Present alternatives
3. Request explicit approval before proceeding
4. Never silently drop functionality

### Band-Aid Fix Detected
1. Reject the fix immediately
2. Re-analyse the root cause
3. Implement a proper structural fix
4. If stuck after 3 attempts on the same issue, escalate to user with full context

## Installation

### Requirements

- **A Claude Code version that supports `claude-opus-4-8`** — run `claude update`
  if `/model claude-opus-4-8` is unavailable
- **Opus 4.8 access** — verify with `/model claude-opus-4-8` in Claude Code
- **Python 3.8+** — for scripts
- **Optional**: Prompt caching enabled for cost reduction on repeated runs

### Claude Code

Copy the package contents to your project:

```bash
# Solo agents — required for agent-enhanced phases (Modes 1 & 2)
cp automate-dev/agents/*.md .claude/agents/

# Team agents — required for Mode 3 (Team Coordination)
cp automate-dev/agent-teams/agents/*.md .claude/agents/

# Commands — enables /feature-development AND all /team-* slash commands
cp automate-dev/commands/*.md .claude/commands/

# Internal team skills — loaded on demand during Mode 3
cp -r automate-dev/skills .claude/skills/automate-dev-teams

# Skill — install via Claude Code skill installation
# or copy SKILL.md and references/ to your skills directory
```

### Enable Agent Teams (Mode 3 prerequisite)

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# Optional: configure display mode in ~/.claude/settings.json
# {
#   "teammateMode": "tmux"  // or "iterm2", "in-process"
# }
```

Without `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, the `/team-*` commands
are unavailable but the skill degrades gracefully to solo-subagent mode.

### Configure Default Model (Optional)

To pin Opus 4.8 globally in Claude Code:

```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-4-8
export ANTHROPIC_DEFAULT_EFFORT=xhigh

# Or set per-session
/model claude-opus-4-8
/effort xhigh
```

### Initialise Token Budget Monitor

At the start of each workflow run:

```bash
python scripts/token_budget_monitor.py init <project_root> --difficulty medium
```

Choose difficulty based on task complexity: `low`, `medium`, `high`, `xhigh`,
or `max` (see `references/model-deployment.md` for classification).

### Claude.ai Projects

Upload the `.skill` or `.zip` file to the project knowledge. The agents
and commands directories are not used in Claude.ai — the skill degrades
gracefully to script-only operation.

### Directory Structure

```
automate-dev/
├── SKILL.md                              Main skill definition (8-phase core loop + 3 modes)
├── LICENSE.txt                           Apache 2.0
├── agents/                               Solo agent definitions (Modes 1 & 2)
│   ├── code-explorer.md                  Codebase tracing (sonnet, yellow)
│   ├── code-architect.md                 Architecture design (claude-opus-4-8 xhigh, green)
│   └── code-reviewer.md                  Deep quality review (claude-opus-4-8 xhigh, red)
├── agent-teams/                          Team agent definitions (Mode 3)
│   └── agents/
│       ├── team-lead.md                  Orchestrator (claude-opus-4-8, blue) — decomposes & synthesises
│       ├── team-implementer.md           Parallel builder (claude-opus-4-8, yellow) — file-ownership boundaries
│       ├── team-reviewer.md              Single-dimension reviewer (claude-opus-4-8, green)
│       └── team-debugger.md              Hypothesis investigator (claude-opus-4-8, red)
├── commands/                             Slash commands for Claude Code
│   ├── feature-development.md            Guided 7-phase feature development workflow (Mode 2)
│   ├── team-spawn.md                     Spawn team via preset or custom composition
│   ├── team-feature.md                   Parallel feature build with file ownership
│   ├── team-debug.md                     Competing-hypotheses debugging
│   ├── team-review.md                    Multi-dimensional parallel code review
│   ├── team-status.md                    Team monitoring dashboard
│   ├── team-delegate.md                  Workload assignment & rebalancing
│   └── team-shutdown.md                  Graceful team termination
├── skills/                               Internal team-coordination skills (Mode 3)
│   ├── team-composition-patterns/        Sizing heuristics, presets, agent-type selection
│   ├── parallel-feature-development/     File ownership, conflict avoidance, integration
│   ├── multi-reviewer-patterns/          Dimension allocation, dedup, severity calibration
│   ├── parallel-debugging/               Analysis of Competing Hypotheses
│   ├── task-coordination-strategies/     Decomposition, dependency graphs, monitoring
│   └── team-communication-protocols/     Messaging discipline, plan approval, shutdown
├── references/                           On-demand reference documentation
│   ├── agents.md                         Solo agent definitions, prompts, orchestration patterns
│   ├── agent-teams-integration.md        When/how to escalate to teams; per-phase mapping
│   ├── feature-development.md            Feature development workflow detail (FD-1 to FD-7)
│   ├── workflow-phases.md                Detailed phase instructions with examples
│   ├── iteration-protocols.md            Loop management, stall detection, escalation
│   ├── quality-gates.md                  Thresholds, scoring, pass/fail criteria
│   ├── code-simplification.md            Simplification rules and patterns
│   ├── model-deployment.md               Opus 4.8 routing strategy, difficulty classification
│   └── token-budgeting.md                Phase budgets, prompt caching, cost patterns
└── scripts/                              Automated analysis and enforcement scripts
    ├── dev_orchestrator.py               Main workflow engine (analyse/test/validate/status)
    ├── code_reviewer.py                  Review with band-aid detection (10 patterns)
    ├── code_simplifier.py                Nesting, duplication, naming analysis
    ├── fix_validator.py                  Validates fixes are permanent, not workarounds
    ├── iteration_planner.py              Creates/updates plans, stall detection, escalation
    ├── deployment_readiness.py           Security, error handling, dependency checks
    └── token_budget_monitor.py           Token usage tracking, budget enforcement, cost reports
```
