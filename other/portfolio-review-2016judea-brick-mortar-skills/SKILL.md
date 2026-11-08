---
name: portfolio-review
description: >-
  Evaluate a person's portfolio end to end — what they actually hold, what their
  past trades really did, and what to do next. Use when someone says "review my
  portfolio", "how's my book doing", "what should I do with this cash", "should I
  sell X", "is now a good time to add", or hands over a brokerage account and asks
  what to make of it. This is the ENTRY POINT for this repo: it decides which
  pulls are needed and forward-references the tool skill that owns each one. Ends
  with a specific recommendation and the grounds for it — never a survey of
  considerations.
---

# Evaluate a portfolio

You are being asked what to do, not what could be considered. The output is a
**decision, with the reasoning loaded and ready** for the follow-up "why?" — not a
list of factors weighted equally.

Everything below is a pull-then-reason loop. Each pull belongs to a tool skill;
this skill only decides which ones are needed and in what order.

## Before you say anything about the numbers

**0. Confirm the data is actually theirs.** If example CSVs are lying around in
`data/` (a demo account loads without error), check the `_accountId` column — example
rows say `EXAMPLE`. *Reading example data and reporting it as someone's
book is the single worst failure available here, because it is confident, specific,
and wrong.*

**1. Confirm it's production, not sandbox.** With `ETRADE_ENV` unset the client
hits the sandbox, which returns four canned accounts and **zero securities
trades**. That reads exactly like "this person doesn't trade." See
`etrade-pull`.

## The order of work

1. **What do they hold right now?** → `etrade-pull` for live positions,
   weights, cost basis, unrealized P&L. Establish concentration before anything
   else: the largest position, and any group of positions that dies on the same
   news. *Two names with one thesis is one position wearing a disguise, and it
   won't show up in a per-name weight table.*

1b. **Is anything they believe is live actually in the market?** →
   `order-check`. Run it before reasoning on top of any gate, and *first* if
   a position is over its cap. *A written stop and a resting stop are different
   states, and a journal cannot tell them apart — one book sat 100% in a single
   name with its stop existing only on paper, and the register said the stop was
   its only remaining risk control. Both were true at once.* If it reports an
   unprotected over-cap position, that is the review's headline; everything about
   weights and P&L waits.

2. **What did their trades actually do?** → `realized-pnl`. Closed lots,
   FIFO-matched, best and worst, and the by-symbol roll-up. This is the difference
   between what someone believes about their investing and what happened.

3. **What does their behavior say?** Run `backtest_holding.py` (documented in
   `realized-pnl`). For every loss they took, it computes what the position
   would be worth held to today and at its 52-week high. *A book can look fine on
   holdings and still be losing money on a repeated exit mistake — that pattern is
   invisible in a positions table and obvious in this one.* If the counterfactual
   is large and consistently against them, that is the finding, and it outranks
   anything about the current holdings.

4. **Where is each name in its own cycle?** → `price-history` for trailing
   returns, distance off the period high, and seasonality. Use it to locate a name,
   not to time it.

5. **Does the thesis survive a skeptic?** → `buffett-checklist` for a
   valuation/moat/temperament read. Apply it hardest to whatever they are most
   confident about.

6. **If the answer is a trade** → `rebalance-plan` to turn target weights
   into a concrete order list with a tax tag per row.

7. **Write the decision down before it's tested** → `trade-journal`. A review
   that changes nothing on paper will be re-litigated from scratch next month.

Skip steps that don't bear on the question. A "should I sell X" question usually
needs 1, 3, 5 and 7 and nothing else. **Step 1b is the exception — never skip it
when the answer will lean on a gate**, because its whole job is to catch the case
where the gate you are reasoning from does not exist.

## Rules

Each carries its reason, because a rule without one gets rationalized around the
first time it's inconvenient.

- **Never place an order, and never imply one was placed.** Nothing in this repo
  can. The division of labor is deliberate: the analysis decides and shows its
  grounds, the person executes. *An agent that both decides and executes removes
  the one checkpoint where a human can catch a wrong premise.*

- **Every figure comes from a pull you just ran.** Never from memory, never from a
  previous session, never estimated to fill a gap. *A plausible wrong number is
  worse than a missing one — it gets acted on, and nothing downstream flags it.*
  If you don't have it, say so.

- **Never state a net realized figure as lifetime performance.** The transactions
  API retains ~3 years. Sells whose matching buys fall outside that window are
  reported separately with no cost basis. *Treating the in-window total as "how
  they've done" is wrong by exactly the amount you can't see.*

- **Say what you cannot see.** Retirement accounts at other institutions, tax lots
  and holding periods, anything held at another broker. *A concentration warning
  that ignores a 401(k) held elsewhere is not conservative, it's just incorrect —
  the position may be 4% of their net worth, not 28%.*

- **Distinguish a drawdown from a thesis break.** Price falling is not new
  information about the business. If they have a written invalidation
  (`trade-journal`), check it before discussing the price at all. *Most "should
  I sell" questions arrive during a drawdown, which is precisely when the answer is
  least reliable if it's decided fresh.*

- **A ratio under ~2x is not a finding.** 29% versus 30.5% is noise dressed as
  insight. *Reporting a spread that small teaches the reader to act on randomness.*

## The shape of the answer

Lead with the call. Then the grounds, in the order that would change the call if
any of them were wrong. Then, briefly, what would make you change your mind.

> **Trim AAPL by ~41 shares.** It's 28.5% of the sleeve against a 20% target, and
> it's the only position where a sale is close to tax-neutral. The concentration
> is the reason, not the price — this would be the same call 10% higher.
>
> Against it: the lot turns long-term in March, so waiting saves the short-term
> rate on the gain. If the concentration isn't keeping you up, waiting is defensible.

Not: *"There are several factors to consider regarding your Apple position…"*
