---
name: execution-plan
description: "Trigger: execution plan, executable plan, deep plan. Draft one neutral plan for direct or SDD execution."
license: MIT
metadata:
  author: andresnator
  version: "1.1.1"
  status: testing
---

## Contract

Create exactly one plan for the requested outcome. The plan may be small or large. Use `assets/plan-template.md`.

## Rules

- Use short complete sentences. Keep paths, symbols, commands, URLs, technical terms, numbers, and Markdown exact.
- Omit empty sections and filler. Keep the artifact clear to a human; do not use cryptic A2A fragments inside it.
- Before writing, check the exact destination. Update an existing plan only when the user supplied its exact path or the active conversation already created or selected it. On any other slug collision, ask one closed choice: reuse the existing plan or generate a new slug. Never overwrite implicitly.
- Qualify behavior identifiers as `<capability>/<requirement>` when canonical specs matter. Use observable `WHEN` and `THEN` scenarios.
- Only for explicit delivery intent, write one `Delivery:` line immediately after the title: no commits means `working-tree`, commits means `commit-per-unit`, and TCR means `tcr`. Otherwise omit it; execution defaults to `working-tree`.
- Contradictory, duplicated, or unknown delivery requests block plan creation until resolved. Never infer delivery from a PR request, route, work group, or skill name.
- Use ordered work groups with explicit dependencies. Keep one file even when groups span sessions.
- Every work group requires `Files:` and `Skills:`. Select names with `implementation-skill-routing`; use names, never paths.
- Keep delivery skills (`tcr`, `work-unit-commits`, or other Git skills) out of `Work groups → Skills:`.
- Include one `Execution guidance` recommendation: `direct` or `SDD`. State the reason and show `ejecuta el plan <path>`.
- Write artifacts in English. Only the plan file may change; `Delivery` authorizes later execution. Never edit production code, stage, commit, or push during planning.

## Self-check

- One file contains every required section from the template.
- Every claim is evidenced or explicitly marked as an open question.
- Every task is actionable and verifiable; behavior changes do not hide in tasks.
- Every work group names its implementation skills or `none`.
- `Delivery`, when present, appears once immediately after the title and reflects explicit user language.
- Dependencies are explicit and acyclic.
- Risks contain only real rollback conditions or execution hazards.

## Resource

- `assets/plan-template.md`
