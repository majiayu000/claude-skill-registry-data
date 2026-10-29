---
name: submission-writeup
description: Draft or revise submission.md, the Project Mark submission write-up, and every golden deliverable that ships with it. Invoke whenever a submission.md is being written, rewritten, extended or reviewed for a task folder, including when the request just says "write the submission", "draft the write-up", "do the submission for taskNN", or when a review says a block is thin. Carries the five blocks in order (tags, final recommendation, critical components, a step-by-step solution of at most eight one-line steps, and deliverable answers stated as bare answers grouped by file), the concision rule that keeps the write-up from failing the in-task determinism grader (every figure written is a claim the grader recomputes, so the write-up states the answer and a reproducible path and nothing else), and the golden deliverable rules for the one-to-three-file set. There is no deliverable format rationale, justification or golden solution block.
---

# Writing the Submission

The write-up is the answer key. The rubric is **generated** from it, the prompt and the goldens, never
hand-edited, and needs **25 or more criteria**; a wrong rubric is fixed in the prompt or the golden. Asks
carry about 55 to 60 percent. Spec: `guidelines/rubric.md`.

## Short is the standard

The in-task grader recomputes every figure in every block from the shipped files ("reproduce, do not
assume", `guidelines/determinism_judge_system_prompt.md`). Every extra figure is one more claim that can
fail, so a long write-up fails determinism even when the answer is right.

- **Cut words and incidental figures, never owed figures.** Every figure a component or an ask owes stays
  (each is a criterion). A figure that only shows working (a sub-count, a denominator, a rival's
  intermediate) goes.
- **Reproducible, not low-level.** Steps name the file and rule that produce each result; they do not walk
  arithmetic, restate the files' conventions or narrate cleaning. A convention needing a paragraph belongs pinned
  in a shipped file.

**Not written:** Deliverable Format Rationale, Justification, Golden Solution listing, Key Assumptions,
Determinism block. Never copy one from an older task or from `guidelines/`.

**Every figure is emitted, never typed.** The generator writes `<task>/generator/figures.json` (the call,
each component, each step result, each deliverable answer, as the write-up states them); blocks 1 to 4
are drafted from it, and this fails the build on any number absent from it:

```
python3 .claude/skills/determinism-check/figures_check.py taskNN
```

Typed figures and steps that read differently when followed literally were twelve of sixteen write-up
findings in one window of judge reports, so each step uses the verifier's words and figure.

**Order:** build, `determinism-check`, this skill, `golden-realism`; never before the analysis is done.

## The blocks, in order

| # | Block | Length |
|---|---|---|
| 0 | `## Tags` (unnumbered) | 2 to 3 lines |
| 1 | `## 1. Final Recommendation` | 1 sentence, the deciding figure, 1 clause per rival |
| 2 | `## 2. Critical Components` | 2 to 5 one-liners |
| 3 | `## 3. Step-by-Step Solution` | at most 8 one-liners |
| 4 | `## 4. Deliverable Answers` | grouped by file, answer lines only |

Nothing else goes in the file.

**0. Tags.** The Axis 0 domain and the Axis 1 objective in the taxonomy's exact wording (`guide-to-prompt`);
the objective is one of the **eight** labels or the task is rejected on the tag. No scenario recap.

> **Domain:** Economics, prices and inflation (inflation decomposition).
> **Analytical objective:** Forecasting and predictive modelling.

**1. Final Recommendation.** The call in one sentence, no conditions, no "subject to". A hold is stated as
a call ("We should fund none of the three programs this cycle"). Then the deciding figure and the margin,
then one clause per rival: what it leads on and why it loses. No figure blocks 2 to 4 do not carry.

> **We should not acquire Data Corporation at the asking price.**
> The price is 20x normalized EBITDA against the 12x mandate ceiling. Not the reported revenue case, which
> counts one-time and related-party sales. Not the trailing margin, which defers R&D.

**2. Critical Components.** 2 to 5 intermediate results **every valid methodology must compute** for the
main call, one line each, figure in bold at its rounding everywhere else. Test: if a defensible method
could skip it and still land the call, cut it.

> 1. Recurring revenue is **USD 38M**
> 2. Normalized EBITDA margin is **13%**

**3. Step-by-Step Solution.** At most eight one-sentence steps, the last being the recommendation. Each
is the method, the shipped file or rule, and the one result it produced.

> 2. Removed one-time and related-party sales per the revenue policy: recurring revenue is USD 38M.
> 5. Divided the asking price in the term sheet by normalized EBITDA: 20x, above the mandate's 12x ceiling.

- No sub-bullets; never pad to eight or cram two steps into one line.
- Carry only the result the next step uses or the call rests on; owed detail lives in block 4, once.
- The one exception: an ask whose device is silent gets a step naming the handling the golden uses and
  the files it joins, ending in the ask's figures, so the grader can verify what the solver is never told
  (`supplemental-stumping` Part 3). It counts toward the eight.
- Cite where a convention is pinned ("per the revenue policy"), never restate it. A convention a
  competent analyst could reverse is an unpinned fork, fixed in a shipped file.
- Name only files the pack ships, by their pack names, or the grader finds missing input.
- End in a figure or finding, never an intention ("Analyzed the cohort data" is not a step).

**4. Deliverable Answers.** Graded at the main call's bar: each reproduces and is uniquely forced. Grouped
by file under `### <file.ext>`, in the prompt's order of files and asks. **Answer lines only**, in the
exact unit and rounding asked: no Basis line, no restated ask, no method.

- **Concise is not summarised.** An ask owing a row-set gets every row as its own point, every column value
  named, in the deliverable's order, one level of points under the numbered item.

> 1. Transfers, 42 rows in the file's order, whole units:
>    - Store 118: send 340 to store 204, 1,120 on hand now, 780 after

- **Never a markdown table** (pipes in names break columns, wide tables wrap, odd tables are an LLM tell).
- A content requirement gets one line saying what the deliverable contains and where ("Bar chart of
  margin by category on page 2 of the memo, runner-up highlighted").
- A figure in two files has the same rounding in both and here; compute it once in code and carry it.

## Golden deliverables

- **One to three files, every one the prompt named, in its format.** Four is a spec failure. No format
  family is assigned; prefer a visual where it makes the decision read at a glance. Together they answer
  every ask and the call.
- **Business-realistic is a gate**: once figures are frozen, run every golden through `golden-realism`.
- **The recommendation is unmissable**, never inferred from output.
- **The code deliverable prints the critical components' figures**, not only the answer.
- **Prefer code-produced artifacts** (a library chart, a script-written workbook, an emitted CSV); a chart
  in a text deliverable still comes from the script.
- **Consistency is graded**: every shared figure agrees, same rounding, in every file and in block 4.

## Rejection causes

LLM tells (em dashes, odd tables, white space, extra headers, filler such as *leverage, robust, seamless,
comprehensive*, hedging near the call); a figure that does not recompute; padding; a component another
valid method skips; an unpinned convention; a conditional call.

## Checklist

- [ ] Exactly the five blocks; none of the banned blocks
- [ ] Tags in taxonomy wording; block 1 one committed sentence, deciding figure, one clause per rival
- [ ] Block 2: 2 to 5 components every method computes; block 3: at most 8 one-line steps naming shipped files
- [ ] Block 4: every ask and every owed figure, answer lines only, exact unit and rounding, no table
- [ ] No incidental figure; shared figures agree everywhere to the same rounding
- [ ] One to three goldens, code prints the components, charts rendered by code, `golden-realism` run after figures froze
- [ ] `figures_check.py` exits 0; no em dashes
