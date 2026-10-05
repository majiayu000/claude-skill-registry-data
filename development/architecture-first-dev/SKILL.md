---
name: architecture-first-dev
description: >-
  Architecture-first software router for feature, portfolio, and retrospective
  audit workflows. Use for non-trivial features, refactors, or redesigns where
  upfront design pays off; cross-cutting concerns needing multiple expert
  lenses; or work where scientific reasoning matters as much as structure.
  Covers planning, handoff, verification, and MADRs.
---

# Architecture-First Development Router

Use one entry point for the architecture-first workflow. Keep this file as the routing spine and load the complete stage specification from `references/` only when that stage is selected.

The canonical sequence and worked examples live in [`00-quickstart.md`](../../docs/workflows/architect/00-quickstart.md). The canonical rationale and component model live in [`01-architecture.md`](../../docs/workflows/architect/01-architecture.md). Read the quickstart for navigation questions, stage transitions, and after-stage tips; read the architecture document when the pipeline shape or responsibility boundaries are at issue.

## Routing decision tree

```text
What does the user need?
│
├─ Orientation, current state, or "what next?"
│     → status
│
├─ One feature or refactor
│  │
│  ├─ Need codebase cartography
│  │     → map
│  ├─ Need independent or iterative expert lenses
│  │     → review
│  ├─ Need consensus across two or more reviews
│  │     → synthesize
│  ├─ Need architecture, behavior, and ADRs
│  │     → design
│  ├─ Need a fresh consistency verdict on existing design files
│  │     → architect
│  ├─ Need phased decomposition of an approved feature design
│  │     → plan
│  ├─ Need implementation of an existing plan
│  │     → external implement command
│  ├─ Need plan/design-to-code drift verification
│  │     → verify
│  └─ Need a consolidated Mermaid view
│        → diagram
│
├─ Two or more related features with shared touch-points
│     → portfolio/meta workflow
│
├─ Large multi-artifact work whose decomposition needs its own campaign
│     → external decompose command, then external implement command
│
└─ Retrospective cross-cutting architecture audit requested by the user
      → probationary architecture-treemap audit stack
```

Follow the canonical cadence when state permits:

```text
map → review → synthesize → design → plan → implement → verify
```

`review` and `synthesize` remain conditional. `architect`, `diagram`, and `status` are utility routes. The portfolio layer wraps related per-feature work; the audit stack is a separate retrospective route.

## Routing contract

1. Inspect the request and existing artifacts, select one route, and read its complete specification before acting.
2. Pass the invocation arguments through unchanged. Skills support `$ARGUMENTS`, `$ARGUMENTS[N]`, and `$N`; bind every positional index, remainder, flag, default, rejection, and usage message exactly as the loaded specification defines it.
3. Treat the loaded reference as authoritative for phases, tools, outputs, gates, and stop conditions. Preserve every human judgment gate.
4. Read upstream artifacts named by the selected stage. Honor the no-re-exploration and scribe-on-latest rules carried by the stage specifications.
5. After a stage completes, read the matching tips in `00-quickstart.md` and surface the relevant next route.
6. Keep implementation and large-campaign decomposition at their external command boundaries. Load [`commands/implement.md`](../../commands/implement.md) for implementation and [`commands/decompose.md`](../../commands/decompose.md) for multi-agent decomposition; their own argument contracts control those routes.

## Per-feature references (load on demand)

| Intent | Load | Argument entry |
|---|---|---|
| Build or refresh feature cartography | [`references/map.md`](references/map.md) | `$ARGUMENTS[0]` slug/path; `$ARGUMENTS[1+]` context |
| Run reviewer lenses or an iterate round | [`references/review.md`](references/review.md) | `$ARGUMENTS[0]` slug plus `--as`, `--but`, `--iterate` |
| Collapse two or more reviews | [`references/synthesize.md`](references/synthesize.md) | `$ARGUMENTS[0]` slug |
| Draft and gate the feature design | [`references/design.md`](references/design.md) | `$ARGUMENTS[0]` slug; `$ARGUMENTS[1+]` design notes |
| Re-run the standalone architecture gate | [`references/architect.md`](references/architect.md) | `$ARGUMENTS[0]` slug; `$ARGUMENTS[1+]` redirects |
| Decompose an approved feature design | [`references/plan.md`](references/plan.md) | `$ARGUMENTS[0]` slug |
| Check implementation drift | [`references/verify.md`](references/verify.md) | `$ARGUMENTS[0]` slug; `$ARGUMENTS[1+]` phase scope |
| Consolidate feature Mermaid diagrams | [`references/diagram.md`](references/diagram.md) | `$ARGUMENTS[0]` slug |

## Portfolio, audit, and boundary references (load on demand)

| Intent | Load | Scope |
|---|---|---|
| Produce a fast portfolio snapshot | [`references/status.md`](references/status.md) | `$ARGUMENTS` optional comma-separated slugs |
| Map, design, apply, or sequence a related feature portfolio | [`references/portfolio.md`](references/portfolio.md) | Full `/meta-map`, `/meta-design`, `/meta-apply`, and `/meta-plan` specifications; `$ARGUMENTS` scope survives intact |
| Run the retrospective architecture-treemap stack | [`references/architecture-treemap-audit.md`](references/architecture-treemap-audit.md) | Full `/components-extract`, `/audit-slice`, `/synthesize-audit`, and `/architecture-treemap` specifications |
| Execute an implementation plan | [`commands/implement.md`](../../commands/implement.md) | External command; preserve its `$ARGUMENTS` and flags |
| Run large-campaign decomposition | [`commands/decompose.md`](../../commands/decompose.md) | External command; preserve its `$ARGUMENTS` and flags |

`status.md` is intentionally separate from the portfolio blob because its frontmatter-and-grep snapshot is a narrow, fast orientation path.

## When not to use

- Do not use for one-line fixes, throwaway scripts, or exploratory data analysis.
- Do not use to run a bioinformatics analysis pipeline. Use the assay or interpretation skill that matches the data and question.

## Audit-stack status

The architecture-treemap audit stack is **retrospective and probationary**. Its prune review is due **2026-11-20**. Keep it off the navigation autopilot: `/audit-slice` requires concerns authored by the user, and the complete audit blob controls the refusal, provenance, validation, and rendering contracts.
