---
name: grill-me
description: >-
  Stress-test a plan or design by interviewing the owner about it: maximize
  question coverage — every assumption, every edge, every dependency, every
  implicit decision gets a question. Use whenever planning is needed — a plan or
  design is about to be locked, a large task is about to start — and on the
  direct ask "grill me" / "прожарь меня". Batched asks are the norm: cover
  everything, resolve branch by branch, record confirmed answers at once.
license: MIT
metadata:
  derived_from: "https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me"
  original_author: "Matt Pocock (@mattpocock)"
  original_license: MIT
  reworked_for: "Oper workspace 2026-09-19 — owner verdict: maximize coverage, batched asks, no vendor doc ceremony"
  version: "3.2.0"
---

# Grill Me

> Home branch in Memora: `root/skill/grill-me`. Reworked per owner verdict
> 2026-09-19 and answers 586–590 (2026-10-18): the vendor "one question at a
> time" discipline was wrong for this workspace. The job is **maximum coverage**;
> what survives from the original is walking the tree depth-first, exploring the
> codebase before asking what it can answer, and attaching a recommended answer.

## Choosing a part

| Situation | Part |
|---|---|
| A plan or design exists and must be interrogated branch by branch | this page, inline (`Rules` below) |
| Intent is still fuzzy and the owner wants a slow, one-question-at-a-time discovery with a brief at the end | `parts/interview/` |
| The request arrived already shaped as a solution and the direction itself may be wrong | `parts/nodumb/` |
| A product or interface must be invented or reworked and the options look equivalent | `parts/ask-nodumb/` |

## Rules

1. **Coverage is the metric.** An unasked question is a decision made silently
   later. One branch at a time (dependency order), but the questions inside a
   branch are batched.
2. **Explore first.** Anything answerable from the codebase, the workspace
   indexes or prior owner verdicts — resolve it yourself and state the finding as
   an assumption for confirmation, not as a question.
3. **Extract the decision tree, then store it.** Scope, data, behavior, edge
   cases, failure modes, tooling, rollout, rollback, what is out of scope. Write
   that tree as a Memora node under `root/skill/grill-me` **before the first
   question**; the answers land in the same node.
4. **Batch by branch** through `ask_questions` — up to 20 questions per call
   while the batch stays inside one branch; each question carries a one-line
   recommended answer with its consequence. Unresolved branches spawn the next
   batch; a plan of any real size takes several batches, which is success.
5. **Record as you go.** Confirmed answers go into the Memora node in the same
   turn; the chat gets a short summary, not the transcript. Write your version of
   the understanding down once the owner confirms it, not before.
6. **Stop when coverage is complete**: every branch resolved or explicitly
   deferred by the owner, and no question left that has no consequence. Then
   summarize the locked decisions and the open deferrals.

Not a substitute for `AGENTS.md`: during execution, questions come at the moment
a deviation appears. Grill-me is for the **plan** stage, where the owner wants the
full interrogation. No CONTEXT.md / ADR ceremony, no session-tracker scripts.

## Related

`planning`, `brainstorming`, the `challenge` part of the `review` router, `interview`.
