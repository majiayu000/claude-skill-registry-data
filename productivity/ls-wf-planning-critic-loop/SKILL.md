---
name: ls-wf-planning-critic-loop
description: Use when creating decision-complete plans through grounding, capped clarification, subagent delegation, and critic iteration.
metadata:
  version: "1.0"
---

Use this workflow package for non-trivial planning work where the agent must produce a structured plan before implementation, handoff, or approval.

Ground first: inspect available repo files, docs, config, schemas, current GitHub state, or local system facts before asking the user. Do not ask questions that non-mutating inspection can answer.

Clarify only when it materially changes the plan. Ask at most three user questions total, one at a time, using the reverse decision-tree style from `ls/docs/DECISION_TREE_WORKFLOW.md`: A-D options, preferred choice, and rationale. Use available question/input/TUI tooling when supported; otherwise render clear markdown or plain-text choices. This three-question cap is local to this planning workflow and does not change the default `ls-wf-spec-clarify-reverse` protocol.

For non-trivial plans, use subagents when they reduce risk or context load: `explorer` for broad repo discovery, `researcher` for current external facts, `tester` for validation plans or long command logs, and `reviewer` as an independent critic when that materially improves evidence and is available and authorized. Keep the controller responsible for verification, checkpoints, and final plan quality. Do not force delegation for trivial direct tasks or when direct execution is the only useful route.

Review plans for requirement coverage, resolved decisions, grounding evidence, verification, safety, and scope. Use an independent critic when it materially improves evidence and is available and authorized. Repeat review after material corrections or when material findings remain; do not impose a minimum number of rounds or a numeric satisfaction quota. Turn unresolved prerequisites into explicit blockers, and keep the controller responsible for decision completeness. Submit the resulting plan through the active client's plan-submission mechanism; do not require literal `<proposed_plan>` output.

Primary references: `ls/docs/DECISION_TREE_WORKFLOW.md`, `ls/docs/WORKFLOW_STANDARD.md`, `ls/docs/WORKFLOW_PACKAGES.md`, and `ls/docs/SKILLS_AND_RULES.md`.
