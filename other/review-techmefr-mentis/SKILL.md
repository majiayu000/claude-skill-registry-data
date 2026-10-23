---
name: review
description: Use when the GATE is green, before simplification, review along two parallel axes (Standards + Spec) then a pass by the house agents.
---

# review

Step 8 of the pipeline (`WORKFLOW.md`). Two independent viewpoints that don't pollute each
other.

## When
After `gate` (`verified`), before `simplify`.

## Steps
0. **Get the diff in.** `references/review-transports.md` decides how: locally
   (`bin/prefetch_local.py`, git only — the default), from a CI checkout, or from a forge merge request. The
   review below is identical in all three; only the way in, and what happens to the findings, differ.
1. Run **two subagents in parallel** (separate contexts, no cross-pollution):
   - **Standards axis**: the stack's conventions + code smells (reuse, simplification, duplicated
     CSS), **then the cross-cutting sweep of `references/mr-review-plumbing.md`'s companion,
     `references/review-axes.md`** — accessibility, trust boundary, tests owed, cost on a hot path,
     diagnosability, contract, deletion, user-visible words. Each axis has an entry condition, so a
     diff that doesn't meet it produces nothing on that axis.
   - **Spec axis**: is the diff **faithful to the ticket / the spec**? (which a generic
     code-review command doesn't cover). Clean skip if there's no spec.
2. Aggregate both side by side.
3. A pass by the **per-stack reviewer** in the dev's usual style: `elrond` to route, or
   `aragorn`/`gimli`/`legolas`/`boromir`/`theoden`/`frodo` directly if the stack is known.
3b. **Behaviour the spec does not name** is judged by what a reasonable user would expect, graded by its
   effect on that user, not by whether the spec mentions the trigger. Every behaviour a reviewer considered
   and set aside as out of scope goes under **Declined to judge**, one line each with the reason. An empty
   list means nothing was set aside.
4. **Triage before posting anything.** The findings from steps 1-3 are raw coverage, not a review:
   verify each one against the real code, drop what would only start a pointless argument, rank
   bugs above nits, rule on every Declined-to-judge line (triage cannot absorb the list without saying so), and reword each surviving point short and sourced. A wrong or unsourced
   finding costs more credibility than the bug it claimed to catch.
5. When the thing under review is a plan, the reviewer adds phases and never rewrites the original
   (`skills/plan` step 7).
6. For depth: the runtime's own code-review and security-review commands, where it has them (gandalf as the final gate).
7. **Review per task, inside a delegated run, is the lighter cousin of this step**: one task's diff read once,
   conformity to its brief before quality, read-only (`skills/execute-plan` §2). It never replaces steps 1-4
   on the finished branch.
8. **The author's side** of whatever this step posts is `skills/receiving-review`: verify, stop on the unclear,
   answer with substance. A reviewer who wants a point acted on makes it checkable (a location, a failing case)
   instead of relying on tone.

## Output / checkpoint
`reviewed`.

## Guardrails
**A finding that was not checked against the real code is not posted.** The rest of this section applies that.

The two axes stay **independent** (no shared context). We invoke the native tooling, we don't
reimplement it. Plain comments, no emojis/arrows, lowercase at the start of a sentence.

| Thought while reviewing | What to do instead |
|---|---|
| "The tests pass, so it is fine" | Tests check what their author thought of. Read the diff against the spec. |
| "I will approve, the author knows this area" | The review exists for the author's blind spots. Read it. |
| "This is a nit, but I will block on it anyway" | Rank. A nit that blocks teaches authors to stop listening. |
| "Looks wrong, I will post it and let them explain" | Open the code first. A wrong comment costs more than the bug it claimed. |
| "The summary from the other reviewer covered that" | Cover what you were assigned; a reviewer that assumes coverage leaves a hole. |

Predicted, not recorded: replace with verbatim sentences from a `skills/testing-blocks` run when one exists.

## Adaptation
In Claude Code the two axes are two subagents run in parallel and the depth commands are native `/code-review` and `/security-review`. Any other runtime uses its equivalents; the steps do not change.

## Origin
A recognised market skill author (non-polluting two-axis code review) + the house agents + native,
rewritten. Step 4 (triage before posting) is the generic form of a mechanism that proved itself on
an agent kept private: the agent was calibrated on one named person's habits, which doesn't belong
in a shared framework, but the discipline it encoded holds for any reviewer.

Steps 3b and the Declined-to-judge list come from the reviewer prompt and execution flow of `superpowers` (MIT), read 2026-10-02. Step 7 is the shape of the task reviewer of that repo's `subagent-driven-development` skill (same licence and date), step 8 the pointer to the receiving side.
