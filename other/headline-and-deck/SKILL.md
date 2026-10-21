---
name: headline-and-deck
description: "Use when writing or checking a headline, deck (subhead), executive-summary bullet, email subject line or figure title for a report: decomposes it into checkable atoms (number, direction, comparison, period, cause, superlative) and verifies each against a claim ledger before it ships. Use whenever a title contains a number, a trend verb, 'record', 'first', 'because' or 'driven by'."
license: CC-BY-4.0
---

# Headlines and decks

The headline is the sentence most people will read and the one most likely to
be wrong: it is written last, compressed hardest and checked least. Treat it
as a set of claims.

## Anatomy

- **Headline**: the single most important finding, specific, with a number
  if the number is the news. 6–12 words.
- **Deck**: the next fact the reader needs to not be misled: the comparison
  base, the main caveat, or the decision at stake. One sentence.

Illustrative example (figures invented):

> Headline: Conversion fell to 24% as the lead mix shifted toward Meta ads
> Deck: Every channel converted at least as well as in August; Meta's share
> of consultations rose from 18% to 29%, and it converts at half the referral rate.

## Atom check

Split the headline and deck into atoms. Each needs a ledger entry (query or
computed field, value, period, source) or it is cut.

| Atom | Example | Check |
|---|---|---|
| Number | 24% | equals the ledger value after rounding |
| Direction | fell | sign of the change over the stated comparison |
| Comparison | (vs August) | base period complete and like-for-like (`when-numbers-lie-audit` C1–C5) |
| Period | in September | exact and in the deck or subtitle |
| Cause | as cheaper leads poured in | design supports it (`statistical-claims` ladder) |
| Superlative | record, first, biggest | full history checked and its start date stated |
| Scope | North region, all regions | matches the filter in the query |

## Rules

1. **No atom without a ledger entry.** The ledger is a short table kept with
   the report (claim → value → query/field → source → retrieved at).
2. **Causal words are claims.** "as", "after", "because", "driven by",
   "thanks to", "due to": each is checked against the design. Prefer "after"
   or "while" when the design is before/after.
3. **"Record" needs the full series.** Say "highest since records began in
   2021" if the data start in 2021.
4. **No question headlines** and no headlines the body has to walk back.
5. **Headline and figure agree.** The direction and size claimed are visible
   in the chart, over the window the chart shows.
6. **Monitoring is allowed to be dull.** "Orders in line with last year"
   is a valid headline if the report states what counts as "in line" (e.g.
   within ±5%); do not manufacture tension, and do not turn an inconclusive
   test into "no change" (`statistical-claims` Rule 5).
7. **Specific beats clever.** No puns or idioms that a non-native reader or
   a translation would lose.
8. **Same number, same rounding** in headline, deck, body and chart.

## Business example (illustrative; a fictional online shop, figures invented)

Bad: "Record month as new campaign drives orders surge"
- "Record": data since March 2024 only. "drives": before/after, no control.
  "surge": +13%.

Good: "Orders rose 13% in September, the most since records began in March 2024"
Deck: "The rise came in the first full month of the Google campaign; seasonal
demand also peaks in September, so the campaign's share is not yet known."

## AI-research example

Bad: "New method beats baseline on all benchmarks"
- "beats": five benchmarks means five comparisons; with a Bonferroni
  correction for the five (99% paired intervals for a 95% family level),
  2 of the 5 intervals include zero.

Good: "New method leads on 3 of 5 benchmarks; on the other two the
difference is not distinguishable from zero"
Deck: "Paired 99% intervals over items and seeds (Bonferroni, 95% across the
five benchmarks). The two inconclusive intervals span gains and losses that would
matter, so they are not ties (`statistical-claims` Rules 3 and 5)."

## Checklist

- [ ] Headline and deck split into atoms; each atom has a ledger entry.
- [ ] Every number matches the ledger at the stated rounding.
- [ ] Direction, comparison base and period verified.
- [ ] Causal words match the design; superlatives checked against full history.
- [ ] Headline claim visible in the accompanying figure.
- [ ] No question, pun or hype; same rounding everywhere.

Adapted in part from jamditis `data-journalism` and `fact-check-workflow`
(MIT); changed: rewritten as an atom check, examples replaced. Sources and
licences: `SOURCES.md`.
