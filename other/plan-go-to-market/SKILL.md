---
name: plan-go-to-market
description: >-
  Writes a business plan's go-to-market section, with the first ten customers, one channel, its
  arithmetic, and a pass-or-fail channel test, called by ceh-business-plan:develop-business-plan.
disable-model-invocation: false
user-invocable: false
license: Apache-2.0
---

# Plan go-to-market

Turn "we will market it" into a named list of first customers, one channel, and a test with a
number that decides whether to continue. Done is a §09 in `BUSINESS_PLAN.md` with every part of
the Output block filled, and the channel test scheduled in §13 with its dates and pass number.

## Procedure

1. Read the plan, schema in `${CLAUDE_PLUGIN_ROOT}/references/business-plan-schema.md`. Take the
   segment from §03 and the price and acquisition ceiling from §08.
2. Name the first ten customers. Real names or accounts where the user has them. Otherwise the
   exact list they come from: a directory, a community, a conference attendee list, a street. A
   segment description is not a list.
3. Find uncontested ground. Ask where these customers are that larger rivals find unprofitable or
   beneath them to serve. Sam Walton opened in small towns the big chains skipped and was
   established before they noticed.
4. Write the working-backwards page: a one-paragraph press release in the customer's own words,
   then the five hardest questions that customer would ask and the answers. (Amazon's practice
   under Jeff Bezos.) A dull release means the offer is dull. Fix the offer, not the wording.
5. Design the first taste. State how a customer experiences the value before paying or before any
   effort. Estée Lauder put the product on the customer's hand and gave samples away. Name the
   equivalent here: a free first job, a live demo on their data, a trial, a result delivered by
   hand.
6. Choose one channel using the table below. Start with selling by hand, founder to customer,
   until the pitch converts. Things that do not scale come first because they are how the pitch
   gets learned.
7. Do the channel arithmetic: people reached, share who respond, share who buy, cost and hours
   spent. The result is a cost per customer. Compare it with the ceiling from §08.
8. Look for the loop: what does each customer make cheaper or easier about winning the next?
   Referral, content they create, data that improves the product, lower prices from scale. If
   there is none, say the growth is linear and budget for it.
9. Set the channel test: two to four weeks, one number that means pass, and the next channel to
   try on a fail.
10. Name the one adjacent segment that follows the beachhead and what must be true before moving
    to it. Do not plan beyond that: anything further rests on beachhead results that do not exist
    yet.
11. Write §09 now, and put the channel test in §10 and §13 as one line each, ending
    `(plan-go-to-market)`. Writing before asking keeps the plan if the session is interrupted.
12. Ask about the weakest step, one question per turn, three questions at most. Revise §09 in
    place after each answer. Whatever is still open stays tagged `[assumption]`. Then re-score
    criteria 2 and 7 of the PMF gate.

## Choosing the channel

| Channel type        | Fits when                                                        | First test                                          |
| ------------------- | ---------------------------------------------------------------- | --------------------------------------------------- |
| Direct, by hand     | High price, few customers, each reachable by name                | Contact 30 on the list, count conversations         |
| Community           | Customers already gather somewhere and help each other           | Answer questions there for two weeks, count replies |
| Content and search  | Customers search for the problem in words you can name           | One page on the exact query, count qualified visits |
| Partner or reseller | Someone already sells to this customer and gains by adding you   | One partner, one joint offer, count introductions   |
| Paid                | Unit economics are known and the payback is short                | Small fixed budget, count cost per paying customer  |
| Product-led         | The product shows its value in minutes with no one explaining it | Count signups that reach the first result unaided   |

A channel fits when the customer is already there and the cost per customer sits under the ceiling.
Pick the one that passes both, and write down why the others were declined.

## Rules

- One channel until it works or fails its test. Several half-run channels teach nothing about any
  of them.
- People before populations. Push every "small businesses" to "name one".
- The founder sells first. Hiring sales or buying ads before the pitch converts by hand pays to
  scale a message that does not work.
- Never invent a customer name, a community, a conversion rate, or a list. Unknowns go in as
  `[assumption]` with the way to find out.
- Record what customers say word for word. Their phrasing becomes the press release and the page
  headline.
- A cost per customer above the §08 ceiling is a finding to report, not a number to tune until it
  fits.

## Output

Written into §09 of `BUSINESS_PLAN.md` as one subsection, replaced whole on a re-run:

```markdown
### Go-to-market plan

#### First ten

| #   | Name or source list | Why them | How reached | Status |
| --- | ------------------- | -------- | ----------- | ------ |

#### Press release and questions

<one paragraph, customer's words>

1. <hardest customer question> — <answer>

#### First taste

<what the customer gets before paying, and what it costs to give>

#### Channel

- Chosen: <one channel>
- Why this one: <customer is already there because ...>
- Arithmetic: <reached> x <respond %> x <buy %> = <customers>, cost <amount> = <per customer>
- Ceiling from §08: <amount> — <under | over>
- Declined: <channel> because <reason>

#### Loop

<what each customer makes easier about the next, or "none, growth is linear">

#### Channel test

<dates>, pass at <number>, on fail try <next channel>

#### Next segment

<segment>, only after <condition>
```

## Stop conditions

- The user cannot name a single candidate customer or the list they come from → stop. The segment
  is not yet real. Name `ceh-business-plan:find-product-market-fit`.
- Every plausible channel costs more than the §08 ceiling → report that the business cannot reach
  its customers at this price, with the gap in money per customer.
- §08 has no price or no acquisition ceiling → stop before step 6, because no channel can be
  judged without one. Name `ceh-business-plan:stress-test-unit-economics`.
- **No human to answer** (a headless run, or called by another agent): ask nothing. Draft and
  revise from what the plan holds, tag every gap `[assumption]`, and end with the questions you
  would have asked, in order, each with the assumption you used instead.

## Hands off to

- When the channel test is set, suggest `ceh-business-plan:set-operating-plan` to give it an owner
  and a weekly number.
