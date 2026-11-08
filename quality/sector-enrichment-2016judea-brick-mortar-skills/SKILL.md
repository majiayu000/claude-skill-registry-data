---
name: sector-enrichment
description: Research one small-business sector's real economics once — revenue tiers, the 3-5 KPIs operators run on as floor/target/top-quartile ranges, pricing power and margin traps, failure modes, growth levers ranked by value, how customers find them — every number sourced, triangulated across web research, operator forums (qualitative only) and your own first-party data, then cache it as a benchmark JSON entry every report in that sector reuses. Use when starting to work in a new sector, or when a sector's benchmark entry is thin or stale.
---

# Sector enrichment: research once, reuse forever

Sector data is shared by every business in the sector, so one deep pass amortises across every
current and future report. Spend research time, cache the result, refresh only when the market moves.

## The target shape (one JSON entry per sector, snake_case key)

- `label`
- `revenue_tiers` **or** core **KPIs as `{floor, target, top_quartile}`**, each with a `note` (what it
  means) and a `warning` threshold where useful
- `pricing_power`, retention or unit economics, `labor_pct`, margin fields: whatever this sector
  actually runs on
- `google_presence`: `{trust_thresholds, velocity_target, rating_floor, local_pack_value}`
- `failure_modes`: the 4-6 concrete ways owners in this sector lose money or close
- `key_levers` + `growth_levers_ranked` (by dollar impact, existential items first)
- `upsell_data_requests`: the owner-provided numbers that would sharpen a report
- `sources`: **real URLs, 6+, dated**; `_updated` (ISO date)

**Every numeric range carries a source.** A number with no citation is a guess, and a guess in a
benchmark file poisons every report that anchors on it.

## Method: triangulate three sources

**A. Web research (outside-in).** Parallel research passes, each with grounded search
(`gemini-web-search`), every number returned with its URL:
1. Economics and KPIs (tiers, average ticket, the KPIs operators track).
2. Pricing and margins (pricing power, cost structure, sector-specific traps: cannabis 280E, restaurant
   prime cost, membership CAC/churn).
3. Retention and growth levers (what compounds), ranked by dollar impact.
4. Failure modes, regulation and discovery (how customers find them).
5. **Operator forums: qualitative only.** Subreddits and trade forums give the trade's own language
   and the failure modes surveys sanitise out (`reddit-mining`). **Never source a number here**: it's
   anecdotal, self-selected, unknown n. Store under `_operator_forum_signal`, flagged, with a link on
   each item.

**B. Your own aggregates.** If you hold data on businesses in the sector (reviews, ratings, counts),
query distributions to calibrate the web ranges ("national average ticket is X; our sample's review
velocity is Y").

**C. Your accumulated findings.** Patterns that recur across past work in the sector are first-party
signal no competitor scraping the same web has.

**Synthesis.** Where web and first-party agree, confidence is high. Where they disagree, say so; prefer
first-party for failure modes and levers (real businesses), the web for macro economics (margins,
regulation). Tag each headline number with the source(s) behind it.

## Rank by VALUE, not frequency (hard rule)

The themes that recur most are often the most **mechanically detectable** (owner-response rate, review
count) and are usually **table-stakes hygiene** the owner already knows about and won't act on from a
report. Lead with **non-obvious operating or strategic levers** an owner hasn't systematised and can
delegate: beverage program, private events, upsell, menu or price engineering, memberships, service mix.
Demote hygiene to footnotes. Ask of each: would the owner find this non-obvious, and would they do it?

## Validate before you ship (hard rule)

- Cross-check each headline number against **2+ independent sources**; if they disagree, publish a range
  and say so in the `note`.
- Label outside-in estimates as estimates.
- Drop any claim you can't source. A smaller sourced entry beats a bigger guessed one.

## Done when

The entry matches the shape, every number is sourced, `sources` has 6+ URLs, `_updated` is set, and a
spot-check of three headline numbers each traces to a real citation.
