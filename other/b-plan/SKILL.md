---
name: b-plan
description: >
  Turn goals into execution-ready plans. Handles both underspecified
  requests and fuzzy problem statements by investigating enough to compare
  options, choose a path, and write ordered steps. Unlike b-implement,
  b-plan does not change code. Routing signals: plan, decompose, approach,
  explore, not sure, figure out, "how should I", implementation plan,
  clarify, requirements, scope. Delegated: runs only in the `b-planner`
  subagent; the main session never executes it itself.
metadata:
  phase: Decide
  execution_mode: subagent
  agent: b-planner
---

<!-- Generated from skills/registry.yaml and skills/b-plan/prompt.md. Edit those sources, not this file. -->

# b-plan

Turn an unclear goal into the smallest execution-ready plan. Do not implement.

## Delegation boundary

`b-plan` runs only in the `b-planner` subagent.

- Main session: reading this file prepares the handoff; it never authorizes running the steps below yourself. Gather the parent-owned evidence and confirm the effective `b-planner.md` (project `.pi/agents/` over the Pi agent directory's `agents/`) is readable and its parsed frontmatter `tools` value, normalized to a list (comma-separated scalar or YAML sequence), is explicit, non-empty, and contains neither `edit` nor `write` (a missing, blank, or null `tools` grants them), then call `subagent` with agent `b-planner` and a bounded task naming `b-plan`. Do not do this skill's work with your own tools, even for a quick, small, or single-lookup request. If the subagent is unavailable or fails, or its result notes an unknown agent type or `general-purpose` fallback (discard that result), report the gap and ask the user; never fall back to self-execution. Evaluate the returned result before any user-facing or worktree action.
- `b-planner` child: execute the steps below read-only, return this skill's Output format to the main session, and do not delegate again.

## When to use

- The user asks for a plan, approach, decomposition, or requirements clarification.
- Scope, acceptance criteria, risk, sequencing, or constraints are unclear.

## When NOT to use

- A small clear non-UI change -> **b-implement**.
- Clearly scoped frontend/UI work -> **b-frontend**.
- External facts are the blocker -> **b-research**.
- A runtime failure needs diagnosis -> **b-debug**.

## Tool guidance

- Use native `read` and local search for routine evidence. Per the kernel CodeGraph rule, use it for affected symbols, callers, and tests in indexed code. When one versioned external library/API fact decides between viable options, one Context7 lookup (resolve once, query once) using only public library names and symbols is permitted; otherwise list it as an open **b-research** item. Use only planning context supplied in the current task; report missing history rather than guessing.

## Steps

1. State the interpreted goal, constraints, non-goals, and success criteria.
2. Inspect only the local evidence needed to avoid guessing. Use CodeGraph for affected symbols, callers, and tests when an index is available; otherwise report the fallback gap to the main session.
3. For non-trivial or risky work, compare viable paths and relevant quality dimensions, including the simpler option, then recommend the smallest safe one with evidence-backed rationale and accepted trade-offs. Keep small obvious tasks free of forced comparison or research.
4. Specify ordered implementation steps, affected paths/symbols, invariants, and `Done when` verification that proves observable behavior.
5. For a material user-facing decision, state 2–4 concrete options and their trade-offs for the main session to resolve with the user. Do not invoke `ask_user_question` or claim approval.
6. Return the plan to the main session with scope, acceptance, affected paths, invariants, verification, risks, and open items. The main session owns approval and any later implementation.
7. For changed work, include applicable checks and the kernel's risk classification of the final candidate: a bounded, verified low-risk change may finish without independent review, with direct tests/docs and faithfully regenerated outputs counted with their source; a triggered change must freeze the exact tracked plus relevant untracked/derived snapshot after fresh checks and obtain independent **b-reviewer** review. This is not authorization to commit or push.

## Output format

Concise scope, recommended path, ordered steps, verification, explicit blockers, and unresolved decisions for the main session.

## Rules

- Do not implement.
- Keep plans short unless risk requires detail.
- Do not invent behavior, names, acceptance criteria, or commands.
- This subagent returns planning evidence to the main session; it does not resolve user decisions or implement.
