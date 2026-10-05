---
name: cross-model-orchestrator
description: Coordinate two or more available AI assistants or model sessions through explicit roles, artifact handoffs, and quality gates. Use for high-risk.
---

# Cross-Model Orchestrator

Coordinate independent assistants without hard-coding provider names or assuming one model family is permanently best at a role.

## Decide Whether to Orchestrate

Use multiple models or sessions only when at least one applies:

- independent review materially reduces risk;
- tasks are separable and parallel work reduces elapsed time;
- specialist capabilities differ, such as vision, code execution, large-context reading, or a domain tool;
- a disputed decision needs evidence from independent approaches.

Stay with one capable assistant for small, tightly coupled, or low-risk work. Cross-model workflows add cost, latency, handoff loss, and privacy exposure.

## Capability Inventory

Before assigning roles, inventory only capabilities actually available in the active environment:

| Candidate | Available tools | Context/input limits | Data boundary | Cost/latency | Observed strengths | Constraints |
|---|---|---|---|---|---|---|

Do not infer quality from a provider name or version number. Prefer measured performance on the user's task, required tool access, privacy constraints, and current availability. Do not switch providers or send data to an external service without authorization.

## Workflow

### 1. Define the task contract

Write a compact contract containing:

- goal and measurable acceptance criteria;
- in-scope files, systems, and data;
- prohibited changes and external actions;
- required tests and evidence;
- final decision owner;
- shared-workspace and write-scope rules.

### 2. Assign roles by capability

Use the smallest useful set of roles:

- **Planner**: explores constraints and proposes a decision-complete approach;
- **Builder**: implements within a disjoint write scope;
- **Reviewer**: independently checks requirements, regressions, and maintainability;
- **Verifier**: reruns tests and confirms artifacts from source;
- **Breaker**: performs bounded adversarial testing for high-risk changes.

One assistant may fill sequential roles only when independence is not required. Never let the implementer be the sole reviewer of its own work.

### 3. Choose a topology

- **Sequential handoff** for coupled plan -> build -> verify work.
- **Parallel specialists** for genuinely independent subtasks with disjoint files or read-only outputs.
- **Competitive alternatives** for an uncertain design decision; compare against the same rubric.
- **Independent verification** for a finished change where implementation context should not bias review.

### 4. Define handoffs

Pass the minimum complete context. Use an existing task artifact or chat payload; do not force fixed filenames when the host provides native handoff tools.

Each handoff must include:

```markdown
Goal:
Acceptance criteria:
Inputs and source paths:
Write scope or read-only boundary:
Constraints and prohibited actions:
Required output contract:
Validation command or evidence:
Known uncertainties:
```

When agents share a filesystem, assign non-overlapping write ownership. When they do not, include exact artifacts or patches rather than references the recipient cannot access.

### 5. Apply quality gates

**Plan gate**

- assumptions are verified or clearly marked;
- acceptance criteria are testable;
- scope, migration, rollback, and risks are covered;
- the approach fits the existing codebase.

**Integration gate**

- every output matches its contract;
- overlapping edits are reconciled intentionally;
- build, typecheck, lint, and relevant tests pass;
- security and data-boundary checks match the risk;
- no unrelated user changes were overwritten.

**Final gate**

- a verifier reconstructed the result from source artifacts;
- failures and skipped checks are explicit;
- the human retains control over merge, deploy, publish, spending, and external messages.

### 6. Resolve disagreement with evidence

Classify the disagreement:

- factual: inspect source, docs, tests, or runtime output;
- requirement: return to the user-provided contract;
- design tradeoff: compare options against agreed criteria;
- risk: require a bounded experiment or choose the reversible option;
- scope: keep the original scope and log follow-up work.

Record the competing claims, evidence, decision, and residual uncertainty. A majority vote is not evidence.

## Failure Handling

- If an agent fails, preserve completed independent outputs and retry only the failed contract with corrected context.
- If outputs conflict in the same files, stop parallel writes and reconcile sequentially.
- If tool or model availability changes, reassign by capability; do not invent a replacement name.
- If cost, privacy, or authorization is unclear, pause external delegation and continue locally where safe.
- If orchestration overhead exceeds the task benefit, collapse to one coordinator plus one independent verifier.

## Final Report

Summarize role assignments, artifacts, validation results, disagreements, unresolved risks, and approximate added cost/latency. Report which checks were truly independent.
