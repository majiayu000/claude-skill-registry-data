---
name: review-business-plan
description: >-
  Report-only board review of a business plan that scores seven lenses and names the one finding
  that most changes it, called by ceh-product-direction:develop-business-plan.
disable-model-invocation: false
user-invocable: false
compatibility: >-
  Checking and rendering BUSINESS_PLAN.yaml needs uv; without it the YAML is saved unchecked
  and its Markdown is not rendered.
license: Apache-2.0
---

# Review business plan

Judge a business plan on the seven things experienced operators check first, and return a scored
report with one headline finding. Done is the report in the Output format with all seven lenses
scored, each score backed by a quote or "nothing found", and the next skill named.

## Procedure

1. Read the whole plan. Default to `.agents_workspace/product/business/BUSINESS_PLAN.yaml`,
   checked first as the `business-plan/v3` section of
   `${CLAUDE_SKILL_DIR}/references/business-plan-schema.md` says, or its `BUSINESS_PLAN.md` when
   no YAML exists, since a review only reads. Any other plan, deck, or memo the user supplies is
   reviewed the same way.
2. Score each lens 0, 1, or 2 using the table below. Quote the sentence in the plan that earns the
   score. A lens with nothing to quote scores 0.
3. Answer the fresh-owner question: if new owners took this plan over tomorrow with no attachment
   to it, what would they stop, and what would they do first? (Andy Grove asked this of Intel's
   memory business and exited it.)
4. Pick the headline finding: the single lens whose failure makes the other scores irrelevant.
   Order of precedence when several score 0: customer, then survival, then money, then edge, reach,
   focus, execution. A plan nobody wants needs no cost model.
5. Set the verdict from the scores, not from impression:
   - **do not build:** Customer scores 0 and the plan offers no path to a test.
   - **build:** no lens scores 0 and the total is 10 or more.
   - **fix first:** everything else.
6. Write the report in the Output format and stop. Do not edit the plan.

## The seven lenses

| Lens      | The question                                                                                                                   | Scores 2 when                                                                                      |
| --------- | ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| Customer  | Who is the customer, what do they value, and what do they do today instead? (Drucker's three questions.)                       | A named person or account, their words quoted, and their current workaround with its cost          |
| Edge      | Why does this customer pick you, and what stops a better-funded rival doing the same? (Buffett's moat.)                        | The advantage costs a rival something real to copy, and the plan says what                         |
| Focus     | What is the plan refusing to do? (Jobs cut Apple's line to four products in 1997.)                                             | One segment, one product, one channel, and an explicit list of attractive things declined          |
| Money     | Does one unit make money, and does cash arrive before it runs out?                                                             | Unit arithmetic is shown, the cash low point is dated, and the plan survives its own bad case      |
| Reach     | How do the first ten customers hear about this, and what does each one cost to win?                                            | The first ten are named or listed, one channel is chosen, and a cost per customer is estimated     |
| Survival  | What kills this, how would you know early, and what is the most that can be lost? (Munger: invert.)                            | Top risks have a warning signal, a kill criterion set in advance, and the maximum loss is a number |
| Execution | What happens in the next 90 days, who owns it, and which weekly number shows it working? (Grove's objectives and key results.) | At most three objectives, each with an owner, a date, and a controllable weekly input              |

Score 1 is the middle case on every lens: the plan asserts an answer but offers no evidence and no
test.

## Rules

- Score what is written, not what the author probably meant. A reviewer who fills gaps with charity
  hides exactly the holes the review exists to find.
- Evidence is a quote, a transaction, a signed letter, a measured number, or a comparable spend. A
  market-size report and "everyone I asked liked it" are not evidence.
- Treat the plan's own confidence tags as claims to check. An `[evidence]` tag with nothing behind
  it scores as an assertion, and the report says so.
- Say "do not build this" when the customer lens scores 0 and the plan offers no path to a test.
  That verdict is the most valuable one a review can give.
- Praise only what is specific. Name the strongest sentence in the plan and why it is strong, so
  the author keeps it through the next revision.
- No rewrite suggestions longer than one line per lens. The fix belongs to the skill the report
  routes to.

## Output

The review fills `assets/business-plan-review.template.yaml`, per the `business-plan-review/v3`
section of `references/business-plan-review-schema.md`. Save it as a round of the one review file
in `.agents_workspace/product/review/business-plan/`, never into the plan, which this skill only
reads, so the scores survive into the session that runs the next skill. Follow the schema's Review
lifecycle, and score the plan before reading the file, so earlier rounds do not anchor this one:

1. Find the file, `<YYYYMMDD-HHMMSS>-business-plan-review.yaml`. With none, take the time from one
   `date +%Y%m%d-%H%M%S` call. A found `business-plan-review/v2` file is converted to `v3` in
   place first.
2. Set each `open` finding whose lens now scores 2 to `fixed`, with the resolution
   `found fixed in round <n>`.
3. Append the round, and add an `open` finding for each lens below 2 that has none open.

Name the path in the reply. After the last edit, run `uv run --script ${CLAUDE_SKILL_DIR}/scripts/artifact.py render <file>.yaml`,
which writes the `.md` beside it in the layout of `assets/business-plan-review.template.md`, and
fix the YAML for each error it lists. Never edit the generated `.md`. On exit 2 or 3, or without
uv, say in the reply that the review went unchecked and unrendered.

## Stop conditions

- No plan exists, only an idea → say there is nothing to review yet and name
  `ceh-product-direction:find-product-market-fit` as the place to start.
- The plan describes a different product than the app plan or repository it sits beside → report
  the mismatch as the headline finding. Every other score is unreliable until it is settled.

## Hands off to

Each handoff is conditional on the lens scoring below 2, so the user chooses which to run.

- Customer → `ceh-product-direction:find-product-market-fit`
- Edge or Focus → `ceh-product-direction:sharpen-strategy`
- Money → `ceh-product-direction:stress-test-unit-economics`
- Reach → `ceh-product-direction:plan-go-to-market`
- Survival → `ceh-product-direction:run-premortem`
- Execution → `ceh-product-direction:set-operating-plan`
