---
name: workflow-router
description: Routes a software-work request to the smallest applicable delivery workflow and records repository conventions once. Use when a user asks what engineering workflow to follow, wants help starting a change, needs a release or blocker path, or says setup workflow.
argument-hint: "<situation, or setup>"
---

# Workflow Router

Use this as the entry point; downstream skills own their detailed instructions.

## Route

Classify the request, choose only the matching sequence below, and state each transition rationale in one line. Do not add steps from another route unless its trigger is present. In an unfamiliar repository, perform repository reconnaissance first (inspect structure, README/CONTRIBUTING, build/test framework, CI, recent git log, and existing patterns per `AI_ENGINEERING_WORKFLOW.md`).

### Idea to staging

#### Vague but issue-sized request

- Vague or decision-heavy request that clarification resolves into one independently verifiable issue: `clarify-work` → `define-done`.
- Transition rationale: clarify creates a safe boundary; define-done makes success testable; a single bounded issue needs no decomposition or durable spec.

#### Broad or multi-issue request

- Broad request that will not fit one independently verifiable issue even after clarification (several independent slices, unsettled cross-cutting decisions, a durable spec the team will reference across issues): `clarify-work` → `to-prd` → `decompose-to-issues`.
- Transition rationale: clarify creates a safe boundary; `to-prd` drafts and publishes the durable spec the multi-issue breakdown depends on; decomposition protects independent delivery.

#### Concrete single behavior change

- Concrete single behavior change: define done → `test-driven-development` test-first change → `code-simplification` on the changed code → `review-gate` → staging PR.
- Transition rationale: the request is already bounded, so clarification and decomposition add no value; tests prove behavior before review.

#### Claimed non-trivial GitHub issue

- Sequence: `subagent-pipeline` → CI → staging PR.
- Transition rationale: a claimed non-trivial GitHub issue has an issue-sized boundary, so the pipeline supplies independent implementation, review, and CI evidence.

### Bug or regression

- Sequence: diagnose → regression test → smallest fix → `review-gate`.
- Transition rationale: reproduce and isolate before changing code; retain the failing case as proof; review checks regressions after the fix.

### Release

- Sequence: `release-gate`.
- Transition rationale: release needs a reviewed artifact, target, health signal, and rollback path rather than a new implementation workflow.

### Human-held blocker

- Sequence: `hitl-blocker`.
- Transition rationale: missing credentials, DNS, billing, permissions, or approval require a visible owner and verification command, not repeated automation.

### Standalone tools

- `clarify-work` for unclear scope; `define-done` for acceptance criteria on a single bounded issue; `to-prd` for a durable spec a multi-issue plan will reference; `decompose-to-issues` for a multi-issue plan; `review-gate` before merge; `handover` at a context boundary.
- Use `subagent-pipeline` only for a claimed non-trivial GitHub issue. Its CI gate ends with the appropriate staging PR.

## Run-once setup

When invoked as `workflow-router setup`, inspect before proposing anything:

1. Tracker: GitHub remotes, issue/PR templates, and local tracker files.
2. Delivery: target branch from remote/default-branch configuration and existing CI workflows.
3. Labels: existing issue labels and any documented label vocabulary.
4. Project context: `docs/` layout, ADRs, and existing `AGENTS.md`, `CLAUDE.md`, or equivalent instructions.
5. Verification: test commands, runtime/container instructions, and test-storage constraints.

Report detected conventions and gaps, then show a file-by-file proposed edit or command. Ask for approval before writing any instruction, config, label, or tracker change. Never overwrite or replace existing instructions; add only an approved, conflict-free change, or report the conflict for a human decision.

## Setup output

Return: detected tracker; target branch; labels; docs/instruction files; test/runtime command; proposed changes; and `Approval required: yes/no`. `yes` is mandatory whenever a change is proposed.
