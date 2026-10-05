---
name: multi-agent-coordinator
description: Decompose a complex task into safe parallel and sequential agent work, assign disjoint ownership, track dependencies, reconcile outputs, and verify the.
---

# Multi-Agent Coordinator

Coordinate agents through the active host's available delegation features. Do not assume a vendor-specific agent name, tool schema, model selector, concurrency limit, or background capability.

## Delegation Gate

Delegate only when at least one is true:

- two or more independent subtasks can run concurrently;
- a large read-only investigation can return a compact conclusion;
- an isolated specialist or verifier materially reduces risk;
- context isolation prevents the coordinator from carrying bulky raw evidence.

Keep work local when it is a single file/read, highly interactive, tightly coupled, or cheaper than the coordination overhead.

## 1. Build the Task Graph

For each work item record:

| ID | Outcome | Dependencies | Read scope | Write scope | Output contract | Validation |
|---|---|---|---|---|---|---|

Mark the critical path. Parallelize only items with satisfied dependencies and no shared mutable state. Treat external services, generated artifacts, databases, package manifests, and repository configuration as shared state even when file paths differ.

## 2. Define Ownership

Each agent receives one bounded role and one completion contract:

```markdown
Goal:
Source paths and required context:
Read scope:
Exclusive write scope, or READ ONLY:
Files/state that must not change:
Expected output:
Validation command/evidence:
Failure and escalation conditions:
```

Rules:

- never assign overlapping write scopes concurrently;
- preserve user changes and inspect current state before editing;
- give reviewers read-only scope unless they are explicitly tasked with a fix;
- pass raw artifacts, not the coordinator's desired conclusion, to independent verifiers;
- do not grant broader authority than the parent task provides.

## 3. Launch by Dependency Layer

Use the host's native agent/delegation mechanism when available. Launch ready independent items together up to the actual concurrency limit. If the host lacks delegation, execute the same task graph sequentially and keep the contracts.

Do not invent tool calls. Discover the available interface and use only supported operations. Avoid forcing a named model; agent capability and tool access matter more than provider labels.

## 4. Monitor Without Duplicating Work

The coordinator owns integration, not a competing implementation of every delegated task.

- Continue useful non-overlapping local work while agents run.
- Record state as pending, running, complete, failed, or superseded.
- Send corrective context when evidence shows a misunderstanding.
- Do not repeatedly poll faster than the host supports.
- On user steering, determine whether it replaces or extends the active graph and notify affected agents.

## 5. Reconcile Outputs

For every result:

1. verify the claimed files/artifacts exist and are within scope;
2. inspect diffs and evidence rather than trusting the summary;
3. detect overlaps, incompatible assumptions, and stale-base edits;
4. integrate in dependency order;
5. rerun focused checks after each risky integration;
6. run the full relevant validation at the end.

If two agents conflict, stop concurrent edits in that area. Reconcile against requirements and source evidence; never pick a result because its author sounds more confident.

## 6. Failure Handling

- **Agent unavailable**: continue locally or reassign the same bounded contract.
- **Partial result**: retain valid artifacts and create a smaller follow-up task for the gap.
- **Wrong scope**: reject unrelated edits; do not silently integrate them.
- **Repeated misunderstanding**: refine requirements and handle the task locally after one targeted retry.
- **Shared-state conflict**: serialize the work and rebase each step on the integrated state.
- **Validation failure**: identify which integration introduced it, repair or roll back that part, then rerun checks.

## Completion Report

Report the task graph, agent roles, artifacts accepted/rejected, validation commands and results, conflicts resolved, skipped checks, residual risks, and any work that still requires user authority.

## Quality Checklist

- [ ] Delegation had a measurable speed, context, or independence benefit.
- [ ] Every agent had a bounded contract and non-overlapping write ownership.
- [ ] Dependencies and shared state were explicit.
- [ ] Integrated artifacts were inspected from source.
- [ ] Relevant tests ran after reconciliation.
- [ ] No provider, model, tool, or concurrency capability was invented.
