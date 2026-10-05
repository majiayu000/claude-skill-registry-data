---
name: review-against-intent
description: Review code changes against the active intent's outcomes and constraints. Use after writing code meant to implement an intent, or when reviewing a PR to check it actually delivers on the spec. Anchors review to product intent, not generic code style.
---

<what-to-do>

Load the active intent from `intent.md` in the project root — the file is bound to this repository, which makes it the authority on what governs this diff. If `PATHMODE_API_KEY` is set and the file's frontmatter carries a cloud id, also fetch that intent's execution bundle (`get_agent_prompt` with the id) to pick up what the file cannot hold: open PM change requests, findings, handoff notes, and authorization state. Never let `get_current_intent` choose an intent for a repository review: "current" is a workspace heuristic, not a repo binding. If the repository has no `intent.md`, stop and ask for an explicit `intentId` or inline spec instead of guessing.

If the execution bundle reports an open PM change request, or says the current repository revision is pending, rejected, or stale, stop before reviewing the diff as delivered work. Name the exact request/revision blocker and direct the agent through `preflight`: a requested spec change must be applied with request-bound `intent_save`, then a signed-in product manager must authorize that exact resulting revision. Never approve code against the superseded or unauthorized spec.

Identify the changed files using git diff against the base branch (or staged changes if no base specified).

For each outcome in the intent, check whether the changes actually deliver it — with specific file/line evidence. For each constraint, check whether the changes respect it. For each edge case, check whether it's handled.

Report:
- Outcomes delivered (with file/line evidence)
- Outcomes not yet delivered (and what's missing)
- Constraint violations (specific files/lines)
- Edge cases that look unhandled

Do NOT review for unrelated code style, formatting, or quality concerns. That's not this skill's job. Stay anchored to the intent.

</what-to-do>

<supporting-info>

## Why anchor to intent, not generic review

Most code review tools check correctness, style, or security. They cannot check whether the code does what it was MEANT to do, because they don't see the intent.

This skill bridges that gap. It treats the intent spec as a contract and the code change as the proposed satisfaction of that contract. A PR can pass every other check and still fail this one — because the intent it was supposed to deliver isn't actually delivered.

## What "delivers an outcome" looks like

For an outcome like "Payment completes in under 3 seconds (p95)":

- ✓ The payment code path has a measurable timeout under 3s
- ✓ There's a metric or test confirming p95 behavior
- ✓ Failure modes are handled (covers the constraint side)

A code change that adds a feature without a corresponding metric does NOT deliver this outcome. Surface that gap.

## Constraint violations

Constraints are hard limits — "PII must not survive a logout", "checkout must not block on network calls > 500ms", etc.

If a change introduces a constraint violation, treat it as a blocker. Be specific: name the constraint, name the file/line, explain how the change violates it.

## Logging gaps

When the review finds gaps, the user often wants to record what's not yet done so a future session can pick it up. Call `log_implementation_note` for each significant gap. Make the note self-contained — the next reader won't have this conversation's context.

</supporting-info>

If the diff is right and the spec is wrong (the code satisfies what users need but contradicts an outcome, constraint, or edge case as written), do not approve the diff against the stale text and do not rewrite intent.md yourself. Record the finding with `record_implementation_finding` and propose the exact correction with `propose_spec_change`; a signed-in product manager accepts or rejects it, and only an accepted request may be applied. Say in the review which claim is contradicted and that a proposal is pending.
