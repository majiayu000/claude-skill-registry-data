---
name: using-forge-skills
description: Use when starting a session, when you need to discover which forge skill applies to the current task, when uncertain which skill to invoke for a request, or when a session begins and the pipeline should be loaded.
---

# Using Forge Skills

## Overview

Forge Skills is a planning-first engineering skill library. Skills encode structured workflows — not reference docs. This meta-skill maps your task to the right skill and explains the full .forge/ handoff chain.

## Skill Discovery

```
Task arrives
    │
    ├── Raw idea, not yet pressure-tested? ────────→ idea-griller
    ├── Ready to write a spec/PRD? ────────────────→ spec-driven-development
    ├── Have prd.md, need architecture? ───────────→ architecture-and-contracts
    ├── Establishing brand foundations / voice? ───→ brand-and-identity
    ├── Design REST endpoints / API contracts? ────→ api-design
    ├── Schema / migrations / query design? ───────→ database-design
    ├── Establish design tokens / component lib? ──→ design-system
    ├── Modal vs sheet / expand vs nav decisions? ─→ interaction-patterns
    ├── Catalog components before a UI sprint? ────→ component-library
    ├── Define page templates + responsive plan? ──→ page-composition
    ├── Charts / dashboards / data displays? ──────→ data-visualization
    ├── Research competitors / positioning? ───────→ competitive-analysis
    ├── Will this scale / capacity planning? ──────→ scalability-analysis
    ├── Security / compliance / PII / SOC 2? ──────→ security-and-compliance
    ├── Go-to-market / how to sell this? ──────────→ gtm-strategy
    ├── Validate decisions / get external input? ──→ cross-validation
    ├── Have architecture, need tasks? ────────────→ planning-and-task-breakdown
    ├── 3+ independent tasks, run in parallel? ────→ parallel-execution-strategy
    ├── Need realistic demo / test data? ──────────→ seed-data-and-fixtures
    ├── Define test pyramid / coverage targets? ───→ testing-strategy
    ├── Have tasks.yaml, implementing? ────────────→ incremental-implementation
    │     └── Need test-first discipline? ──────────→ tdd
    ├── Error handling / retries / resilience? ────→ error-handling-and-resilience
    ├── Logging / monitoring / alerts? ────────────→ observability
    ├── Latency / cost / LLM budgets? ─────────────→ performance-and-cost-optimization
    ├── Outage / postmortem / runbook? ────────────→ incident-response-and-postmortems
    ├── Something broke or behaves wrong? ─────────→ debugging-and-recovery
    ├── Bug triage → GitHub issue + fix plan? ─────→ triage-issue
    ├── Code ready for review? ────────────────────→ code-review-and-quality
    ├── Tech debt / refactor / rewrite plan? ──────→ refactoring-and-tech-debt
    ├── WCAG / a11y / keyboard / screen reader? ───→ accessibility
    ├── UI quality pass before demo/ship? ─────────→ visual-polish
    ├── Doc rot / README / changelog discipline? ──→ documentation-hygiene
    ├── Sales / investor demo script? ─────────────→ demo-narrative
    ├── Committing / branching? ───────────────────→ git-workflow
    ├── Deploying or launching? ───────────────────→ shipping-and-launch
    ├── Redact / prepare for external sharing? ────→ redaction-and-cleanup
    ├── Creating or editing a forge-skill? ────────→ writing-skills
    ├── Upstream artifact changed — what's stale? ─→ forge-sync
    └── Stress-testing a design? ──────────────────→ (relentless questioning — ask one branch per turn)
```

## The Forge Pipeline

```
/grill → /spec → /architect → /plan → /build → /review → /ship
```

Each stage consumes the previous stage's artifact. Join mid-pipeline if the artifact already exists. The full `.forge/` artifact chain is in `AGENTS.md` (20+ artifacts; the design phase fans out across architecture, api-design, database-design, and the UI chain brand-and-identity → design-system → component-library → page-composition + data-visualization + interaction-patterns).

The **UI skill chain** runs in order: `brand-and-identity → design-system → component-library → page-composition → data-visualization`. `visual-polish` runs after `/build`, before `/ship`.

## Agent Team

Thirteen specialist personas available via the Task tool or dispatch:

| Agent | File | When to invoke |
|-------|------|----------------|
| **Architect** | `agents/architect.md` | Designing system structure, evaluating tech decisions |
| **Platform Architect** | `agents/platform-architect.md` | Multi-product boundaries, shared vs forked decisions, deploy topology |
| **Project Manager** | `agents/project-manager.md` | Task breakdown, dependency ordering, scope management |
| **Test Engineer** | `agents/test-engineer.md` | TDD coaching, test quality review |
| **Code Reviewer** | `agents/code-reviewer.md` | PR review, contract validation, quality gates |
| **Security Auditor** | `agents/security-auditor.md` | Threat modeling, input validation, hardening |
| **Competitive Analyst** | `agents/competitive-analyst.md` | Competitor research, positioning |
| **Compliance Officer** | `agents/compliance-officer.md` | Regulatory, privacy, certifications |
| **Reliability Engineer** | `agents/reliability-engineer.md` | Errors, observability, incidents, performance |
| **Data Engineer** | `agents/data-engineer.md` | Schema, migrations, query performance |
| **QA Engineer** | `agents/qa-engineer.md` | Test strategy, quality gates |
| **Design Engineer** | `agents/design-engineer.md` | Visual system, interaction, accessibility |
| **Brand Strategist** | `agents/brand-strategist.md` | Brand identity, voice and tone, cross-product consistency |

## Core Operating Behaviors

Apply at all times, across all skills. Behaviors 1, 4, 5, and 6 are grounded in Andrej Karpathy's principles for LLM coding and his Agentic Engineering concept (Feb 2026).

### 1. Surface Assumptions *(Karpathy: Think Before Coding)*

Before implementing anything non-trivial:

```
ASSUMPTIONS I'M MAKING:
1. [about requirements]
2. [about architecture]
3. [about scope]
→ Correct me now or I'll proceed with these.
```

### 2. Manage Confusion Actively

When you encounter inconsistencies: STOP. Name the confusion. Present the tradeoff. Wait for resolution. Never silently pick one interpretation.

### 3. Push Back When Warranted

You are not a yes-machine. Name issues directly, explain concrete downside, propose an alternative, accept the human's decision if they override with full information.

### 4. Enforce Simplicity *(Karpathy: Simplicity First)*

Before finishing: Can this be done in fewer lines? Are these abstractions earning their complexity? Would a staff engineer say "why didn't you just..."?

### 5. Maintain Scope Discipline *(Karpathy: Surgical Changes)*

Touch only what you're asked to touch. Do NOT refactor adjacent code, add unasked features, delete code without approval, or remove comments you don't understand.

### 6. Verify, Don't Assume *(Karpathy: Goal-Driven Execution)*

Every skill includes a verification checklist. A task is not complete until verification passes. "It looks right" is not verification.

Full lifecycle (define → ship → operate → polish → share) and the complete `.forge/` artifact chain are documented in `AGENTS.md`. Read it for cross-phase decisions.

## Anti-Rationalization

| Thought | Why it's wrong |
|---------|----------------|
| "This is too simple for a skill" | Simple tasks are where unchecked assumptions cause the most waste |
| "I'll gather context first, then check skills" | Skills tell you HOW to gather context — check first |
| "I remember this skill" | Skills evolve. Always read the current version. |
| "The brief/PRD is close enough" | Missing artifacts break the handoff chain downstream |
| "I can skip architecture for a small feature" | Contracts protect parallel workers — skip them and work diverges |
| "Tests can come after the implementation" | Then they test implementation, not behavior |
| "I'll clean up the adjacent code while I'm here" | Scope creep disguised as helpfulness |

## Red Flags

- Starting implementation without a `.forge/prd.md`
- Writing tests after all implementation code is done
- Module list names files instead of behaviors
- Contracts written at function-level instead of module-boundary level
- Tasks in `.forge/tasks.yaml` that touch more than 2-3 modules
- PR that touches files not listed in the task's file list
- "Out of Scope" section in the PRD is empty

## Skill Rules

1. Check for an applicable skill before starting work — even a 1% chance.
2. Skills are workflows, not suggestions. Follow steps in order.
3. Multiple skills can apply — use the lifecycle sequence to choose order.
4. When in doubt, start with a spec.

