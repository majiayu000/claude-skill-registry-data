---
name: epci:implement
description: >-
  Full implementation workflow for STANDARD and LARGE features through multi-phase
  EPCI execution. Routes through Explore, Plan, Code, Inspect phases with TDD enforcement.
  Supports plan-first workflow via @plan-path to skip E-P phases (uses Claude Code native plan).
  Use when: building features, implementing specs, developing from PRD.
  Triggers: implement feature, build, develop, create feature.
  Not for: quick fixes (use /quick), debugging (use /debug), refactoring (use /refactor).
user-invocable: true
argument-hint: "<feature-slug> [@spec-path | @plan-path] [--team | --no-team]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, Task
---

# Implement

Full implementation workflow for STANDARD and LARGE features using EPCI phases.

## Quick Start

```
/epci:implement feature-slug
/epci:implement feature-slug @docs/specs/feature.md
/epci:implement feature-slug @.claude/plans/feature-plan.md
/epci:implement feature-slug --team          # Force team mode
/epci:implement feature-slug --no-team       # Force classic mode
```

## Input Detection

```
INPUT
├── @.claude/plans/*.md → PLAN-FIRST workflow (skip E-P)
│   └─ Native Claude Code plan already done, go directly to CODE
├── @docs/specs/*.md → SPEC-FIRST workflow (skip E)
│   └─ Spec exists, do minimal planning then CODE
└── feature-slug only → FULL workflow (E-P-C-I-M)
    └─ Full Explore + Plan phases first
```

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER execute steps out of order
- 🔴 NEVER skip the planning phase
- 🔴 NEVER modify files during exploration (Step 01)
- 🔴 NEVER skip TDD for STANDARD+ complexity
- 🔴 NEVER call EnterPlanMode during skill execution
- ✅ ALWAYS start with step-00-init.md
- ✅ ALWAYS follow next_step from each step
- ✅ ALWAYS present breakpoints at phase transitions
- ✅ ALWAYS complete code review before documentation
- ⛔ FORBIDDEN skipping tests for STANDARD or LARGE features
- 🔵 YOU ARE A METHODICAL IMPLEMENTER following EPCI discipline
- 💭 FOCUS on one phase at a time, complete before proceeding

## EXECUTION PROTOCOLS:

1. **Load** step-00-init.md
2. **Execute** current step protocols completely
3. **Present** breakpoint if specified in step
4. **Evaluate** next step trigger conditions
5. **Proceed** to next_step or conditional_next

## CONTEXT BOUNDARIES:

- IN scope: Feature implementation following EPCI phases, TDD workflow, code review
- OUT scope: Quick fixes (use /quick), debugging (use /debug), pure refactoring (use /refactor)

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    IMPLEMENT WORKFLOW (EPCI)                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Step 00: INIT                                                       │
│  └─ Detect complexity, validate input                                │
│     └─ If TINY/SMALL → step-00b-turbo (redirect to /quick)           │
│     └─ If STANDARD/LARGE → step-00c-worktree                         │
│                                                                      │
│  Step 00c: WORKTREE [W] (STANDARD+ only)                             │
│  └─ Check existing worktree status                                   │
│  └─ Offer worktree creation (opt-in)                                 │
│     └─ BREAKPOINT: Worktree setup                                    │
│                                                                      │
│  Step 01: EXPLORE [E]                                                │
│  └─ Read-only codebase analysis                                      │
│  └─ Identify patterns, dependencies                                  │
│     └─ BREAKPOINT: Exploration findings                              │
│                                                                      │
│  Step 02: PLAN [P]                                                   │
│  └─ Create implementation plan                                       │
│  └─ Define test strategy                                             │
│     └─ BREAKPOINT: Plan validation                                   │
│                                                                      │
│  Step 03b: TEAM [T] (conditional)                                    │
│  └─ Detect domains from plan files                                   │
│  └─ If STANDARD+ AND >=2 domains (or --team flag):                   │
│     └─ Activate team mode                                            │
│     └─ Launch parallel Code Reviewer (background)                    │
│     └─ Launch Security/QA reviewers if applicable                    │
│     └─ BREAKPOINT: Team mode activation                              │
│  └─ Else: skip to step-03 (classic mode)                             │
│                                                                      │
│  Step 03: CODE [C]                                                   │
│  └─ TDD cycle: RED → GREEN → REFACTOR                                │
│  └─ Implement feature incrementally                                  │
│  └─ If team mode: background reviewer runs during coding             │
│                                                                      │
│  Step 04: REVIEW [I]                                                 │
│  └─ If team mode: aggregate parallel review results                  │
│  └─ Else: invoke @code-reviewer synchronously                        │
│     └─ If security concerns → step-04b-security                      │
│     └─ If QA needed → step-04c-qa                                    │
│     └─ BREAKPOINT: Review approval                                   │
│                                                                      │
│  Step 05: DOCUMENT                                                   │
│  └─ Update Feature Document                                          │
│  └─ Update relevant docs                                             │
│                                                                      │
│  Step 06: FINISH                                                     │
│  └─ Final validation                                                 │
│  └─ Completion summary                                               │
│                                                                      │
│  Step 07: MEMORY [M]                                                 │
│  └─ Generate summary (1-2 sentences)                                 │
│  └─ Collect modified_files list                                      │
│  └─ Count tests added                                                │
│  └─ Append/update index.json                                         │
│  └─ If worktree: offer finalization                                  │
│     └─ BREAKPOINT: Worktree finalization                             │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Feature Document

**Location**: `docs/features/{feature-slug}-{YYYYMMDD-HHmmss}.md` (in target project)

The Feature Document is a human-readable Markdown file that serves as the **traceability thread** throughout the entire implementation lifecycle. Each step fills its section using the Edit tool.

| Section | Filled by | Phase |
|---------|-----------|-------|
| §0 Metadata | step-00-init | Init |
| §1 Contexte & Objectif | step-00-init | Init |
| §2 Plan d'implementation | step-02-plan | [P] |
| §3 Implementation | step-03-code | [C] |
| §4 Revue & Validation | step-04-review | [I] |
| §5 Finalisation | step-05-document | Doc |

**Rules**:
- Created by step-00-init using **Write tool**
- Updated by each step using **Edit tool** (never overwrite, only edit sections)
- Path stored in `artifacts.feature_doc` in state.json
- Status updated to COMPLETED by step-06-finish

See [references/feature-document-template.md](references/feature-document-template.md) for the full template.

## Steps

| Step | Name | Phase | Description |
|------|------|-------|-------------|
| 00 | init | - | Detect complexity, validate input |
| 00b | turbo | - | Redirect TINY/SMALL to /quick |
| 00c | worktree | [W] | Worktree setup for parallel dev (opt-in) |
| 01 | explore | [E] | Read-only codebase analysis |
| 02 | plan | [P] | Implementation planning |
| 03b | team | [T] | Agent team orchestration (conditional) |
| 03 | code | [C] | TDD implementation |
| 04 | review | [I] | Code review |
| 04b | security | [I] | Security-focused review |
| 04c | qa | [I] | QA validation |
| 05 | document | - | Feature Document §5 + related docs |
| 06 | finish | - | Finalization |
| 07 | memory | [M] | Update index.json with summary |

## Decision Tree

```
IF complexity == TINY or SMALL:
  → Redirect to /quick (step-00b-turbo)
ELSE IF complexity == STANDARD:
  → Worktree setup (step-00c, opt-in)
  → Full EPCI workflow (step-01 → step-07)
  → IF --team flag OR (>=2 domains detected):
    → step-03b-team activates (parallel agents)
ELSE IF complexity == LARGE:
  → Worktree setup (step-00c, opt-in)
  → Full EPCI workflow with enhanced reviews
  → Always include step-04b-security
  → step-03b-team activates by default (multi-domain likely)
  → IF CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1:
    → Agent Teams mode (teammates) instead of subagents

TEAM MODE OVERRIDE:
  --team flag   → Force team mode regardless of auto-detect
  --no-team flag → Force classic mode regardless of auto-detect
  Both flags    → Error
```

## Complexity Routing

| Complexity | LOC | Files | Workflow |
|------------|-----|-------|----------|
| TINY | < 50 | 1-2 | → /quick |
| SMALL | 50-200 | 1-3 | → /quick |
| STANDARD | 200-500 | 2-5 | → Full EPCI |
| LARGE | 500+ | 5+ | → Full EPCI + security |

## Step Files

- [steps/step-00-init.md](steps/step-00-init.md) — Initialization
- [steps/step-00b-turbo.md](steps/step-00b-turbo.md) — Turbo redirect
- [steps/step-00c-worktree.md](steps/step-00c-worktree.md) — Worktree setup [W]
- [steps/step-01-explore.md](steps/step-01-explore.md) — Exploration [E]
- [steps/step-02-plan.md](steps/step-02-plan.md) — Planning [P]
- [steps/step-03b-team.md](steps/step-03b-team.md) — Agent team orchestration [T]
- [steps/step-03-code.md](steps/step-03-code.md) — Coding [C]
- [steps/step-04-review.md](steps/step-04-review.md) — Review [I]
- [steps/step-04b-security.md](steps/step-04b-security.md) — Security review
- [steps/step-04c-qa.md](steps/step-04c-qa.md) — QA review
- [steps/step-05-document.md](steps/step-05-document.md) — Documentation
- [steps/step-06-finish.md](steps/step-06-finish.md) — Finalization
- [steps/step-07-memory.md](steps/step-07-memory.md) — Memory update

## Reference Files

- [references/tdd-rules.md](references/tdd-rules.md) — TDD workflow rules
- [references/review-checklists.md](references/review-checklists.md) — Code review checklists
- [references/breakpoint-formats.md](references/breakpoint-formats.md) — ASCII box templates for breakpoints
- [references/output-templates.md](references/output-templates.md) — Output format templates
- [references/domain-mapping.md](references/domain-mapping.md) — File extension to domain mapping for team mode
- [references/feature-document-template.md](references/feature-document-template.md) — Feature Document structure (§0-§5)

## Shared Components Used

- `epci:state-manager` — Track progress across sessions
- `epci:complexity-calculator` — Scope validation and routing
- `epci:tdd-enforcer` — Ensure TDD compliance
- `epci:breakpoint-system` — Phase checkpoints
- `epci:project-memory` — Context persistence

## Breakpoints

This skill uses `epci:breakpoint-system` at key workflow points.

| Step | Type | Purpose |
|------|------|---------|
| step-00-init | `validation` | Complexity assessment confirmation |
| step-00c-worktree | `validation` | Worktree opt-in decision |
| step-01-explore | `phase-transition` | Exploration [E] → Planning [P] |
| step-02-plan | `plan-review` | Plan validation before coding |
| step-03b-team | `validation` | Team mode activation (conditional) |
| step-04-review | `phase-transition` | Coding [C] → Inspection [I] |
| step-04b-security | `validation` | Security review approval |
| step-04c-qa | `validation` | QA validation approval |
| step-07-memory | `validation` | Worktree finalization (if enabled) |

**Note:** Les step files utilisent le format impératif direct (pas `@skill:epci:breakpoint-system`).

## Team Mode (Multi-Agent Orchestration)

For STANDARD and LARGE features spanning multiple technology domains, /implement can activate team mode to parallelize reviews and (experimentally) coding.

### Activation

Team mode activates when:
- **Auto-detect**: complexity >= STANDARD AND >= 2 distinct domains in plan files
- **Override**: `--team` flag forces activation, `--no-team` flag forces classic mode

### Domain Detection

Domains are detected from file extensions in the approved plan:

| Domain | Extensions |
|--------|-----------|
| `backend` | `*.py`, `*.php`, `*.java` |
| `frontend` | `*.tsx`, `*.jsx`, `*.ts`, `*.js`, `*.css`, `*.scss`, `*.html` |
| `database` | `*.sql` |

See [references/domain-mapping.md](references/domain-mapping.md) for full mapping.

### Orchestration Modes

| Mode | Condition | Mechanism |
|------|-----------|-----------|
| **Subagents** (default) | STANDARD+ with >=2 domains | Task tool with `run_in_background` |
| **Agent Teams** (experimental) | LARGE + `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` | TeammateTool with shared task list |

### Parallel Agents (Subagents Mode)

| Agent | Trigger | Model | When |
|-------|---------|-------|------|
| Code Reviewer | Always in team mode | Opus | During step-03 coding |
| Security Auditor | Auth/security patterns in plan | Opus | During step-03 coding |
| QA Reviewer | Complex test strategy | Sonnet | During step-03 coding |

Results are aggregated in step-04-review (and step-04b/04c if applicable).

### Agent Teams Mode (Experimental)

When enabled, spawns specialized implementer teammates per domain:
- Each teammate gets exclusive file access (no conflicts)
- Shared task list with DAG dependencies
- Plan approval workflow before coding starts
- Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

### Flags

| Flag | Effect |
|------|--------|
| `--team` | Force team mode (even on single-domain features) |
| `--no-team` | Force classic mode (even on multi-domain features) |
| Both | Error: "Conflicting flags" |

## Worktree Support

For STANDARD and LARGE features, /implement offers optional worktree isolation.

| Aspect | Behavior |
|--------|----------|
| Location | `../worktrees/{feature-slug}/` |
| Branch | `feature/{feature-slug}` |
| Activation | Opt-in via breakpoint at step-00c |
| Cleanup | Offered at step-07 completion |

### Benefits

- **Parallel development**: Run multiple /implement sessions simultaneously
- **Clean isolation**: Each feature has its own working directory
- **Safe rollback**: Abandon worktree without affecting main repo
- **Branch ready**: Feature branch preserved for PR creation

### Scripts

| Script | Purpose |
|--------|---------|
| `scripts/worktree-create.sh` | Create worktree with branch |
| `scripts/worktree-status.sh` | Check worktree status (JSON) |
| `scripts/worktree-finalize.sh` | Remove worktree, optionally delete branch |

### State Tracking

Worktree metadata is persisted in `state.json`:

```json
{
  "worktree": {
    "enabled": true,
    "path": "../worktrees/feature-slug",
    "branch": "feature/feature-slug",
    "status": "active",
    "created_at": "2026-01-29T10:00:00Z"
  }
}
```

Status transitions: `active` → `merged` (finalized) or `abandoned` (deleted)

## INVOCATION PROTOCOL (CRITICAL)

Les syntaxes `@skill:epci:xxx` et `@agent:xxx` dans les step files sont **DOCUMENTAIRES SEULEMENT**.
Claude interprète les blocs de code comme des exemples, pas comme des instructions d'exécution.

**Pour invoquer réellement:**

| Type | Syntaxe documentaire | Invocation réelle |
|------|---------------------|-------------------|
| Breakpoints | `@skill:epci:breakpoint-system` | Section impérative + AskUserQuestion explicite |
| Agents | `@agent:code-reviewer` | `Task({ subagent_type: "code-reviewer", ... })` |
| Stack skills | `@skill:python-django` | `Read("src/skills/stack/python-django/SKILL.md")` |

**Règle pour auteurs de step files:**
- Utiliser le format impératif direct (pas dans bloc de code)
- Afficher les boîtes ASCII hors bloc exécutable
- Appeler AskUserQuestion explicitement
- Ajouter `⏸️ ATTENDS la réponse` après chaque breakpoint

## Limitations

This skill does NOT:
- Handle quick fixes (use /quick)
- Debug existing bugs (use /debug)
- Pure refactoring without feature change (use /refactor)
- Generate specifications (use /spec)
