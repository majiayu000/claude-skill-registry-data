---
name: analysis-code-conventions
description: >
  Owner's conventions for readable analysis code. Use when creating, reviewing,
  or refactoring 02_analysis; deciding what belongs in stages, helpers, config,
  or notebooks; grouping helper families behind provisional APIs; designing
  restartable data flow; assessing package-readiness; or writing R and Python
  to house idiom.
---

# Analysis Code Conventions Router

Use this skill for decisions inside analysis code -- structural, and at the level of the line. 
Apply the CRAFT Code shape contract first; 
this router selects the qualitative guide needed for the decision at hand. 

Exact file matching, thresholds, exemptions, and finding behavior remain owned by `lib/scio/lint.sh`.

## Before writing code

Use these questions as a pre-flight checklist:
1. Does durable state for this computation already exist?
2. Is this a compute stage or its visualization twin?
3. Does one place already own this parameter, colour, or threshold?
4. Can an existing helper or toolkit function do this?
5. Will the output be consumed across languages, and does that set its format?
The routing tree and its references carry the answers.

## Routing decision tree

```text
What decision is being made?
│
├─ Should this code remain visible in the stage?
│     → stage-narrative.md
│
├─ Does this machinery need one helper or a cohesive helper family?
│     → helper-family-apis.md
│
├─ Where should state, checkpoints, and cross-stage contracts live?
│     → restartability-and-dataflow.md
│
├─ Has a project helper become an independent library candidate?
│     → promotion-readiness.md
│
└─ How is the line itself written -- naming, progress, failure, paths?
      → language-style.md
```

## Routing contract

1. Read the repository's rendered CRAFT block and preserve its Code shape contract. 
2. Identify the structural decision being made and load the corresponding
   reference completely before editing code or proposing a layout.
3. Load multiple references when a change crosses boundaries, such as extracting
   stage machinery into a family that may also need a durable checkpoint.
4. Use the reference for judgment and review methods. Use `scio lint` for the
   executable checks and respond to its current diagnostics as written.
5. Defer assay formats, scientific thresholds, figure design, notebook behavior,
   teaching stance, and deployment to the skills or project context that own them.

## References (load on demand)

| Decision | Load | Outcome |
|---|---|---|
| What a reviewer must see in the stage | [`references/stage-narrative.md`](references/stage-narrative.md) | A readable story-order stage |
| Flat helper or cohesive family; public boundary | [`references/helper-family-apis.md`](references/helper-family-apis.md) | A small named API with reviewable internals |
| Restart boundaries and cross-stage data flow | [`references/restartability-and-dataflow.md`](references/restartability-and-dataflow.md) | Explicit state and resumable execution |
| Independent repository candidacy | [`references/promotion-readiness.md`](references/promotion-readiness.md) | A keep-local or promote decision |
| Naming, progress and failure idiom, paths, documentation | [`references/language-style.md`](references/language-style.md) | Code that reads as house R or house Python |

## Boundary routes

- Use `figure-style` for figure design, saving, and caption contracts.
- Use the relevant assay skill for data objects, scientific methodology, and
  domain-specific deliverables.
- Use `notebook-exploration` to look at what a stage produced, live in Python or
  as a rendered Quarto review; use `notebook-annotation` for a multi-round
  relabelling campaign.
- Use `architecture-first-dev` for software architecture campaigns, ADRs, and
  multi-stage implementation planning.

## When not to use

- A one-off exploratory notebook with no durable analysis-code boundary.
- A purely scientific choice whose code placement is already settled.
- A request to add or change lint predicates; lint design needs separate evidence.
