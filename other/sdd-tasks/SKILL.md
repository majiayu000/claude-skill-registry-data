---
name: sdd-tasks
description: Pha 3 SDD — phân rã PLAN.md thành TASKS.md có ownership, dependency và verification command
user-invocable: true
---

# SDD Phase 3 — Task Decomposition (`/sdd-tasks`)

**Output language:** Mirror the invoking prompt. Canonical tokens, `@ears` references, paths and commands remain language-invariant.

Dùng `PLAN.md` đã approved để tạo `.sdd/features/{feature-slug}/TASKS.md`. Sửa Tasks approved khi Plan không đổi dùng `/sdd-update --artifact=tasks --reason="..."`.

## Parameters

- `--feature=<feature-slug>`: Required feature identifier.

## Required contract and Architecture Profile gate

Read AI Review Protocol, Intent Packet, Methodology Profile, Feature Lock, Plan consistency map, shared-contract impact, `.sdd/shared_context.md` and Architecture Profile. Tasks only implement locked scope. Each task must use approved exact paths, package/config/migration choices and exact verification command; do not substitute guessed commands. Missing binding or command blocks Tasks.

## Task sizing

An independent implementation task should generally fit about four hours. Split when work has multiple boundaries, requirements, commands, checkpoints, shared-contract/integration phases, or cannot be verified atomically. A larger task requires a Human-approved exception with dependency, integration risk, checkpoint, owner, exact command and split rationale.

## Required task record

```markdown
### T00X — <title>
- Intent reference: <Intent Packet WHAT/DoD and REQ-XXX>
- Input and expected outcome: <verifiable starting state and observable result>
- Layer and file boundary: <owned paths>
- Owner and dependencies: <human accountable owner or approved agent role; blockedBy or none>
- Estimated effort: <duration/range>
- Sizing signal: within-guideline | split-recommended | approved-exception
- Profile binding and exact verification command: <approved evidence>
- Scope category: none | <material state-change category>
- Human checkpoint: required | N/A; <review route/evidence>
- Shared contract and sync-back: <contract responsibility; /sdd-trace and /sdd-sync decision>
- High-risk review route: <approved route or N/A>
- Post-code review: required | N/A; <trigger/review route>
- Execution readiness: <single-owned | parallel-owned | sequential-handoff; approved agent role or direct; exclusive boundary>
```

## Procedure

1. Decompose tasks as Atomic, Independent and Verifiable.
2. Attach `@ears .sdd/features/{slug}/SPEC.md#REQ-XXX` to business behavior.
3. Record all required fields, including explicit human/accountable owner and execution readiness.
4. `parallel-owned` tasks cannot overlap paths, dependencies or shared-contract mutation. Shared/integration work is `sequential-handoff`.
5. `Project Ownership` does not select the execution route: solo and team both may use `direct` or `orchestrated` execution. `Execution readiness` authorizes task selection only; it is not a task execution grant. Only `/add-execute` may issue a feature- and task-bound grant after preflight, with immutable boundary and route evidence resolved from persisted governance. The named frozen-contract owner alone mutates shared contract; a sole solo Human owner may be named, while team ownership follows named delegation.
6. Record risks and create recommendation.

## DoD

- [ ] Tasks are atomic, independent or declare `blockedBy`, and verifiable.
- [ ] Each task has Intent/input/outcome/path/layer/owner/profile binding/requirement/exact command.
- [ ] Sizing signal is present; exceptions have evidence.
- [ ] Scope category, checkpoint, post-code route and high-risk route are recorded where applicable.
- [ ] Contract/sync-back and execution readiness are explicit.
- [ ] No task exceeds Feature Lock or Out of Scope.
- [ ] Human Final Review is `APPROVED` before `/add-execute`.

## AI Recommendation and Human Final Review

Record the canonical recommendation with task order, dependencies, boundaries, sizing, verification, checkpoints, review routes, contract/sync-back, execution readiness and delivery risk. Keep review `PENDING` until a human persists `APPROVED`; agents never approve task plans.

## Hướng dẫn sử dụng
- **Khi dùng:** Decompose an approved Plan into bounded, atomic, verifiable task records.
- **Không dùng:** Không dùng để dispatch, issue grants, exceed Feature Lock, or substitute guessed commands.
- **Input:** Bắt buộc `--feature`; reject missing profile/exact command/checkpoint/owner and unapproved sizing exceptions.
- **Điều kiện trước:** PLAN approved, Spec locked, consistency map, shared context and profile evidence resolve.
- **Evidence:** `TASKS.md` task records with ownership, dependencies, sizing, checkpoint, exact command, readiness and recommendation.
- **Dừng khi:** Task cannot be atomic/verifiable, boundaries overlap, contract owner missing, or required review remains pending.
- **Human quyết định:** Human approves task plan and exceptions; only `/add-execute` later issues matching grants.
- **Lệnh tiếp theo:** `/sdd-review --feature=<feature-slug> --artifact=tasks --status=APPROVED ...`, then `/add-execute --feature=<feature-slug> --all`.
- **Ví dụ:** `/sdd-tasks --feature=feat-orders` splits shared-contract integration into a sequential handoff task.

## Completion output

Use the [Completion output contract](../_shared/ai-review-protocol.md#completion-output-contract). A complete task plan with review `PENDING` is `Human decision required`; an authorized Human reviewer records the selected non-placeholder decision, reviewer identity and persisted Follow-up with `/sdd-review --feature=<feature-slug> --artifact=tasks --status=<APPROVED|REVISE|REJECTED> --decision="<human decision>" --reviewer="<authorized human reviewer>" --follow-up="<exact next command or required action>"`. `continue` only after `TASKS.md` is `APPROVED`: `/add-execute --feature=<feature-slug> --all`. Missing profile binding, exact verification command, checkpoint, ownership or frozen-contract evidence is `BLOCKED`; report the failed precondition and do not invoke execution.
