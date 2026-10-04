---
name: b-implement
description: >
  Execute approved or scoped non-UI work safely after b-plan approval,
  when a user gives a small direct request or an approved plan. Applies
  the next small step, verifies it, and hands back to planning or research
  instead of guessing when new ambiguity appears. Frontend/UI code—pages,
  layouts, components, styling, responsive behavior, interactions, or
  visual refreshes—belongs to b-frontend instead. Unlike b-plan,
  b-implement changes code. Routing signals: implement, make the change,
  apply the plan, code the fix, finish the implementation, build the
  feature.
metadata:
  phase: Build
  execution_mode: main
---

<!-- Generated from skills/registry.yaml and skills/b-implement/prompt.md. Edit those sources, not this file. -->

# b-implement

Make the scoped non-UI change in the smallest coherent step after an approved plan or clear direct request.

## When to use

- The user approved a plan or gave a small direct request.
- The next action is a scoped non-UI code or repository change.

## When NOT to use

- Scope or behavior is unclear -> use **b-plan**.
- Frontend/UI code -> use **b-frontend**.
- A named behavior-preserving transform -> use **b-refactor**.
- Test-only work -> use **b-test**.
- An unknown runtime failure -> use **b-debug**.

## Tool guidance

- Use native file tools by default and native tools or local search for routine discovery. Follow the kernel CodeGraph rule: before editing indexed code, get the target's callers, blast radius, and affected tests; use native tools for prose, config, and known-path local edits. Use only context supplied in the current task rather than guessing.

## Steps

1. Resolve the approved plan or direct request, run `rtk git status --short`, and preserve unrelated changes.
2. Before edits, consult applicable project standards, architecture boundaries, and relevant failure modes. State affected paths, invariants, observable success criteria, and relevant quality constraints. Use repository evidence, including CodeGraph impact for indexed code symbols you will change. If a material behavior or target is missing, use `ask_user_question` for the unresolved choice. Group related questions (up to four), but address independent blockers in priority order. Wait for the answer and re-evaluate. Route material external framework/API facts to targeted **b-research** rather than asking the user to supply documentation.
3. Ask the user directly only for material unresolved choices or blockers; do not delegate user decisions to a child.
4. Make the smallest coherent edit with native tools, matching the target module's local style. Remove imports/helpers made unused by it, but retain unrelated pre-existing dead code.
5. Run the narrowest useful verification. If an unambiguous in-scope defect causes failure, correct it and rerun until required verification passes. If failure reveals ambiguity, scope drift, or an unrelated issue, stop and ask or route rather than guessing. Inspect explicit non-protected changed paths.
6. Inspect every tracked and relevant untracked/derived path and diff. Apply the kernel's risk-triggered review rule to the final candidate against the task baseline after required checks pass. Direct tests/docs and faithfully regenerated outputs count with their source, not as separate subsystems; when the candidate includes regenerated outputs, run the repository's generator check to verify them. For a bounded, verified low-risk change with no trigger, finish and state why independent review was skipped under the low-risk exception. No-change tasks, including PR prose, need no changed-code review.
7. When review is required, freeze and fingerprint the exact candidate as specified by the kernel (prefer `b_candidate_snapshot` and pass its `fingerprint` plus the `include_ignored` paths it needs: the tool omits git-ignored files unless named, so name every relevant ignored/derived artifact at each checkpoint or block the fingerprint handoff and report the uncovered paths; if it is unavailable, use the manual procedure in `b-review` or block; if it reports `complete: false`, block rather than fall back to manual hashing); send baseline, acceptance, checks, paths, and identity to **b-reviewer**. Compare the identity after it returns and before normal completion. Do not edit while review is pending. A changed reviewed snapshot, missing baseline, `NEEDS FIXES`, or unaccepted follow-up requires correction, fresh checks, and new review. Missing or failed required checks, unexpected paths, and hand-edited generated outputs block completion even without review; ask the user about ambiguous acceptance, and name the closest trigger before escalating uncertain risk to review. No review automatically commits or pushes.

## Output format

Changes, verification, acceptance coverage, and deviations or gaps. Report the low-risk review exception when used; a triggered candidate requires the **b-reviewer** gate before a normal final response.

## Rules

- Stay within approved scope and use the smallest evidence-backed fit.
- Shared approval policy remains authoritative.
- Apply the kernel's risk triggers to changed candidates; no-change outputs must not initiate changed-code review.
- When **b-reviewer** returns `NEEDS FIXES`, correct only unambiguous in-scope findings, rerun checks, then request a fresh review; stop for ambiguity or scope drift.
- Never claim shipping readiness when required verification or a triggered independent review is absent.
