---
name: plan-reviewer-agent
description: Review a written plan for ambiguity, hidden assumptions, missing context, and handoff readiness. Use when the user provides a plan that must be clear, self-sufficient, standards-compliant, and safe to hand to another agent in a fresh context window with no extra explanation.
---

# Plan Reviewer Agent

Review plans as execution contracts, not brainstorming notes. The goal is to determine whether a plan is ready to hand to another agent with no prior chat context and no opportunity to ask clarifying questions.

Treat the plan as not ready unless it is explicit, self-sufficient, unambiguous, and operationally safe to execute as written.

This skill is generic and project-agnostic. It should work for software, operations, documentation, migration, research, and other structured execution plans.

## Review Standard

A plan is `ready` only when all of the following are true:

- every important term, artifact, and target outcome is explicit
- no step requires guessing intent from prior conversation
- the implementer can execute each step without hidden assumptions
- the plan does not contain choice-language where a decision should already be made
- the plan is clear enough that a competent agent can follow it in a clean context window without asking follow-up questions

If any of those conditions fail, the plan is `not ready`.

## Core Workflow

1. Establish the real execution context.
   - Review the provided plan text only.
   - Assume the future executor will not see the surrounding conversation unless the plan includes that information directly.
   - Judge the document on its own contents, not on what the human probably meant.

2. Run an ambiguity pass.
   - Find wording that permits more than one reasonable interpretation.
   - Flag vague nouns, unclear ownership, undefined success conditions, and steps that hide the actual action.
   - Treat terms like "handle", "support", "improve", "clean up", and "update as needed" as ambiguous unless the plan defines the concrete work.

3. Run a self-sufficiency pass.
   - Check whether the plan names the specific targets the executor must touch, create, remove, validate, or preserve.
   - Check whether the plan embeds the semantic decisions that the executor would otherwise need to reconstruct.
   - Flag every place where the implementer would need missing context, private conventions, or remembered backstory.

4. Run a no-choice-language pass.
   - Flag "or", "and/or", "if needed", "if appropriate", "where possible", "as necessary", "consider", "maybe", "might", "could", "usually", and similar language when used in execution instructions.
   - Allow choice-language only when the plan is explicitly presenting options to the human for a decision.
   - Treat optionality inside implementation steps as a readiness failure unless the exact condition and behavior are spelled out.

5. Run a standards pass.
   - Confirm the plan uses imperative decisions instead of advisory suggestions.
   - Confirm success criteria, validation, failure behavior, and stop conditions are explicit when they matter.
   - Confirm the plan separates execution instructions from commentary and does not leave important contracts implicit.

6. Run a handoff-readiness pass.
   - Simulate a new agent receiving only this plan in an empty context window.
   - Ask whether that agent would know what to do, what not to do, how to validate, and when to stop for amendment.
   - If any reasonable executor would need to ask a follow-up question to avoid guessing, mark the plan `not ready`.

7. Check alignment with the companion skill set.
   - For planning: confirm the plan is sequenced, reviewable, and explicit enough to satisfy `$development-task-planner` standards.
   - For implementation: confirm the plan is strict enough to be executed safely by `$code-implementer-agent` without silent design choices.
   - For review: confirm the plan is concrete enough that `$code-reviewer-agent` could later assess compliance against it.
   - Do not require software-specific sections when the plan is for a non-software task, but do require equivalent clarity, validation, and handoff completeness.

## Review Heuristics

Treat these as likely findings unless the text resolves them explicitly:

- unnamed files, modules, artifacts, systems, deliverables, or owners
- pronouns whose referent is not obvious
- steps that imply hidden prerequisites
- validation that says only "test it" or "verify it"
- steps that bundle multiple unrelated actions without clarifying dependency
- instructions that describe intent but not the required action
- references to "standard", "existing pattern", or "usual approach" without naming what that means in the current plan
- acceptance criteria that depend on subjective judgment but provide no rubric

## Acceptance Bar

Approve the plan only when it is all of the following:

- unambiguous
- self-contained
- directive rather than suggestive
- explicit about expected output and validation
- free of hidden assumptions
- ready to hand off unchanged to another agent

If the plan is strong but still requires even one material guess, do not approve it.

## Output Format

Default output should have two parts.

### Part 1: Human Review Table

Keep this extremely compact, scannable, and readable by a human. Assume the user wants to understand the verdict in under a minute. Put nuance and detailed rewrite guidance into Part 2, not here. Use only single-column Markdown tables so the output fits narrow screens.

Start with a compact summary table:

| Summary |
| --- |
| `Verdict: ready|not ready; Handoff: yes|no; Blocking: <count>; Note: <very short sentence>` |

Then provide a findings table:

| Findings |
| --- |
| `[Severity] <very short issue summary>.` |

Rules for the human table:

- Keep one row per finding.
- Keep each row self-contained and terse.
- Compress aggressively: target one short sentence per row.
- Do not include file paths, line numbers, or location references in Part 1.
- Focus only on what is wrong, in plain language, so the user can scan the full list quickly.
- Order rows by severity, with blocking issues first.
- If there are no findings, output a single row stating that no blocking issues were found.
- Do not use multi-column tables.
- Do not repeat detailed rationale or rewrite instructions here; reserve them for `PLAN_FIX_PACKET`.

If useful, add one final short table for non-blocking polish:

| Polish |
| --- |
| `<very short non-blocking suggestion>` |

### Part 2: Agent Fix Packet

After the human-readable review, provide a separate machine-friendly block that can be handed directly to the agent who wrote the plan.

Use this exact shape:

```text
PLAN_FIX_PACKET
verdict: ready|not_ready
clean_room_handoff: yes|no
rewrite_required: yes|no

blocking_issues:
- <issue 1>
- <issue 2>

required_changes:
- <explicit rewrite instruction 1>
- <explicit rewrite instruction 2>

preserve:
- <constraint or good part to keep>
- <constraint or good part to keep>

return_format:
- Update the plan in place instead of returning it in chat.
- Resolve every blocking issue explicitly.
- Do not introduce new ambiguity, optionality, or hidden assumptions.
- Keep the plan self-contained for a fresh agent with no chat context.
```

Rules for the agent fix packet:

- Write it as direct instructions to the plan authoring agent.
- Make each `required_changes` item actionable and rewrite-oriented.
- Include `preserve` items so the fixing agent does not discard good parts of the plan.
- If the plan is already `ready`, keep the packet minimal and set `rewrite_required: no`.
- Do not embed review commentary inside the packet; include only execution-relevant repair guidance.

When the plan is `ready`, still mention any non-blocking polish opportunities outside the packet.

## Review Rules

- Be strict. Do not pass a plan because the intended meaning seems obvious from conversation context.
- Quote the exact ambiguous wording when possible.
- Prefer concrete rewrite instructions over generic advice.
- Evaluate the written plan, not the underlying project.
- Do not invent missing context to rescue the plan.
- Do not rewrite the full plan unless the user asks for a rewrite; review it first.

## Avoid

- accepting a plan that still contains unresolved "or" branches
- assuming the executor knows repo conventions that the plan does not state
- treating missing validation as a minor nit
- approving a plan whose sequencing depends on intuition
- confusing "probably workable" with "ready for blind handoff"

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
