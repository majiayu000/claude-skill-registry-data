---
name: engineer-software
description: >-
  Route substantive software engineering work through the smallest evidence-driven workflow:
  close unclear requirements or plans, trace an unknown failure, run a disposable decision probe,
  deliver and verify a defined code change or refactor, inspect structural redundancy, or draft
  local work items. Use when software behavior, diagnosis, architecture, implementation, or
  acceptance evidence materially matters. Do not use for ordinary explanations, simple code
  reading, translation or formatting, or mechanical file and Git operations whose method and
  outcome are already clear.
---

# Engineer Software

Use the least workflow that can produce a trustworthy outcome. The modules below are
alternative starting modes, not phases that every task must traverse.

## Operating contract

1. Read repository instructions and inspect existing user changes before any edit.
2. Check the bypass boundary, then select the first module from the user's current uncertainty.
3. Read exactly one primary module before acting. Do not pre-read other modules; stay until its exit
   evidence closes the module or proves another is necessary.
4. Before a transition, state the closing evidence and unresolved next need, then return here and
   read only that next module. Never repeat a module or cycle without new evidence; stop with the
   blocker when another pass would only repeat questions, probes, or patches.
5. Bind completion claims to fresh evidence from the final relevant state. Label manual, missing,
   flaky, or environment-dependent evidence instead of calling it a pass.
6. Treat invented numeric policies, service levels, or compatibility promises as hypotheses, not
   recommendations. Tie a proposed default to repository or user evidence, or leave it explicitly
   unresolved for the user.
7. Reuse fresh evidence. Repeat a read, probe, or check only after relevant state changed or the
   earlier result was inconclusive.

## Bypass

Bypass this workflow and answer or act directly for factual explanations, code reading,
translation, formatting, obvious text corrections, specified reversible file operations, and
explicitly authorized mechanical Git operations. Upgrade into a module only if inspection reveals
a material software decision, unknown cause, structural risk, or nontrivial acceptance burden.

## Choose the first module

| Current need | Read |
| --- | --- |
| Outcome, behavior, scope, compatibility, or plan is materially unresolved | [Shape work](references/shape-work.md) |
| A reported symptom exists but its cause or failure mechanism is unknown | [Trace failure](references/trace-failure.md) |
| One bounded design or interaction question needs a disposable experiment | [Probe choice](references/probe-choice.md) |
| Production behavior and edit scope are closed enough to change and verify | [Deliver change](references/deliver-change.md) |
| The task is to find or assess architecture, design, policy, or implementation redundancy | [Inspect structure](references/inspect-structure.md) |
| The requested output is a local PRD, task breakdown, or triage draft | [Manage work items](references/manage-work-items.md) |

## Tie breakers

- Route an unknown cause to `trace-failure`, even when the user also asks for a fix.
- Route a known cause with a closed fix boundary directly to `deliver-change`.
- Route an assessment of structure to `inspect-structure`; route an already-approved structural
  change to `deliver-change`, which still applies its conditional structure gate.
- Use `probe-choice` only when an experiment can resolve a named decision. It is never a routine
  pre-implementation stage.
- For a mixed request, start with the earliest unresolved condition that can invalidate later work.
  Skip `shape-work` when the request and repository already close the contract.

## Shared boundaries

- Preserve pre-existing work and stay inside the requested scope.
- Inspect facts that are cheap to obtain before asking the user. Ask only when the answer can
  change visible behavior, compatibility, data, security, external state, or task scope.
- Do not add speculative abstractions, options, interfaces, migration lanes, or coordination
  machinery.
- Do not commit, push, publish, deploy, or mutate remote systems unless the user separately and
  explicitly authorizes that action.
