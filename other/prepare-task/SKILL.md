---
name: prepare-task
description: Convert a shaped idea or approved architecture slice into an implementation-ready task specification, preserving traceability to use cases, Business Decision Records, Architecture Design Documents, C4 views, ADRs, governance controls, and acceptance evidence. Use when preparing or reviewing a task for any repository or task system; create or update an external task only when the user authorizes that write.
---

# Prepare Task

Create a task specification that an implementation agent can execute without inventing product or architecture decisions.

## Accepted inputs

- An `$idea-task` draft for a small change that does not require formal architecture.
- Reviewed `UC-NNN` and, when applicable, reviewed/approved `BDR-NNN`.
- An approved architecture slice with `ADD-NNN`, required C4 views, and accepted ADRs.
- An existing task or issue reference plus its linked architecture evidence.

## Workflow

1. Read `AGENTS.md`, the project profile, supplied input, repository evidence, and all linked artifacts.
2. Determine task-system behavior from repository instructions. Do not assume GitHub or a specific project board.
3. Identify the smallest independently deliverable scope. Split unrelated outcomes or separately deployable changes into separate tasks.
4. Build a traceability section linking requirements, business outcomes, architecture constraints, accepted decisions, governance controls, and verification.
5. Copy [references/task-description-template.md](references/task-description-template.md) and remove irrelevant sections.
6. Ask focused questions when missing information changes scope, behavior, data handling, risk, acceptance, rollout, or rollback.
7. Mark `Ready` only when acceptance criteria are testable, blocking questions are closed, required decisions are accepted, dependencies are explicit, and applicable governance gates pass.
8. Report rather than resolve contradictions between code and approved artifacts; route them to `$review-architecture-conformance` or `$generate-adr`.
9. Create or update an external task only when the user explicitly requests or confirms the write and the target is known.

## Rules

- Do not implement code while using this skill.
- Do not copy entire architecture documents into a task; link them and extract only binding constraints.
- Do not treat a proposed ADR as binding. A task specifically created to resolve that ADR may remain ready with the decision listed as its outcome.
- Include documentation, observability, migration, rollback, security, privacy, safety, accessibility, and human-oversight work when applicable.
- Preserve repository-specific branch, worktree, versioning, validation, and release rules.
- Never include regulated records, credentials, secrets, or sensitive endpoints.

## Output

Return the task specification, readiness result, source artifacts, blockers, assumptions, governance result, and proposed destination. Clearly distinguish drafting from any authorized external write.
