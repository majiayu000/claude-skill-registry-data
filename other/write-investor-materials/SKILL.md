---
name: write-investor-materials
description: >-
  Turns a validated business plan into a pitch deck outline and investor outreach notes, every
  claim traced to a plan section, called by ceh-business-plan:develop-business-plan.
disable-model-invocation: false
user-invocable: false
license: Apache-2.0
---

# Write investor materials

Turn the plan into what an investor reads: a slide-by-slide deck outline and the outreach notes
that get it opened. Done is `.agents_workspace/product/business/INVESTOR_DECK.md` and
`.agents_workspace/product/business/INVESTOR_OUTREACH.md`, where every slide's claim cites the plan section it comes from with its confidence tag,
and the ask states the amount, the months of runway it buys, and the milestones it reaches.

## Procedure

1. Read the plan, schema in `${CLAUDE_PLUGIN_ROOT}/references/business-plan-schema.md`. Check the
   frontmatter: `status: validated` and `pmf_gate: 8/8`. Anything less, stop (see Stop
   conditions).
2. Write the one-liner: who it is for, what it does for them, and the one number that proves
   someone wants it. It opens the deck and the email, so draft it first and fit the rest to it.
3. Draft the deck, one slide per row of the table below, in that order. Each slide is a headline
   that states a claim, not a topic ("Clinics lose 11 hours a week to rebooking", not "Problem"),
   two or three lines of proof, and the plan section it comes from.
4. Write the ask from §11 and §13: the amount, the months of runway it buys at the plan's burn,
   and the milestones from §13 it reaches before the money runs out. A raise that reaches no
   milestone buys time, not progress, and an investor reads it that way.
5. Write the outreach notes: the investor profile that fits (stage, cheque size, sector, a thesis
   this plan matches), a cold email of at most 120 words, and one follow-up line for two weeks
   later.
6. Write both files, then show the one-liner and the ask, and ask about the weakest slide, one
   question per turn, three at most. Revise in place after each answer.

## Deck

| #   | Slide             | From the plan                                             |
| --- | ----------------- | --------------------------------------------------------- |
| 1   | One-liner         | §01                                                       |
| 2   | Problem           | §02, with the customer's own words where §02 quotes them  |
| 3   | Customer          | §03, the beachhead, not the whole market                  |
| 4   | Solution          | §04 and §05                                               |
| 5   | Traction          | §10, numbers with dates                                   |
| 6   | Market            | §07, the bottom-up count, never a top-down percentage     |
| 7   | Business model    | §08 and the unit economics in §11                         |
| 8   | Competition, edge | §06 and the strategy subsection, what stops a copy        |
| 9   | Go-to-market      | §09, the channel and its arithmetic                       |
| 10  | Team              | not in the plan: ask, and mark `[assumption]` until given |
| 11  | Risks             | §12, the top risk and the test already scheduled for it   |
| 12  | Ask               | step 4                                                    |

## Rules

- **Carry every confidence tag onto the slide.** A number tagged `[assumption]` in the plan stays
  `[assumption]` in the deck. Investors check, and one inflated claim discounts every true one.
- **Never invent an investor, a quote, a logo, or a team member.** Name investors only when the
  user supplies them or a source is cited beside each name.
- **Traction beats vision.** When §10 holds a real number, it moves up to slide 2 and the order
  shifts down by one. When it holds none, slide 5 says what the next test is and when it ends.
- **Keep the risks slide.** A deck with no risks reads as a founder who has not looked, and the
  scheduled test in §12 is the strongest answer to "what could kill this".
- The deck is an outline in Markdown. Layout and visuals belong to whatever tool builds the
  slides.

## Output

Both files stay local beside the plan, not committed, like all business material: the outreach
notes may name investors and contacts.

`.agents_workspace/product/business/INVESTOR_DECK.md` fills `assets/investor-deck.template.md`, per
`references/investor-deck-schema.md`, one numbered `##` slide per headline claim.

`.agents_workspace/product/business/INVESTOR_OUTREACH.md`, beside it, fills `assets/investor-outreach.template.md`, per
`references/investor-outreach-schema.md`.

## Stop conditions

- `status` is `draft` or `pmf_gate` is below `8/8` → stop, and name
  `ceh-business-plan:find-product-market-fit`. Materials built on an unvalidated plan sell its
  assumptions as facts. If the user still wants them, write them with `Draft: gate <N>/8` at the
  top of both files.
- §11 has no burn or runway → the ask cannot say what the money buys. Name
  `ceh-business-plan:stress-test-unit-economics`.
- **No human to answer** (a headless run, or called by another agent): ask nothing. Draft from the
  plan, tag every gap `[assumption]`, and end with the questions you would have asked, in order,
  each with the assumption you used instead.
