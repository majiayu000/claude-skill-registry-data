---
name: ln-spike
description: "Time-boxed throwaway investigation to answer one hard question. Use when facing technical uncertainty before committing to a frontier item or scoped slice — the output is knowledge, not production code."
argument-hint: "[question to answer and what you'll try]"
---

# Ln Spike

Retire one uncertainty. Output is knowledge, not code — spike code is throwaway, never promoted directly (Beck, XP). One question per spike; if multiple unknowns exist, run multiple spikes.

Spike notes are temporary. Reconcile durable findings into `memory/SPEC.md` and `memory/PLAN.md` instead of inventing standalone investigation docs unless the user explicitly asks for one.

## Input

The question and approach: $ARGUMENTS

## Investigate

1. State the question and what would constitute an answer.
2. Time-box the investigation. Stop when answered or exhausted.
3. Write a verdict.

## Spike Verdict

```md
## Question
[The question]

## Approach
[What was tried]

## Verdict
[Answer: yes/no/partially, with evidence]

## Recommendation
[Proceed with ln-scope, try a different approach, or abandon]
```

## Traceability (mandatory — do before routing)

After the verdict, do all of these before presenting routing options:

1. Mark the spike `done` in `memory/PLAN.md` if the spike itself was tracked as a frontier item, or update the affected frontier definition if it was a proving step inside a frontier
2. Update `memory/SPEC.md` §Assumptions — set `Status` to `validated` or `invalidated` as evidence warrants, update `Confidence` if the evidence changed it, and flag implicated frontier items in `memory/PLAN.md`
3. Add any new decisions to `memory/SPEC.md` §Decisions, new assumptions to §Assumptions
4. If the verdict changes frontier or slice feasibility → update affected frontier definitions / sequencing in `memory/PLAN.md`

These are bookkeeping steps, not optional. Routing comes after.

## Routing

After traceability is complete, present these options to the user (use `tool-ask-question`):

| #   | Label           | Target       | Why                                               |
| --- | --------------- | ------------ | ------------------------------------------------- |
| 1   | Scope a slice   | `ln-scope`   | Question answered — ready to define the next scoped slice |
| 2   | Spike again     | `ln-spike`   | New question emerged, needs another investigation |
| 3   | Revise spec     | `ln-spec`    | Verdict revealed the spec needs structural revision |
| 4   | Revise plan     | `ln-plan`    | Verdict changes what frontier items or slices are needed |
| 5   | Back to triage  | `ln-consult` | Verdict changes the overall direction             |

Recommended: **1** if the spike validated. If it invalidated an architectural or requirement-level assumption, prefer **3**; if it mainly changes frontier/slice feasibility, ordering, or dependencies, prefer **4**.
