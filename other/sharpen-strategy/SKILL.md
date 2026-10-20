---
name: sharpen-strategy
description: >-
  Turns a business plan's strengths into a strategy of where to play, how to win, and what to
  refuse, checked against nine tests, called by ceh-business-plan:develop-business-plan.
disable-model-invocation: false
user-invocable: false
license: Apache-2.0
---

# Sharpen strategy

Replace a plan's list of strengths with a strategy: a small set of choices that fit together, that
a rival cannot copy cheaply, and that visibly give something up. Done is a §04 Strategy block in
`BUSINESS_PLAN.md` that passes the nine tests below or carries a named test for each one it fails.

## Procedure

1. Read the plan, schema in `${CLAUDE_PLUGIN_ROOT}/references/business-plan-schema.md`. Read §02
   to §09 in full: strategy is a claim about how those sections fit.
2. Answer three questions from the plan alone, one sentence each: what business is this, who is the
   customer, what does the customer value? (Peter Drucker's questions.) A question the plan cannot
   answer is the first gap. Stop there and ask it.
3. Draft the strategy statement yourself before asking anything else. Three parts:
   - **Where we play:** one segment, one occasion of use, one geography or channel.
   - **How we win:** the single advantage, stated as what the customer gets that the alternative
     cannot give.
   - **What we refuse:** at least three things a reasonable competitor does and this plan will not.
4. Run the nine tests. Mark each pass, fail, or untested, with the reason in one line.
5. Write the block into §04 now, then show it with the test results. Writing before asking keeps
   the draft if the session is interrupted.
6. Ask about the worst failure, one question per turn, offering your own hypothesis for the user
   to correct. Fold each answer into §04 in place and re-run the tests it touches. Stop when
   every test passes or has a cheap dated test attached, or after five questions, whichever comes
   first. A test still failing then stays in the table as a failure.
7. Update §06 with one copy-cost line per named competitor, ending `(sharpen-strategy)`, and
   re-score criterion 3 of the PMF gate.
8. List what §05, §09, and §13 now contain that the strategy refuses, and ask the user to confirm
   the list before removing anything. Never touch another skill's subsection: report a conflict
   with it instead, because each specialist owns its tagged lines and some are fixed on purpose.

## The nine tests

| Test          | Ask                                                                                                                                            | Fails when                                                                              |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Trade-off     | Would a sane competitor choose the opposite? (Michael Porter: strategy is choosing what not to do.)                                            | Nobody would choose the opposite. "High quality" and "customer-focused" are not choices |
| Copy cost     | If the strongest incumbent copied this tomorrow, what would it cost them?                                                                      | It costs them nothing. The best answer hurts their existing business to copy            |
| Ten-year      | Which customer want here will still hold in ten years? (Jeff Bezos built on low prices, selection, fast delivery.)                             | The advantage rests on a fashion, a loophole, or a platform's current rules             |
| Pricing power | Could the price rise 10% without losing the customer? (Warren Buffett's test of a good business.)                                              | The customer would switch at once, so the product is a commodity with a nicer wrapper   |
| Small pond    | Can this be first or second in a market defined narrowly enough to matter? (Sam Walton started in towns rivals ignored. Jack Welch: #1 or #2.) | The market named is one where this plan is a rounding error for years                   |
| Activity fit  | Do the choices reinforce each other? (Southwest: one aircraft type, point to point, fast turnarounds, each making the others cheaper.)         | The choices are independent, so a rival can copy the best one and skip the rest         |
| Why now       | What changed recently that makes this possible or necessary? (Andy Grove's 10x force.)                                                         | It could have been built five years ago and nobody did, with no account of why          |
| Competence    | What does this team know or own that others do not? (Buffett's circle of competence.)                                                          | The plan depends on the team being smarter in a field it has not worked in              |
| Fresh owner   | If new owners took over tomorrow, what would they drop? (Grove's question before Intel left memory chips.)                                     | The answer is something the plan keeps for sentiment, sunk cost, or habit               |

## Sources of advantage

When the "how we win" line is vague, test it against the five sources that survive competition.
Name which one the plan claims and what evidence exists today.

- **Cost from scale or design:** lower unit cost a smaller rival cannot match. Ingvar Kamprad set
  the price first and designed the furniture down to it.
- **Network:** each customer makes the product more useful to the next.
- **Switching cost:** leaving costs the customer data, retraining, or integration work.
- **Brand:** the customer pays more for the name, or trusts it where trust is the product.
- **Exclusive asset:** a license, a location, a dataset, a relationship no rival can buy.

A plan at idea stage usually holds none of them. Then the honest strategy is speed inside a small
pond, plus a statement of which source it intends to build first and what would show it forming.

## Rules

- Draft first, ask second. A concrete strategy the user can correct gets a sharper answer than
  "what is your strategy?".
- One question per turn, aimed at the worst failing test.
- The refusal list is the test of the whole exercise. A strategy that gives nothing up is a wish
  list, and each refusal must be something genuinely tempting.
- Keep the confidence tags from the schema. A moat claim is `[assumption]` until a customer or a
  number shows it.
- Do not invent competitors or their prices. Name the ones the plan or the user supplied, and tag
  anything recalled from general knowledge `[assumption]` for the user to confirm.
- Inertia counts as a competitor. Run the copy-cost and pricing-power tests against "keeps doing
  what they do now" as well as against named rivals.

## Output

Written into §04 of `BUSINESS_PLAN.md`:

```markdown
### Strategy

- **Where we play:** <segment, occasion, geography or channel>
- **How we win:** <the one advantage, in customer terms> [tag]
- **What we refuse:** <thing>, <thing>, <thing>
- **Advantage being built:** <cost | network | switching cost | brand | exclusive asset> — <what
  would show it forming>

| Test | Result | Reason or test attached |
| ---- | ------ | ----------------------- |
```

## Stop conditions

- The plan has no named customer or no stated problem → strategy has nothing to stand on. Report
  that and name `ceh-business-plan:find-product-market-fit`.
- Every candidate advantage fails the copy-cost test and the user has no further material → write
  the block with the failures showing and say plainly that the plan has no defensible edge yet.
- **No human to answer** (a headless run, or called by another agent): ask nothing. Draft and
  revise from what the plan holds, tag every gap `[assumption]`, and end with the questions you
  would have asked, in order, each with the assumption you used instead. Remove nothing in step 8:
  list the conflicts, because a removal is the user's call.

## Hands off to

- When the pricing-power test fails or is untested, suggest
  `ceh-business-plan:stress-test-unit-economics`.
- When the small-pond test changes the segment, suggest `ceh-business-plan:plan-go-to-market`,
  because the first-ten list is now wrong.
