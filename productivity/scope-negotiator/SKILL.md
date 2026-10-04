---
name: scope-negotiator
description: Use when a request is broad, fuzzy, overgrown, multi-directional, or likely to balloon, and Codex needs to reduce it to the smallest valuable current-turn scope. Use for scope negotiation, slicing work, defining in/out of scope, choosing a first milestone, preventing overbuild, turning "do everything" into a staged plan, or aligning effort level before implementation.
---

# Scope Negotiator

Shrink messy work into a useful slice. This skill is for scope control, not for deep requirements interviewing or full implementation planning.

## Workflow

1. Name the broad request.
   - Restate the user's desired outcome in one sentence.
   - Identify why the request could expand: unclear audience, too many artifacts, too many repos, quality bar, dependencies, or hidden decisions.

2. Separate scope layers.
   - Core outcome: the smallest result that creates real value.
   - Required support: checks, docs, migrations, tests, or artifacts needed for trust.
   - Optional expansion: polish, automation, extra formats, broad refactors, future-proofing.
   - Explicit non-goals: tempting work that should stay out for now.

3. Propose 2-3 scope options when useful.
   - Minimal safe slice: fastest useful outcome with basic verification.
   - Standard slice: balanced outcome likely matching the user's intent.
   - Expanded slice: only when the extra work changes long-term leverage.

4. Recommend one slice.
   - Choose the smallest slice that satisfies the user's apparent goal and risk level.
   - If the user asked for execution and the recommended slice is safe, proceed after stating the chosen scope.
   - Ask one concise question only when choosing the wrong slice would waste substantial work or violate a boundary.

5. Preserve future work.
   - List deferred items so they are not forgotten.
   - Route to `$define-goal` when the user wants a goal-backed objective.
   - Route to `$codex-consensus-plan` when the chosen scope still needs a decision-complete implementation plan.
   - Route to `$codex-completion-loop` when the scope is clear and should be executed through verification.

## Output Shape

Use this structure:

- Recommended scope
- Why this slice
- In scope
- Out of scope
- Deferred
- Acceptance criteria
- Next action

When comparing options, use:

`Option | What it includes | Cost | Risk | When to choose`

## Scope Rules

- Prefer current-turn value over theoretical completeness.
- Do not force a large plan when a small reversible edit or answer solves the need.
- Do not silently drop important work; defer it explicitly.
- Keep non-goals visible when they prevent scope creep.

## Stop Conditions

- Stop negotiating once the current slice is clear enough to execute.
- Do not ask broad preference questions when repo context or user history provides a safe default.
- Do not use this skill to avoid doing clear implementation work.
