---
name: epci:implement-auto
description: >-
  Headless EPCI workflow for autonomous feature implementation via claude -p.
  Executes Explore-Plan-Code-Inspect without interaction. Produces incremental JSON output.
  3-level circuit breaker protects against token-burning. TDD enforced per component.
  Uses @planner, @plan-validator, @code-reviewer, @security-auditor, @qa-reviewer and stack skills
  for quality parity with interactive /implement.
  Use when: automated pipeline, headless execution, CI/CD.
  Triggers: pipeline automation, cron job, autonomous implementation, batch processing.
  Not for: interactive development (use /implement), quick fixes (use /quick), debugging (use /debug).
user-invocable: true
argument-hint: "<feature-slug> [@<spec-path> | @<plan-path>] [--worktree] [--skip-plan-validation] [--skip-review] [--skip-security] [--skip-qa] [--skip-publish] [--auto-merge]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
---

# implement-auto

Headless EPCI skill for autonomous feature implementation without user interaction.
Functionally equivalent to `/implement` — same subagents, stack skills, and review depth — with zero breakpoints.

## Quick Start

```bash
# With spec (full EPCI workflow, in-place)
claude --dangerously-skip-permissions -p "/implement-auto feature-slug @path/to/spec.md"

# With worktree isolation (isolated git worktree)
claude --dangerously-skip-permissions -p "/implement-auto feature-slug @path/to/spec.md --worktree"

# With plan (skip Explore + Plan phases)
claude --dangerously-skip-permissions -p "/implement-auto feature-slug @.claude/plans/feature-plan.md"

# With all quality gates disabled (fast mode)
claude --dangerously-skip-permissions -p "/implement-auto feature-slug @spec.md --skip-plan-validation --skip-review --skip-security --skip-qa"
```

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| `feature-slug` | Yes | Kebab-case feature identifier |
| `@spec-path` | Yes* | Path to spec/PRD file (Markdown). *Required unless @plan-path provided |
| `@plan-path` | No | Path to Claude Code plan (.claude/plans/*.md). Skips Explore + Plan phases |
| `--worktree` | No | Enable git worktree isolation. Default: disabled (work in-place) |

### Input Detection

```
INPUT
├── @.claude/plans/*.md → PLAN-FIRST workflow (skip E-P)
│   └─ Plan already done, go directly to CODE
├── @docs/specs/*.md or @*.md → SPEC-FIRST workflow (full E-P-C-I)
│   └─ Full Explore + Plan phases
└── No path → ERROR (spec or plan required in headless mode)
```

## Output

JSON file at `.implement-auto-output.json` in the working directory. See [references/output-json-schema.md](references/output-json-schema.md).

Status values: `SUCCESS`, `PARTIAL`, `FAILED`.

## MANDATORY EXECUTION RULES:

- NEVER call AskUserQuestion (headless mode)
- NEVER call EnterPlanMode
- NEVER display ASCII breakpoint boxes
- NEVER wait for user input
- ALWAYS write JSON output at each step transition
- ALWAYS follow step order sequentially
- ALWAYS enforce TDD per component (RED-GREEN-REFACTOR)
- ALWAYS apply circuit breaker rules on failure
- ALWAYS load stack skills per file extension before implementation
- FOCUS on autonomous execution from start to finish

## Workflow

```
step-00-init-auto     Parse args, complexity detection, branch setup (+ worktree if --worktree), Feature Doc, JSON init
       |
       ├── @plan-path provided? → Skip to step-03-code-auto
       |
step-01-explore-auto  Explore codebase + sanity check (30% threshold)
       |
step-02-plan-auto     @planner + @plan-validator + implementation plan
       |
step-03-code-auto     TDD implementation + stack skills + circuit breaker + background reviewer
       |
step-04-review-auto   Self-review + @code-reviewer + @security-auditor + @qa-reviewer
       |
step-05-document-auto Feature Document completion + executive summary
       |
step-06-finish-auto   Final validation, commit, index.json update, status determination
       |
step-07-output-auto   Final JSON write
       |
step-08-publish-auto  Push branch, create PR, cleanup worktree (if --worktree)
```

## EXECUTION PROTOCOLS:

1. **Load** step-00-init-auto.md
2. **Execute** current step protocols completely
3. **Write** JSON output after step completion
4. **Evaluate** circuit breaker conditions
5. **Proceed** to next_step or abort if circuit breaker triggers

## Subagents

| Agent | Model | Step | Default | Skip Flag |
|-------|-------|------|---------|-----------|
| Explore | Haiku | 01 | Always | - |
| @planner | Sonnet | 02 | Always | - |
| @plan-validator | Opus | 02 | Always | `--skip-plan-validation` |
| @code-reviewer | Opus | 03 (background) + 04 | Always | `--skip-review` |
| @security-auditor | Opus | 04 | Conditional* | `--skip-security` |
| @qa-reviewer | Sonnet | 04 | Conditional** | `--skip-qa` |

\* Triggered when auth/security patterns detected OR complexity is LARGE.
\** Triggered when >3 acceptance criteria OR >5 components OR complexity is LARGE.

## Stack Skills

Dynamic per-file loading via domain-mapping. See [references/domain-mapping.md](references/domain-mapping.md).

| Extension | Stack Skill |
|-----------|-------------|
| `*.py` | python-django |
| `*.php` | php-symfony |
| `*.java` | java-springboot |
| `*.tsx`, `*.jsx`, `*.ts`, `*.js` | javascript-react |
| `*.css`, `*.scss`, `*.html` | frontend-editor |

Each stack skill is loaded once per type (cached). Provides architecture patterns, testing conventions, and anti-patterns.

## Circuit Breaker (3 Levels)

| Level | Scope | Threshold | Action |
|-------|-------|-----------|--------|
| 1 | Component | 2 retries | Mark FAILED, skip to next |
| 2 | Task | 3 consecutive OR >50% | ABORT task, status FAILED |
| 3 | Timeout | External (orchestrator) | Kill process, read partial JSON |

See [references/circuit-breaker-rules.md](references/circuit-breaker-rules.md).

## TDD Rules

Self-contained TDD workflow: RED -> GREEN -> REFACTOR -> VERIFY.
Coverage targets adapt to complexity: STANDARD (70%/60%), LARGE (80%/70%).
See [references/tdd-rules.md](references/tdd-rules.md).

## Review Pipeline

1. **Self-review** (always): Automated grep-based checks (tests, code quality, architecture, security basics)
2. **@code-reviewer** (default): Deep Opus analysis — quality, tests, performance, architecture, plan alignment
3. **@security-auditor** (conditional): OWASP Top 10 — triggered on auth/security patterns or LARGE complexity
4. **@qa-reviewer** (conditional): Acceptance criteria, edge cases, error handling — triggered on >3 AC or >5 components

See [references/review-checklist.md](references/review-checklist.md).

## Steps

| Step | Name | Phase | Description |
|------|------|-------|-------------|
| 00 | init-auto | - | Parse args, complexity detection, branch setup (+ worktree if --worktree), Feature Doc, JSON |
| 01 | explore-auto | [E] | Explore + sanity check (skippable via @plan-path) |
| 02 | plan-auto | [P] | @planner + @plan-validator (skippable via @plan-path) |
| 03 | code-auto | [C] | TDD + stack skills + circuit breaker + background reviewer |
| 04 | review-auto | [I] | Self-review + @code-reviewer + @security-auditor + @qa-reviewer |
| 05 | document-auto | - | Feature Document + summary |
| 06 | finish-auto | - | Finalization + commit + index.json update |
| 07 | output-auto | - | Final JSON output |
| 08 | publish-auto | - | Push, PR, worktree cleanup (if --worktree) |

## Step Files

- [steps/step-00-init-auto.md](steps/step-00-init-auto.md)
- [steps/step-01-explore-auto.md](steps/step-01-explore-auto.md)
- [steps/step-02-plan-auto.md](steps/step-02-plan-auto.md)
- [steps/step-03-code-auto.md](steps/step-03-code-auto.md)
- [steps/step-04-review-auto.md](steps/step-04-review-auto.md)
- [steps/step-05-document-auto.md](steps/step-05-document-auto.md)
- [steps/step-06-finish-auto.md](steps/step-06-finish-auto.md)
- [steps/step-07-output-auto.md](steps/step-07-output-auto.md)
- [steps/step-08-publish-auto.md](steps/step-08-publish-auto.md)

## Reference Files

- [references/tdd-rules.md](references/tdd-rules.md) — TDD workflow (self-contained)
- [references/circuit-breaker-rules.md](references/circuit-breaker-rules.md) — Circuit breaker logic
- [references/output-json-schema.md](references/output-json-schema.md) — JSON output contract
- [references/review-checklist.md](references/review-checklist.md) — Review checklists (self-review + code + security + QA)
- [references/feature-document-template.md](references/feature-document-template.md) — Feature Document template
- [references/domain-mapping.md](references/domain-mapping.md) — File extension to stack skill mapping

## Flags

| Flag | Default | Effect |
|------|---------|--------|
| `--worktree` | Off | Enable git worktree isolation. Without this flag, works in-place on current directory |
| `--skip-plan-validation` | Off | Skip @plan-validator invocation (plan still created by @planner) |
| `--skip-review` | Off | Skip @code-reviewer, keep self-review only |
| `--skip-security` | Off | Skip @security-auditor even if patterns detected |
| `--skip-qa` | Off | Skip @qa-reviewer even if threshold met |
| `--skip-publish` | Off | Skip push, PR creation, and worktree cleanup |
| `--auto-merge` | Off | Squash-merge PR immediately (SUCCESS only, PARTIAL keeps draft) |

## Conventions

The skill loads stack skills dynamically based on file extensions for architecture patterns and testing conventions.
It also uses the target project's CLAUDE.md and .claude/rules/ for project-specific conventions.

## Limitations

- No interactive breakpoints (by design)
- No team mode / multi-agent orchestration (background reviewer serves similar purpose)
- Timeout managed externally by orchestrator
- Auto-merge requires gh CLI installed + merge permissions
