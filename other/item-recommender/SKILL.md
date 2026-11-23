---
name: item-recommender
description: "Use when the user asks Claude to find, pick, compare or recommend a product to buy (for example 'find me the best toothbrush', 'which laptop should I get', 'best budget vacuum', 'X vs Y, which one?', 'what's worth buying for ...')."
---

# Item Recommender

## Overview

A buying recommendation is only as good as its sources. Most "best X" pages are affiliate listicles that rank by commission, copy each other, and are rarely tested. This skill picks from independent testing and real owner experience, and reports how sure it is. A search result or its summary is a lead, not a source: only a page you opened counts.

## Setup

Take the item from the user. Do not interrogate. State assumptions in one line and proceed: budget (say the range you assume), main use, and any stated constraint (country, size, brand dislikes, ecosystem). Pick the one thing most likely to flip the answer and name it in the report. Ask a question only if the item is so ambiguous that research would be wasted. If the category splits on a fact the user did not give (laptop: macOS or Windows, gaming or not), do not bet on one assumption: give a pick for each of the 2 to 3 real segments and say which fits whom.

## Process

1. **Criteria first.** From independent testing methodology pages, learn what actually separates good from bad in this category, then fix 3 to 5 criteria before reading any ranking. Include any criterion where the user's stated need breaks ties.
2. **Gather sources by tier.** Open pages. A page that returns only a title or navigation was not opened: try an archived copy if your tools allow it, then another outlet's test of the same model, otherwise count it as unchecked. Ignore date stamps in the future. Record URL, date, and whether the source bought its own units and measured them.
   - **Tier 1, tested:** labs and reviewers that buy and measure (Wirecutter, Consumer Reports, RTINGS, Which?, category specialists, standards bodies and certification listings).
   - **Tier 2, practitioners:** category forums and subreddits, repair shops, professionals who use the item daily.
   - **Tier 3, owners:** retailer and forum reviews. Read the 1 to 3 star and long-term ones for failure modes.
   - **Tier 4, affiliate listicles and "best of" pages without a stated test method:** leads for model names only. They never count as evidence.
   A self-tested site funded by affiliate links is Tier 1 only if it states how it tested (units, protocol or measured results); otherwise Tier 4. Disclosed affiliate links do not disqualify a tester. Prefer sources from the last 2 years; older ones are stale for fast-moving categories, so say so when you use one.
3. **Consensus.** Need at least 3 opened sources from Tiers 1 to 3, at least 2 of them independent and using different methods. A pick two independent sources agree on beats one with a higher score. Report disagreements and why they differ; do not pick the convenient side. If a major source is blocked or paywalled, try its archived copy or a second outlet that cites its test, then continue. If the bar is still not met, give the pick as **tentative**, state the confidence (high, medium or low), and name which sources would settle it. Snippets and unopened owner reviews stay `unverified`.
4. **Mine failures** for each finalist: search the exact model with "problems", "broke", "after 1 year", "recall", "returns". If the model is under a year old, say there is no long-term evidence; the predecessor's long-term issues are a lead, marked as such.
5. **Check the model and the price.** Confirm the exact current model and year, since names are reused for different hardware. Check current price at two retailers or a price tracker, and note the date. If product pages will not load, a dated deal or price report is acceptable; label it as that and tell the user to re-check. Add running costs (refills, subscription, consumables). If the item is a new release, or reviews predate a revision, say so.
6. **Decide.** The user's stated limits (budget, size, compatibility) are filters, not preferences: the pick must meet them at the price you verified. If the best-tested product is over budget, list it as the stretch option and say what it costs, and pick the best product that fits. If the in-budget price is unconfirmed, say the pick holds only at or below the limit. One top pick, a cheaper alternative, and a "pick this instead if ..." only for use cases your sources actually support. If differences are negligible for this user, say that plainly and recommend the cheap adequate option. Do not invent a winner.

## Report format

- **Pick:** model, current price with date and where, one sentence on why it wins for this user, and a confidence level (high, medium or low).
- **Also consider:** the budget pick, and 1 to 2 "instead if" alternatives.
- **Why:** the criteria and how each finalist scored, in a small table.
- **Evidence ledger:** each claim, source link, date, tier, and status `confirmed` (two independent sources, or one primary source such as a lab measurement or manufacturer spec), `single-source`, or `unverified`.
- **Known failure modes** of the pick, in owners' words.
- **What would change this pick:** the assumption most likely to be wrong.
- **Could not check:** blocked or paywalled sources (Reddit, Consumer Reports), and what you used instead.

Keep the pick, alternatives and reasoning to about 400 words per segment. The table, ledger and failure modes may extend it.

## Common Mistakes

- Reporting a pick from search snippets without opening the pages.
- Counting two listicles that cite the same press release or each other as two sources.
- Treating an "editor's choice" badge as testing.
- Quoting a price from memory or from a page without a date.
- Recommending the model the sources reviewed when the current store listing is a different revision.
- Skipping the user's constraint and answering the generic question.
- Always naming a winner, when the honest answer is that the category barely matters.
- Stating no affiliate or sponsor ties without checking. If a source discloses affiliate links, say so; that alone does not disqualify a Tier 1 tester.
