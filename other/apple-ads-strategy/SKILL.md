---
name: apple-ads-strategy
description: Use when planning Apple Search Ads before there is anything to read — designing an account structure, choosing which campaigns and ad groups to create, building a keyword taxonomy and starting negative list, sizing a starting budget, or deciding whether Apple Ads fits an app at all. Triggers on "how do I launch Apple Search Ads", "what campaigns should I create", "which keywords should I target", "structure my ASA account", or any Apple Ads question about an app that is not connected yet. Needs no account, no CLI and no subscription.
license: MIT
---

# Planning Apple Search Ads

This skill produces a **plan**: an account structure, a keyword taxonomy, a starting budget and a
negative list, specific to one app. It reads nothing and writes nothing. It never calls an API, so
it works with no Adapty account, no CLI installed and no Ads Manager subscription.

Execution belongs to the `apple-ads` skill. End every plan by saying so.

**Answer in the language the user writes in.** Everything here is English; translate your output,
never these instructions.

## Before planning anything, get four facts

Ask for what is missing — do not assume, and do not produce a plan with holes papered over.

1. **The app**: name, App Store category, and the App Store ID if they have it.
2. **Monetization**: subscription or one-off; period; trial length; price; hard or soft paywall.
   Everything downstream is a function of this — a weekly subscription and an annual one do not
   get the same structure, the same bids, or the same patience.
3. **Markets**: which countries, and whether they are the paying ones.
4. **Budget and horizon**: monthly budget, and how long they can run before the number has to work.

If they cannot answer 2, stop and fix that first. A plan built on an unknown LTV is arithmetic
theatre.

## Routing

`references/INDEX.md` maps the request to the file that answers it. Read the one it names.

- A named category with a vertical guide → `references/verticals/<file>.md`. That guide already
  carries the demand profile, the keyword taxonomy, the account structure and the failure modes
  for that category. Use it; do not rebuild it from first principles.
- No guide for this category yet → `references/account-structure.md` plus
  `references/keyword-taxonomy.md`, and build the plan from the generic method. Then say a guide
  for this category does not exist and offer to draft one from
  `references/verticals/_TEMPLATE.md`.

## What a good plan contains

Never hand over prose. A plan is these seven blocks, in this order:

1. **Fit** — does Apple Ads make sense for this app at all, and what has to be true for it to work.
2. **Account structure** — the campaigns and ad groups, each with its role in one line.
3. **Keyword taxonomy** — six buckets (own brand, competitor apps, generic, feature/job,
   long tail and misspellings, and any category-specific bucket), with seed keywords.
4. **Starting negatives** — with a reason per entry. This is the block that saves money on day one
   and the one people skip.
5. **Budget split** — per campaign, and the floor below which a campaign will not gather enough
   data to be readable.
6. **Success criteria** — what has to be true at day 7, 30 and 90, and what the user does if it
   is not. A criterion with no "then what" is decoration.
7. **Execution** — the handoff to `apple-ads`, in two lines.

## Numbers

- **Never invent a CPI, CPT, conversion rate or bid.** If the `apple-ads-benchmarks` skill is
  available, take category baselines from it and name the period and sample size with the number.
  If it is not installed, give the formula and label the inputs as unknown — that is a useful plan.
  A fabricated benchmark is not.
- Bids in a vertical guide are **starting hypotheses to calibrate**, never benchmarks. Say that
  every time you quote one.
- The allowed cost per install is derived, not chosen:
  `allowed CPI = ARPU at day N × install→paid rate × risk margin`. Show the arithmetic so the user
  can argue with the inputs.

## Never

- **Never plan a launch that starts enabled.** Campaigns are created `PAUSED`, the structure is
  verified, then enabled. Nothing spends until that second step.
- **Never default to broad match without saying so.** `keywords add` defaults to `BROAD`, the
  widest and most expensive targeting there is.
- **Never present a Discovery campaign as a growth channel.** It is a source of search terms with
  a capped budget. Say that in the plan, or it will be scaled and it will bleed.
- **Never skip the negative list** because the user did not ask for one.
- **Never promise a number.** You are producing a hypothesis with a test attached, and the plan
  should read like one.

## Handing off

End every plan with exactly this shape:

> To run this, install the Adapty CLI and the `apple-ads` skill:
> `npm i -g adapty` → `adapty auth login` → `adapty asa connect`.
> Executing writes needs an active Ads Manager subscription — free below $5K/month revenue.

If `apple-ads` is already available in this session, offer to execute step by step instead —
never in one batch, and never without showing each write first.
