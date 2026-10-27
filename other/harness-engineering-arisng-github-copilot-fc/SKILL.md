---
name: harness-engineering
description: >-
  Design and implement harnesses for AI-agent-driven software development.
  A harness is the scaffolding—context engineering, architectural constraints,
  feedback loops, and entropy management—that enables coding agents to produce
  reliable, maintainable software at scale. Use when assessing a codebase's
  agent-readiness, building repository knowledge bases, designing layered
  architectures with mechanical enforcement, setting up application legibility
  (observability, browser automation), implementing "garbage collection" agents,
  or adopting an agent-first development workflow.
  Triggers: "harness engineering", "agent-first development", "harness",
  "agent-readiness", "agent legibility", "repository knowledge base",
  "coding agent scaffolding", "AI-maintainable codebase", "garbage collection agents",
  "context engineering for agents", "architectural enforcement", "structural tests",
  "custom linters for agents", "agent autonomy", "harness assessment".
metadata: 
  version: 1.0.0
  author: arisng
---

# Harness Engineering

Design environments, feedback loops, and control systems that enable AI coding agents to produce reliable software at scale. A **harness** is everything around the code that keeps agents effective: structured knowledge, mechanical constraints, application legibility, and entropy management.

**Core insight**: When agents struggle, the fix is almost never "try harder." Ask: *what capability is missing, and how do we make it both legible and enforceable for the agent?*

**Variant**: `harness-engineering-copilot` — strategies and patterns specialized for GitHub Copilot agent customization.

**Sources**: [OpenAI — Harness Engineering](https://openai.com/index/harness-engineering/) | [Martin Fowler — Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)

## Three Harness Components

| Component | What it does | Deterministic? |
|---|---|---|
| **Context Engineering** | Curated, structured knowledge base in the repo + dynamic context (observability, browser) | Mixed |
| **Architectural Constraints** | Layered architecture enforced by custom linters and structural tests | Deterministic |
| **Garbage Collection** | Periodic agents that detect drift, stale docs, and constraint violations | LLM-based |

## Assess Current Harness

Before building, audit what exists. Run through this checklist with the user:

1. **Repository knowledge** — Is there an `AGENTS.md` or equivalent entry point? Is it a concise map (~100 lines) or a bloated monolith?
2. **Documentation structure** — Is there a `docs/` directory with architecture, design docs, product specs, and plans? Are they versioned and cross-linked?
3. **Architectural constraints** — Are module boundaries defined? Are dependency directions enforced mechanically (linters, structural tests)?
4. **Application legibility** — Can an agent boot, drive, and observe the application (logs, metrics, traces, browser)?
5. **Feedback loops** — When the agent produces drift, is there a process to detect and correct it?
6. **CI/CD gates** — Do linters and tests catch constraint violations before merge?

Rate each 0–2 (absent / partial / enforced). Total ≤ 5 = early stage; 6–8 = developing; 9–12 = mature.

## 1. Context Engineering

The repository is the agent's only world. Anything not accessible in-context effectively does not exist.

### Repository Knowledge as System of Record

**Anti-pattern**: One giant AGENTS.md with everything. It crowds out task context, rots instantly, and is unverifiable.

**Pattern**: AGENTS.md as table of contents (~100 lines), pointing to structured `docs/`:

```
AGENTS.md              ← map, not manual
ARCHITECTURE.md        ← top-level domain + layer map
docs/
├── design-docs/       ← indexed, with verification status
│   ├── index.md
│   └── core-beliefs.md
├── exec-plans/        ← active, completed, tech-debt
│   ├── active/
│   └── completed/
├── product-specs/     ← requirements + acceptance criteria
├── references/        ← external docs, llms.txt files
├── DESIGN.md
├── FRONTEND.md
├── QUALITY_SCORE.md
├── RELIABILITY.md
└── SECURITY.md
```

**Key principles**:
- Progressive disclosure: agents start with a small stable entry point and are taught where to look next
- Plans as first-class artifacts: execution plans with progress logs checked into the repo
- Mechanical freshness: CI jobs validate the knowledge base is up-to-date, cross-linked, and correctly structured
- Doc-gardening agent: periodic background task scans for stale docs and opens fix-up PRs

### Dynamic Context Providers

Extend what agents can observe beyond static files:

- **Browser automation**: Wire Chrome DevTools Protocol (CDP) into agent runtime. Agents take DOM snapshots, screenshots, and navigate UI to reproduce bugs and validate fixes.
- **Observability stack**: Ephemeral per-worktree observability (logs via LogQL, metrics via PromQL, traces via TraceQL). Agents query: "ensure startup < 800ms" or "no span in critical journeys exceeds 2s."
- **App bootability**: Make the application bootable per git worktree so agents can launch isolated instances per task.

## 2. Architectural Constraints

Agents replicate patterns that exist in the repository — including bad ones. Mechanical enforcement prevents drift.

### Layered Domain Architecture

Divide each business domain into fixed layers with strictly validated dependency directions:

```
Types → Config → Repo → Service → Runtime → UI
                         ↑
                    Providers (auth, connectors, telemetry, feature flags)
```

- Code may only depend "forward" through the layers
- Cross-cutting concerns enter through a single explicit interface: Providers
- Enforced by custom linters and structural tests (not just conventions)

### Mechanical Enforcement

| Mechanism | Purpose | Examples |
|---|---|---|
| Custom linters | Catch violations with remediation instructions in error messages | Dependency direction, structured logging, naming conventions, file size limits |
| Structural tests | Validate architecture invariants | ArchUnit-style tests, import graph validation |
| Pre-commit hooks | Block violations before they enter the repo | Schema validation, boundary checks |
| CI validation | Catch what slips through locally | Full lint + test suite, doc freshness checks |

**Critical detail**: Write custom lint error messages that include remediation instructions. These messages become agent context when violations occur, teaching the agent how to fix issues.

### Enforce Invariants, Not Implementations

Be prescriptive about boundaries (e.g., "parse data shapes at the boundary"), but not about specific tools. Specify *what*, let agents decide *how* within boundaries.

## 3. Garbage Collection

Full agent autonomy introduces entropy. Without active management, drift compounds.

### Golden Principles

Define opinionated, mechanical rules that keep the codebase legible:
- Prefer shared utility packages over hand-rolled helpers (centralized invariants)
- Validate data at boundaries — don't probe data "YOLO-style"
- Enforce consistency in naming, logging, and error handling

### Periodic Cleanup Agents

Schedule recurring background tasks that:
1. Scan for deviations from golden principles
2. Update quality grades per domain and layer
3. Open targeted refactoring PRs (most reviewable in under a minute)

**Cadence**: Daily or per-sprint. Treat like garbage collection — continuous small increments, not painful bursts.

### Quality Scoring

Maintain a quality document that grades each product domain and architectural layer, tracking gaps over time. This gives both humans and agents a map of where debt lives.

## Agent-First Workflow

When adopting harness engineering, the development loop changes:

```
Human: Define task → Write acceptance criteria
  ↓
Agent: Validate codebase state → Implement → Self-review → Request agent reviews
  ↓
Agent: Respond to feedback → Iterate until reviewers satisfied
  ↓
Agent: Detect/remediate build failures → Escalate only when judgment required
  ↓
Merge (minimal blocking gates — corrections are cheap, waiting is expensive)
```

**Humans work at a different abstraction layer**: prioritize work, translate user feedback into acceptance criteria, validate outcomes. When agents struggle, identify what's missing and feed it back into the repo.

## Applying to Existing Codebases

Not every technique applies to brownfield code. Assess feasibility:

| Technique | Retrofit difficulty | Start here |
|---|---|---|
| AGENTS.md + docs/ structure | Low | Create entry point, incrementally document |
| Custom linters | Medium | Start with 2–3 high-value rules |
| Structural tests | Medium | Enforce module boundaries first |
| App legibility (CDP, observability) | High | Requires infra investment |
| Full garbage collection agents | High | Start with doc-gardening only |

**Pragmatic approach**: Start with context engineering (cheapest, highest ROI), add architectural constraints incrementally, garbage collection last.

## Harness as Service Template

For organizations with 2–3 main tech stacks, consider packaging harnesses as reusable templates:
- Pre-configured linters and structural tests for the stack
- Knowledge base skeleton (AGENTS.md, docs/ structure)
- CI pipeline with doc-freshness and constraint-validation jobs
- Starter golden principles for the technology

This parallels "golden path" service templates, but optimized for agent-driven development.
