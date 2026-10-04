---
name: task-decomposer
license: Apache-2.0
description: >-
  Turn a stated outcome into a reviewable task graph with deliverables, decision/unknown
  nodes, typed dependency reasons, and authority gates. It plans work; it does not execute,
  schedule, or prove that a DAG can run concurrently. NOT for runtime orchestration or granting effect authority.
allowed-tools: Read,Grep,Glob
argument-hint: '[problem-description]'
metadata:
  category: Agent & Orchestration
  tags: [task, decomposer, decompose-task, break-down-problem, plan-workflow]
  pairs-with:
    - skill: dag-planner
      reason: Converts validated node/edge requirements into a graph representation.
    - skill: human-gate-designer
      reason: Defines authority required before irreversible actions.
---

# Task Decomposer

## Status and boundary

This is a first-party planning scaffold. It preserves phase, dependency, vagueness, and decision workflows from the inherited skill. Domain labels are prompts for investigation, not keyword routing: a mixed request can have research, product, data, and operational concerns. A planned DAG represents prerequisite claims; it is neither an execution trace nor proof of parallel safety.

Use an HTN only when a task-network formalism with primitive tasks, method applicability, preconditions, effects, and solution semantics is actually supplied. This skill does not supply those semantics. See [method boundaries](references/method-boundaries.md).

## Decomposition procedure

### 1. Write an outcome contract

State the observable deliverable, acceptance evidence, hard constraints, authority boundary, irreversible actions, and unknowns. Do this before proposing phases or domain treatments.

For each unknown that can change downstream work, create an evidence or decision node with a named output. “Resolve Node 3” is not a task. `choose-storage` becomes a valid decision node only when its inputs, decision record, output, and consumers are named.

### 2. Propose phases as a hypothesis

Use domain treatment as a hypothesis, not a classifier result. A software-shaped request may include contract, decision, implementation, test, approval, and verification phases; a research request may include question, source collection, analysis method, synthesis, and review. Merge trivial reads into the deliverable they support; split a node when its output/acceptance evidence cannot be stated coherently.

### 3. Add typed dependency reasons

For each edge, name one reason and the required producer output:

- `data`: consumer needs a versioned value or artifact.
- `decision`: consumer needs a decision record and rationale.
- `evidence`: consumer needs a test, research, or review receipt.
- `authority`: an approval must exist before an irreversible action.

A shared input is not an edge by itself. Two nodes are only *candidates* for concurrent work after their inputs, write/effect sets, resources, authority, and semantic coupling are examined.

### 4. Classify commitment honestly

- `concrete`: inputs, output, acceptance check, and dependencies are known.
- `evidence-gathering`: output reduces a named uncertainty.
- `decision`: produces a choice/rationale that changes consumers.
- `deferred`: a future node whose contract cannot yet be fixed.
- `human-gate`: records required authority; it is not satisfied by intent.

No confidence score is a probability unless calibration data, outcome definition, and validation set are stated. Record confidence as a qualitative planning assessment or abstain and add an evidence node.

### 5. Hand-check the graph

Run a topological check, verify each typed edge names an existing producer output, and inspect every candidate-concurrent pair for conflicts. [02-typed-edge-check.md](diagrams/02-typed-edge-check.md) separates graph layers from actual admission.

## Worked example: URL shortener

| ID | Kind | Output / acceptance | Depends on |
|---|---|---|---|
| `contract` | concrete | Versioned endpoint/response contract artifact reviewed | — |
| `choose-storage` | decision | Storage decision record with evidence | — |
| `implement` | concrete | Versioned implementation satisfying contract | `contract` (data), `choose-storage` (decision) |
| `test` | evidence-gathering | Passing test receipt tied to implementation digest | `implement` (data) |
| `approve-release` | human-gate | Release approval bound to the implementation digest and test receipt | `test` (evidence) |
| `deploy` | concrete | Deploy receipt | `implement` (data), `test` (evidence), `approve-release` (authority) |
| `verify` | evidence-gathering | Observed endpoint result tied to deploy receipt | `deploy` (data) |

`contract` and `choose-storage` may be worked in parallel only if the storage investigation is constrained not to redefine the API contract. The inherited `api-spec -> data-model` edge and its claimed parallelism were contradictory; this example makes the decision dependency explicit. The deploy contract requires the versioned implementation artifact and matching test/approval receipts. A missing receipt or mismatched subject digest fails that declared contract; this plan does not enforce it at runtime.

## Diagnostics

| Observation | Repair |
|---|---|
| A node says “resolve” without a deliverable | Split it into evidence and/or decision nodes with outputs and consumers. |
| A cycle appears | Find the mutually required facts; introduce an earlier evidence/decision boundary or a deliberate iterative contract. |
| “Parallel” is justified only by no shared input | Review effects, writes, resources, authority, and semantic/API coupling before treating it as an admission candidate. |
| A numerical complexity/cost threshold decides a route | Label it local policy and expose an abstain/research path; do not call it evidence. |
| A downstream action lacks an acceptance receipt | Keep it blocked; a plan or dispatch is not success. |

## References and diagrams

- [Method boundaries and HTN contrast](references/method-boundaries.md)
- [URL-shortener graph fixture](examples/url-shortener-fixture.md)
- [Outcome-to-node procedure](diagrams/01-outcome-to-nodes.md)
- [Typed edges and admission check](diagrams/02-typed-edge-check.md)

## NOT-FOR boundaries

Do not use this skill to execute nodes, choose a runtime schedule, assign skills as a proof of adequacy, or authorize deployment. Those require their own contracts and evidence.
