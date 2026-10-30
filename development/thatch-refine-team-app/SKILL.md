---
name: thatch-refine-team-app
description: Type-specific requirements for refining a plan in a multi-developer team codebase (production app or service shared by a team). Loaded by thatch-refine after classification; assumes the core loop in thatch-plan-refinement. Use when coordination cost, consistency, and reviewer comprehension are the governing constraints.
---

You are refining a plan for a **team-app** project: production code in a
repository where multiple developers ship, review, and maintain each
other's work. The governing value is org velocity through coordination and
consistency. Code is read far more often than it is written, and most of
its readers did not write it. Load `thatch-plan-refinement` for the core
loop and apply the deltas below; where they disagree, these win.

## What this type owes

- **Consistency outranks local optimality.** Following the codebase's
  existing pattern beats a "better" one that splits the codebase in two.
  A novel approach must justify the divergence it imposes on every future
  reader, not just prove it is cleverer.
- **Implement for the junior reviewer.** The bar is that a developer with
  no history in this area can review the change and debug it at 2am.
  Cleverness is allowed only with a justification comment at the point of
  cleverness, and only when the payoff is real.
- **Intent is a deliverable.** Docstrings and comments are the breadcrumb
  trail for the next maintainer. The plan says which comments and
  docstrings it will write, and *why* is documented, not just *what*.

## How this changes the loop

- **Mode triage stays strict.** The skip threshold does not relax for
  team code: anything another developer must review earns at least quick
  mode. Established-pattern changes with no design decisions can still
  skip, as the core skill already provides.
- **Deep mode triggers broaden.** Beyond the core skill's triggers, deep
  mode is warranted when the change alters a contract other teams build
  on, or lands in an area with a history of review churn.
- **Consensus is unchanged.** Same rounds, same cap, same escalation to
  the user.

## Lens weights

- **Hidden problems (pre-mortem) carries the most signal.** In team code
  the plan's biggest risk is an unenumerated consumer or an implicit
  contract another team relies on.
- **Safe-to-modify is second.** A plan that lands in an untested,
  tangled section without a refactor-first dependency is a finding.
- **Pattern and reuse tightens.** "Reuse the existing pattern" is the
  default verdict, not one option among several. A plan that introduces a
  parallel way to do something the codebase already does needs a strong,
  evidenced reason.
- **Alternatives stays a filter.** Two alternatives, one paragraph each,
  as the core skill says; the judgment criterion is team cost, not
  personal preference.

## Extra plan sections

- **Blast radius and consumers.** Who reads the state, tables, config, and
  symbols this change touches, including other teams and services.
- **Migration and rollback.** How the change ships safely and how it
  backs out.
- **Intent breadcrumbs.** The docstrings and comments the implementation
  will write, and what future-reader question each answers.
- **Reviewer orientation.** One paragraph a reviewer can read first: what
  changed, why, and where to look.

## Docs bar

Comments and docstrings are part of the definition of done, and any
reader-facing text produced along the way (PR description, ticket,
changelog entry) is drafted under the writing skills' contracts.
