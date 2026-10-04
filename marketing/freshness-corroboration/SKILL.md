---
name: freshness-corroboration
description: Trust-stage audit for current and corroborated brand claims. Use when AI answers show outdated or contradictory facts or content lacks trust signals. Checks machine-readable dates, staleness and fake freshness, unsourced statistics, prices and superlatives, outbound citations, and single-source fragility.
license: MIT
---

# Freshness & Corroboration (trust layer)

Handout appendix D states the mechanism: machines treat a fact as more
trustworthy when many independent places say the same thing, and a claim that
lives in only one spot is fragile.

This layer audits both halves of that — whether a claim is *current*, and
whether it is *corroborated*.

## When to use

After `crawl-reachability`. Run standalone when a brand's facts are stale or
contradicted in AI answers.

## Inputs

- **Required** — a run workspace from the two upstream stages: `preflight.json`
  for the scope domain and `reachability.json` for the page inventory and saved
  HTML paths.
- **Optional** — `--config` (an `AuditConfig` JSON) and `--strictness`
  (`lenient` | `balanced` | `strict`) to override staleness windows and the
  page-type recency expectations. Defaults come from `AuditConfig`.
- **Not consumed** — no network access, no prior stage's findings. Everything
  here is derived from markup already fetched, so the layer is re-runnable
  offline and produces identical output.

```
python3 scripts/check_freshness.py [--workspace PATH] [--json]
```

## Procedure

Deterministic, in this order. Staleness windows come from the page type, never
from a universal constant, and no wall-clock value enters a threshold — the
clock is read once, for the audit timestamp only.

1. **Load the inventory and pages.** Resolve the scope domain from `preflight`,
   then read every fetched page; record pages with missing HTML as a coverage
   limitation.
2. **Datestamp presence (`FR001`).** Check for any date on page types whose
   `expect_date` is true; page types carrying `expect_date: false` are exempt by
   design, not by accident.
3. **Machine-readability (`FR002`).** Distinguish a date a human can read from a
   date a machine can parse — `<time datetime>`, JSON-LD `datePublished` /
   `dateModified`, meta article timestamps.
4. **Staleness (`FR003`).** Age the page against what its type implies about
   recency.
5. **Fake freshness (`FR004`).** Compare the `dateModified` gap against actual
   signals of revision, to catch timestamps bumped on every deploy.
6. **Load-bearing claims (`FR005`).** Flag statistics, prices and superlatives
   asserted with nothing behind them.
7. **Outbound citation density (`FR006`).** Measure references on the page types
   where citing is conventional.
8. **Corroboration profile (`FR007`, `FR008`).** Determine whether every claim
   is single-sourced to the site, and whether corroboration rests on press and
   social coverage only.
9. **Attach the sample caveat.** Every population claim carries its sample size
   for the advisory layer to verify.

## Checks and severities

Every check the procedure above can emit, with the claim level it is allowed to
assert.

| Check | Detects | Severity | Claim level |
|---|---|---|---|
| `FR001` | No datestamp on page types that imply recency | high/medium | 1 |
| `FR002` | Dates present but not machine-readable | medium | 1 |
| `FR003` | Content stale relative to what its page type implies | medium | 1 |
| `FR004` | `dateModified` far newer than `datePublished` with no visible revision | medium | 1 |
| `FR005` | Statistics and superlatives asserted with no source | medium | 3 |
| `FR006` | Explanatory pages with no outbound references at all | medium | 1 |
| `FR007` | Every factual claim single-sourced to the site itself | medium | 3 |
| `FR008` | Corroboration resting on press and social coverage only | medium | 3 |

## The recommendation people get backwards

`FR008` is the non-obvious one. The instinct when a brand is invisible is to
pursue press coverage, and press coverage does help — at the *selection* layer.
But arXiv:2604.25707 §8.4 measures mean influence by publisher domain type:

| Domain type | Mean influence |
|---|---|
| encyclopedia | **0.2144** |
| academic_publishing | 0.1118 |
| commercial | 0.1028 |
| nonprofit | 0.0971 |
| academic | 0.0815 |
| government | 0.0769 |
| **news_media** | **0.0726** |

News media is the *most frequently selected* non-official source type (16.07%
to 31.17% of citations, §7) and the *least absorbed* in this table. Encyclopedia
pages absorb roughly three times as deeply. The paper's reading is that answer
engines often need explanatory pages after they have identified timely ones.

So a corroboration profile made entirely of press hits optimises the weaker of
the two outcomes. `FR008` flags exactly that shape and recommends seeding
explanatory reference coverage alongside the press.

## Fake freshness

`FR004` catches a specific bad practice: bumping `dateModified` on every deploy
so content looks maintained. It compares the modification gap against actual
signals of revision. A site where every page claims to have been updated
yesterday and none of them changed is making a claim a crawler can check and
find false, which damages exactly the trust the timestamp was meant to build.

## Page-type awareness

Staleness thresholds come from what the page type implies. An undated contact
page is fine; an undated news article is not. Pages whose type carries
`expect_date: false` are exempt from `FR001` — a blanket "no datestamp" check
fires on most of a normal site and teaches the reader to ignore the report.

## Output

`05-freshness-corroboration.json` with per-page date inventory, staleness
distribution, outbound-reference hosts by category, unsourced-claim samples,
and the findings.

## Guardrails

Read-only; consumes saved HTML only. Corroboration is assessed from signals
observable on the site itself (outbound references, `sameAs`, cited sources) —
the audit does not crawl third-party sites to verify them, and says so in the
report's limitations rather than implying an off-site check it did not perform.

## Grounding

Handout appendix D (agreement across sources); §8.4 domain-type influence;
§8.3 semantic-role influence, where `reference`-only citations sit lowest at
0.0529 while `definition` leads at 0.1531. Details in
`references/corroboration.md`.
