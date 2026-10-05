---
name: goal-planner-codex
description: Plan, start, inspect, continue, budget, and complete Codex Goals with compact native goal text, live task plans, optional contract files, and evidence-backed completion audits. Use when the user explicitly asks to create/set/plan/refine/continue/replace/check/close a Codex Goal, provides or asks about a token budget, resumes an active Goal, or asks Codex to verify that Goal completion is actually proven.
---

# Goal Planner Codex

## Overview

Use this skill as the Codex-specific goal lifecycle and evidence practice. It
combines native Codex Goal tools with adaptive rigor, definition recovery,
optional durable contract files, `update_plan`, and proof-based completion.

Do not use this skill for ordinary task planning unless the user explicitly
asks for a Codex Goal, asks about Goal state or budget, resumes an active Goal,
or asks to prove/close Goal completion.

## Core Model

Keep the three Codex planning surfaces distinct:

```text
Goal text = compact durable guide that survives compaction.
update_plan = live task decomposition for standard and evidence-led work.
${CODEX_HOME:-~/.codex}/goals/<repo-slug>/<goal-slug>/contract.md = optional detailed contract when needed.
```

The native Goal text is not the full operating contract. Keep it under the
platform limit, outcome-focused, and allowed to quote existing files, scripts,
or contract paths that future turns should follow.

## Rigor Levels

Infer rigor automatically unless the user overrides it.

- `simple`: one-step, read-only, or low-risk Goal with obvious evidence. No
  required `update_plan` or contract file.
- `standard`: scoped implementation, artifact, or multi-step work with clear
  success criteria. Use `update_plan`; show a concise contract in chat when
  useful.
- `evidence-led`: multi-tool, runtime, PR, external state, user-visible
  artifact, handoff, or high false-completion risk. Create a contract file
  before `create_goal` if the Goal text will reference it, and maintain
  `update_plan` against evidence/proof states.

## Workflow

1. Inspect current Goal state with `get_goal` when available. If a Goal is
   active, continue it by default unless the user explicitly asks to replace,
   close, or start separate work.
2. Classify verifiability:
   - `verifiable`: final state and evidence are clear.
   - `clarifiable`: likely final state exists, but criteria are missing.
   - `exploratory`: the user wants discovery, research, or options.
   - `unverifiable`: no responsible final state can be inferred yet.
3. Run Definition Recovery when the request is not verifiable enough:
   - sharpen fuzzy or overloaded terms,
   - test concrete scenarios and edge cases,
   - cross-reference repo docs, glossary, ADRs, or code when local evidence can
     answer the question,
   - propose precise success criteria and evidence,
   - ask only the next necessary question, with a recommended answer.
4. Draft compact Goal text. Include objective, completion condition, rigor, and
   quoted file/script/contract references when they matter.
5. For `evidence-led` Goals that need a detailed contract, write the
   user-level contract file before calling `create_goal`. Never create a Goal
   that references a contract file which does not already exist.
6. Call `create_goal` only when the user explicitly asked for a Goal or
   confirmed a proposed Goal. Set `token_budget` only when the user explicitly
   gave or chose one.
7. Use `update_plan` for `standard` and `evidence-led` work. Keep at most one
   item `in_progress`, and tie evidence-led items to proof states where useful.
8. Execute through the relevant domain Skill(s), Tool Policy, and Tool Adapters
   when the Goal is not trivial.
9. Before `update_goal(status="complete")`, run a completion audit. Map every
   explicit requirement to current evidence and continue unless each required
   item is proved by adequate evidence.

## Contract Files

Use a user-level contract file only when the Goal benefits from durable details
outside the compact Goal text, especially for `evidence-led` or long-running
work.

- Default path:
  `${CODEX_HOME:-~/.codex}/goals/<repo-slug>/<goal-slug>/contract.md`.
- Auto-create `<repo-slug>` from the repository/workspace name and
  `<goal-slug>` from the objective using lowercase ASCII kebab-case, important
  words only, about six words or fewer, with a numeric suffix on collision.
- Use repo-local contract storage only when the user explicitly requests it, the
  repo already has a clearly ignored convention for Goal artifacts, or future
  agents must find the contract from the worktree without relying on the user's
  home directory. Before writing repo-local execution state, verify the target
  path is ignored or ask first.
- Treat the contract as mutable after Goal creation, but update it deliberately.
  Add `updated_at` and record major changes in `## Contract Changes`.
- Do not create scripts or hooks until repeated failure modes justify an
  enforcement layer.

## Definition Recovery Boundaries

Borrow a lightweight docs-aware questioning style, but do not invoke or emulate
a full docs-grilling session by default.

- Do not edit `CONTEXT.md`, ADRs, or project docs unless the user explicitly
  requests documentation updates.
- Do not accept vague goals blindly.
- Do not reject vague goals passively.
- Guide the user toward verifiable language or create a discovery Goal whose
  completion artifact is concrete: clarified terminology, acceptance criteria,
  a decision memo, an options table, a prototype result, or a next Goal proposal.

## Native Tool Policy

- `get_goal`: inspect active Goal state before lifecycle actions.
- `create_goal`: create only after explicit request or confirmation.
- `update_plan`: maintain live decomposition for `standard` and `evidence-led`
  Goals.
- `update_goal`: complete only after evidence proves every required item.
- `request_user_input`: prefer for bounded ambiguity when available.

If a native Goal tool is unavailable, say so briefly and continue with the
closest plain-chat or artifact-based substitute. Respect the active Codex
runtime's current tool contracts rather than duplicating every harness rule.

## References

- Read [goal-lifecycle.md](references/goal-lifecycle.md) for native Goal text,
  contract file, slug, and `update_plan` details.
- Read [evidence-and-completion.md](references/evidence-and-completion.md) for
  Definition Recovery, evidence planning, and completion audits.
- Read [tool-adapter-maturity.md](references/tool-adapter-maturity.md) when
  deciding whether raw tool use is enough or an adapter/enforcement path is
  needed.
- Read [proof-closure-semantics.md](references/proof-closure-semantics.md) when
  intermediate proof states matter.
- Read [examples.md](references/examples.md) for concrete `simple`,
  `standard`, `evidence-led`, and exploratory patterns.
