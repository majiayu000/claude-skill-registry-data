---
name: run-premortem
description: >-
  Premortem on a business plan that writes how it fails and gives each top risk a warning signal, a
  kill criterion set in advance, and a loss cap, called by ceh-business-plan:develop-business-plan.
disable-model-invocation: false
user-invocable: false
license: Apache-2.0
---

# Run premortem

Work backward from failure. Charlie Munger's rule is to invert: find what would guarantee the
outcome you fear, then avoid it. Done is a §12 in `BUSINESS_PLAN.md` where every top risk has a
story, a signal, a kill criterion with a date, and a cap, and where the most that can be lost is
written as a number.

## Procedure

1. Read the plan, schema in `${CLAUDE_PLUGIN_ROOT}/references/business-plan-schema.md`. List
   every `[assumption]` tag. Those are the candidate causes of death.
2. Set the scene and write it down: it is 18 months from today and the business has failed. Write
   five to seven failure stories, each a specific sequence of events with a cause and a month.
   Draft them yourself from the plan, then ask the user which one they privately fear most.
3. Cover the standing causes. At least one story for each that applies:
   - Cash ran out before the model worked.
   - Customers agreed it was a problem and did not care enough to pay or switch.
   - The customers could not be reached at a cost the price supports.
   - An incumbent or platform responded.
   - One person, supplier, platform, or regulation the plan depends on changed.
   - The product shipped late or never worked well enough.
   - The founders ran out of time, money, or will.
4. Rank the stories by likelihood and by whether the outcome is survivable or ruinous. A ruinous
   outcome ranks first whatever its odds. Never risk what you need for what you only want.
5. For each of the top three, write the three guards in the Output table: the early warning
   signal, the kill criterion, and the cheapest test.
6. Classify every major commitment in the plan as a one-way or two-way door (Jeff Bezos's
   distinction). Two-way doors are reversible: decide fast, on roughly 70% of the information you
   would like. One-way doors get slowed down and, where possible, converted. Richard Branson
   leased Virgin Atlantic's first aircraft with the right to hand it back after a year. Find the
   equivalent: a pilot, a monthly contract, an option, a smaller first order.
7. Write the incumbent's best reply. Pick the strongest rival and state the countermove that would
   hurt most, what it would cost them, and the plan's answer. Andy Grove's standing assumption
   was that someone is already working on it.
8. State the cap: the most money and the most months this can consume before it stops, and what
   remains if it fails (skills, customers, code, relationships, reputation).
9. Write §12 now, and schedule each test and kill date in §13 as one line ending
   `(run-premortem)`. Writing before asking keeps the guards if the session is interrupted.
10. Ask about the weakest guard, one question per turn, three questions at most. Revise §12 in
    place after each answer. A guard still open stays tagged `[assumption]`. Then re-score
    criterion 8 of the PMF gate.

## What a good guard looks like

| Guard          | Good                                                                 | Useless                                 |
| -------------- | -------------------------------------------------------------------- | --------------------------------------- |
| Warning signal | Observable within weeks, before the money is gone                    | "Revenue is low" a year in              |
| Kill criterion | A number and a date, written today: "under 5 paid by 31 March, stop" | "If it isn't working, we'll reassess"   |
| Cheapest test  | Days and a small sum, and it could come back negative                | A survey asking if people like the idea |
| Cap            | A sum of money and a number of months                                | "We'll be careful with spending"        |

Set kill criteria now because judgment bends later. Once months and savings are sunk, every result
looks like a reason to continue. A criterion written in advance is the only one that will be
honoured.

## Rules

- Stories, not categories. "Market risk" teaches nothing. "By month six, 40 demos and 2 sales,
  because buyers needed sign-off we never planned for" can be tested.
- Draft the stories before asking. People find it easier to rank failures someone else wrote than
  to imagine their own.
- Stay adversarial to the plan and on the side of the person. The aim is a plan that survives,
  so every story ends with a guard.
- Do not soften a ruinous risk. If the downside includes personal guarantees, debt against a home,
  or a legal exposure, name it in the first line of the report.
- Three guarded risks are worth more than fifteen listed ones.
- For legal, tax, licensing, or regulatory risks, state that the plan needs a qualified
  professional's review and record that as the test. Do not give the ruling yourself.
- Keep the confidence tags. A risk with a scheduled test becomes `[hypothesis-to-test]`.

## Output

Written into §12 of `BUSINESS_PLAN.md` as one subsection. A re-run replaces it, except that a kill
criterion whose date has passed is kept as written (see Stop conditions):

```markdown
### Premortem

Run on <date>.

| #   | Failure story | Likelihood | Survivable | Warning signal | Kill criterion | Cheapest test |
| --- | ------------- | ---------- | ---------- | -------------- | -------------- | ------------- |

#### Commitments

| Commitment | Door | How to make it reversible |
| ---------- | ---- | ------------------------- |

#### Incumbent reply

<rival> would <countermove>, costing them <what>. Our answer: <answer>.

#### Cap

Most this can cost: <money> and <months>. If it fails, what remains: <list>.
```

## Stop conditions

- A ruinous risk has no cap and no way to convert it → stop and tell the user plainly that the
  plan should not proceed in this form, and what would have to change.
- The user asks to delete or weaken a kill criterion after a result has come in → refuse to
  rewrite history. Record the original, the result, and the new decision as a separate dated line.
- **No human to answer** (a headless run, or called by another agent): ask nothing. Draft and
  revise from what the plan holds, tag every gap `[assumption]`, and end with the questions you
  would have asked, in order, each with the assumption you used instead.

## Hands off to

- When the top story is about cash, suggest `ceh-business-plan:stress-test-unit-economics`.
- When the top story is about an incumbent, suggest `ceh-business-plan:sharpen-strategy`.
- When the guards are set, suggest `ceh-business-plan:set-operating-plan` so each has an owner.
