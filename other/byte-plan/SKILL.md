---
name: byte-plan
description: "Create a project execution plan or roadmap when planning is the requested deliverable."
---

# Byte Plan

Plan only to the depth that improves execution. Inspect relevant context before
planning, and prefer a short actionable plan over project-management theater.

## Choose The Planning Depth

- Small, clear task: a few ordered actions in chat.
- Multi-file or multi-stage task: a concise plan with dependencies and checks.
- Long-running or collaborative task: persistent plan files and state may help.

Do not require OKRs, waves, owner roles, subagent fields, or a fixed number of
plans unless the project actually needs them.

## Useful Plan Content

Every plan should make three things understandable:

- the result being pursued;
- the next meaningful actions and important dependencies;
- how completion will be checked.

Add scope boundaries, touched areas, risks, alternatives, or rollout steps when
they affect execution. Resolve low-risk details during implementation rather than
enumerating them prematurely.

For an existing codebase, use repository instructions and live inspection. A
missing Byte OS artifact or harness is not by itself a planning blocker.

Apply relevant active lessons before planning. If evidence or user correction
confirms a reusable wrong assumption, update `.byte-os/LESSONS.md` with the
corrected premise and prevention rule. Do not log ordinary plan revision.

Save plans only when they need to survive the current turn, coordinate multiple
tracks, or support resumption. Reuse the project's existing planning convention;
otherwise prefer `.byte-os/PLAN.md` over many mandatory plan files.

Planning is complete when another capable agent could begin safely without the
plan pretending to eliminate all judgment.

## Minimal design and adaptive execution

Prefer one short plan/state document: overall outcome and acceptance, remaining
work with dependencies, current mode, and next action. Link detailed evidence;
avoid duplicate design documents, exhaustive future phases, and repetitive logs.
For the requested combined workflow, use
[adaptive execution](references/long-running-work.md). Design monitoring before
closing core work, including allowed repairs and when to return to a Goal.
Planning alone does not authorize launching jobs or enabling monitoring.

## Source And Updates

Canonical repository: [elan6666/your-bytedance-skills](https://github.com/elan6666/your-bytedance-skills). Use its current `main` branch when checking for or installing updates.
