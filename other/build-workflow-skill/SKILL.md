---
name: build-workflow-skill
description: Use when an implementation-ready workflow task requires creating or materially updating a canonical Foundry skill, project-packaged skill, standalone product skill, or independently callable workflow-pack member.
---

# Build Workflow Skill

## Overview

Build the approved callable skill deliverable. A skill is a substantive
`SKILL.md` plus matching `agents/openai.yaml`; code, commands, helpers, apps, or
references cannot substitute for it. Leave tracker writes, phase transitions,
and publishing with the invoking lifecycle task.

Use GPT-5.6 Sol for every model-run evaluation. If it is unavailable, stop with
`eval-runner-unavailable`; never select a fallback model.

## Required Context

Read root and project policy, project state, every non-done task, the selected
task, Matt Pocock skill guidance, and the exact product repository policy when
the target is standalone. Then read:

- [the complete bundle contract](references/skill-bundle-contract.md) for
  identity, semantics, ownership variants, optional resources, and completion;
- [the behavior evaluation contract](references/behavior-evaluation-contract.md)
  for RED/GREEN isolation, evidence fields, stable failures, and release gates.

## Input Contract

Require one selected task at `matt_phase: "implement"` with approved version-1
deliverable migration, an exact create/update operation, ownership, target
surface, visibility, runtime targets, required artifacts, guidance, evals,
completion conditions, artifact bindings, and deliverable/role/artifact-bound
phase approvals. Require a complete dependency write plan for every dependency
step.

For `update`, resolve exactly one existing skill identity. Stop on zero or
multiple matches. Never invent a new slug as an update shortcut.

## Workflow

1. Ask `$continue-task` for the selected task and projected blockers. Do not
   repair tracker state here.
2. Match the contract to exactly one ownership branch: canonical Foundry,
   project-packaged, standalone product, or workflow-pack member.
   In a mixed task, select only contracts whose kind is a skill. A UI, package,
   validator, document, or tracker contract remains with its own builder even
   when its paths are separately approved.
3. Load the shared scenario contract. Confirm it separates lifecycle-intent
   routing from implementation-ready construction cases.
4. Capture a fresh first-attempt RED run without this builder. Keep the exact
   prompt, session, output, diff, and validation result.
5. Implement the smallest complete bundle permitted by the approved paths.
6. Run every required scenario variant independently with GPT-5.6 Sol in a
   clean disposable repository. Give the runner only the raw prompt and
   implementation-ready repository context—not the expected route or rubric.
7. Grade emitted contracts, file tree, contents, diff, ownership, visibility,
   catalog state, phase result, and dependency outcome. A narrative claim is
   not evidence.
8. Run deterministic bundle, routing, boundary, catalog, dependency, and
   command/helper regressions. Re-run the affected family after each fix.
9. Return evidence and readiness to the lifecycle task. Never mark it done.

## Decision Points

| Approved branch | Target | Visibility | Foundry catalog |
| --- | --- | --- | --- |
| Canonical | `.agents/skills/<slug>/` | `canonical-active` | Include when complete |
| Project packaged | `projects/<project>/skills/<slug>/` | `project-local-inactive` | Exclude |
| Standalone | Exact product-owned surface | `standalone-only` | Exclude |
| Unresolved | None | unresolved | Stop with zero writes |

Each workflow-pack member needs its own skill contract, identity, complete
bundle, and invocation. Shared files remain declared support. Promotion from a
packaged or standalone surface requires a separate contract.

Never place `SKILL.md` or `agents/openai.yaml` under a non-skill target to make
that contract look complete. In particular, do not write a skill bundle into a
UI application path; return that independent deliverable as pending.

Add optional references, scripts, or assets only when the contract declares
the exact support artifact, `SKILL.md` directly consumes it, policy permits it,
and verification covers it. Keep operator invocation as `$skill-name`.
Commands are secondary and allowed only under `Developer Verification`,
`Package Smoke Test`, `Deterministic Validation`, `Query Helper`, or `Internal
Support`.

## Failure Handling

Stop with zero new writes for pending migration; missing or contradictory
contracts; unresolved ownership; unbound approvals; ambiguous update identity;
undeclared resources; unsafe dependency or external writes; incomplete,
helper-only, thin-wrapper, command-first, or code-only bundles; unavailable
GPT-5.6 Sol; or failed deterministic, fresh-agent, security, or review gates.

Return the stable code, observed evidence, and recovery owner. Do not weaken a
contract or rewrite a failed first attempt into a pass.

## Human Boundaries

The operator approves contracts, product ownership, phase paths, external
writes, promotion, publishing, and consequential dependency actions. This
skill may write only exact task-approved paths inside the declared boundary.

## Output Contract

Return deliverable identity and ownership; primary and justified support files;
catalog result; per-scenario GPT-5.6 Sol session evidence; deterministic results;
dependency provenance; validation and review; blockers; and the lifecycle task
that owns the handoff.

## Completion Gate

Apply every check in the linked bundle and behavior contracts. Completion
requires substantive semantics, exact identities, boundary-safe artifacts,
complete per-variant attempt chains, deterministic verification, dependency
reconciliation when present, and a Standards-plus-Spec review with no critical
or high findings.

## Developer Verification

```bash
node scripts/validate-workflow-state.mjs
node scripts/query-workflow-state.mjs --skill-catalog
```
