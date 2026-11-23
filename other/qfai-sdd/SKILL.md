---
name: qfai-sdd
title: QFAI SDD (Story Tree)
description: "Use when invoked by name or handed a QFAI work order. Its subject is the story tree: policy, business flows, stories, examples and the contracts that enforce them."
argument-hint: "[<BF-ID-or-name>] [--contract <contract-ID-or-path>] [--auto]"
allowed-tools: [Read, Glob, Write, TodoWrite, Task, Agent, Bash]
steps: [sdd-triage, sdd-flow, sdd-story, sdd-contract, common-design-md, sdd-cycle, sdd-gate]
requires: [common-review-cycle]
mode: approval-gated
---

<!-- The shipped body is the SSOT; host wrappers only link here. -->

## /qfai-sdd

Run the entry check of
`.qfai/assistant/rule/shared-skill-operating-baseline.md#workflow-run-entry-check`
first.

Turn a requirement into a checkable story tree: BF → US → AC → EX, with each BR
in the contract that enforces it.

Invoked by name, `/qfai-sdd` runs standalone, ends at SDD and creates no run. A
request to go to the end is handed to a whole run through `qfai-run`. A work
order names its own steps, and runs them as
`.qfai/assistant/rule/shared-skill-operating-baseline.md#a-plans-steps`
states.

## Inputs

- A BF ID or name limits the work to that flow and its shared dependencies. With
  no argument, every incoming requirement is triaged.
- `--contract <contract-ID-or-path>` repairs one existing contract and the flows that
  depend on it.
- `--auto` asks nothing, as
  `.qfai/assistant/rule/shared-skill-operating-baseline.md#user-questions-askuserquestion-protocol`
  states.

## Steps

Run the steps in this order, as
`.qfai/assistant/rule/shared-skill-operating-baseline.md#a-parent-skill-invoked-by-name`
states: read `.qfai/assistant/step/<id>/STEP.md` for the current step only, run
it, then move to the next.

| Step               | What it does                                                    | Skipped when                                               |
| ------------------ | --------------------------------------------------------------- | ---------------------------------------------------------- |
| `sdd-triage`       | Source, preflight, triage, critical decisions and ID allocation | Never                                                      |
| `sdd-flow`         | Policy, `tech.md` and business flows                            | Triage changed no policy fact and no flow                  |
| `sdd-story`        | Stories, Gherkin AC and EX                                      | Never                                                      |
| `sdd-contract`     | Contracts and the BRs they enforce, or the `--contract` repair  | Triage changed no BR and no contract                       |
| `common-design-md` | Root `DESIGN.md`                                                | The flow is not UI-bearing, or its surface is CLI-only     |
| `sdd-cycle`        | The concrete-abstract cycle between BRs and EXs                 | `sdd-contract` wrote or changed no BR Statement or Example |
| `sdd-gate`         | Per-flow `validate --profile sdd` and the flow report           | Never                                                      |

`sdd-triage` records whether each affected flow is UI-bearing. A step that
changes an input an earlier step consumed reruns that step's authors and
reviewers.

## Review

After the last step, run one review with `common-review-cycle`, one affected
business flow at a time: the specification review, by `requirements-reviewer`,
joined by `architecture-reviewer` when a contract changed and by
`product-surface-reviewer` for a UI-bearing flow.
What they check is the `## Review` section of `sdd-gate`. Roles are selected
under `.qfai/assistant/rule/shared-skill-delegation-baseline.md`.

## Completion

A flow is complete when its `sdd-gate` passed and every finding of the
specification review is fixed or answered. When a step needs user input or cannot proceed, record the
question as a row of `open-questions.md` and report what the stage waits on.

Report the source selected, BF and US IDs touched, decision and OQ IDs, contract
files and index rows, each per-flow validation result and log, independent
reviewer verdicts, adopted grilling decisions, rejected options still excluded,
and remaining questions. The next implementation route is `/qfai-implement`; UI work
may pass through `/qfai-prototyping` first. Ask about those next actions only
when proceeding requires the user's answer, as `.agents/rules/user-questions.md`
§ 6 sets out. A completion-only report needs no question. Under a no-question
mode, list any remaining actions instead.

## Default Autopilot Policy

- hard-required: a usable requirement source,
  an identifiable affected flow or an explicit decision to create one,
  and product brand intent when a root `DESIGN.md` is required.

project_memory:

- The story tree is BF → US → AC → EX ← BR.
- Every EX cites one AC; every AC and BR has an EX; every EX has a BR.
- Every spec document takes its template's shape and nothing more.
- Gate each touched BF separately with `--flow BF-NNNN`.
