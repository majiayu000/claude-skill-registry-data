---
name: clarify-before-acting
description: Use when a request is missing the target repo, customer or outcome, or whether the work is planning versus implementation. Stop and ask instead of inventing a path.
kind: skill
status: active
owner: APT
last_updated: 2026-09-06
source: APT clarify and model-routing rollout
title: "Clarify Before Acting"
domain: "thinking"
source_paths: ["apt-principles-agents/skills/thinking/clarify-before-acting/SKILL.md"]
---

# Clarify Before Acting

## Purpose

Stop work when direction is not reviewable. Ask the smallest set of questions that would make the next step safe, then wait. Do not invent a customer, repo, outcome, or implementation path to keep moving.

## When to Use

Use at the start of a session and again before switching from planning to implementation, whenever any of these are missing or contradictory:

- Which child repository owns the change.
- Who the work is for and what outcome changes for them.
- Whether the user wants framing, a plan, or an implementation.
- For product or feature work, whether an approved Working Backwards package exists.

## Inputs

- The user request as written.
- Target-repo `AGENTS.md`, `.apt/installation.json`, and `docs/project-context.md` when a repo is already identified.
- Any Working Backwards package, PRD, or readiness status that is already on disk.
- Known open items and blockers with owners.

## Process

1. Restate the request in one sentence and list what is verified versus assumed.
2. Treat these as stop conditions, not prompts to guess:
   - no owning repository in a multi-repo workspace;
   - no customer, operator, or audience plus a desired outcome for product work;
   - plan versus implement is ambiguous;
   - product work has no Working Backwards package and the user asked for requirements or code.
3. Ask at most one or two questions that would clear the stop condition. Prefer concrete options over open essays.
4. If the user cannot answer, record `[OPEN - owner: name]` when work can continue with visible risk, or `[BLOCKER - owner: name]` when build or implementation must not start.
5. For missing product intent, route to Working Backwards intake (customer, problem, current workaround, outcome). Do not draft requirements or code to fill the gap.
6. Only after the stop condition is cleared, build or resume a task packet and hand off to model routing.

## Outputs

A go or stop decision, the questions asked, any `[OPEN]` or `[BLOCKER]` items, and either a cleared task packet or an explicit wait for the user.

## Quality Bar

The skill asks only what blocks a safe next step, preserves uncertainty instead of inventing facts, and never treats silence or model confidence as approval.

## Domain Checklist

- Treat **Clarify Before Acting** as a gate, not a writing style.
- One or two questions, then stop. Do not continue behind a question.
- Product intent gaps go to Working Backwards, not to a feature list or a patch.
- `[BLOCKER]` prevents implementation and engineering handoff until an accountable person accepts or resolves it.
- State what is verified, what is assumed, and what requires a human answer.

## Required Reading

Read the Thinking principle hub, Practical Thinking, Working Backwards role contracts, and the target repository's local instructions.

## References

- [Thinking principles](../../../principles/thinking/README.md)
- [Practical thinking](../../../principles/thinking/practical-thinking.md)
- [Working Backwards role contracts](../../../templates/working-backwards/agent-role-contracts.md)
- [Templates](../../../templates/README.md)
- [Agents](../../../agents/README.md)
