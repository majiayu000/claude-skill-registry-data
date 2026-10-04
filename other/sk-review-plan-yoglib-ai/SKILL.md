---
name: sk-review-plan
description: Read-only review of a technical plan. Use when sk-planning has drafted a plan, or the user passes a plan and asks for a review.
---

# Plan Review

Evaluate a technical plan before implementation. Flag correctness blockers, gaps, and unnecessary complexity.

## When to use

- After `sk-planning` writes a draft.
- When the user pastes a plan and asks for a review.
- Before presenting a masterplan or sub-plan to a stakeholder.

## Input

Paste the full plan text into the prompt. Do not point the subagent at plan files. Include repo constraints, user scope, masterplan ↔ sub-plan linkage (if split), and known validation gaps.

## Output contract

Return ONLY the findings block. No prose intro.

```text
Output ONLY in this format (no prose intro, no sections swapped).

### Plan Review Findings

section:line: <emoji> <tag>: <problem/over-engineering>. <fix/replacement>.
totals: N🔴 N🟡 N✂️ N🪵 N⚡ N🔵 N❓ | net: -<N> lines/steps possible

Or exactly when no findings:

### Plan Review Findings

Lean & valid. Ship.

Rules for Plan Review Findings:
- Sort findings section → line ascending
- One finding per line; problem then fix separated by ". "
- Location: section = exact ## heading name; line = line number within that section (1-based from heading line), or — when issue spans whole section
- Action tags (literal after colon):
  - 🔴 bug: correctness blocker, contradiction, broken logic, missing critical step
  - 🟡 gap: weak testability, missing file/dependency, unclear sequencing, unmitigated risk
  - ✂️ cut: redundant prose, duplicate information, speculative task not required for goal (replacement: nothing)
  - 🪵 yagni: over-engineered scaffolding, premature generalization, unnecessary abstraction (replacement: inline or drop)
  - ⚡ simplify: over-complicated sequencing, multi-tier nesting, complex pattern (replacement: simpler layout or step)
  - 🔵 nit: wording, formatting, minor presentation tweak
  - ❓ question: unclear intent, missing context, needs author clarification
- Focus: self-containment, executability, TODO atomicity/testability, scope/acceptance alignment, missing files/dependencies, contradictions, realistic sequencing, untestable verification, risks without mitigation, Complexity Check accuracy, masterplan ↔ sub-plan consistency, and ponytail complexity reduction. Do NOT perform pure micro prose edits unless they reduce scope, file count, or steps.

End with exactly one line:
- totals: N🔴 N🟡 N✂️ N🪵 N⚡ N🔵 N❓ | net: -<N> lines/steps possible
- Or: Lean & valid. Ship.
```

## Tags

- `🔴 bug`: correctness blocker, contradiction, broken logic, missing critical step
- `🟡 gap`: weak testability, missing file/dependency, unclear sequencing, unmitigated risk
- `✂️ cut`: redundant prose, duplicate information, speculative task not required for goal
- `🪵 yagni`: over-engineered scaffolding, premature generalization, unnecessary abstraction
- `⚡ simplify`: over-complicated sequencing, multi-tier nesting, complex pattern
- `🔵 nit`: wording, formatting, minor presentation tweak
- `❓ question`: unclear intent, missing context, needs author clarification

## Review criteria

1. **Self-containment**: executable using only the plan plus a normal repo checkout.
2. **Executability**: every step can be done without guessing missing context.
3. **TODO atomicity/testability**: each TODO is one focused, testable action.
4. **Scope/acceptance alignment**: the plan matches the goal and acceptance.
5. **Missing files or dependencies**: the `Files` section covers every path that needs to change.
6. **Contradictions**: sections do not contradict each other.
7. **Realistic sequencing**: dependencies and ordering are possible.
8. **Verifiable**: verification steps are concrete and runnable.
9. **Risk coverage**: risks are acknowledged or mitigated.
10. **Complexity Check accuracy**: counts and Proceed/Split decision are honest.
11. **Masterplan ↔ sub-plan consistency**: sub-plans repeat every fact they need from the masterplan.
12. **Ponytail complexity reduction**: the plan is as small as it can be while still correct.

## Triage

Label each finding `valid`, `false_positive`, or `unvalidated` with a one-line reason. If zero `valid` findings remain, output exactly `Lean & valid. Ship.`.

## Rules

- Read-only: do not edit the plan or any repo files.
- Single block: emit exactly one `### Plan Review Findings` block.
- Sort findings by section, then line.
- One finding per line; problem then fix, separated by ". ".
- Do not add new sections or rewrite the plan.
- Minor wording issues are not findings unless they mislead.
