---
name: grill-intent
description: Adversarial review of an existing intent spec. Walk the spec field-by-field and pressure-test the weakest claims before code gets written against them. Use when an intent feels "done" but the user wants to stress-test it, or before handing it to an implementation agent.
---

<what-to-do>

Load the active intent from `intent.md` in the project root first. That file is bound to this repository and remains the content authority even when `PATHMODE_API_KEY` is set. Only call `get_current_intent` when no local file exists. If the file carries a cloud id, use that id for any team-only note call below.

Walk the spec field-by-field — objective, outcomes, edge cases, constraints. For each field, find the weakest claim and pressure-test it. Ask ONE pointed question at a time. For each question, propose your best-guess answer based on the spec and the codebase.

When a weakness is confirmed, edit the spec itself — not a note about it. Write the change back to `intent.md` and save with `intent_save` (it preserves the file's identity and syncs in team mode; use `update_intent` only when no local file exists). Then, in team mode, call `log_implementation_note` to record WHY the change was made: the note reaches the next agent's prompt, the spec carries the change.

Stop when all five dimensions below pass, or the user explicitly accepts a known weakness.

</what-to-do>

<supporting-info>

## The five dimensions

1. **Objective** — Does it name who is harmed? Is it specific enough to disqualify other interpretations? Is it a problem, or a solution in disguise? ("Add a dropdown" is a solution; "members cannot switch products without leaving their work" is a problem.)
2. **Outcomes** — Are they observable state changes, not activities? Could someone verify this in 5 minutes without asking the spec author?
3. **Edge cases** — Are they real edge cases, or restatements of the outcome failing?
4. **Constraints** — What must NEVER happen? An intent with zero constraints has no teeth.
5. **Contradictions** — Do any two fields imply opposite things?

Alongside the five, check scope. More than about seven outcomes usually means several intents; split before building. One outcome and no edge cases is usually a task, not an intent.

## Stop conditions

- All five dimensions pass — the spec is agent-ready
- The user explicitly accepts a known weakness — record that acceptance as a decision in the spec with `intent_save`; when a cloud id is available, one consolidated `log_implementation_note` may preserve rationale that does not fit the decision field
- More than 6 turns without surfacing new issues — the spec is settled

## Difference from compile-intent

- `compile-intent` BUILDS a spec from a vague problem
- `grill-intent` BREAKS an existing spec to find weaknesses

Run grill before treating a spec as agent-ready. If you compile a spec and immediately hand it to an implementation agent, you're trusting your first draft — and first drafts are wishful.

## Codebase grounding

When proposing answers, look at the actual code. If the spec says "users see a spinner during payment" but the codebase has no spinner component on the payment path, that's a gap worth surfacing. The point isn't to be right — it's to be specific enough that the user can correct you.

</supporting-info>
