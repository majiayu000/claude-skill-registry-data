---
name: ln-disambiguate
description: "Collapse meaningful ambiguity with contrastive examples. Use when a plan/design has several plausible meanings, requirements feel vague, examples would clarify intent faster than grilling, or the user asks to disambiguate, find ambiguity, use behavioral kernels, or ask contrastive questions."
---

# Ln Disambiguate

Generate cases where plausible interpretations diverge; ask the user to classify the case.

Users recognize intent in concrete examples faster than they author abstract predicates. Use the TiCoder move generalized beyond tests: produce examples, counterexamples, edge cases, and candidate outcomes that separate meanings. Then translate the answer into typed conclusions.

Use this instead of `ln-grill` when the work has enough shape that ambiguity collapse is the next move. Use `ln-grill` when the idea still needs broad Socratic pressure.

If local context can answer the question, inspect it instead of asking. Read only the context needed to form precise contrasts: `memory/SPEC.md`, `memory/PLAN.md`, and files they explicitly point to. Use the current lexicon; when terms are overloaded, name the competing meanings.

For each ambiguity:

1. Name the ambiguous claim.
2. Generate 2–4 competing interpretations.
3. Find the smallest scenario where they produce different outcomes.
4. Ask one contrastive classification question.
5. Translate the answer into candidate durable conclusions:
   - `decision`
   - `invariant`
   - `constraint`
   - `assumption`
   - `example`
   - `counterexample`
   - `criterion`
   - `unresolved ambiguity`

Prefer one high-yield question at a time. Multiple choice is useful when options are real; forced choice is harmful when it hides the likely fifth answer. Always allow “other / depends — explain.”

Ask questions like:

- “In this exact case, which outcome is correct?”
- “Is this inside or outside the commitment?”
- “Would this count as a bug?”
- “Which option should be rejected?”
- “Does this example witness the rule, contradict it, or sit outside scope?”

Include your recommended answer when you have enough context, and explain why.

Use behavioral kernels as hidden interviewer machinery. Activate at most the top 2–3 relevant kernels:

| Kernel | Looks for | Typical artifact |
| --- | --- | --- |
| Identity & reference | ids, references, links, uniqueness | entity / reference invariant |
| Containment & topology | parent/child, folders, ordering, graphs | membership / topology invariant |
| Validation & normalization | valid/invalid input, canonical forms | parser or validation contract |
| State & lifecycle | states, transitions, terminal states | state-machine invariant |
| Temporal history | undo, redo, audit, expiration | history / timeline invariant |
| Optimization & preference | best, preferred, tie-breaks | ranking or objective rule |
| Authority & capability | roles, permissions, delegation | authorization predicate |
| Concurrency & collaboration | offline, stale, conflict, merge | conflict-resolution semantics |
| Transactions & atomicity | all-or-nothing multi-object updates | transaction invariant |
| Resource accounting | balances, quotas, capacity, limits | conservation / bounds invariant |
| Derived data & views | counts, filters, projections, caches | view consistency invariant |
| Error & recovery | retry, rollback, compensation | failure / recovery contract |
| External effects | APIs, queues, webhooks, clocks | boundary / adapter contract |
| Change & migration | legacy, compatibility, upgrade | migration / refinement invariant |
| Observability & evidence | logs, traces, explanations, audit | trace / provenance invariant |

Example:

> A project is deleted while it still has tasks. Which behavior is correct?
>
> A. Delete the tasks too.
> B. Archive the tasks and keep them readable.
> C. Move tasks to an unassigned pool.
> D. Block deletion until tasks are reassigned or deleted.
> E. Other / depends.
>
> My recommendation is B if historical traceability matters more than cleanup, because it preserves references and gives us a clear data-integrity invariant.

Translate the answer:

- decision: “Deleted projects archive their tasks rather than deleting or reassigning them.”
- invariant: “Archived tasks retain a tombstone reference to the deleted project.”
- positive example: “Deleting a project with open tasks makes those tasks archived and readable.”
- counterexample: “Tasks silently disappearing after project deletion is rejected.”
- criterion: “A deletion test verifies task archival and readable tombstone references.”

Stop when the ambiguity is collapsed, explicitly deferred, or ready for `ln-spec`.

Do not create or edit planning artifacts here. Durable conclusions promote into `memory/SPEC.md` or `memory/PLAN.md` through the next routed skill.

## Routing

When the ambiguity pass is complete, present these options to the user. If `tool-ask-question` is available, use it; otherwise use a numbered list.

| # | Label | Target | Why |
| --- | --- | --- | --- |
| 1 | Write/update spec | `ln-spec` | Durable conclusions should enter `memory/SPEC.md` |
| 2 | Plan frontier | `ln-plan` | The meaning is clear but work needs sequencing |
| 3 | Scope one slice | `ln-scope` | One implementation slice is now obvious |
| 4 | Grill further | `ln-grill` | The ambiguity pass exposed broader design uncertainty |

Recommended: choose `ln-spec` when decisions, invariants, assumptions, lexicon, examples, or criteria changed.
