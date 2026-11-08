---
name: trade-journal
description: >-
  Write and maintain JOURNAL.md — one block per position stating the thesis, the
  non-price condition that would prove it wrong, and what "the market caught up"
  looks like; plus a gate register of every dated trigger. Use when opening or
  closing a position, when a review reaches a conclusion worth keeping, when asked
  "should I sell X" and no written invalidation exists yet, or when checking whether
  a trigger has fired today.
---

# Maintain the trade journal

> **Setup.** The scripts sit beside this file. Run them from a working folder that
> holds your `.env` (E*TRADE consumer key/secret) and a `data/` directory; install
> deps with `pip install -r requirements.txt` where one is included. Part of a set:
> `etrade-pull`, `order-check`, `portfolio-review`, `realized-pnl`, `rebalance-plan`,
> `price-history`, `trade-journal`, `intrinsic-value`, `sec-financials`, `buffett-checklist`.

Start from `JOURNAL.template.md` in the repo root; copy it to `JOURNAL.md`, which is
gitignored. The template carries the full structure — this skill is how to operate it.

The purpose is narrow and worth stating plainly: **the hold/exit decision gets made
before conviction is tested, so it isn't made live in a moment of fear or greed.**
Everything below serves that.

## Opening a position

Write the block *before* the buy, not after. It must answer:

- **Thesis** — the real-world mechanism. Not "it's cheap."
- **Why I'm early** — what the market hasn't priced, and why not. *If this can't be
  answered, the position is consensus and should expect consensus returns. Writing
  it down is the only cheap way to find that out.*
- **Invalidation** — specific, fundamental, and **non-price**. A named event or
  number meaning the thesis was wrong.
- **Sell-into-strength signal** — what recognition looks like.
- **Catalyst / timeline** — the dated events that would close the gap.

## Rules

- **Invalidation is never a price.** "Down 20%" is volatility, not evidence. *A
  price-based invalidation converts every drawdown into a sell signal, which is the
  exact behavior the journal exists to prevent* — and see `realized-pnl`'s
  counterfactual for what that habit costs in practice.

- **Never edit a past entry to match what happened.** Amend by appending a dated
  line to the review log. *A journal rewritten in hindsight records only that you
  were always right, which is worth nothing when you later need to know whether you
  were unlucky or wrong.*

- **Log what you considered and did not do, with the reason.** *The rejected trades
  are half the record and the half nobody keeps.*

- **Most bad news is not invalidation.** When something happens, state explicitly
  whether it meets a written criterion or is merely bad. *Forcing that answer in
  writing is the whole mechanism; "this seems concerning" is how a rule gets
  quietly abandoned.*

- **Keep exited positions in the file**, marked `EXITED <date>` with what actually
  happened. *A thesis that didn't work is the most useful thing in here later.*

- **Adding to a position is a new decision.** It must re-clear the thesis, not
  inherit it. *Averaging down without re-underwriting is how a small mistake becomes
  the largest line in the book.*

## The gate register

One table indexing every dated trigger already written in prose somewhere in the
file. It is **the index, not the authority** — the position block wins on reasoning.
It exists because once the file is long, reconstructing every live trigger from prose
is exactly where one gets missed.

| Date | Name | What | Action it unlocks | State |
|---|---|---|---|---|

**Fire on the transition, not the state.** A gate reading "under $227" is true every
day the price sits there. *Acting on the state means re-deciding a settled trade
every morning; ignoring the noise means missing the crossing.* So each gate is
`ARMED` until it crosses, then stamped `FIRED <date>`, and stays fired until
deliberately re-armed with a reason.

When asked whether something fires today: read the register, check the transition,
and answer yes or no with the date. Don't re-derive the trade — it was already
decided, by design.

## After a review

A review that changes nothing on paper gets re-litigated from scratch next month.
When `portfolio-review` reaches a conclusion, append it to the review log with
the date, what changed, and what it means for each affected thesis.
